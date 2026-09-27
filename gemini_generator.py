import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class GeminiDocumentGenerator:
    """Generate legal-document drafts using Google's Gemini API."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured. Add it to .env."
            )

        self.client = genai.Client(
            api_key=self.api_key,
            http_options=types.HttpOptions(
                retry_options=types.HttpRetryOptions(
                    attempts=5,
                    initial_delay=2.0,
                    max_delay=30.0,
                )
            ),
        )

    @staticmethod
    def build_prompt(document_type, parties, terms, effective_date):
        return f"""
You are a careful legal-document drafting assistant.

Create a professional DRAFT of the requested legal document.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

USER-PROVIDED TERMS:
{terms}

Requirements:
1. Use only supplied facts for names, dates, amounts, addresses, and other details.
2. Do not invent missing personal facts. Use [INSERT ...] placeholders when needed.
3. Produce an editable document with a title, structured sections, relevant rights/
   obligations, term/termination provisions, and signature blocks.
4. Preserve all user-provided terms.
5. If jurisdiction is not supplied, use a clear placeholder for governing law.
6. Use plain but professional language.
7. Return only the document draft, without commentary.
8. This is a draft; it is not a substitute for qualified legal review.
""".strip()

    def generate_document(self, document_type, parties, terms, effective_date):
        prompt = self.build_prompt(
            document_type,
            parties,
            terms,
            effective_date
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=6000,
            ),
        )

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        # Clean Markdown formatting from the generated legal document
        cleaned_text = (
            text.strip()
            .replace("### ", "")
            .replace("###", "")
            .replace("**", "")
            .replace("---", "")
        )

        return cleaned_text
