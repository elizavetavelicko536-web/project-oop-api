from src.annotations.providers import MockProvider, GigaChatProvider

def test_mock_provider():
    provider = MockProvider()
    result = provider.annotate("Привет", "Сделай тест")
    assert "MOCK RESPONSE" in result
    assert "Привет" in result

def test_gigachat_provider_instance():
    provider = GigaChatProvider(credentials=None)
    assert provider is not None