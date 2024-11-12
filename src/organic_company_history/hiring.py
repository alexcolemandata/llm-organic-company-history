"""python -m organic_company_history.hiring"""
import ollama

from .basis import basis_data


BASE_MODEL = "llama3.1"
SYSTEM_MESSAGE = (
    "You are an expert of company structures, HR data, and growth consulting. "
    "Provide all your responses as in a 'csv' format only. "
    "Do not include any additional whitespace. "
    "Do not quote strings unless they contain a comma. "
    "All dates should be in YYYY-MM-DD format. "
    "Always include the column headers as the first row of the response. "
)
modelfile = f"""
FROM {BASE_MODEL}
SYSTEM {SYSTEM_MESSAGE}
"""

MODEL_NAME = "ac-hiring"

ollama.create(model=MODEL_NAME, modelfile=modelfile)

response = ollama.chat(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": (
                f"My knitting company currently has {len(basis_data)} employees. "
                "I want to grow my company by hiring a few more people. "
                "What positions should I hire for, and what would their salary ranges be?"
            ),
        }
    ],
)["message"]["content"]
print(response)
