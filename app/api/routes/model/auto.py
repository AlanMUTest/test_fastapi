import random
from typing import Any, Dict, List, Literal

from fastapi import File, Query, UploadFile, APIRouter

from app.api.routes.model.alibaba.qwen25_vl_72b_instruct import generate as alibaba_generate
from app.api.routes.model.google.gemini_20_flash_exp import generate as google_flash_generate
from app.api.routes.model.google.gemini_20_pro_exp_02_05 import generate as google_pro_generate
from app.api.routes.model.meta.llama_32_11b_vision_instruct import generate as meta_generate
from app.api.routes.model.mistral.mistral_small_31_24b_instruct import generate as mistral_generate

router = APIRouter()

SchemaType = Literal["null", "mcq", "flashcard"]

@router.post("/auto")
async def auto_select_generate(file: UploadFile = File(...),
                   schema_type: SchemaType = Query("null", description="Type of content to generate ('mcq' or 'flashcard')"),
                   num: int = Query(5, description="Number of items to generate(1 - 10)")):

    model_functions: List[Dict[str, Any]] = [
        {"name": "qwen25_vl_72b_instruct", "func": alibaba_generate},
        {"name": "gemini_20_flash_exp", "func": google_flash_generate},
        {"name": "gemini_20_pro_exp_02_05", "func": google_pro_generate},
        {"name": "llama_32_11b_vision_instruct", "func": meta_generate},
        {"name": "mistral_small_31_24b_instruct", "func": mistral_generate},
    ]

    random.shuffle(model_functions)  # Randomize the order

    for model_info in model_functions:
        model_name = model_info["name"]
        model_func = model_info["func"]
        print(f"Attempting to use model: {model_name}")
        try:
            result = await model_func(file=file, schema_type=schema_type, num=num)
            print(f"Model {model_name} succeeded.")
            return result  # Return the result if successful
        except Exception as e:
            print(f"Model {model_name} failed with error: {e}")
            # Log the error for debugging purposes
            # Consider adding more specific exception handling if needed
            continue  # Try the next model

    # If all models fail, raise an exception or return a default value
    raise Exception("All models failed to generate content.")