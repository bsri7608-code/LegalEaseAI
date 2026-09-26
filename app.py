import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv

from document_formatter import format_docx, format_html_preview, format_pdf, sanitize_text

load_dotenv()

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
BACKEND_URL = os.getenv("BACKEND_URL", "https://legaleaseai-njtr.onrender.com").rstrip("/")

st.markdown("""
<style>
.main-title{text-align:center;font-size:42px;font-weight:800;margin-bottom:0}
.subtitle{text-align:center;color:#777;margin-bottom:25px}
.preview{background:#171717;color:#f5f5f5;padding:24px;border-radius:12px;
min-height:500px;max-height:650px;overflow-y:auto;font-family:Georgia,serif;line-height:1.65}
.preview h2,.preview h3{color:#fff}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Powered Legal Document Generator</div>', unsafe_allow_html=True)
st.info("LegalEase creates editable legal-document drafts. It does not replace legal advice or jurisdiction-specific review.")

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "generated_type" not in st.session_state:
    st.session_state.generated_type = ""

with st.form("document_form"):
    left, right = st.columns(2)
    with left:
        document_type = st.text_input("Document Type", "Non-Disclosure Agreement")
        parties = st.text_area("Parties Involved", height=130,
                               placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)")
    with right:
        effective_date = st.date_input("Effective Date", date.today())
        terms = st.text_area("Terms & Conditions", height=130,
                             placeholder="Use semicolons between key terms.")
    submitted = st.form_submit_button("Generate Document", type="primary", use_container_width=True)

if submitted:
    if not all([document_type.strip(), parties.strip(), terms.strip()]):
        st.error("Please complete Document Type, Parties, and Terms.")
    else:
        payload = {
            "document_type": document_type.strip(),
            "parties": parties.strip(),
            "terms": terms.strip(),
            "effective_date": effective_date.isoformat(),
        }
        with st.spinner("Generating your legal draft with Gemini..."):
            try:
                response = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=120)
                if response.ok:
                    data = response.json()
                    st.session_state.generated_text = data["content"]
                    st.session_state.generated_type = data["document_type"]
                    st.success("Document generated successfully.")
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                    st.error(f"Backend error: {detail}")
            except requests.RequestException as exc:
                st.error(f"Could not connect to FastAPI at {BACKEND_URL}. Details: {exc}")

if st.session_state.generated_text:
    st.divider()
    st.subheader("Document Preview & Editing")
    edited = st.text_area("Edit the generated document",
                           value=st.session_state.generated_text, height=600)
    st.session_state.generated_text = edited

    st.subheader("Styled Preview")
    st.markdown(f'<div class="preview">{format_html_preview(edited)}</div>',
                unsafe_allow_html=True)

    st.subheader("Download")
    c1, c2, c3 = st.columns(3)
    safe_type = "".join(ch.lower() if ch.isalnum() else "_" for ch in st.session_state.generated_type).strip("_") or "legal_document"

    with c1:
        st.download_button("Download TXT", sanitize_text(edited).encode("utf-8"),
                           file_name=f"{safe_type}.txt", mime="text/plain", use_container_width=True)
    with c2:
        st.download_button("Download DOCX", format_docx(edited, st.session_state.generated_type),
                           file_name=f"{safe_type}.docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           use_container_width=True)
    with c3:
        st.download_button("Download PDF", format_pdf(edited, st.session_state.generated_type),
                           file_name=f"{safe_type}.pdf", mime="application/pdf", use_container_width=True)

st.caption("LegalEase • FastAPI + Streamlit + Gemini")
