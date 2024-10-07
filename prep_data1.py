# %%
import requests
from bs4 import BeautifulSoup
import langchain_text_splitters
import llm_functions 
from openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st


# %% [markdown]
# scrape data from IRAS
@st.cache_resource
def scrap_iras_data():
# %%

    def scrape_section(section):
        """Extracts data from a single section."""
        section_data = {}
        
        # title = section.find('h2')
        # section_data['title'] = title.get_text(strip=True) if title else 'No Title Found'

        # # Extract all paragraphs
        # paragraphs = section.find_all('p')
        # section_data['paragraphs'] = [p.get_text(strip=True) for p in paragraphs]

        # # Extract lists
        # list_items = section.find_all('li')
        # section_data['list_items'] = [li.get_text(strip=True) for li in list_items]


        # Extract the title, but only if it's not empty
        title = section.find('h2')
        if title and title.get_text(strip=True):  # Check if the title exists and is non-empty
            section_data['title'] = title.get_text(strip=True)

        # Extract paragraphs, but only if they are not empty
        paragraphs = section.find_all('p')
        paragraph_texts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        if paragraph_texts:  # Only add paragraphs if there are any non-empty ones
            section_data['paragraphs'] = paragraph_texts

        # Extract list items, but only if they are not empty
        list_items = section.find_all('li')
        list_item_texts = [li.get_text(strip=True) for li in list_items if li.get_text(strip=True)]
        if list_item_texts:  # Only add list items if there are any non-empty ones
            section_data['list_items'] = list_item_texts


        tables = section.find_all('table')
        table_data = []
        for table in tables:
            rows = table.find_all('tr')
            if rows:
                table_rows = []
                for row in rows:
                    columns = row.find_all(['td', 'th'])
                    row_data = [col.get_text(strip=True) for col in columns if col.get_text(strip=True)]
                    if row_data:  # Only add the row if it's not empty
                        table_rows.append(row_data)
                if table_rows:  # Only add the table if it contains valid rows
                    table_data.append(table_rows)

        if table_data:  # Only add tables if they contain non-empty rows
            section_data['tables'] = table_data

        return section_data

    def scrape_page(url):
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        soup = BeautifulSoup(response.text, 'html.parser')
        data = []

        # Extract all sections with the specified class
        sections = soup.find_all('section', class_='eyd-rte')
        for section in sections:
            section_data = scrape_section(section)
            data.append(section_data)

        return data



    # Get the different types of relief


    all_relief_main_url = "https://www.iras.gov.sg/taxes/individual-income-tax/basics-of-individual-income-tax/tax-reliefs-rebates-and-deductions/tax-reliefs"


    all_relief_url = ['earned-income-relief',
    'spouse-relief-spouse-relief-(disability)',
    'foreign-domestic-worker-levy-(fdwl)-relief',
    "central-provident-fund(cpf)-relief-for-employees",
    "central-provident-fund-(cpf)-relief-for-self-employed-employee-who-is-also-self-employed",
    "nsman-relief-(self-wife-and-parent)",
    "parent-relief-parent-relief-(disability)",
    "grandparent-caregiver-relief",
    "sibling-relief-(disability)",
    "working-mother's-child-relief-(wmcr)",
    "qualifying-child-relief-(qcr)-child-relief-(disability)",
    "life-insurance-relief",
    "course-fees-relief",
    "central-provident-fund-(cpf)-cash-top-up-relief",
    "compulsory-and-voluntary-medisave-contributions"]

    base_url = "https://www.iras.gov.sg/taxes/individual-income-tax/basics-of-individual-income-tax/tax-reliefs-rebates-and-deductions/tax-reliefs/"



    # %%
    scrapped_all = {}   
    for relief_ in  all_relief_url:
        #scrapped_ = scrape_page(url)
        print(f"Scrapping:{base_url}{relief_}")
        scrapped_ = scrape_page(f"{base_url}{relief_}")
        scrapped_all[relief_] =scrapped_


    scrapped_all

    special_url = "https://www.iras.gov.sg/taxes/individual-income-tax/basics-of-individual-income-tax/special-tax-schemes/srs-contributions#title4"

    scrapped_ = scrape_page(special_url)
    scrapped_all["srs-contributions"] =scrapped_



    from langchain_text_splitters import RecursiveJsonSplitter

    splitter = RecursiveJsonSplitter(max_chunk_size=400)

    json_chunks = splitter.split_json(json_data=scrapped_all)

    json_docs = splitter.create_documents(texts=[scrapped_all])
    for chunk in json_chunks:
        print(chunk)


    #from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings

    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')


    # Create the vector database
    # vectordb = Chroma.from_documents(
    #     documents=json_docs,
    #     embedding=embeddings_model,
    #     collection_name="json_splitter", # one database can have multiple collections
    #     persist_directory="./vector_db"
    # )


    # from langchain import hub
    # from langchain_core.output_parsers import StrOutputParser
    # from langchain_core.runnables import RunnablePassthrough


    # from langchain_community.vectorstores import FAISS

    # # Store splits
    # vectorstore = FAISS.from_documents(documents=json_docs, embedding=embeddings_model)

    # # See full prompt at https://smith.langchain.com/hub/rlm/rag-prompt
    # prompt = ChatPromptTemplate([
    #     ("system", "You are a helpful assistant tasked to help Singapore citizens learn more about personal income tax relief \n \
    #      If you do not understand the question or do no have sufficient infomation, reply and say 'I am not sure'. \n \
    #      Use a friendly and cheerful tone "),
    #     ("human", "{question}")
    # ])

    # prompt = ChatPromptTemplate([ ("human", "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use a friendly tone. \
    # Question: {question} \
    # Context: {context} \
    # Answer:")])

    # # def format_docs(docs):
    # #     return "\n\n".join(doc.page_content for doc in docs)

    # def format_docs(docs):
    #     return "\n\n".join(doc.page_content for doc in docs)

    # llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

    # qa_chain = (
    #     {
    #         "context": vectorstore.as_retriever()| format_docs,
    #         "question": RunnablePassthrough(),
    #     }
    #     | prompt
    #     | llm
    #     | StrOutputParser()
    # )
    
    # qa_chain.invoke( {"question":"What is the NS men relief?"})

    vectorstore = FAISS.from_documents(documents=json_docs, embedding=embeddings_model)

    return vectorstore 

prompt = ChatPromptTemplate([ ("human", "You are an assistant for question-answering tasks.\
                                Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. You can present the findings in a table or in point form. \
Question: {question} \
Context: {context} \
Answer:")])

qa_chain = RetrievalQA.from_chain_type(
    ChatOpenAI(model='gpt-4o-mini', temperature=0), retriever=scrap_iras_data().as_retriever(), chain_type_kwargs={"prompt": prompt}
)

def ask_tax_relief_qn(question):
    result = qa_chain.invoke({"query": question})
    return(result["result"])




