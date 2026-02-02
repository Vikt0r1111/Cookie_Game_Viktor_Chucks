from deep_translator import GoogleTranslator
import json
import os

FILENAME = "users.json"

def translate_text(sourse, language):
    with open(f"{sourse}", "r", encoding="utf-8") as file:
        text = file.read()
    translate_text = GoogleTranslator(source='auto', target=language).translate(text)
    return translate_text

def generate_data_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=4)

def create_user_data(id):
        return {
        "userId": id,
        "cookies": 0,
        "cookiesPerClick": 1,
        "cookiesPerSecond": 0,

        "upgrades": {
            "doubleClick": {
                "level": 1,
                "quantity": 0,
                "price": 50,
                "multiplier": 1,
                "affects": "click"
            },
            "grandma": {
                "level": 1,
                "quantity": 0,
                "price": 100,
                "multiplier": 1,
                "affects": "passive",
                "cookiesPerSecond": 4
            },
            "farm": {
                "level": 1,
                "quantity": 0,
                "price": 500,
                "multiplier": 1,
                "affects": "passive",
                "cookiesPerSecond": 16
            },
            "factory": {
                "level": 1,
                "quantity": 0,
                "price": 3000,
                "multiplier": 1,
                "affects": "passive",
                "cookiesPerSecond": 32
            },
            "mine": {
                "level": 1,
                "quantity": 0,
                "price": 10000,
                "multiplier": 1,
                "affects": "passive",
                "cookiesPerSecond": 128
            },
            "bank": {
                "level": 1,
                "quantity": 0,
                "price": 40000,
                "multiplier": 1,
                "affects": "passive",
                "cookiesPerSecond": 512
            },
            "temple": {
                "level": 1,
                "quantity": 0,
                "price": 200000,
                "multiplier": 1,
                "affects": "passive",
                "cookiesPerSecond": 2048
            },
            "wizardTower": {
                "level": 1,
                "quantity": 0,
                "price": 1666666,
                "multiplier": 1,
                "affects": "passive",
                "cookiesPerSecond": 8192
            },
            "shipment": {
                "level": 1,
                "quantity": 0,
                "price": 12345678,
                "multiplier": 1,
                "affects": "passive",
                "cookiesPerSecond": 32768
            }
        }
    }

def save_users(data: dict):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_user_data(id):
    with open(FILENAME, "r", encoding="utf-8") as file:
        users = json.load(file)
    
    user_id = id
    if user_id in users:
        return users[user_id]
    
def load_users():
    if not os.path.exists(FILENAME):
        return {}

    if os.path.getsize(FILENAME) == 0:
        return {}

    with open(FILENAME, "r", encoding="utf-8") as file:
        return json.load(file)


def add_user(user_id: str):
    users = load_users()

    if user_id in users:
        print("Пользователь уже существует")
        return

    users[user_id] = create_user_data(user_id)
    save_users(users)

    print(f"Пользователь {user_id} добавлен")

def make_click(user_id):
    with open(FILENAME, "r", encoding="utf-8") as file:
        users = json.load(file)

    if user_id in users:
        cookies_per_click = users[user_id].get("cookiesPerClick", 1)
        doubleclick = users[user_id]["upgrades"]["doubleClick"]["level"]
        if doubleclick > 1:
            cookies_per_click *= doubleclick
        users[user_id]["cookies"] += cookies_per_click

        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)

        return users[user_id]["cookies"]
    return None

def update_click(user_id):
    with open(FILENAME, "r", encoding="utf-8") as file:
        data  = json.load(file)

    user_data = data[user_id]
    cookies_to_add = 0

    if user_id in data:
        for upgrade in user_data.get("upgrades", {}).values():
            if upgrade["affects"] == "passive":
                level = upgrade.get("level", 0)
                cps = upgrade.get("cookiesPerSecond", 0)
                cookies_to_add += level * cps

        user_data["cookies"] += cookies_to_add

    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return user_data["cookies"]

def buy_update(name, user_id):
    with open(FILENAME, "r", encoding="utf-8") as file:
        data  = json.load(file)

    user_data = data[user_id]
    upgrade = user_data["upgrades"].get(name)

    if upgrade:
        price = upgrade["price"]
        if user_data["cookies"] >= price:
            user_data["cookies"] -= price
            upgrade["level"] += 1
            upgrade["price"] = int(upgrade["price"] * 1.15)

            if upgrade["affects"] == "click":
                user_data["cookiesPerClick"] += 1

            with open(FILENAME, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return True
    return False
    