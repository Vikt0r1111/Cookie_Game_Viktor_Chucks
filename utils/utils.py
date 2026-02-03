from deep_translator import GoogleTranslator
import json
import os
import copy 

from config.user_data import userdata

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
    user_data = copy.deepcopy(userdata)  # создаём независимую копию
    user_data["userId"] = id
    return user_data

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

    user_data = data[str(user_id)]
    cookies_to_add = 0

    for upgrade in user_data.get("upgrades", {}).values():
        if upgrade.get("affects") == "passive" and upgrade.get("quantity", 0) > 0:
            cookies_to_add += upgrade.get("cookiesPerSecond", 0) * upgrade["quantity"]

    user_data["cookies"] += cookies_to_add

    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return user_data["cookies"]

def buy_upgrade(name, user_id):
    with open(FILENAME, "r", encoding="utf-8") as file:
        data  = json.load(file)

    user_data = data[user_id]
    upgrade = user_data["upgrades"].get(name)
    multiplier = upgrade.get("multiplier", 1) if upgrade else 1.15

    if upgrade:
        price = upgrade["price"]
        if user_data["cookies"] >= price:
            user_data["cookies"] -= price

            upgrade["quantity"] += 1

            upgrade["price"] = price * multiplier

            if upgrade["affects"] == "click":
                user_data["cookiesPerClick"] += upgrade.get("cookiesPerSecond", 1)
            elif upgrade["affects"] == "passive":
                user_data["cookiesPerSecond"] += upgrade.get("cookiesPerSecond", 0)

            with open(FILENAME, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return True
    return False

def buy_levelup(user_id, upgrade_name):
    with open(FILENAME, "r", encoding="utf-8") as file:
        data = json.load(file)

    user_data = data[str(user_id)]
    upgrade = user_data["upgrades"].get(upgrade_name)
    if not upgrade:
        return False

    price = upgrade.get("levelup_price", 0)
    multiplier = upgrade.get("multiplier", 1.15)

    if user_data["cookies"] >= price:
        user_data["cookies"] -= price
        upgrade["level"] += 1
        upgrade["levelup_price"] = int(price * multiplier)

        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True

    return False
