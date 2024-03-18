import json
from tkinter import messagebox


class Car:
    def __init__(self):
        self.cars = [{
            "Make": "Honda",
            "model": "BMX2876",
            "year": 2024,
            "availability": True,
            "fare": 5000,
            "insurance": "Included",
            "deposit": 3000,
            "delivery": 500,
        }]
        self.booking_details = []

    def get_cars(self, make, model, year, fare, deposit, delivery):
        data = {
            "Make": make,
            "model": model,
            "year": int(year),
            "availability": True,
            "fare": int(fare),
            "insurance": "Included",
            "deposit": int(deposit),
            "delivery": int(delivery),
        }
        with open("data.json", "w") as cars:
            json.dump(data, cars)
        print("Car Added successfully")

    def display_cars(self):
        for car in self.cars:
            print(car)

    def book_car(self, model):
        # model = input("Model of the car: ")
        for car in self.cars:
            if model == car["model"]:
                if car["availability"]:
                    self.generate_bill(car)
                    car["availability"] = False
                    print("Car Booked successfully")
                else:
                    print("Car is not available")
                    break

    def generate_bill(self, car, name, phone, email, delivery, pickup):
        total = car["fare"] + car["delivery"] + car["deposit"]
        messagebox.showwarning("Bill",
                               f"Base Fare ₹{car["fare"]}\nDoorstep Delivery & Pickup ₹{car["delivery"]}\nInsurance & GST {car["insurance"]}\nRefundable security deposit {car["deposit"]}\nTotal ₹{total}")
        self.booking_details.append({
            "name": name,
            "contact": {
                "phone": phone,
                "email": email
            },
            "delivery": delivery,
            "pickup": pickup,
            "total": total,
            "car_booked": car["model"]
        })

    def return_car(self, name):
        # name = input("Enter name of the customer: ")
        for index, customer in enumerate(self.booking_details):
            if name.lower() == customer["name"].lower():
                print(customer)
                self.booking_details.pop(index)
                for car in self.cars:
                    if customer["car_booked"].lower() == car["model"].lower():
                        car["availability"] = True
                print("Car returned Successfully!")
                return
        print(f"No Customer exist of name {name}")
