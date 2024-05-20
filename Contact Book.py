import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PhoneBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Book App")

        
        self.create_database()

        
        self.setup_gui()

    def create_database(self):
        conn = sqlite3.connect("phonebook2.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone_number TEXT,
                email TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_contact(self):
        name = self.name_entry.get()
        phone_number = self.phone_entry.get()
        email = self.email_entry.get()

        if name and phone_number:
            conn = sqlite3.connect("phonebook2.db")
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contacts (name, phone_number, email) VALUES (?, ?, ?)
            ''', (name, phone_number, email))
            conn.commit()
            conn.close()

          
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

           
            self.display_contacts()

    def update_contact(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showinfo("Error", "Please select a contact to update.")
            return

        
        contact_id = self.tree.item(selected_item, "values")[0]
        name = self.name_entry.get()
        phone_number = self.phone_entry.get()
        email = self.email_entry.get()

        if name and phone_number:
            conn = sqlite3.connect("phonebook2.db")
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE contacts SET name=?, phone_number=?, email=? WHERE id=?
            ''', (name, phone_number, email, contact_id))
            conn.commit()
            conn.close()

            
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

           
            self.display_contacts()

    def delete_contact(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showinfo("Error", "Please select a contact to delete.")
            return

        
        contact_id = self.tree.item(selected_item, "values")[0]

 
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this contact?")
        if confirmation:
            conn = sqlite3.connect("phonebook2.db")
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM contacts WHERE id=?
            ''', (contact_id,))
            conn.commit()
            conn.close()

            
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

           
            self.display_contacts()

    def search_contact(self):
        search_name = self.search_entry.get()

        if search_name:
            conn = sqlite3.connect("phonebook2.db")
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM contacts WHERE name LIKE ?
            ''', (f'%{search_name}%',))
            contacts = cursor.fetchall()
            conn.close()

            
            for row in self.tree.get_children():
                self.tree.delete(row)

            if contacts:
                for contact in contacts:
                    self.tree.insert("", tk.END, values=(contact[0], contact[1], contact[2], contact[3]))
            else:
                messagebox.showinfo("Search Result", "No contacts found.")

    def display_contacts(self):
        
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("phonebook2.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM contacts ORDER BY name
        ''')
        contacts = cursor.fetchall()
        conn.close()

        if contacts:
            for contact in contacts:
                self.tree.insert("", tk.END, values=(contact[0], contact[1], contact[2], contact[3]))

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        if selected_item:
           
            contact_id, name, phone_number, email = self.tree.item(selected_item, "values")

           
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, name)

            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, phone_number)

            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, email)

    def setup_gui(self):
     
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="E")
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")

        tk.Label(self.root, text="Phone Number:").grid(row=1, column=0, padx=5, pady=5, sticky="E")
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5, sticky="W")

        tk.Label(self.root, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="E")
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="W")

        
        add_button = tk.Button(self.root, text="Add Contact", command=self.add_contact)
        add_button.grid(row=3, column=0, padx=5, pady=5)

        update_button = tk.Button(self.root, text="Update Contact", command=self.update_contact)
        update_button.grid(row=3, column=1, padx=5, pady=5)

        delete_button = tk.Button(self.root, text="Delete Contact", command=self.delete_contact)
        delete_button.grid(row=3, column=2, padx=5, pady=5)

        
        tk.Label(self.root, text="Search by Name:").grid(row=4, column=0, padx=5, pady=5, sticky="E")
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=4, column=1, padx=5, pady=5, sticky="W")

        search_button = tk.Button(self.root, text="Search", command=self.search_contact)
        search_button.grid(row=4, column=2, padx=5, pady=5)

    
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Phone Number", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone Number", text="Phone Number")
        self.tree.heading("Email", text="Email")
        self.tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        
        self.display_contacts()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneBookApp(root)
    root.mainloop()
