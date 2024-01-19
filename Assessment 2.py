import tkinter as tk
import requests
from tkinter import font as tkFont

class APIClient:
    # APIClient class handles API requests to TheCocktailDB.
    def __init__(self):
        # Base URL for API requests.
        self.base_url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f="

    def fetch_cocktails(self, letter):
        # Fetches cocktails starting with the given letter.
        response = requests.get(self.base_url + letter)
        if response.status_code == 200:
            return response.json()
        else:
            return None

class Application(tk.Frame):
    # Main Application class for the GUI.
    def __init__(self, master=None):
        super().__init__(master, bg='light gray')
        self.master = master
        self.api_client = APIClient()
        self.create_widgets()
        self.grid(sticky="nsew")  # Allow the widget to expand in all directions (North, South, East, West).
        self.create_grid_config()  # Configure grid for responsive layout.

    def create_widgets(self):
        # Setting up custom font for widgets.
        self.customFont = tkFont.Font(family="Helvetica", size=12)

        # Frame for Search Section.
        self.search_frame = tk.Frame(self, bg='light blue', bd=2, relief='groove')
        self.search_label = tk.Label(self.search_frame, text="Enter a letter:", bg='light blue', font=self.customFont)
        self.search_entry = tk.Entry(self.search_frame, font=self.customFont)
        self.search_button = tk.Button(self.search_frame, text="Search", command=self.perform_search, bg='green', fg='white', font=self.customFont)
        self.search_label.grid(row=0, column=0, padx=5, pady=5)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)
        self.search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)  # Ensure the frame expands horizontally.

        # Frame for Results Section.
        self.result_frame = tk.Frame(self, bg='light gray')
        self.result_listbox = tk.Listbox(self.result_frame, width=40, height=15, font=self.customFont)
        self.result_listbox.bind('<<ListboxSelect>>', self.on_select)  # Bind selection event.
        self.result_scrollbar = tk.Scrollbar(self.result_frame, orient="vertical", command=self.result_listbox.yview)
        self.result_listbox.configure(yscrollcommand=self.result_scrollbar.set)
        self.result_listbox.grid(row=0, column=0, sticky="nsew")
        self.result_scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_frame.grid(row=1, column=0, sticky="nsew", padx=10)

        # Text widget for Detail Section.
        self.detail_text = tk.Text(self, height=10, width=30, font=self.customFont, bg='white', fg='black')
        self.detail_text.grid(row=1, column=1, sticky="nsew", padx=10)

    def create_grid_config(self):
        # Configure the grid for responsive design.
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.result_frame.rowconfigure(0, weight=1)
        self.result_frame.columnconfigure(0, weight=1)

    def perform_search(self):
        # Function to handle search button click.
        letter = self.search_entry.get().strip().lower()
        if len(letter) == 1 and letter.isalpha():
            data = self.api_client.fetch_cocktails(letter)
            self.populate_results(data)
        else:
            self.result_listbox.delete(0, tk.END)
            self.result_listbox.insert(tk.END, "Please enter a single letter.")

    def populate_results(self, data):
        # Populate the result listbox with data.
        self.result_listbox.delete(0, tk.END)
        self.detail_text.delete(1.0, tk.END)
        if data and "drinks" in data:
            for cocktail in data["drinks"]:
                self.result_listbox.insert(tk.END, cocktail["strDrink"])
        else:
            self.result_listbox.insert(tk.END, "No results found.")

    def on_select(self, event):
        # Function to handle listbox selection event.
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            data = widget.get(index)
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, data)  # Placeholder for more detailed info.

root = tk.Tk()
root.title("Cocktail Finder")
root.geometry("800x500")
app = Application(master=root)
root.mainloop()
