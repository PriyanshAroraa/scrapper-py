import os
from langchain_community.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate

def get_llm():
    return AzureChatOpenAI(
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version=os.getenv('OPENAI_API_VERSION'),
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        azure_deployment=os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'),
        temperature=0.3
    )

def summarize_content(content):
    print("🧠 Summarizing content via Azure GPT-4o...")
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert market analyst."),
        ("human", "Summarize the following content and extract key trends, competitors, and insights:\n\n{input}")
    ])
    chain = prompt | llm
    response = chain.invoke({"input": content[:12000]})  # truncate to avoid token limit
    return response.content
