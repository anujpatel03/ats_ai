from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import base64
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]
      
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')

        image_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file Uploaded")


st.set_page_config(page_title="ATS Resume Expert")
st.header("AI based ATS Resume Expert")
input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume in PDF form..", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about Resume")
submit2 = st.button("Percentage Match")
submit3 = st.button("How can I improvise my skills")

input_prompt1 = """You are an experienced HR with Tech Experience in every field, your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job role.
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of all fields and deep ATS functionality,
your task is to evaluate the resume against the provided job description. Give me the percent match of resume with the job description. First, the output should come as a percentage and then keywords missing in bullet point manner.
"""

input_prompt3 = """
You are a skilled HR and have a great tech experience by comparing the resume uploaded and job description, suggest me some changes that I should do to make my resume more effective and have a good percentage match with the job description. Give me details in short and bullet points
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Your Resume review here----")
        st.write(response)
    else:
        st.write("Please Upload the Resume!!!")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("Percentage matched with Job Description-")
        st.write(response)
    else:
        st.write("Please Upload the Resume!!!")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Here is how you can Improvise your skills--")
        st.write(response)        
    else:
        st.write("Please Upload the Resume!!!")
