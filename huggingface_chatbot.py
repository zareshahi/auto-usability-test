from hugchat import hugchat
from hugchat.types.message import Conversation
from hugchat.login import Login
import os
from dotenv import load_dotenv

load_dotenv()


class HuggingFaceChatBot:
    def __init__(self):
        self.email = os.getenv("HF_EMAIL") or ""
        self.password = os.getenv("HF_PASS") or ""
        self.cookie_path_dir = "./ENV/cookies/"  # Ensure trailing slash (/) for directory path
        self.cookies = None
        self.chatbot = None

    def login_to_huggingface(self):
        """Logs in to Hugging Face and saves cookies."""
        try:
            sign = Login(self.email, self.password)
            self.cookies = sign.login(cookie_dir_path=self.cookie_path_dir, save_cookies=True)
            return True
        except Exception as e:
            print(f"Error logging in to Hugging Face: {e}")
            return False

    def ensure_logged_in(self):
        """Ensures the user is logged in."""
        if not self.cookies:
            if not self.login_to_huggingface():
                raise ValueError("Failed to log in to Hugging Face")

    def ensure_chatbot_initialized(self):
        """Ensures the chatbot is initialized."""
        if not self.chatbot:
            self.ensure_logged_in()
            self.chatbot = hugchat.ChatBot(cookies=self.cookies.get_dict()) if self.cookies else None

    def conversation(self, prompt):
        """Conducts a conversation with the chatbot based on the given prompt."""
        try:
            self.ensure_chatbot_initialized()

            convo = self.chatbot.new_conversation() if self.chatbot else Conversation()
            message_result = self.chatbot.chat(prompt, conversation=convo) if self.chatbot else None

            if message_result and message_result.text:
                return message_result.text
            else:
                print("Empty response from Hugging Face ChatBot")
                return None

        except ValueError as ve:
            print(f"ValueError: {ve}")
            return None
        except Exception as e:
            print(f"Error in conversation: {e}")
            return None


# Example usage:
# hf_chatbot = HuggingFaceChatBot()
# response = hf_chatbot.conversation("Hello! How are you?")
# print(response)
