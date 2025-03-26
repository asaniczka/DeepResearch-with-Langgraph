from langchain.prompts import ChatPromptTemplate

SEARCH_QUERY_GENERATOR = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a google search query generator. When provided with a information goal, your task is to reply with 3-5 queries that would"
            " help discover information related to the infromation goal. A different agent willl go, search, and extract information based on"
            " queries provided by you. Each query shoudl not contain more than 3-6 words. Only return a max of 4 search queries (contextually different from one another so they don't return the same search results) Reply in valid JSON with search_queries as the key",
        ),
        (
            "user",
            "Here is what to focus on the query generation: {summarization_target}",
        ),
    ]
)
