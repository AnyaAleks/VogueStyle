from dto.user_schema import UserSchemaCreate, UserSchemaGet, UserSchemaCheck, UserSchemaLink
import requests
import json

async def _link_user(UserInfo: UserSchemaLink):
    headers = {
    "Content-Type": "application/json"
    }
    response = requests.put(f"http://backend:8000/user/link", json=json.loads(UserInfo.model_dump_json()), headers=headers)
    if response.status_code == 200:
        return True
    else:
        print(f"Ошибка при свзяке пользователя: {response.json()}")

async def _create_user(UserInfo: UserSchemaCreate):
    headers = {
    "Content-Type": "application/json"
    }
    if len(UserInfo.phone)>11:
        UserInfo.phone = UserInfo.phone[1:]
    response = requests.post(f"http://backend:8000/user", json=json.loads(UserInfo.model_dump_json()), headers=headers)
    
    if response.status_code == 200:
        return True
    else:
        print(f"Ошибка при добавлении пользователя: {response.json()}")

async def _get_user_by_tg_id(tg_id: str) -> UserSchemaGet:
    response = requests.get(f"http://backend:8000/user/tg_id/{tg_id}")
    user_data = response.json()
    if user_data["ok"] == True:
        if user_data["user"] is not None:
            user = UserSchemaGet(**user_data["user"])
            return user
        else:
            return None
    else:
        raise Exception("Ошибка при получении пользователя")
    
async def _check_user(UserInfo: UserSchemaCheck) -> bool:
    headers = {
    "Content-Type": "application/json"
    }
    if len(UserInfo.phone)>11:
        UserInfo.phone = UserInfo.phone[1:]
    response = requests.post("http://backend:8000/user/check", json=json.loads(UserInfo.model_dump_json()), headers=headers)
    check_data = response.json()
    if check_data["ok"] == True:
        return {"ok":check_data["verified"], "user":check_data["user"]}
    else:
        raise Exception("Ошибка при проверке пользователя")