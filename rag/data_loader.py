import os
import glob
from langchain_community.document_loaders import DirectoryLoader, TextLoader

def load_documents(base_folder: str):
    text_loader_kwargs = {'encoding': 'utf-8'}
    documents = []
    folders = glob.glob(f"{base_folder}/*")

    for folder in folders:
        if os.path.isdir(folder):
            doc_type = os.path.basename(folder)
            loader = DirectoryLoader(
                folder,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs=text_loader_kwargs
            )
            folder_docs = loader.load()
            for doc in folder_docs:
                doc.metadata["doc_type"] = doc_type
                documents.append(doc)
    return documents