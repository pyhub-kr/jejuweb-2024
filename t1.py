tools = [
    {
        "type": "function",
        "function": {
            "name": "search_melon_songs",
            "description": "멜론 사이트에서 곡을 검색합니다.",
            "parameters": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {
                        "type": "string",
                    }
                },
                "additionalProperties": False,
            },
        },
        "strict": True,
    },
]

query = "멜론에서 곡 'APT'의 가수와 가사는?"

from openai import OpenAI

client = OpenAI()
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": query}],
    tools=tools,
)

print(completion.choices[0].message.content)
print()
print(completion.choices[0].message.tool_calls)

