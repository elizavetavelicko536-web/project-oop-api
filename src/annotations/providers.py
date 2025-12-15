from __future__ import annotations
from typing import final
from .core import BaseProvider
from dotenv import load_dotenv
load_dotenv()
from gigachat import GigaChat

class MockProvider(BaseProvider):
    def annotate(self, text: str, prompt: str) -> str:
        return (
            f"[MOCK RESPONSE]\n"
            f"Prompt: {prompt}\n"
            f"Text length: {len(text)} chars\n"
            f"Summary: {text[:200]}{'...' if len(text) > 200 else ''}"
        )

class GigaChatProvider(BaseProvider):
    def __init__(self, credentials: str, model: str = "GigaChat"):
        self.giga = GigaChat(credentials=credentials, model=model, verify_ssl_certs=False)
        self.model = model

    @final
    def annotate(self, text: str, prompt: str) -> str:
        clean_prompt = (
            f"{prompt}\n\n"
            f"ВАЖНО: ответ должен быть в виде чистого текста без использования "
            f"маркдаун разметки (не используй *, **, #, ##, `, [], (), > и другие "
            f"символы форматирования). Просто обычный текст с абзацами.\n\n"
            f"Текст для аннотации:\n{text}"
        )

        resp = self.giga.chat(clean_prompt)
        return resp.choices[0].message.content