
# MSAIS Program Assistant

The MSAIS Program Assistant is a conversational AI tool designed for the University of Florida’s Master’s in Artificial Intelligence Systems (MSAIS) program. It provides accurate, document-grounded answers to questions about admissions, courses, faculty, research opportunities, and other program details. Using a Retrieval-Augmented Generation (RAG) framework, it leverages official documents scraped from the UF MSAIS website to ensure reliable and authoritative responses.

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![HuggingFace Spaces](https://img.shields.io/badge/HuggingFace-Spaces-orange.svg)](https://huggingface.co/spaces/arsubhanpuram/MSAIS_ASSISTANT)

## Features

- **Document-Grounded Answers**: Responds to queries using only official MSAIS documents, ensuring accuracy and relevance.
- **Contextual Citations**: Automatically includes relevant links or contact information from source documents when available.
- **Efficient Search**: Utilizes FAISS for fast, scalable vector-based document retrieval, enabling quick responses even with large datasets.
- **Customized Interface**: Features a user-friendly Gradio web interface with UF-inspired branding for a professional and cohesive experience.
- **Extensible Design**: Easily expand the knowledge base by adding new `.txt` documents to the `DATA/` directory, with automatic indexing.

## Tech Stack

The project is built with a modern, robust stack tailored for conversational AI and document retrieval:

- **LangChain**: A framework for orchestrating the RAG pipeline, handling document loading, text splitting, retrieval, and response generation.
- **FAISS**: A high-performance library for vector similarity search, used to store and query document embeddings efficiently.
- **HuggingFace Transformers**: Provides pre-trained models for generating high-quality document embeddings to enable semantic search.
- **Gradio**: A Python library for creating intuitive, web-based user interfaces, customized with UF branding for this project.
- **NaviGator Toolkit API**: Powers the conversational AI with UF’s Llama-3.1-70B-Instruct model, hosted by the University of Florida’s AI infrastructure.
- **Scrapy**: A web scraping framework used to collect comprehensive data from the official UF MSAIS website, forming the assistant’s knowledge base.
- **Python**: Version 3.9 or higher, ensuring compatibility and access to modern libraries.

## Project Structure

The codebase is organized for modularity and ease of maintenance:

```
├── rag/                    # Core RAG pipeline components
│   ├── data_loader.py      # Loads and processes documents from DATA/
│   ├── text_splitter.py    # Splits documents into chunks for vector search
│   ├── vector_store.py     # Manages FAISS vector database creation and queries
│   └── pipeline.py         # Orchestrates the RAG workflow (retrieval + generation)
├── vector_db_faiss/        # Stores the FAISS index (auto-generated)
├── DATA/                   # Directory for official .txt documents
├── app.py                  # Entry point for the Gradio web application
├── requirements.txt        # Lists all Python dependencies
├── custom.css              # Custom styles for the Gradio UI
├── .env                    # Stores sensitive environment variables (e.g., API key)
└── README.md               # Project documentation
```

## Getting Started

Follow these steps to set up and run the MSAIS Program Assistant locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ankithreddys/MSAIS-CHATBOT.git
   cd MSAIS-CHATBOT
   ```
   This retrieves the project code from GitHub.

2. **Set Up the Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   Creates a virtual environment and installs all required dependencies, ensuring a clean setup.

3. **Add Documents**:
   Place official MSAIS documents as `.txt` files in the `DATA/` directory, organized by category:
   ```
   DATA/
     admissions/requirements.txt
     courses/descriptions.txt
     faculty/directory.txt
   ```
   The project uses [Scrapy](https://scrapy.org/) to scrape data from the UF MSAIS website, which populates the initial dataset. To update the knowledge base, you can either run the Scrapy spider (if provided in a `Webscraping/` directory) or manually add new `.txt` files, which are automatically indexed on the next run.

4. **Set the API Key**:
   Create a `.env` file in the project root with your NaviGator Toolkit API key:
   ```
   GAITOR_API_KEY=your_api_key
   ```
   To obtain a key, visit [ai.ufl.edu](https://ai.ufl.edu) or contact the UF AI infrastructure team for access to the NaviGator Toolkit API.

5. **Run the Application**:
   ```bash
   python app.py
   ```
   This launches the Gradio web interface, accessible in your browser. Alternatively, explore the live demo on [HuggingFace Spaces](https://huggingface.co/spaces/arsubhanpuram/MSAIS_ASSISTANT), which runs the same codebase with the latest document set.

## Customization

The assistant is designed for flexibility to meet evolving needs:

- **Adding Documents**: Place new `.txt` files in the `DATA/` directory, organized by topic. The system automatically indexes them on the next run, expanding the knowledge base without code changes.
- **UI Customization**: Modify `custom.css` for styling adjustments or edit `app.py` to tweak the Gradio interface layout and theming, such as aligning with UF’s visual identity.
- **Model Configuration**: Update `pipeline.py` to experiment with different LLMs or embedding models, allowing adaptation to new AI advancements or UF infrastructure changes.

## Behavior

The assistant adheres to strict guidelines to ensure reliability and professionalism:

- **Document-Based Responses**: Answers are generated exclusively from the provided MSAIS documents, preventing speculation or external data use.
- **Citation of Sources**: When links or contact details (e.g., email addresses, phone numbers) are present in the documents, they are included in responses for user convenience.
- **Fallback Guidance**: If a query cannot be answered due to missing data, the assistant directs users to official UF resources, such as [ai.ufl.edu](https://ai.ufl.edu).
- **Professional Tone**: Responses are clear, courteous, and tailored for students, faculty, and staff, fostering an approachable yet authoritative interaction.

## Security

Security and privacy are prioritized to protect user data and system integrity:

- **Local Processing**: All document processing and vector storage occur locally, with the exception of API calls to the NaviGator Toolkit for LLM inference.
- **Secure API Key Storage**: The API key is stored in the `.env` file, which is excluded from version control, preventing accidental exposure.
- **No Third-Party Sharing**: Documents and user queries are not shared with external services beyond UF’s NaviGator Toolkit API.

## Deployment

The assistant is deployed on [HuggingFace Spaces](https://huggingface.co/spaces/arsubhanpuram/MSAIS_ASSISTANT), providing a publicly accessible interface for users to interact with the system without local setup. The hosted version is kept up-to-date with the latest documents and codebase, offering a convenient way to explore the assistant’s capabilities.

## Support

For assistance, questions, or feedback:
- Open an issue on the [GitHub repository](https://github.com/ankithreddys/MSAIS-CHATBOT/issues) to report bugs or suggest improvements.

## Credits

Developed by [Ankith Reddy](https://github.com/ankithreddys) at the University of Florida, 2025. This project leverages UF’s AI infrastructure and is designed to support MSAIS students, faculty, and staff in accessing program information efficiently.

---

<p align="center">
  <a href="https://huggingface.co/spaces/arsubhanpuram/MSAIS_ASSISTANT">Try it on HuggingFace Spaces 🚀</a>
</p>

---
