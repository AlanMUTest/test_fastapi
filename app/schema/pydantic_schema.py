from typing import List, Dict

#from pydantic import BaseModel
from pydantic import BaseModel, Field

# MCQ
class MCQ_Choice(BaseModel):
    A: str
    A_reason: str
    B: str
    B_reason: str
    C: str
    C_reason: str
    D: str
    D_reason: str


class MCQ_Question(BaseModel):
    Question_Number: int
    Question: str
    Choices: List[MCQ_Choice]
    Answer: str


class MCQ(BaseModel):
    mcq: List[MCQ_Question]

# Flashcard
class FlashcardItem(BaseModel):
    Flashcard_Number: int = Field(..., description="The unique number of the flashcard.")
    Front_Side: str = Field(..., description="The content on the front side of the flashcard.")
    Back_Side: str = Field(..., description="The content on the back side of the flashcard.")


class Flashcard(BaseModel):
    flashcard: List[FlashcardItem] = Field(..., description="An array of flashcard objects.")