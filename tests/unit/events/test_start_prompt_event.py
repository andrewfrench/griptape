import pytest
from griptape.events import StartPromptEvent


class TestStartPromptEvent:
    @pytest.fixture
    def start_prompt_event(self):
        return StartPromptEvent(token_count=123)

    def test_token_count(self, start_prompt_event):
        assert start_prompt_event.token_count == 123
