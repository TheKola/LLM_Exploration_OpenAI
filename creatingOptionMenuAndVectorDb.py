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
    counter = 0
    for companyNumber in companyNumbers:
        counter +=1
        if (not os.path.exists(f'data/Vector_Database/{companyNumber}')):
            print(f"{counter}. {companyNumber} vector database doese not exisits")
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
            Chroma.from_documents(docs, embeddings, persist_directory=f"data/Vector_Database/{companyNumber}")
            print(f"{counter}. {companyNumber} vector database created")
        
        else:
            print(f"{counter}. {companyNumber} vector database already exisits")
        
    print("Vector database created")

# Function to extract company info from a single text file
def extract_company_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    companyNameCleaned = None
    companyNumber = None

    for line in lines:
        if line.startswith("CompanyName :: "):
            companyName = line.split("::")[1].strip()
            extracted_name = re.match(r"^[^(]+", companyName)
            if extracted_name:
                companyNameCleaned = extracted_name.group().strip()

        elif line.startswith("company_number :: "):
            companyNumber = line.split("::")[1].strip()

    if companyNameCleaned and companyNumber:
        # return f"{companyNameCleaned} ({companyNumber})"
        return companyNameCleaned, companyNumber
    else:
        return "Company information not found"

def get_company_names_and_numbers(filePaths):
    companyNameList = []
    companyNumbers = []
    for filePath in filePaths:
        companyNameCleaned, companyNumber = extract_company_info(filePath)
        companyInfo = f"{companyNameCleaned} ({companyNumber})"
        companyNameList.append(companyInfo)
        companyNumbers.append(companyNumber)
    return companyNameList, companyNumbers

def get_company_option(filePaths):
    # Get the list of company name strings
    companyNames,_ = get_company_names_and_numbers(filePaths)
    titledNames = [item.title() for item in companyNames]
    titledNames_dataFrame = pd.DataFrame({'Company Names with Company numbers': titledNames})
    titledNames_dataFrame.to_csv('data/Company_Names_with_Company_Numbers(Options).csv', index=False)
    print("Option menu created sucessfully")
    return titledNames

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