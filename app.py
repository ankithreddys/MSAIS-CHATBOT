import os
from dotenv import load_dotenv
import gradio as gr
from langchain_core.messages import HumanMessage, SystemMessage
from rag.data_loader import load_documents
from rag.text_splitter import split_documents
from rag.vector_store import get_or_create_vector_store
from rag.pipeline import build_rag_pipeline

# Load environment variables
load_dotenv()
GAITOR_API_KEY = os.getenv("GAITOR_API_KEY")

def initialize_rag():
    documents = load_documents("DATA")
    chunks = split_documents(documents)
    vector_store = get_or_create_vector_store(chunks)
    rag_chain = build_rag_pipeline(GAITOR_API_KEY, vector_store)
    return rag_chain

rag_chain = initialize_rag()

SYSTEM_PROMPT = """
You are an expert assistant for the Master’s in Artificial Intelligence Systems (MSAIS) program at the University of Florida. Your primary role is to provide accurate, concise, and authoritative information about the program based solely on the provided documents, covering areas such as courses, admissions, faculty, research opportunities, and other program-specific details.

- Respond to all questions with clarity and professionalism, directly referencing relevant details from the documents to ensure accuracy.
- For every question, actively search the documents for any links (e.g., program websites, application portals, course pages, or faculty profiles) related to the context of the inquiry. If relevant links are found, explicitly include them in your response, formatted clearly (e.g., 'For more details, visit: [link]'), to provide users with immediate access to additional resources.
- If a question pertains to a specific person (e.g., faculty or staff), include their contact details (e.g., email, phone number, or office location) if available in the documents, formatted clearly (e.g., 'Contact: [email/phone]').
- If no relevant links or contact details are found for a specific question, state that no links or contact information are available but provide the most accurate information possible from the documents.
- If a question is unclear or the requested information is not available in the documents, politely explain that the information is not found, and recommend contacting the MSAIS program office at the University of Florida for further assistance (e.g., 'Please contact the MSAIS program office at cise@ufl.edu or visit https://www.cise.ufl.edu/academics/graduate/msais/ for more information').
- Maintain a welcoming, professional, and approachable tone suitable for students, faculty, prospective applicants, and other stakeholders.
"""

def chat(message, history):
    result = rag_chain.invoke({"question": message})
    return result["answer"]

# Load the streamlined CSS
with open("custom.css") as f:
    custom_css = f.read()

theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="orange",
    neutral_hue="gray",
    radius_size="md",
).set(
    body_background_fill="#e6ecef",
    panel_background_fill="linear-gradient(135deg, #1a2a44 0%, #2e4057 100%)",
    button_primary_background_fill="#004A98",
    button_primary_text_color="#ffffff",
    input_background_fill="#2e4057",
)

examples = [
    "What are the admission requirements for the MSAIS program?",
    "Who are the faculty members in the MSAIS program?",
    "What courses are offered in the MSAIS curriculum?",
    "Are there research opportunities for MSAIS students?",
]

description = """
<div id="msais-title">
    MSAIS Program Assistant
</div>
<div style="text-align:center;">
    Welcome to the University of Florida's MSAIS Program Assistant. Ask questions about courses, admissions, faculty, research, and more!
</div>
<hr style="margin-top: 1.5em;">
"""

with gr.Blocks(theme=theme, css=custom_css) as demo:
    gr.ChatInterface(
        fn=chat,
        type="messages",
        examples=examples,
        description=description,
        submit_btn="Send",
        textbox=gr.Textbox(placeholder="Ask about the MSAIS program...")
    )
    gr.HTML(
        "<div class='msais-footer'>Powered by University of Florida Engineering Education Department</div>"
    )


if __name__ == "__main__":
    demo.launch(share=True)
