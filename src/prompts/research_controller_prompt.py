from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

RESEARCH_CONTROLLER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a deep research agent. Your task is to look at the provided topic and suggest relevant queries to comiple a research bundle for the user."
            "If chatlog contains research snippets, evaluate them, find if they have missing information. If yes, reply with more research queries to"
            " fill those gaps. Once all research have been received, compile all data into one single research bundle. Don't exclude any information",
        ),
        ("user", "Here is what to focus on the research: {topic}"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
