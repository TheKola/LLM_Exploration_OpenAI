import os

import pandas as pd
import regex as re
from langchain.document_loaders import TextLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


def create_db_from_text_files(file_paths):
    _, company_numbers = get_company_names_and_numbers(file_paths)
    for counter, companyNumber in enumerate(company_numbers, start=1):
        try:
            db_path = f'data/Vector_Database/{companyNumber}'
            if not os.path.exists(db_path):
                print(f"{counter}. {companyNumber} vector database does not exist")

                # Load entire Folder
                # text_loader_kwargs={'autodetect_encoding': True}
                # loader = DirectoryLoader("data/database/", glob="./*.txt",  show_progress=True, loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)

                # Load one company file
                loader = TextLoader(f'data/database/company_{companyNumber}_info.txt', encoding='utf-8')
                documents = loader.load()

                # Split the text into different chunks
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                docs = text_splitter.split_documents(documents)

                # Save to database
                Chroma.from_documents(docs, embeddings, persist_directory=db_path)
                print(f"{counter}. {companyNumber} vector database created")
            else:
                print(f"{counter}. {companyNumber} vector database already exists")
        except Exception as e:
            print(f"Error processing {companyNumber}: {e}")

    print("Vector database creation process completed")


# Function to extract company info from a single text file
def extract_company_info(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return "Company information not found"

    try:
        company_name_cleaned, company_number = None, None
        for line in lines:
            if line.startswith("CompanyName :: "):
                company_name = line.split("::")[1].strip()
                extracted_name = re.match(r"^[^(]+", company_name)
                if extracted_name:
                    company_name_cleaned = extracted_name.group().strip()
            elif line.startswith("company_number :: "):
                company_number = line.split("::")[1].strip()

        if company_name_cleaned and company_number:
            return company_name_cleaned, company_number
        else:
            return "Company information not found"
    except Exception as e:
        print(f"Error processing company info in {file_path}: {e}")
        return "Company information not found"


def get_company_names_and_numbers(file_paths):
    company_name_list, company_numbers = [], []
    for filePath in file_paths:
        try:
            result = extract_company_info(filePath)
            if isinstance(result, tuple):
                company_name_cleaned, company_number = result
                company_info = f"{company_name_cleaned} ({company_number})"
                company_name_list.append(company_info)
                company_numbers.append(company_number)
            else:
                print(f"Invalid company info in file: {filePath}")
        except Exception as e:
            print(f"Error processing file {filePath}: {e}")

    return company_name_list, company_numbers


def get_company_option(file_paths):
    try:
        company_names, _ = get_company_names_and_numbers(file_paths)
        titled_names = [item.title() for item in company_names]
        titled_names_data_frame = pd.DataFrame({'Company Names with Company numbers': titled_names})
        titled_names_data_frame.to_csv('data/Company_Names_with_Company_Numbers(Options).csv', index=False)
        print("Option menu created successfully")
    except Exception as e:
        print(f"Error creating option menu: {e}")


# Specify the directory path of the Database
database_path = f'data/database/'

# Get a list of all files and directories in the specified directory
file_name_list = os.listdir(database_path)

# Get the full file paths
file_paths = [os.path.join(database_path, fileName) for fileName in file_name_list]

# Creating option menu for the chatbot
get_company_option(file_paths)

# Creating the Vector database
create_db_from_text_files(file_paths)
