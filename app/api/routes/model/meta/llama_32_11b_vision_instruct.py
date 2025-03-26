from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from openai import OpenAI
from typing import Literal, List
import base64
import os
import app.schema.pydantic_schema as pydantic_schema
from app.config import settings
import fitz

client = OpenAI(
    base_url=os.getenv("or_url"),
    api_key=os.getenv("or_api"),
)

model = "meta-llama/llama-3.2-11b-vision-instruct:free"

router = APIRouter()

SchemaType = Literal["null", "mcq", "flashcard"]

def pdf_to_base64_images(pdf_content: bytes) -> List[str]:
    base64_images = []
    try:
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)  # number of page
            pix = page.get_pixmap()
            img_data = pix.tobytes("png")  # Convert to PNG format
            base64_image = base64.b64encode(img_data).decode("utf-8")
            base64_images.append(base64_image)
        doc.close()
    except Exception as e:
        raise Exception(e)
    return base64_images

@router.post("llama-3.2-11b-vision-instruct")
async def generate(file: UploadFile = File(...),
                   schema_type: SchemaType = Query("null", description="Type of content to generate ('mcq' or 'flashcard')"),
                   num: int = Query(5, description="Number of items to generate(1 - 10)")):
    
    #print(os.environ)
    
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF file is allowed.")
    
    if file.size > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail="PDF file is too large!")
    
    if num > settings.max_num or num < 1:
        raise HTTPException(
            status_code=400,
            detail="Invalid number!")
    
    if schema_type not in ("mcq", "flashcard"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid schema_type: {schema_type}.  Must be 'mcq' or 'flashcard'.")
        
    if schema_type == "mcq":
        response_schema = pydantic_schema.MCQ
        prompt_suffix = f"Generate {num} MCQs that are related to the topic."
    elif schema_type == "flashcard":
        response_schema = pydantic_schema.Flashcard
        prompt_suffix = f"Generate {num} flashcards that are related to the topic."
    else:
        # This should be unreachable due to the validation above, but included for safety.
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: Invalid schema_type (this should not happen).")
    
    try:
        content = await file.read()
        base64_images = pdf_to_base64_images(content)
        
        message_content = [
            {
                "type": "text",
                "text": prompt_suffix
            }
        ]
        for base64_image in base64_images:
            message_content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",  # Add data URL prefix
                    }
                }
            )

        completion = client.beta.chat.completions.parse(
            model="qwen/qwen2.5-vl-72b-instruct:free",
            messages=[
                {
                    "role":
                    "system",
                    "content":
                    "You are a structured data processor. You are proficient in json format data and can output structured json data. You can output json data that conforms to the scheme based on the given text and json scheme. Please note that your output will be parsed directly. If the format is incorrect, the parsing will fail."
                },
                {
                    "role": "user",
                    "content": message_content,
                },
            ],
            response_format=response_schema,
        )

        print(f"result: \n{completion}")
        llm_response = completion.choices[0].message
        if (llm_response.refusal):
            print(f"llm_response: {llm_response.refusal}")
        else:
            print(f"llm_response: {llm_response.parsed.model_dump(warnings=False)}")

        if llm_response.parsed:
            return JSONResponse(llm_response.parsed.model_dump(warnings=False))
        else:
             raise HTTPException(status_code=500, detail="Failed to generate content.")

    except Exception as e:
        print(f"Error processing file: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500,
                            detail=f"Error processing file: {e}")

if __name__ == "__main__":
    pass
