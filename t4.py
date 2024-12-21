import os
from typing import Optional
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
django.setup()


from django.contrib.auth import get_user_model
from pyhub_ai.models import UserType, Conversation


import asyncio
from pyhub_ai.blocks import TextContentBlock
from pyhub_ai.mixins import AgentMixin
from pyhub_ai.specs import LLMModel

from pyhub_ai.tools.melon import (
    get_song_detail,
    search_melon_songs,
)


# 설정에 가까운 코드로 에이전트 개발 - 장고 CBV 컨셉
class AgentManager(AgentMixin):
    llm_model = LLMModel.OPENAI_GPT_4O_MINI
    llm_temperature = 0
    llm_system_prompt_template = "You're helpful assistant"
    tools = [
        get_song_detail,
        search_melon_songs,
    ]

    # 기본 동작 : 요청 객체의 .user 속성 자동 참조
    async def get_user(self) -> Optional[UserType]:
        # 임의의 User 인스턴스를 반환
        username = "chinseok"
        user, created = await get_user_model().objects\
            .aget_or_create(username=username)
        return user

    # 기본 동작 : 요청 URL에서 conversation_pk, pk 추출하여, 자동 조회
    async def get_conversation(self) -> Optional[Conversation]:
        # 임의의 Conversation 인스턴스를 반환
        user = await self.get_user()
        conv, created = await Conversation.objects\
            .aget_or_create(user=user)
        return conv

async def main():
    manager = AgentManager()
    await manager.agent_setup()

    # input_query = "[Human] 멜론에서 'APT'의 발매일은?"
    # if True:
    while input_query := input("[Human] ").strip():
        async for content_block in manager.think(input_query=input_query):
            if isinstance(content_block, TextContentBlock):
                # print(content_block.value, end="", flush=True)
                print(content_block.value)  # , end="", flush=True)
                if content_block.usage_metadata:
                    print(f"\n{content_block.usage_metadata}\n")
            else:
                print(f"received {type(content_block)}, {repr(content_block)}")

if __name__ == "__main__":
    asyncio.run(main())