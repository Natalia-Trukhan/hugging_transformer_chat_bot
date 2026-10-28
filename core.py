from typing import Final, Dict, List

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class ConversationHistory:
    # Constants defining history length limits and trimming thresholds
    MAX_HISTORY_MESSAGES: Final[int] = 50
    START_HISTORY_MESSAGES: Final[int] = 6
    END_HISTORY_MESSAGES: Final[int] = 10

    def __init__(self, system_prompt: str) -> None:
        # Initialize system prompt and empty message history list
        self.system_prompt = system_prompt
        self.history: List[Dict[str, str]] = []

    def add_request(self, text_user: str) -> None:
        # Append user message to history and check if history control is needed
        self.history.append({
            'role': 'user',
            'content': text_user,
        })
        self.control_history()

    def add_response(self, text_bot: str) -> None:
        # Append assistant response to history and check if history control is needed
        self.history.append({
            'role': 'assistant',
            'content': text_bot,
        })
        self.control_history()

    def get_messages(self) -> List[Dict[str, str]]:
        # Prepare the full message payload including system prompt and history
        message = [{
            'role': 'system',
            'content': self.system_prompt,
        }]
        message.extend(self.history)
        return message

    def control_history(self) -> None:
        # Trim history if it exceeds the maximum allowed message count
        if len(self.history) > ConversationHistory.MAX_HISTORY_MESSAGES:
            start_history = self.history[:ConversationHistory.START_HISTORY_MESSAGES]
            end_history = self.history[-ConversationHistory.END_HISTORY_MESSAGES:]
            self.history = start_history + end_history


class Bot:
    def __init__(self, name_model: str = "Qwen/Qwen3-1.7B", system_info: str = "system_prompt.txt") -> None:
        # Read system prompt from the configuration file
        with open(system_info, "r", encoding='utf-8') as file:
            system_prompt = file.read().strip()

        # Initialize the conversation history manager
        self.history_manager = ConversationHistory(system_prompt)

        # Set up device, tokenizer, and model
        self.device, self.tokenizer, self.model = self.prepare_model_and_device(name_model)

    def prepare_model_and_device(self, model_name):
        # Determine the compute device (GPU if available, otherwise CPU)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Use device: {device}.")

        # Load tokenizer and causal language model from pretrained source
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        # Move model to device and switch to evaluation mode
        model.to(device)
        model.eval()

        return device, tokenizer, model

    def generate_response(self, user_text: str) -> str:
        # Add user request to history and retrieve formatted messages
        self.history_manager.add_request(user_text)
        messages = self.history_manager.get_messages()

        # Apply chat template to convert messages into model inputs
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors='pt'
        )

        # Move input tensors to the model's device
        inputs = inputs.to(self.model.device)

        # Generate tokens in inference mode without gradient calculation
        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=3000,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Extract only the newly generated tokens by slicing past the input length
        inputs_len = inputs['input_ids'].shape[-1]
        new_tokens = outputs[0][inputs_len:]

        # Decode generated tokens back into a readable text response
        response_text = self.tokenizer.decode(new_tokens, skip_special_tokens=True)

        # Save assistant response to history
        self.history_manager.add_response(response_text)

        return response_text
