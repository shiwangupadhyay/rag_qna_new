from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from schema.schema import OutputSchema

load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

model = model.with_structured_output(OutputSchema)