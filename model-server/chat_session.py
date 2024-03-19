from typing import TypeVar, Generic
from dataclasses import dataclass, asdict
import requests
import json
from logger import log
import os
    
@dataclass
class Message:
    role: str
    content: str
    def __init__(self, content: str, role="user") -> None:
        self.role = role
        self.content = content

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    

@dataclass
class ChatResponse:
    message: Message

    @classmethod
    def from_dict(cls, data):
        data['message'] = Message.from_dict(data['message'])
        return cls(**data)

    def to_dict(self):
        data = asdict(self)
        data['message'] = asdict(data['message'])
        return data    

class Chat:
    _session_id: str
    _context: str
    _model_name: str
    _summary: str
    _key_entities: list[str]
    _chat_content: list[Message] = []

    _system="""
        You are Enigma, an LLM developed by Team Strivers to summarize legal documents and extract key insights. Your primary function is to respond to questions related to specific paragraphs within these documents.

        Master Prompt:

        Input: [Contextual Paragraph]

        you will be given the input and you have to provide the answer of the question based on the given input.

        Don't provide the answer of the question if it is not related to the context paragraph.
    """

    def set_summary(self, summary: str):
        self._summary = summary

    def get_summary(self):
        log(self._summary)
        return self._summary

    def set_key_entities(self, entities: list[str]):
        self._key_entities = entities

    def get_key_entities(self):
        return self._key_entities

    def __init__(self, id: str):
        self._session_id = id

    def set_context(self, context: str):
        self._context = context
        log(self._chat_content)
        self._chat_content.append(
            Message(f"[Context] \n{self._context} [Context]", role="assistant"))
        return "done"

    def get_context(self):
        return self._context

    def _get_model_response(self) -> str:
        try:
            model_url = "https://api.mistral.ai/v1/chat/completions"
            key=os.environ.get("MISTRAL_KEY")
            response = requests.post(model_url, headers={
                "Authorization": f"Bearer {key}",
                "content-type": "application/json"
            }, json={
                "model": "open-mistral-7b",
                "messages": [
                    {"role": "system", "content": self._system},
                    *self.get_messages()
                ],
            })
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except:
            return "failed"
    

    def send_message(self, inp: str, bot=False):
        self._chat_content.append(Message(inp))
        model_response = self._get_model_response()
        self._chat_content.append(Message(role="assistant", content=model_response))
        return model_response
    
    def get_messages(self):
        return [message.__dict__ for message in self._chat_content]

    def get_session_details(self):
        return {
            "session_id": self._session_id,
            "context": self._context,
            "model_name": self._model_name,
            "messages": self.get_messages()[1:]
        }

    def get_session_id(self):
        return self._session_id



class ChatSession:
    _chat_sessions: list[Chat] = []

    def get_chat_session(self, id: str):
        for session in self._chat_sessions:
            if id == session.get_session_id():
                return session
        return self.create_chat_session(id)
    
    
    def create_chat_session(self, id: str):
        for session in self._chat_sessions:
            if session.get_session_id() == id:
                return None
        self._chat_sessions.append(Chat(id))
        return self._chat_sessions[-1]
    




if __name__=="__main__":
    message = Message("Hi")
    print(json.dumps(message))

