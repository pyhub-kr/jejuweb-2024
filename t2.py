import asyncio
import json

from openai import AsyncOpenAI

from pyhub_ai.tools import function_to_json  # 함수 설명을 작성해주는 함수
from pyhub_ai.tools.melon import search_melon_songs, get_song_detail

from pyhub_ai.tools import OpenAITools
from pyhub_ai.tools.yes24 import search_yes24_books, get_yes24_toc
from pyhub_ai.tools.naver import naver_map_router


from environ import Env
env = Env()
env.read_env()  # 현재 디렉토리 .env 파일을 환경변수로서 로딩 (no overwrite)


async def main():
    # query = "멜론에서 곡 'APT'의 가수와 가사는?"

    # OpenAI LLM에게 전달할 함수 정보 생성 (function description 자동 생성)
    # tools = list(map(function_to_json, FUNCTIONS.values()))
    # keyword = "파이썬"
    # query = f"""1. {keyword} 키워드로 도서 목록을 검색해줘.
# 2. 각 도서들의 목차를 모두 읽어온 후에,
# 3. 종합해서 내가 앞으로 집필할 베스트셀러의 목차를 작성해줘."""

    query = "강남역에서 서울역으로 운전해서 가는 길을 알려줘."

    # tools = OpenAITools(search_yes24_books, get_yes24_toc)
    tools = OpenAITools(naver_map_router)

    messages = [
        {"role": "user", "content": query},
    ]

    client = AsyncOpenAI()

    while True:
        completion = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
        )
        ai_message = completion.choices[0].message
        messages.append(ai_message)  # 대화기록에 추가

        print(
            f"prompt tokens: {completion.usage.prompt_tokens}, "
            f"completion_tokens: {completion.usage.completion_tokens}"
        )

        if ai_message.tool_calls:
            async for tool_message in tools.call_funcs(ai_message.tool_calls):
                print("tool_content:", repr(tool_message["content"]))
                messages.append(tool_message)
            continue  # Tools 호출결과를 기록하고, 다시 LLM 호출
        elif ai_message.content:
            print("[AI]", ai_message.content)
            break
        else:
            print("Invalid:", ai_message)
            break


if __name__ == "__main__":
    asyncio.run(main())

