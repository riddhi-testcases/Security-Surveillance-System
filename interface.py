import tkinter as tk
from tkinter import filedialog, StringVar
from PIL import Image, ImageTk
import shutil
from datetime import datetime
from database_manager import DatabaseManager
from surveillance_system import start_surveillance

class SecurityInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Advanced Security Surveillance System')
        self.window.geometry("600x400")
        self.db = DatabaseManager()
        self.setup_interface()

    def setup_interface(self):
        # Registration Frame
        reg_frame = tk.LabelFrame(self.window, text="Personnel Registration", padx=10, pady=10)
        reg_frame.pack(fill="x", padx=10, pady=5)

        # Name Entry
        tk.Label(reg_frame, text='Full Name:').grid(row=0, column=0, sticky='w')
        self.name_var = StringVar()
        tk.Entry(reg_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5)

        # ID Entry
        tk.Label(reg_frame, text='Personnel ID:').grid(row=0, column=2, sticky='w')
        self.id_var = StringVar()
        tk.Entry(reg_frame, textvariable=self.id_var).grid(row=0, column=3, padx=5)

        # Image Upload
        tk.Button(reg_frame, text='Upload Photo', command=self.upload_photo).grid(row=1, column=1, pady=10)
        
        # Surveillance Frame
        surv_frame = tk.LabelFrame(self.window, text="Surveillance Control", padx=10, pady=10)
        surv_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(surv_frame, text='Start Surveillance', command=self.start_surveillance).pack(pady=5)

        # Tracking Frame
        track_frame = tk.LabelFrame(self.window, text="Personnel Tracking", padx=10, pady=10)
        track_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(track_frame, text='Search ID:').pack(side='left', padx=5)
        self.search_var = StringVar()
        tk.Entry(track_frame, textvariable=self.search_var).pack(side='left', padx=5)
        tk.Button(track_frame, text='Track', command=self.track_person).pack(side='left', padx=5)

        # Results Area
        self.results_frame = tk.LabelFrame(self.window, text="Results", padx=10, pady=10)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def upload_photo(self):
        file_types = [('Image files', '*.jpg *.jpeg *.png')]
        filename = filedialog.askopenfilename(filetypes=file_types)
        if filename:
            person_id = self.id_var.get()
            shutil.copy(filename, f'images/{person_id}.jpg')
            self.db.add_person(self.name_var.get(), 'Entry Point')
            tk.messagebox.showinfo("Success", "Personnel registered successfully!")

    def start_surveillance(self):
        start_surveillance(self.db)

    def track_person(self):
        person_id = self.search_var.get()
        details = self.db.get_person_details(person_id)
        if details:
            name, location, timestamp = details
            for widget in self.results_frame.winfo_children():
                widget.destroy()

            tk.Label(self.results_frame, text=f"Name: {name}").pack()
            tk.Label(self.results_frame, text=f"Location: {location}").pack()
            tk.Label(self.results_frame, text=f"Last seen: {datetime.fromtimestamp(timestamp)}").pack()

            try:
                img = Image.open(f'images/{person_id}.jpg')
                img = img.resize((100, 100))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(self.results_frame, image=photo)
                img_label.image = photo
                img_label.pack()
            except:
                pass
        else:
            tk.messagebox.showerror("Error", "Person not found!")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = SecurityInterface()
    app.run()