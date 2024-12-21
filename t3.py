import asyncio

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.tools import tool     # 렝체인 기본 tool
from langchain_openai import ChatOpenAI
from pyhub_ai.tools import tool_with_retry  # 재시도를 지원하는 tool
from pyhub_ai.tools.melon import search_melon_songs, get_song_detail

async def main():
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    tools = [
        # 랭체인에서는 Tool로서 함수를 바로 못 써요. 함수를 Tool 타입으로 반드시 변환 후에 활용.
        tool_with_retry(search_melon_songs),
        tool_with_retry(get_song_detail),
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You're helpful assistant."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    query = "멜론에서 'APT'의 발매일은?"

    # 에이전트 생성 : 주어진 입력으로 LLM을 통한 1회성 실행 및 응답
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

    # 에이전트 실행기 생성 : 에이전트 실행/관리, Tool 실행 및 결과 처리, 최대 실행 시간 체크 등
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    res = await agent_executor.ainvoke({"input": query})
    print("[AI]", res["output"])  # or "input" key

if __name__ == "__main__":
    asyncio.run(main())
