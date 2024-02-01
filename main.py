import os
import streamlit as st
import pandas as pd
import regex as re
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
import json
from output_praser import parse_response

try:
    load_dotenv()
except Exception as e:
    st.error(f"Error loading environment variables: {e}")

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

st.set_page_config(page_title="Companies Information Bot", page_icon="🌐")
st.title("💬 Companies Info Chat Bot")

# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True)

@st.cache_resource(ttl="1h")

def get_retriever(companyNumber):
    try:
        db = Chroma(persist_directory=f"data/Vector_Database/{companyNumber}", embedding_function=embeddings)
        retriever = db.as_retriever(search_kwargs={"k": 4, "fetch_k": 4})
        return retriever
    except Exception as e:
        st.error(f"Error in get_retriever: {e}")
        return None

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        # Workaround to prevent showing the rephrased question as output
        if prompts[0].startswith("Human"):
            self.run_id_ignore_token = kwargs.get("run_id")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.run_id_ignore_token == kwargs.get("run_id", False):
            return
        self.text += token
        self.container.markdown(self.text)

class PrintRetrievalHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.status = container.status("Company Information Context")

    def on_retriever_start(self, serialized: dict, query: str, **kwargs):
        print("Query :- ", query)
        #self.status.write(f"**Question:** {query}")
        #self.status.update(label=f"**Context Retrieval:** {query}")
        self.status.update(label=f"Company Information Context")

    def on_retriever_end(self, documents, **kwargs):
        for idx, doc in enumerate(documents):
            source = os.path.basename(doc.metadata["source"])
            self.status.write(f"**Document {idx+1} from {source}**")
            self.status.markdown(doc.page_content)
        self.status.update(state="complete")

def clear_content():
    msgs.clear()
    initialMessage = 'Ask me anything about "' + st.session_state['issue'] + '" !'
    msgs.add_ai_message(initialMessage)

with st.sidebar:
    # Dropdown Menu
    try:
        option = st.selectbox(
        'Select a company about which you want to know',
        (pd.read_csv(f'data/Company_Names_with_Company_Numbers(Options).csv')),index=None, placeholder="Select a company",on_change=clear_content, key = 'issue')
    
        if option is not None:
            match = re.search(r'\(([^)]+)\)', option)
            extractedOption = match.group(1)
            temp = extractedOption
            extracted_name = re.match(r"^[^(]+", option)
            if extracted_name:
                companyName = extracted_name.group().strip()

    except Exception as e:
        st.error(f"Error loading company options: {e}")

    # st.write('You selected:', option)
        
    jsonOutput = st.checkbox('JSON Response')
    "[View the source code](https://github.com/TheDataCity/LLM_Exploration_OpenAI/tree/json_response)"

if not option:
        st.info("Please select a company from the drop down menu")
        st.stop()

try:
    retriever = get_retriever(extractedOption)
    if retriever is None:
        st.stop()
except Exception as e:
    st.error(f"Error initializing the retriever: {e}")
    st.stop()

# Setup LLM and QA chain
try:
    llm = ChatOpenAI(model_name="gpt-4", temperature=0, streaming=True)
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory, verbose=True)
except Exception as e:
    st.error(f"Error initializing language model or QA chain: {e}")
    st.stop()

avatars = {"human": "❓", "ai": "❄️"}

for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input(placeholder="Ask me anything about the company!"):
    st.chat_message("user", avatar= "❓").write(user_query)

    with st.chat_message("assistant", avatar="❄️"):
        retrieval_handler = PrintRetrievalHandler(st.container())
        stream_handler = StreamHandler(st.empty())
        print("user_query :- ", user_query)
        response = qa_chain.run(user_query, callbacks=[retrieval_handler, stream_handler])
        print("response : - ", response)
        if jsonOutput == True:
            jsonResponse = parse_response(response)
            st.json(jsonResponse)

