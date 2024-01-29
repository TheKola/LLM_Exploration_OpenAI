# Company Chatbot

## Introduction
This is a chatbot application that provides information about companies based on their website content. Users can select a company and ask questions, and the chatbot will extract and analyze information from the company's website to provide detailed responses.

## Features
- Select a company from the dropdown menu.
- Ask questions about the selected company.
- Receive detailed responses based on the company's website content.

## Prerequisites
Before running this application, make sure you have the following dependencies installed:
- Python
- Streamlit
- Langchain

## Getting Started
1. Clone this repository to your local machine.
2. Run the creatingOptionMenuAndVectorDbcreatingOptionMenuAndVectorDb.py file to generate and store the options used in the dropdown menu of the application. The options will be stored in `Company_Names_with_Company_Numbers(Options).csv`, under the data folder.
3. Run the Streamlit application by executing `streamlit run src/main.py`.
4. Select a company from the dropdown menu and start chatting with the chatbot.

## Usage
- Choose a company from the dropdown menu.
- Enter your question in the chat input.
- Chat with the chatbot to get information about the selected company.

## Database Folder

The database folder contains text files extracted from various companies' websites. These text files are used by the chatbot to provide information about specific companies.

**Location**: The database folder is expected to be located in the root directory of this project. You can download the database sample or provide your own set of text files (Follow the structure (body and name) of the file, remove "(Sample)"). The project folder structure should look like this:<br/>
project-root/<br/>
│<br/>
├── database/<br/>
│ ├── company_1_info.txt<br/>
│ ├── company_2_info.txt<br/>
│ ├── company_3_info.txt<br/>
│ └── ...<br/>
│<br/>
├── downloaded-folder<br/>
│ ├── src<br/>
│ │ ├── main.py<br/>
│ │ ├── langchain_func.py<br/>
│ │ ├── README.md<br/>
│ │ ├── company_00856444_info(Sample).txt<br/>
│ │ ├── requirements.txt<br/>
│ ├── data<br/>
│ │ ├── Company_Names_with_Company_Numbers(Options).csv<br/>


