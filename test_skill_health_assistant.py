import pytest
import app
import logic
import requests
import json

url = "http://127.0.0.1:8080/health_assistant"
payload = json.dumps({
  "meta": {
    "client_id": "MailRu-VC/1.0",
    "locale": "ru_RU",
    "timezone": "Europe/Moscow",
    "interfaces": {
      "screen": {},
      "audio_player": {}
    },
    "_city_ru": "Москва"
  },
  "request": {
    "command": "привет",
    "original_utterance": "Привет",
    "type": "SimpleUtterance",
    "nlu": {
      "tokens": [
        "привет"
      ],
      "entities": []
    }
  },
  "session": {
    "session_id": "883c3706-4318-4f4a-a19b-b59c6ab09761",
    "user_id": "03b08d6ce1eb15a591bb8650129b330aa7c3a47ddc6f5508d731b8259bc6a742",
    "skill_id": "52401ef1-935a-49ef-bd57-1f3f83ac3447",
    "new": True,
    "message_id": 0,
    "user": {
      "user_id": "b3c2b564f33675571912ea7aaa0788637bcd0c18405192100a47f3a7ddafe864"
    },
    "application": {
      "application_id": "03b08d6ce1eb15a591bb8650129b330aa7c3a47ddc6f5508d731b8259bc6a742",
      "application_type": "mobile"
    },
    "auth_token": "636d5f7d6fb18e1aff48bb161ab82de12012fec213a0bf2e9a9efd8b7825c69c"
  },
  "state": {
    "session": {},
    "user": {
      "calories": 14
    }
  },
  "version": "1.0"
})
headers = {
  'Content-Type': 'application/json'
}
with open("test.json", "r") as read_file:
    response = json.load(read_file)


def test_main_func_code():
    response_from_server = requests.request("POST", url, headers=headers, data=payload)
    assert 200 == response_from_server.status_code


def test_main_func_content():
    response_from_server = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response_from_server.text)
    assert response == data


def test_get_recipes():
    temp = logic.get_recipe()
    isinstance(tuple, type(temp))
    isinstance(list, type(temp[0]))
    isinstance(str, type(temp[0][0]))
    isinstance(str, type(temp[0][1]))
    isinstance(str, type(temp[1]))


def test_get_random_train():
    temp = logic.get_random_train()
    isinstance(tuple, type(temp))
    isinstance(list, type(temp[0]))
    isinstance(str, type(temp[0][0]))
    isinstance(str, type(temp[0][1]))
    isinstance(str, type(temp[1]))


def test_get_root_state():
    temp = logic.get_root_state()
    assert temp.get_id() == "100"


def test_get_leaf_state():
    temp = logic.get_leaf_state()
    assert temp.get_id() == "101"


def test_get_state():
    temp = logic.get_state("200")
    assert temp.get_id() == "200"

