import json
from tkinter import messagebox
import threading
from smtplib import SMTP


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
        self.availability_mutex = threading.Lock()  # Mutex for car availability
        self.booking_semaphore = threading.Semaphore(value=3)

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
        self.cars.append(data)
        print("Car Added successfully")
        print(data)

    def display_cars(self):
        for car in self.cars:
            print(car)

    def book_car(self, model, name, phone, email, delivery, pickup, date):
        self.booking_semaphore.acquire()
        # model = input("Model of the car: ")
        for car in self.cars:
            if model == car["model"]:
                self.availability_mutex.acquire()  # Protect availability updates
                if car["availability"]:
                    self.generate_bill(car, name, phone, email, delivery, pickup, date)
                    car["availability"] = False
                    print("Car Booked successfully")
                else:
                    messagebox.showerror("Car Not Available", message="Car is not Available")
                    print("Car is not available")
                self.availability_mutex.release()
        self.booking_semaphore.release()

    def generate_bill(self, car, name, phone, email, delivery, pickup, date):
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
        self.send_mail(car, name, phone, email, delivery, pickup, total, date)
        messagebox.showinfo(message="Car Booked! \nAn Detailed email sent to you!")

    def send_mail(self, car, name, phone, email, delivery, pickup, total, date):
        mail = f"""Subject: Booking Information\n\n
    Dear {name},

    Thank you for choosing Carlow for your car rental needs! We're excited to help you get on the road.

    Your Booking Details:
    Pickup Location: {pickup}
    Pickup Date & Time: {date}
    Return Location: {delivery}
    Vehicle Name: {car["model"]}

    Payment Summary:
    Rental Cost: {car["fare"]}
    Deposit: {car["deposit"]}
    Delivery: {car["delivery"]}
    Total Charged: {total}

    If you have any questions or need to make changes to your reservation, please contact our customer support at [phone number] or [email address]. We wish you a safe and enjoyable journey!

    Sincerely,
    The Carlow Team"""

        user = "rahulaauji71@gmail.com"
        password = "kube kkdl uinf jcnd"

        with SMTP('smtp.gmail.com', port=587) as smtp:
            smtp.starttls()
            smtp.login(user=user, password=password)
            smtp.sendmail(from_addr=user, to_addrs=email, msg=mail)

        print(mail)

    def return_car(self, name):
        # name = input("Enter name of the customer: ")
        for index, customer in enumerate(self.booking_details):
            if name.lower() == customer["name"].lower():
                print(customer)
                self.booking_details.pop(index)
                for car in self.cars:
                    if customer["car_booked"].lower() == car["model"].lower():
                        car["availability"] = True
                        self.availability_mutex.acquire()  # Protect availability updates
                        for car in self.cars:
                            if customer["car_booked"].lower() == car["model"].lower():
                                car["availability"] = True
                        print("Car returned Successfully!")
                        self.availability_mutex.release()
                print("Car returned Successfully!")
                return
        print(f"No Customer exist of name {name}")
