from langchain.prompts import ChatPromptTemplate

SUMMERIZE_GROUP_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a summary aggregrator. You'll be provided with a few summaries created by different agent all with the goal of extracting certain information. Your task is to aggregate those summaries into one reseach document. Reply back with a full summary and don't exclude any requried info. Maintain any related or important urls. Include citations",
        ),
        ("user", "Here is what to focus on the summerization: {summarization_target}"),
        ("user", "{all_pages}"),
    ]
)
