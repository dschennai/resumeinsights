import json
import streamlit as st
from docx import Document
import os
from ChatApp import ChatApp


pdfapiurl = st.secrets["PDF_API_URL"]
pdfauthtoken = st.secrets["PDF_AUTH_TOKEN"]

COMMAND_1= """I will present you with a candidate resume. Read and Memorize the Contents. I will be presenting you with some questions"""
COMMAND_3="""Give me the supporting lines from the resume that made you come to this conclusion/result.[No pre or post text required]"""


# Set wide display
st.set_page_config(
    page_title="Resume Insights using AI",
    page_icon="🌀",
    initial_sidebar_state="collapsed",
    layout="wide"
)

st.header("Resume Insights using AI")

##########3
def ask_chat_api_3command(resumetext, userquestion):
    app = ChatApp()
    status_of_table = True
    mcount = 0
    message_list = [COMMAND_1,resumetext, userquestion, COMMAND_3]
    for m in message_list:
        res = app.chat(m)
        if mcount==2:
            answer = res['content'].strip()
        elif mcount==3:
            reference =res['content'].strip()
        mcount = mcount +1
    return answer, reference

def pdf_reader_using_api(pdf_file_name):

    # Set the API endpoint URL and authentication token

    # Set the headers for the API request
    headers = {
        'Content-Type': 'application/pdf',
        'Authorization': f'Bearer {pdfauthtoken}'
    }

    # Send the API request with the PDF file data
    with open("data/"+pdf_file_name, 'rb') as pdf_file:
        response = requests.post(pdfapiurl, headers=headers, data=pdf_file)

    # Check the response status code
    if response.status_code == requests.codes.ok:
        # Use JSON to read the data
        # Parse the JSON response into a Python dictionary
        data = json.loads(response.text)

        # We will get pagenumbner and text
        text_to_extract = ""
        for item in data:
            # Access the data fields
            field1 = item['pageNumber']
            field2 = item['text']
            text_to_extract = text_to_extract + field2
        # Remove the newlines from the response
        #response = response.text.replace('\n', '')
        #clean_text = re.sub(r'[^\w\s]', ' ', response)
        # Print the updated response

        return text_to_extract
    else:
        # Print the error mauth_tokenessage
        print(f'Error: {response.status_code} - {response.text}')

def save_file(uploadedfile):
    with open(os.path.join("data", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return format(uploadedfile.name)

def read_docx(docx_file):
    document = Document(docx_file)
    text = []
    for para in document.paragraphs:
        text.append(para.text)
    return "\n".join(text)

main,section = st.columns([5,1])
with main:
    st.write('<p style="font-size:18px; font-name:Verdana;color:black;">Resume Insight can provide you with a summary of a resume, '
             'allowing you to ask targeted questions and evaluate a candidate more effectively</p>',unsafe_allow_html=True)
    st.markdown("---")
left, center, right = st.columns([2,3, 0.75])
with left:

    st.write('<p style="font-size:18px; font-name:Verdana; color:black;">Upload your Resume</p>',unsafe_allow_html=True)
    uploadedresume = st.file_uploader("Upload your Resume", type=['pdf','doc', 'docx'],label_visibility="collapsed")
    if uploadedresume:
        #### DOCX #####
        if uploadedresume.name.lower().endswith(".docx"):
            with st.spinner("Processing " + uploadedresume.name+ "..."):
                save_file(uploadedresume)
                document_text = read_docx(uploadedresume)
        #### PDF #####
        elif uploadedresume.name.lower().endswith(".pdf"):
            with st.spinner("Uploading..."):
                save_file(uploadedresume)
                document_text = pdf_reader_using_api(uploadedresume.name)

    #st.write('<p style="font-size:22px; color:gray;">What specific knowledge or insights are you seeking? </p>',unsafe_allow_html=True)
    #question = st.text_input("text","", label_visibility="collapsed")

with center:
    st.write('<p style="font-size:18px; font-name:verdana;color:black">What specific knowledge or insights are you seeking? </p>',unsafe_allow_html=True)
    question = st.text_input("text","", label_visibility="collapsed")
    submitbtn = st.button("Get Insights")

if submitbtn:
        with st.spinner("Working on it..."):
            if uploadedresume is not None:
                st.markdown("---")
                result, response = ask_chat_api_3command(document_text, question)
                s1,s2 = st.columns([2,2])
                with s1:
                    text_input_container = st.empty()
                    t = text_input_container.text_area("Your Answer ", result)
                    if t != "":
                        text_input_container.empty()
                        st.subheader("Answer")
                        st.info(t)
                with s2:
                    text_input_container1 = st.empty()
                    t1 = text_input_container1.text_area("Reference Sentence ", response)
                    if t1 != "":
                        st.subheader("Supporting Text from Resume")
                        text_input_container1.empty()
                        st.info(t1)
