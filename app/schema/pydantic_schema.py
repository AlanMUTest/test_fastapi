from typing import List, Dict

#from pydantic import BaseModel
from langchain_core.pydantic_v1 import BaseModel, Field


class Choice(BaseModel):
    A: str
    B: str
    C: str
    D: str


class Question(BaseModel):
    Question_Number: int
    Question: str
    Choices: List[Choice]
    Answer: str


class MCQ(BaseModel):
    mcq: List[Question]
