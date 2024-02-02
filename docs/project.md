# LLM Exploration – Open AI

**Project Overview**

This research initiative focused on evaluating the capabilities of Large Language Models (LLM) in processing and extracting insights from the website content of approximately 1.6 million companies. The primary objective was to explore the practical applications of LLMs in managing extensive text datasets, extracting pertinent information, and generating intelligent responses based on this data.

**Definition and Significance of LLMs**

Large Language Models (LLMs), such as the well-known ChatGPT, are advanced computational models trained on extensive data volumes. This extensive training enables them to comprehend and produce text that closely resembles human writing. Such capabilities make LLMs highly suitable for a variety of uses, including chatbots and content creation.

**Interesting Fact** : ChatGPT-3 has been trained on 45TB of data. ([source link](https://www.springboard.com/blog/data-science/machine-learning-gpt-3-open-ai/#:~:text=To%20summarise%3A,text%20data%20from%20different%20datasets.))

**Project Scope and Methodology**

Data City provided access to text data from over 1.6 million company websites. For this study, a random sample of 1,000 companies was selected for analysis.

This project utilised the Langchain [library](https://python.langchain.com/docs/get_started/introduction), a user-friendly, open-source tool with a growing user base. We employed GPT-4, provided through Data City's access to OpenAI's paid API.

**Project Implementation**

The project's key component was a 'retriever'. Simply put, this function involves fetching relevant documents (paragraphs) containing specified query terms. For instance, a query like "Who is Dwayne Johnson?" would prompt the retriever to locate and return all document sections mentioning Dwayne Johnson.

Conversion of documents and queries into vectors was essential for this process. (More about vectors can be found [here](https://www.mongodb.com/blog/post/vector-search-llm-essentials-what-when-why#:~:text=This%20enables%20users%20to%20query,is%20represented%20by%20a%20vector.)).

After experimenting with various Sentence Transformers, the project selected "all-MiniLM-L6-v2" for document vectorisation.

Considering the large volume of text from 1,000 companies, the transformed vectors were stored in a vector database named Chroma. This database was chosen for its open-source nature and seamless integration with Langchain.

Prior to vectorisation, each document, often extensive in size, was segmented into smaller 1,000-character chunks.

**Challenges and Solutions**

Upon testing, it was found out that the results were not promising has vectorising such huge chunk of data was reducing the accuracy of the answers. Additionally, the limitation of GPT-4's token length to 8,192 posed a challenge, as it restricted the amount of data that could be processed in a single instance.

More about tokens can be read [here](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)

This means that if the query was, "Tell me about all the Artificial Intelligence companies," the retriever would fetch all documents relevant to Artificial Intelligence companies and pass those documents to GPT to form an answer. However, since the token size is limited, not all documents could be passed. As a result, either an error due to maximum token size would be prompted, or the results would be inefficient.

To address these issues, a new approach was developed. The revised method involved creating a vector database for all companies, organised into 1000 separate folders based on company numbers. This method allowed for more efficient query responses, although it limited queries to one company at a time.

Now, the database contains 1000 folders, each labelled with company numbers, and the vectors of those companies are stored in these folders. This approach helped to answer queries accurately, but the only catch is:

**YOU CAN QUERY INFORMATION OF ONE COMPANY AT A TIME AND NOT SET OF COMPANIES.**

Through prompt engineering and various trials, the response efficiency was significantly improved. Langchain's support for prompt engineering was instrumental in this enhancement.

**User Interface and Experience**

To improve user interaction, a locally hosted application was developed using the Streamlit library. This intuitive application features a menu on the left side, allowing users to select and query about a specific company. [Snapshot of the application below]

![](RackMultipart20240202-1-82htox_html_28514858de0496b0.png)

Following the testing phase, the next project phase involves implementing [Retrieval Augmented Generation (RAG)](https://python.langchain.com/docs/use_cases/question_answering/). This feature will provide sources for the generated answers, enhancing user trust in the accuracy and reliability of the responses.

Since the retriever already implemented fetches relevant chunks of data based on the query, implementing RAG using Langchain was straightforward. The source context was printed on a drop down to keep the output tidy.

**JSON format**

At this point the answer is generated is a paragraph (sentence) and to maintain a consistent format, Jack (The project mentor) suggested to explore how well can answers (responses) be generated in JSON format which would be easier to process the responses in the later stage.

So moving ahead, firstly the prompts were modified saying "…..generate the response in JSON format". This was a good (not so good) first step. The responses generated by this was not exactly in a valid JSON format and every response was varied in terms of format.

Many different prompts (detailed) were used but none were of great deal.

Luckly, right at this stage during the project Open AI launched the chat completion in [JSON format](https://platform.openai.com/docs/guides/text-generation/json-mode). This was the perfect thing for the project.

The response generated was passed through the JSON mode, which generated clean structured validated JSON format responses.

**Conclusion**

This project was a great start to understand the booming technology of LLM (as of late 2023). LLM's are advancing day by day and new models are being launched on a weekly basis. With access to approximately 1.6 million texts from various websites, there are numerous opportunities for further exploration and development of LLM-based applications.

**Future Task**

- The project currently relies on OpenAI's paid API, which may not be scalable in the long term. Future endeavours will include exploring local LLM implementations
- **Querying grouped companies instead of individual ones.**