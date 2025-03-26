mcq = {
    "type": "OBJECT",
    "properties": {
        "mcq": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "Question_Number": {
                        "type": "INTEGER"
                    },
                    "Question": {
                        "type": "STRING"
                    },
                    "Choices": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "A": {
                                    "type": "STRING"
                                },
                                "A_reason": {
                                    "type": "STRING"
                                },
                                "B": {
                                    "type": "STRING"
                                },
                                "B_reason": {
                                    "type": "STRING"
                                },
                                "C": {
                                    "type": "STRING"
                                },
                                "C_reason": {
                                    "type": "STRING"
                                },
                                "D": {
                                    "type": "STRING"
                                },
                                "D_reason": {
                                    "type": "STRING"
                                },
                            },
                        },
                    },
                    "Answer": {
                        "type": "STRING"
                    },
                },
                "required": [
                    "Question_Number",
                    "Question",
                    "Choices",
                    "Answer"
                ],
            },
        },
    },
}

flashcard = {
    "type": "OBJECT",
    "properties": {
        "flashcard": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "Flashcard_Number": {
                        "type": "INTEGER"
                    },
                    "Front_Side": {
                        "type": "STRING"
                    },
                    "Back_Side": {
                        "type": "STRING"
                    }
                },
                "required": [
                    "Flashcard_Number",
                    "Front_Side",
                    "Back_Side"
                ]
            }
        }
    }
}