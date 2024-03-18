import json
from tkinter import *
from tkinter import messagebox
from car import Car
from smtplib import SMTP


class CarRental:
    def __init__(self):
        self.window = Tk()
        self.car = Car()
        self.window.title("Car Rental Reservation")
        self.window.minsize(600, 500)

    def car_add(self):
        def add():
            user_choice = messagebox.askquestion("Warning", "You are about to add the info are you sure?",
                                                 icon="warning")
            if user_choice:
                self.car.get_cars(make.get(), model.get(), year.get(), fare.get(), deposit.get(), delivery.get())
                messagebox.showinfo("Info", "Info got added", icon="info")

        Label(text="Carlow").grid(column=2, row=0)
        Label(text="Make").grid(column=1, row=1)
        make = Entry()
        Label(text="Model").grid(column=1, row=2)
        model = Entry()
        Label(text="Year").grid(column=1, row=3)
        year = Entry()
        Label(text="Fare").grid(column=1, row=4)
        fare = Entry()
        Label(text="Deposit").grid(column=1, row=5)
        deposit = Entry()
        Label(text="Delivery").grid(column=1, row=6)
        delivery = Entry()
        Label().grid(column=0, row=7)
        Button(text="Add", command=add).grid(column=2, row=8)
        make.grid(column=2, row=1)
        model.grid(column=2, row=2)
        year.grid(column=2, row=3)
        fare.grid(column=2, row=4)
        deposit.grid(column=2, row=5)
        delivery.grid(column=2, row=6)

    def run(self):
        self.window.mainloop()

    def show_cars(self):
        for car in self.car.cars:
            Label(text=car["Make"]).grid(column=0, row=1)
            Label(text=car["model"]).grid(column=1, row=1)
            Label(text=car["year"]).grid(column=2, row=1)
            Label(text=car["availability"] if "yes" else "no").grid(column=3, row=1)
            Label(text=car["insurance"]).grid(column=4, row=1)
            Label(text=car["deposit"]).grid(column=5, row=1)
            Label(text=car["delivery"]).grid(column=6, row=1)
            Button(text="Book Now", command=lambda: self.book_car(car)).grid(column=7, row=1)

    def book_car(self, car):
        self.get_customer_detail(car)
        messagebox.showinfo(message="Car Booked!")

    def get_customer_detail(self, car):
        Label(text="Carlow").grid(column=2, row=0)
        Label(text="Name").grid(column=1, row=2)
        name = Entry()
        name.grid(column=2, row=2)
        Label(text="Phone").grid(column=1, row=3)
        phone = Entry()
        phone.grid(column=2, row=3)
        Label(text="Email").grid(column=1, row=4)
        email = Entry()
        email.grid(column=2, row=4)
        Label(text="Enter delivery location").grid(column=1, row=5)
        delivery = Entry()
        delivery.grid(column=2, row=5)
        Label(text="Enter return location").grid(column=1, row=6)
        return_loc = Entry()
        return_loc.grid(column=2,row=6)
        Label().grid(column=0, row=7)

        Button(text="Add", command=lambda: self.car.generate_bill(car, name.get(), phone.get(), email.get(), delivery.get(), return_loc.get())).grid(
            column=2, row=8)

    def send_mail(self, name, c_email):
        user = "rahulaauji71@gmail.com"
        password = "kube kkdl uinf jcnd"
        with SMTP('smtp.google.com', port=587) as smtp:
            smtp.starttls()
            smtp.login(user=user, password=password)
            smtp.sendmail(from_addr=user, to_addrs=c_email, msg=f"")


carRental = CarRental()
carRental.show_cars()
carRental.run()
