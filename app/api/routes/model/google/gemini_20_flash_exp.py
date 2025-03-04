from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
from google import genai
from google.genai import types
import base64
import os
import schema.json_schema as json_schema
#from app.config import Settings

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('gcp_credential')
client = genai.Client(
    vertexai=True,
    project=os.getenv('gcp_project'),
    location=os.getenv('gcp_genai_location'),
)
model = "gemini-2.0-flash-exp"
#print(os.environ)
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
    response_schema=json_schema.mcq,
)

router = APIRouter()


@router.post("gemini-2.0-flash-exp")
async def generate_mcqs(file: UploadFile = File(...), num=5):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are allowed.")

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
                    types.Part.from_text(
                        text=
                        f"Generate {num} MCQs that are related to the topic")
                ]),
        ]

        response = client.models.generate_content(
            model=model, contents=contents, config=generate_content_config)

        response_dict: Dict[str, Any] = response.to_json_dict()  # Type hint
        parsed_response = response.parsed

        return JSONResponse({
            #"raw_response": response_dict,
            "mcq": parsed_response.get("mcq")
        })

    except Exception as e:
        print(f"Error processing file: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500,
                            detail=f"Error processing file: {e}")


if __name__ == "__main__":
    pass
