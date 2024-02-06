import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class RealEstateApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Real Estate Application")
        self.root.geometry("300x300")

        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)

        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1)

        self.type_label = ttk.Label(self.root, text="Type:")
        self.type_var = ttk.Combobox(self.root, values=["buy", "rent"])
        self.type_label.grid(row=0, column=0, padx=5, pady=5)
        self.type_var.grid(row=0, column=1, padx=5, pady=5)

        self.cat_label = ttk.Label(self.root, text="Category:")
        self.cat_var = ttk.Entry(self.root)
        self.cat_label.grid(row=1, column=0, padx=5, pady=5)
        self.cat_var.grid(row=1, column=1, padx=5, pady=5)

        self.city_label = ttk.Label(self.root, text="City:")
        self.city_var = ttk.Entry(self.root)
        self.city_label.grid(row=2, column=0, padx=5, pady=5)
        self.city_var.grid(row=2, column=1, padx=5, pady=5)

        self.km_label = ttk.Label(self.root, text="Kilometer:")
        self.km_var = ttk.Combobox(self.root, values=["0", "1", "2", "3",
                                                      "4", "5", "7", "10",
                                                      "15", "20", "30", "50"])
        self.km_label.grid(row=3, column=0, padx=5, pady=5)
        self.km_var.grid(row=3, column=1, padx=5, pady=5)

        self.rooms_label = ttk.Label(self.root, text="Rooms:")
        self.rooms_var = ttk.Combobox(self.root, values=["any", "1", "1.5",
                                                         "2", "2.5", "3",
                                                         "3.5", "4", "4.5",
                                                         "5", "5.5", "6",
                                                         "6.5", "7", "7.5",
                                                         "8"])
        self.rooms_label.grid(row=4, column=0, padx=5, pady=5)
        self.rooms_var.grid(row=4, column=1, padx=5, pady=5)

        self.price_label = ttk.Label(self.root, text="Price:")
        self.price_var = ttk.Entry(self.root)
        self.price_label.grid(row=5, column=0, padx=5, pady=5)
        self.price_var.grid(row=5, column=1, padx=5, pady=5)

        self.generate_button = ttk.Button(self.root, text="Go !",
                                          command=self.generate_url_wrapper)
        self.generate_button.grid(row=6, column=0, columnspan=2, pady=10)
        self.args = None

    def generate_url(self, type_value, cat_value, city_value, km_value,
                     rooms_value, price_value):
        if not type_value or not city_value:
            messagebox.showerror("Error", "Input Type And City")
            return

        if not cat_value:
            cat_value = 'real-estate'
        url = (
            f"Type: {type_value}, "
            f"Category: {cat_value}, "
            f"City: {city_value}, "
            f"Kilometer: {km_value}, "
            f"Rooms: {rooms_value}, "
            f"Price: {price_value}"
              )

        messagebox.showinfo("Request Details", url)
        self.args = {"Type": type_value, "Category": cat_value,
                     "City": city_value, "Kilometer": km_value,
                     "Rooms": rooms_value, "Price": price_value}
        self.root.destroy()

    def generate_url_wrapper(self):
        type_value = self.type_var.get()
        cat_value = self.cat_var.get()
        city_value = self.city_var.get()
        km_value = self.km_var.get()
        rooms_value = self.rooms_var.get()
        price_value = self.price_var.get()
        self.generate_url(type_value, cat_value, city_value, km_value,
                          rooms_value, price_value)
