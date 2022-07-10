import requests
import json

key_category = ["id", "brand", "model", "production_year", "convertible"]
kay_spaces = [10, 15, 15, 20, 10]


class InputError(TypeError):
    pass

def check_server(cid=None):
    reply = requests.head("http://localhost:3000/cars")
    if reply.status_code == requests.codes.ok:
        return True
    else:
        return False

def print_menu():
    print("""
    +-----------------------------+
    |   Vintage  Cars  Database   |
    +-----------------------------+
    M E N U
    =======
    1. List cars
    2. Add new car
    3. Delete car
    4. Update car
    0. Exit
    Enter your choice(0..4):
    """)

def read_user_choice():
    choice = input("Enter you choice: ")
    if choice not in ["0", "1", "2", "3", "4"]:
        raise InputError from TypeError("You entered wrong choice")
    else:
        return choice

def print_header():
    for (c, s) in zip(key_category, kay_spaces):
        print(c.ljust(s), end="| ")
    print()

def print_car(car):
    for (n, w) in zip(key_category, kay_spaces):
        print(str(car[n]).ljust(w), end='| ')
    print()

def list_cars():
    reply = requests.get("http://localhost:3000/cars")
    print_header()
    for car in reply.json():
        print_car(car)

def name_is_valid(name):
    for char in name:
        if char.isalnum():
            return True
    if name == "":
        return False

def enter_id():
    id = input("Car ID (empty string to exist):")
    for char in id:
        if char.isdigit():
            return int(id)
    if id == "":
        return None

def enter_production_year():
    production_year = input("Car production year (empty string to exist):")
    if int(production_year) > 2000:
        raise InputError("The car is too new to be on Vintage Car Database")
    elif int(production_year) < 1900:
        raise InputError("Car did not exist before 1900")
    for char in production_year:
        if char.isdigit():
            return int(production_year)
    if production_year == "":
        return None

def enter_brand():
    brand = input("Car brand (empty string to exist):")
    for char in brand:
        if char.isalnum():
            return brand
    if brand == "":
        return False

def enter_model():
    model = input("Car model (empty string to exist):")
    for char in model:
        if char.isalnum():
            return model
    if model == "":
        return False

def enter_convertible():
    convertible = input("Is this car convertible? [y/n] (empty string to exist):")
    if convertible == "y":
        return True
    elif convertible == "n":
        return False
    elif convertible == "":
        return None

def input_car_data():
    id = enter_id()
    brand = enter_brand()
    model = enter_model()
    year = enter_production_year()
    convertible = enter_convertible()
    car_data = {"id": f"{id}", "brand": f"{brand}", "model": f"{model}",
                "production_year": f"{year}", "convertible": f"{convertible}"}
    return car_data

def add_car():
    h_content = {"Content-Type": "application/json"}
    new_car_str = input_car_data()
    reply = requests.post("http://localhost:3000/cars", headers=h_content, data=json.dumps(new_car_str))

def delete_car():
    id = enter_id()
    reply = requests.delete("http://localhost:3000/cars" + f"/{id}")

def update_car():
    id = int(input("Car ID (empty string to exist):"))
    reply = requests.head("http://localhost:3000/cars" + f"/{id}")
    if reply.status_code == requests.codes.ok:
        print("OK to update.")
        new_car_str = input_car_data()
        h_content = {"Content-Type": "application/json"}
        reply = requests.put("http://localhost:3000/cars" + f"/{id}", headers=h_content, data=json.dumps(new_car_str))
    else:
        return None

while True:
    if not check_server():
        print("Server is not responding - quitting!")
        break
    print_menu()
    choice = read_user_choice()
    if choice == '0':
        print("Bye!")
        break
    elif choice == '1':
        list_cars()
    elif choice == '2':
        add_car()
    elif choice == '3':
        delete_car()
    elif choice == '4':
        update_car()

