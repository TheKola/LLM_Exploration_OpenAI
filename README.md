# Company Chatbot

## Introduction
This chatbot application provides information about companies based on their website content. Users can select a company and ask questions, with the chatbot extracting and analyzing information from the company's website to provide detailed responses.

This project represents the first step in understanding how well Large Language Models (LLMs) can be utilized with The Data City's data, specifically website texts. More information about this research can be found  [here](https://thedatacity.sharepoint.com/:w:/s/TheDataCity/EZ05n8QrgDhBthvy82tVjkwBGSUQyS5eAyjBUlx1lWahTg?e=aVBo7E) 

## Features
- Select a company from the dropdown menu.
- Ask questions about the selected company.
- Receive detailed responses based on the company's website content.

## Getting Started
- Clone the repository to your local machine:
```shell
git clone https://github.com/TheDataCity/LLM_Exploration_OpenAI.git
```
- Set up and activate the virtual environment:
```shell
# pip install virtualenv
virtualenv [virtual_env_name]
[virtual_env_name]/Scripts/activate   

```
- Install the dependencies using pip:
```shell
pip install --no-cache -r requirements.txt
```
## Populating the Database
The database folder in the data directory should contain text files extracted from various companies' websites. These text files will be used by the chatbot to provide information about specific companies. Sample text files are provided in the root directory. Please paste all the company files in the database folder.
Note: The naming convention of the files should follow the format provided in the sample file.

## Creating the Vector Database
To create the database and the option menu required for the application, run:
```shell
python creatingOptionMenuAndVectorDb.py
```
This will create the vector database for each company and store it in the data/Vector_Database directory. A .csv file with all company names and numbers will be generated in the data directory.

Once the database is created, execute the main.py file:
```shell
streamlit run main.py
```

## Usage
- Choose a company from the dropdown menu.
- Enter your question in the chat input.
- Chat with the chatbot to get information about the selected company.
- Select the "JSON Response" option from the side menu to get the answer in JSON format.