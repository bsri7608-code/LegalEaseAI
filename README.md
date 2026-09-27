# LegalEase

AI-Powered Legal Document Generator using Streamlit, FastAPI, and Google Gemini.

## Overview

LegalEase is an AI-powered application that helps users generate editable legal-document drafts from simple user inputs.

Users can provide:

- Document type
- Parties involved
- Terms and conditions
- Effective date

The application sends the request to a FastAPI backend, generates the document using Google Gemini, and displays the result in the Streamlit interface.

> **Disclaimer:** LegalEase generates document drafts and does not replace qualified legal advice or jurisdiction-specific legal review.

## Features

- AI-powered legal document generation
- Streamlit user interface
- FastAPI backend API
- Google Gemini integration
- Editable generated document
- TXT export
- DOCX export
- PDF export
- Structured legal-document formatting
- Secure API-key configuration using environment variables

## Architecture

```text
User
  |
  v
Streamlit Frontend
  |
  v
FastAPI Backend
  |
  v
Google Gemini API
  |
  v
Generated Legal Document
  |
  +--> TXT
  +--> DOCX
  +--> PDF
```

## Project Structure

```text
LegalEase/
├── app.py
├── main.py
├── routes.py
├── gemini_generator.py
├── document_formatter.py
├── test_api.py
├── requirements.txt
├── Python-version
├── .gitignore
└── README.md
```

## Backend API

### Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### Generate Document

```text
POST /generate
```

Request:

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Company and Employee",
  "terms": "Confidentiality; Non-disclosure; Termination",
  "effective_date": "2026-09-27"
}
```

## Environment Variables

Create a `.env` file locally:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Never commit API keys or `.env` files to GitHub.

For cloud deployment, store the API key using the deployment platform's secret or environment-variable settings.

## Installation

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## Run Backend

Start the FastAPI backend:

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Run Frontend

Start the Streamlit application:

```bash
streamlit run app.py
```

## Usage

1. Open the LegalEase Streamlit application.
2. Select the document type.
3. Enter the parties involved.
4. Enter the terms and conditions.
5. Enter the effective date.
6. Click **Generate Document**.
7. Review the generated document.
8. Edit the document if required.
9. Export the document in the required format.

## Document Export

LegalEase supports the following output formats:

- **TXT** — Plain text document
- **DOCX** — Editable Microsoft Word document
- **PDF** — Formatted PDF document

## Deployment

The application uses separate frontend and backend deployments:

- **Backend:** FastAPI deployed on Render
- **Frontend:** Streamlit deployed on Streamlit Community Cloud

The Streamlit frontend communicates with the deployed FastAPI backend for document generation.

## Security

API credentials must be stored using environment variables or the deployment platform's secret-management system.

Do not upload the following to GitHub:

- `.env` files
- Gemini API keys
- Passwords
- Access tokens
- Other sensitive credentials

## API Testing

The FastAPI backend can be tested using the interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

The deployed backend also provides the same API documentation through its `/docs` endpoint.

## Project Status

LegalEase includes:

- AI-powered document generation
- FastAPI backend
- Streamlit frontend
- Gemini API integration
- Document preview and editing
- TXT, DOCX, and PDF export
- Cloud deployment

## Disclaimer

LegalEase provides AI-generated legal-document drafts for informational and drafting purposes.

AI-generated documents may contain errors or omissions. Documents should be reviewed and, where appropriate, customized by a qualified legal professional before being used for legal purposes.

## License

This project is provided for educational and demonstration purposes.
