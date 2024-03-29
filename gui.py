import json
from tkinter import *
from tkinter import messagebox
from car import Car
from tkcalendar import DateEntry
from smtplib import SMTP


class CarRental:
    def __init__(self, car):
        self.window = Tk()
        self.car = car
        self.window.title("Car Rental Reservation")
        self.window.minsize(600, 500)
        self.show_cars()
        self.window.mainloop()

    def show_cars(self):
        def redirect(c):
            self.window.destroy()
            BookCars(self.car, c)

        for car in self.car.cars:
            try:
                Label(text=f"Make: {car['Make']}").pack()
                Label(text=f"Model: {car['model']}").pack()
                Label(text=f"Year of Manufacture:{car['year']}").pack()
                Label(text=f"Availability: {'Yes' if car['availability'] else 'No'}").pack()
                Label(text=f"Insurance: {car['insurance']}").pack()
                Label(text=f"Deposit: {car['deposit']}").pack()
                Label(text=f"Delivery: {car['delivery']}").pack()
                Button(text="Book Now", command=lambda: redirect(car)).pack()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while displaying cars: {e}")


class AddCars:
    def __init__(self):
        self.window = Tk()
        self.car = Car()
        self.window.title("Add Cars")
        self.window.minsize(600, 500)
        self.car_add()
        self.window.mainloop()

    def car_add(self):
        def add():
            user_choice = messagebox.askquestion("Warning", "You are about to add the info are you sure?",
                                                 icon="warning")
            if user_choice:
                try:
                    self.car.get_cars(make.get(), model.get(), year.get(), fare.get(), deposit.get(), delivery.get())
                    messagebox.showinfo("Info", "Info got added", icon="info")
                    self.window.destroy()
                    CarRental(self.car)
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while adding car: {e}")

        Label(text="Carlow").pack()
        Label(text="Make").pack()
        make = Entry()
        make.pack()
        Label(text="Model").pack()
        model = Entry()
        model.pack()
        Label(text="Year").pack()
        year = Entry()
        year.pack()
        Label(text="Fare").pack()
        fare = Entry()
        fare.pack()
        Label(text="Deposit").pack()
        deposit = Entry()
        deposit.pack()
        Label(text="Delivery").pack()
        delivery = Entry()
        delivery.pack()
        Label().pack()
        Button(text="Add", command=add).pack()


class BookCars:
    def __init__(self, car, c):
        self.window = Tk()
        self.car = car
        self.window.title("Car Rental Reservation")
        self.window.minsize(600, 500)
        self.book_car(c)
        self.window.mainloop()

    def book_car(self, car):
        self.get_customer_detail(car)

    def get_customer_detail(self, car):
        def redirect(names, phones, emails, deliverys, rets, ds):
            self.window.destroy()
            try:
                self.car.book_car(car["model"], names, phones, emails, deliverys, rets, ds)
                CarRental(self.car)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while booking car: {e}")

        Label(text="Name").pack()
        name = Entry()
        name.pack()
        Label(text="Phone").pack()
        phone = Entry()
        phone.pack()
        Label(text="Date").pack()
        d = DateEntry(width=12, background='darkblue', foreground='white', borderwidth=2)
        d.pack()
        Label(text="Email").pack()
        email = Entry()
        email.pack()
        Label(text="Enter delivery location").pack()
        delivery = Entry()
        delivery.pack()
        Label(text="Enter return location").pack()
        return_loc = Entry()
        return_loc.pack()
        Label().pack()

        Button(text="Book",
               command=lambda: redirect(name.get(), phone.get(), email.get(), delivery.get(), return_loc.get(),
                                        d.get())).pack()


class ReturnCar:
    def __init__(self):
        self.car = Car()
        self.window = Tk()
        self.window.title("Car Rental Reservation")
        self.window.minsize(600, 500)
        self.return_car()
        self.window.mainloop()

    def return_car(self):
        def redirect(n):
            if self.car.return_car(n):
                self.window.destroy()
                messagebox.showinfo(title="Return Car", message="Car returned Successfully")
                Main(self.car)
            else:
                Label(text="User Does not exist!", fg="red").pack()

        Label(text="Carlow.com", font=("Arial", 20)).pack()
        Label(text="Enter the Name who have borrowed the car!").pack()
        name = Entry()
        Button(text="Return", command=lambda: redirect(name.get()))


class Main:
    def __init__(self, car):
        self.car = car
        self.window = Tk()
        self.window.title("Car Rental Reservation")
        self.window.minsize(600, 500)
        self.menu()
        self.window.mainloop()

    def menu(self):
        def choice(c):
            if c.lower() == "admin":
                self.window.destroy()
                AddCars()
            elif c.lower() == "rent":
                self.window.destroy()
                CarRental(self.car)
            elif c.lower() == "return":
                self.window.destroy()
                ReturnCar()
            else:
                Label(text="Please Add correct input").pack()

        Label(text="Carlow.com", font=('Arial', 20)).pack()
        Label(text="Type Rent(to rent a car) or Admin(to add car details)").pack()
        ch = Entry()
        ch.pack()
        Button(text="Press", command=lambda: choice(ch.get())).pack()


carRental = Main()
