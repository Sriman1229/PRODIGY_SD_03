import tkinter as tk
from tkinter import messagebox
import os

CONTACTS_FILE = "contacts.txt"

class ContactManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Contact Manager")
        
        self.contacts = {}
        self.load_contacts()
        
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=10)

        self.add_button = tk.Button(self.menu_frame, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=0, column=0, padx=5)

        self.view_button = tk.Button(self.menu_frame, text="View Contacts", command=self.view_contacts)
        self.view_button.grid(row=0, column=1, padx=5)

        self.edit_button = tk.Button(self.menu_frame, text="Edit Contact", command=self.edit_contact)
        self.edit_button.grid(row=0, column=2, padx=5)

        self.delete_button = tk.Button(self.menu_frame, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=0, column=3, padx=5)

        self.exit_button = tk.Button(self.menu_frame, text="Exit", command=self.root.destroy)
        self.exit_button.grid(row=0, column=4, padx=5)

        self.root.mainloop()

    def load_contacts(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r") as file:
                for line in file:
                    name, phone, email = line.strip().split(",")
                    self.contacts[name] = {"phone": phone, "email": email}

    def save_contacts(self):
        with open(CONTACTS_FILE, "w") as file:
            for name, info in self.contacts.items():
                file.write(f"{name},{info['phone']},{info['email']}\n")

    def add_contact(self):
        add_window = tk.Toplevel()
        add_window.title("Add Contact")

        name_label = tk.Label(add_window, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(add_window)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        phone_label = tk.Label(add_window, text="Phone:")
        phone_label.grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(add_window)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        email_label = tk.Label(add_window, text="Email:")
        email_label.grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(add_window)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        add_button = tk.Button(add_window, text="Add", command=self.save_new_contact)
        add_button.grid(row=3, columnspan=2, padx=5, pady=5)

    def save_new_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if name and phone and email:
            self.contacts[name] = {"phone": phone, "email": email}
            self.save_contacts()
            messagebox.showinfo("Success", "Contact added successfully.")
            self.view_contacts()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def view_contacts(self):
        view_window = tk.Toplevel()
        view_window.title("View Contacts")

        if not self.contacts:
            empty_label = tk.Label(view_window, text="No contacts available.")
            empty_label.pack(padx=10, pady=10)
        else:
            for i, (name, info) in enumerate(self.contacts.items(), start=1):
                contact_info = f"Name: {name}, Phone: {info['phone']}, Email: {info['email']}"
                contact_label = tk.Label(view_window, text=contact_info)
                contact_label.pack(padx=10, pady=5, anchor="w")

    def edit_contact(self):
        edit_window = tk.Toplevel()
        edit_window.title("Edit Contact")

        name_label = tk.Label(edit_window, text="Enter contact name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        self.edit_name_entry = tk.Entry(edit_window)
        self.edit_name_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(edit_window, text="Search", command=self.search_contact)
        search_button.grid(row=0, column=2, padx=5, pady=5)

    def search_contact(self):
        name = self.edit_name_entry.get()
        if name in self.contacts:
            edit_window = tk.Toplevel()
            edit_window.title("Edit Contact")

            phone_label = tk.Label(edit_window, text="Phone:")
            phone_label.grid(row=0, column=0, padx=5, pady=5)
            self.edit_phone_entry = tk.Entry(edit_window)
            self.edit_phone_entry.grid(row=0, column=1, padx=5, pady=5)
            self.edit_phone_entry.insert(0, self.contacts[name]["phone"])

            email_label = tk.Label(edit_window, text="Email:")
            email_label.grid(row=1, column=0, padx=5, pady=5)
            self.edit_email_entry = tk.Entry(edit_window)
            self.edit_email_entry.grid(row=1, column=1, padx=5, pady=5)
            self.edit_email_entry.insert(0, self.contacts[name]["email"])

            update_button = tk.Button(edit_window, text="Update", command=lambda: self.update_contact(name))
            update_button.grid(row=2, columnspan=2, padx=5, pady=5)
        else:
            messagebox.showerror("Error", "Contact not found.")

    def update_contact(self, name):
        phone = self.edit_phone_entry.get()
        email = self.edit_email_entry.get()

        if phone and email:
            self.contacts[name]["phone"] = phone
            self.contacts[name]["email"] = email
            self.save_contacts()
            messagebox.showinfo("Success", "Contact updated successfully.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def delete_contact(self):
        delete_window = tk.Toplevel()
        delete_window.title("Delete Contact")

        name_label = tk.Label(delete_window, text="Enter contact name:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        self.delete_name_entry = tk.Entry(delete_window)
        self.delete_name_entry.grid(row=0, column=1, padx=5, pady=5)

        delete_button = tk.Button(delete_window, text="Delete", command=self.confirm_delete)
        delete_button.grid(row=1, columnspan=2, padx=5, pady=5)

    def confirm_delete(self):
        name = self.delete_name_entry.get()
        if name in self.contacts:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?")
            if confirm:
                del self.contacts[name]
                self.save_contacts()
                messagebox.showinfo("Success", "Contact deleted successfully.")
                self.view_contacts()
        else:
            messagebox.showerror("Error", "Contact not found.")

if __name__ == "__main__":
    app = ContactManagerApp()
