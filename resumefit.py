import streamlit as st
from openai import OpenAI
import os
import io
import PyPDF2
import docx2txt

# Get your OpenAI API key from environment variables
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize the client with your API key
client = OpenAI(api_key=api_key)

# Define the comparison function
def compare_resume_to_job_description(resume_text, job_description_text):
    # ... (rest of the function remains the same)

def read_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return read_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(uploaded_file)
    else:
        return uploaded_file.read().decode("utf-8")

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    return " ".join(page.extract_text() for page in pdf_reader.pages)

def read_docx(file):
    return docx2txt.process(io.BytesIO(file.read()))

# Streamlit app
# Main Page Design
st.title('ResumeFit📝')
st.subheader('Find the job that is the best _fit_ for you!', divider='rainbow')
st.write('⚠️ Important: Always verify AI-generated responses. Do not enter any personal identifying information such as your address or contact information. Please remove any sensitive data before submitting to better protect your privacy.')

# When the user clicks the 'Compare' button, process the inputs
if submit_button:
    if resume_text and job_description_text:
        with st.spinner("Comparing resume to job description..."):
            try:
                comparison_result = compare_resume_to_job_description(resume_text, job_description_text)
                st.markdown("### Comparison Results")
                st.write(comparison_result)
                
                # Prepare the results for download
                st.download_button(
                    label="Download Results",
                    data=comparison_result,
                    file_name="comparison_results.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please provide both resume and job description.")
