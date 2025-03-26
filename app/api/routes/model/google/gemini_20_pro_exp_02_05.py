from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Literal
from google import genai
from google.genai import types
import base64
import os
import app.schema.json_schema as json_schema
from app.config import settings

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('gcp_credential')
client = genai.Client(
    vertexai=True,
    project=os.getenv('gcp_project'),
    location=os.getenv('gcp_genai_location'),
)
model = "gemini-2.0-pro-exp-02-05"

router = APIRouter()

SchemaType = Literal["null", "mcq", "flashcard"]

@router.post("gemini-2.0-pro-exp-02-05")
async def generate(file: UploadFile = File(...),
                   schema_type: SchemaType = Query("null", description="Type of content to generate ('mcq' or 'flashcard')"),
                   num: int = Query(5, description="Number of items to generate(1 - 10)")):
    
    #print(os.environ)
    
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are allowed.")

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
        response_schema = json_schema.mcq
        prompt_suffix = f"Generate {num} MCQs that are related to the topic."
    elif schema_type == "flashcard":
        response_schema = json_schema.flashcard
        prompt_suffix = f"Generate {num} flashcards that are related to the topic."
    else:
        # This should be unreachable due to the validation above, but included for safety.
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: Invalid schema_type (this should not happen).")
    
    #print(os.environ)
    
    try:
        content = await file.read()
        encoded_content = base64.b64encode(content)

        msg1_document1 = types.Part.from_bytes(
            data=base64.b64decode(encoded_content),
            mime_type="application/pdf",
        )
        contents = [
            types.Content(
                role="user",
                parts=[
                    msg1_document1,
                    types.Part.from_text(text=prompt_suffix)
                ]),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=8192,
            response_modalities=["TEXT"],
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH",
                                    threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT",
                                    threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                    threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT",
                                    threshold="OFF")
            ],
            response_mime_type="application/json",
            response_schema=response_schema,
        )
        
        response = client.models.generate_content(
            model=model, contents=contents, config=generate_content_config)
        # response_dict: Dict[str, Any] = response.to_json_dict()  # Type hint
        parsed_response = response.parsed

        if schema_type == "mcq":
            return JSONResponse({"mcq": parsed_response.get("mcq")})
        elif schema_type == "flashcard":
            return JSONResponse({"flashcard": parsed_response.get("flashcard")})
        else:
            # Should be unreachable due to prior validation, but included for completeness.
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error:  Invalid schema_type after generation.")

    except Exception as e:
        print(f"Error processing file: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500,
                            detail=f"Error processing file: {e}")


if __name__ == "__main__":
    pass
