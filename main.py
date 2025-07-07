import os
import re
import cv2
import json
import pytesseract
from typing import List
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=GEMINI_API_KEY
)

class RunnerAgent:
    def load_text(self, file_path: str) -> str:
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        elif file_path.lower().endswith((".jpg", ".jpeg", ".png")):
            image = cv2.imread(file_path)
            text = pytesseract.image_to_string(image)
        else:
            raise ValueError("Unsupported file type. Use PDF, TXT, or JPG/PNG.")
        return text

class RedactorAgent:
    def detect_sensitive_info(self, text: str) -> List[dict]:
        prompt = (
            "Extract and return a list of sensitive data from this text. "
            "Types should include email, phone number, URL, and names. "
            "Return in this JSON format:\n"
            "[{\"type\": \"email\", \"value\": \"abc@email.com\"}, ...]\n\n"
            f"Text:\n{text}"
        )
        result = llm.invoke(prompt)
        return self._parse_json_list(result.content)

    def redact(self, text: str, sensitive_items: List[dict]) -> str:
        for item in sensitive_items:
            value = re.escape(item["value"])
            tag = f"[REDACTED_{item['type'].upper()}]"
            text = re.sub(value, tag, text, flags=re.IGNORECASE)
        return text

    def _parse_json_list(self, raw: str) -> List[dict]:
        try:
            start = raw.index('[')
            end = raw.rindex(']') + 1
            return json.loads(raw[start:end])
        except:
            return []

class CoordinatorAgent:
    def __init__(self):
        self.runner = RunnerAgent()
        self.redactor = RedactorAgent()

    def handle_file(self, file_path: str):
        print("\n[RunnerAgent] Extracting content...")
        raw_text = self.runner.load_text(file_path)

        print("[RedactorAgent] Detecting sensitive data...")
        sensitive_items = self.redactor.detect_sensitive_info(raw_text)

        print(f"[RedactorAgent] Found {len(sensitive_items)} item(s):")
        for item in sensitive_items:
            print(f" - {item['type']}: {item['value']}")

        redacted = self.redactor.redact(raw_text, sensitive_items)

        out_file = os.path.splitext(file_path)[0] + "_redacted.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(redacted)

        print(f"\n Redacted file saved to: {out_file}")

def main():
    file_path = input("Enter file path (.txt, .pdf, .jpg, .png): ").strip()
    if not os.path.exists(file_path):
        print(" File not found.")
        return

    coordinator = CoordinatorAgent()
    coordinator.handle_file(file_path)

if __name__ == "__main__":
    main()
