from openai import OpenAI


def summerize_page(page: str, summarization_target: str):
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4o",
        instructions="You are page summerizer for a researcher. You'll be provided with the markdown page and the target information to extract in the summerizations. Reply back with a full summary and don't exclude any requried info. Maintain any related or important urls. Include citations",
        input=[
            {
                "role": "user",
                "content": f"Here is what to focus on the summerization: {summarization_target}",
            },
            {
                "role": "user",
                "content": page,
            },
        ],
    )

    print(response.output_text)
