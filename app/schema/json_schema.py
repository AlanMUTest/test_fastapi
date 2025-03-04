mcq = {
    "type": "OBJECT",
    "properties": {
        "mcq": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "Question Number": {
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
                                "B": {
                                    "type": "STRING"
                                },
                                "C": {
                                    "type": "STRING"
                                },
                                "D": {
                                    "type": "STRING"
                                }
                            }
                        }
                    },
                    "Answer": {
                        "type": "STRING"
                    }
                },
                "required": [
                    "Question Number",
                    "Question",
                    "Choices",
                    "Answer"
                ]
            }
        }
    }
}

flashcard = {
    
}