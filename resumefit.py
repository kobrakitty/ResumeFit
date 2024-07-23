from openai import OpenAI
import streamlit as st
import os

# Get your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Used in production

# Initialize the client with your API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")  # Ensure your API key is set in the environment variables
)

# Define the comparison function
def compare_resume_to_job_description(resume_text, job_description_text):
    # Prepare the prompt for the AI
    prompt = f"""
    Compare the following resume with the job description below:
    Resume:
    {resume_text}
    Job Description:
    {job_description_text}
    Identify the skills and qualifications mentioned in both texts. Highlight the skills and qualifications present in the resume but missing from the job description, and those required by the job but missing from the resume. Provide a qualification percentage based on the overlap of skills and qualifications.
    Additionally, provide detailed suggestions for improvement, including specific skills or qualifications that the individual should focus on acquiring or improving to better match the job description.
    """
    # DO NOT CHANGE THIS SECTION:::
    # Set the temperature to 0 for consistent results
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0
    )
    
    # Extract the relevant information from the response
    return response.choices[0].message.content.strip()
    # DO NOT CHANGE THIS SECTION^^^
    
# Streamlit app
# Main Page Design
st.title('ResumeFit📝')
st.subheader('Find the job that is the best _fit_ for you!', divider='rainbow')
st.write('⚠️ Important: Always verify AI-generated responses. Do not enter any personal identifying information such as your address or contact information. Please remove any sensitive data before submitting to better protect your privacy.')

# Options for user inputs
option = st.radio("Choose how you want to input your resume and job description:", 
                  ("Upload resume and job description files",
                   "Enter text for resume and job description"))

resume_text = ""
job_description_text = ""

# Handling different options
if option == "Upload resume and job description files":
    resume_file = st.file_uploader("Upload your resume", type=["txt", "pdf", "docx"])
    job_description_file = st.file_uploader("Upload the job description", type=["txt", "pdf", "docx"])
    if resume_file is not None and job_description_file is not None:
        resume_text = resume_file.read().decode("utf-8")
        job_description_text = job_description_file.read().decode("utf-8")

elif option == "Enter text for resume and job description":
    resume_text = st.text_area("Paste your resume here", height=300)
    job_description_text = st.text_area("Paste the job description here", height=300)

# Submit Button
submit_button = st.button("Compare")

# When the user clicks the 'Compare' button, process the inputs
if submit_button:
    if resume_text and job_description_text:
        comparison_result = compare_resume_to_job_description(resume_text, job_description_text)
        st.markdown("### Comparison Results")
        st.write(comparison_result)
        
        # Prepare the results for download
        def convert_to_file(text):
            return str(text)

        result_file = convert_to_file(comparison_result)
        st.download_button(
            label="Download Results",
            data=result_file,
            file_name="comparison_results.txt",
            mime="text/plain"
        )
    else:
        st.error("Please provide both resume and job description.")