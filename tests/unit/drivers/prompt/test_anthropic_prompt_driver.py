from griptape.drivers import AnthropicPromptDriver
from griptape.utils import PromptStack
from unittest.mock import ANY
import pytest


class TestAnthropicPromptDriver:
    @pytest.fixture(autouse=True)
    def mock_completion_create(self, mocker):
        mock_completion_create = mocker.patch("anthropic.Anthropic").return_value.completions.create
        mock_completion_create.return_value.completion = 'model-output'
        return mock_completion_create

    def test_init(self):
        assert AnthropicPromptDriver(api_key='1234')

    def test_try_run(self, mock_completion_create):
        # Given
        prompt_stack = PromptStack()
        prompt_stack.add_generic_input('generic-input')
        prompt_stack.add_system_input('system-input')
        prompt_stack.add_user_input('user-input')
        prompt_stack.add_assistant_input('assistant-input')
        driver = AnthropicPromptDriver(api_key='api-key')

        # When
        text_artifact = driver.try_run(prompt_stack)

        # Then
        mock_completion_create.assert_called_once_with(
            prompt=''.join([
                '\n\n',
                'Human: generic-input\n\n',
                'Human: system-input\n\n',
                'Human: user-input\n\n',
                'Assistant: assistant-input\n\n',
                'Assistant:'
            ]),
            stop_sequences=ANY,
            model=driver.model,
            max_tokens_to_sample=ANY,
            temperature=ANY,
        )
        assert text_artifact.value == 'model-output'

    def test_try_run_throws_when_prompt_stack_is_string(self):
        # Given
        prompt_stack = 'prompt-stack'
        driver = AnthropicPromptDriver(api_key='api-key')

        # When
        with pytest.raises(Exception) as e:
            driver.try_run(prompt_stack)

        # Then
        assert e.value.args[0] == "'str' object has no attribute 'inputs'"

