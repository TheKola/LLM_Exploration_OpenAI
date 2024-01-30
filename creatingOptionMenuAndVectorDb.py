import os
import pandas as pd
import regex as re
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def create_db_from_text_files(filePaths):
    _, companyNumbers = get_company_names_and_numbers(filePaths)
    for counter, companyNumber in enumerate(companyNumbers, start=1):
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
                textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
                docs = textSplitter.split_documents(documents)

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
        companyNameCleaned, companyNumber = None, None
        for line in lines:
            if line.startswith("CompanyName :: "):
                companyName = line.split("::")[1].strip()
                extracted_name = re.match(r"^[^(]+", companyName)
                if extracted_name:
                    companyNameCleaned = extracted_name.group().strip()
            elif line.startswith("company_number :: "):
                companyNumber = line.split("::")[1].strip()

        if companyNameCleaned and companyNumber:
            return companyNameCleaned, companyNumber
        else:
            return "Company information not found"
    except Exception as e:
        print(f"Error processing company info in {file_path}: {e}")
        return "Company information not found"

def get_company_names_and_numbers(filePaths):
    companyNameList, companyNumbers = [], []
    for filePath in filePaths:
        try:
            result = extract_company_info(filePath)
            if isinstance(result, tuple):
                companyNameCleaned, companyNumber = result
                companyInfo = f"{companyNameCleaned} ({companyNumber})"
                companyNameList.append(companyInfo)
                companyNumbers.append(companyNumber)
            else:
                print(f"Invalid company info in file: {filePath}")
        except Exception as e:
            print(f"Error processing file {filePath}: {e}")

    return companyNameList, companyNumbers

def get_company_option(filePaths):
    try:
        companyNames, _ = get_company_names_and_numbers(filePaths)
        titledNames = [item.title() for item in companyNames]
        titledNames_dataFrame = pd.DataFrame({'Company Names with Company numbers': titledNames})
        titledNames_dataFrame.to_csv('data/Company_Names_with_Company_Numbers(Options).csv', index=False)
        print("Option menu created successfully")
    except Exception as e:
        print(f"Error creating option menu: {e}")



# Specify the directory path of the Database
databasePath = f'data/database/'

# Get a list of all files and directories in the specified directory
fileNameList = os.listdir(databasePath)

# Get the full file paths
filePaths = [os.path.join(databasePath, fileName) for fileName in fileNameList]

# Creating option menu for the chatbot
get_company_option(filePaths)

# Creating the Vector database
create_db_from_text_files(filePaths)