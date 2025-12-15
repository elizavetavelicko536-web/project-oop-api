from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar, Protocol, List
import os

T = TypeVar('T')

@dataclass
class AnnotationResult:
    file_name: str
    prompt: str
    text: str

    def __post_init__(self):
        if not self.text.strip():
            raise ValueError("Текст аннотации не может быть пустым")

    def __add__(self, other: 'AnnotationResult') -> 'AnnotationResult':
        if not isinstance(other, AnnotationResult):
            return NotImplemented
        return AnnotationResult(
            file_name=f"{self.file_name}|{other.file_name}",
            prompt=f"{self.prompt}|{other.prompt}",
            text=self.text + "\n\n" + other.text
        )

    def __iadd__(self, other: 'AnnotationResult') -> 'AnnotationResult':
        self.text += "\n\n" + other.text
        self.prompt = f"{self.prompt}|{other.prompt}"
        self.file_name = f"{self.file_name}|{other.file_name}"
        return self

    @property
    def file_basename(self) -> str:
        return os.path.basename(self.file_name)

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    @property
    def char_count(self) -> int:
        return len(self.text)

    @property
    def summary(self) -> str:
        if len(self.text) <= 100:
            return self.text
        return self.text[:100] + "..."

    def to_dict(self) -> dict:
        return {
            'file_name': self.file_name,
            'prompt': self.prompt,
            'text': self.text,
            'word_count': self.word_count,
            'char_count': self.char_count,
            'file_basename': self.file_basename
        }

    @classmethod
    def combine_all(cls, results: List['AnnotationResult']) -> 'AnnotationResult':
        if not results:
            raise ValueError("Нет результатов для объединения")

        combined = results[0]
        for result in results[1:]:
            combined += result
        return combined


class BaseProvider(Protocol):
    def annotate(self, text: str, prompt: str) -> str:
        ...


class ProviderFactory:
    @staticmethod
    def create(name: str) -> BaseProvider:
        from .providers import GigaChatProvider, MockProvider
        import os

        if name == "gigachat":
            cred = os.getenv("GIGACHAT_AUTH_KEY")
            if not cred:
                raise RuntimeError("GIGACHAT_AUTH_KEY не задан")
            return GigaChatProvider(credentials=cred)
        elif name == "mock":
            return MockProvider()
        else:
            raise ValueError(f"Неизвестный провайдер: {name}")