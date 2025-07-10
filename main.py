import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Hotel Management System")
app.geometry("700x600")

bookings = {}
room_status={i: "Available" for i in range(101, 111)}
room_prices={
    'Single Non-AC': 1000,
    'Single AC': 1500,
    'Double Non-AC': 1800,
    'Double AC': 2500
}

def create_booking():
    name = entry_name.get()
    age = entry_age.get()
    room_type = option_room_type.get()
    checkin = entry_checkin.get()
    checkout = entry_checkout.get()
    nights = entry_nights.get()

    if not (name and age and room_type and checkin and checkout and nights):
        messagebox.showwarning("Input Error", "All fields must be filled.")
        return

    try:
        age = int(age)
        nights = int(nights)
    except:
        messagebox.showerror("Input Error", "Age and Nights should be numbers.")
        return

    room_number = next((room for room, status in room_status.items() if status == "Available"), None)
    if room_number is None:
        messagebox.showinfo("No Rooms", "No rooms available.")
        return

    room_status[room_number] = "Booked"
    bookings[room_number] = {
        'name':name,
        'age':age,
        'room_type': room_type,
        'checkin': checkin,
        'checkout': checkout,
        'nights': nights
    }

    messagebox.showinfo("Success", f"Room {room_number} booked for {name}.")

def view_bookings():
    output_box.delete("1.0", "end")
    if not bookings:
        output_box.insert("end", "No bookings yet.\n")
    else:
        for room, data in bookings.items():
            output_box.insert("end", f"Room {room}: {data}\n")

def check_availability():
    output_box.delete("1.0", "end")
    for room, status in room_status.items():
        output_box.insert("end", f"Room {room}: {status}\n")

def generate_bill():
    try:
        room = int(entry_bill_room.get())
    except:
        messagebox.showerror("Error", "Enter a valid room number")
        return

    if room in bookings:
        b = bookings[room]
        price = room_prices.get(b['room_type'], 1000)
        total=price*b['nights']
        output_box.delete("1.0", "end")
        output_box.insert("end", f"Bill for Room {room}\n")
        output_box.insert("end", f"Customer: {b['name']}\n")
        output_box.insert("end", f"Room Type: {b['room_type']}\n")
        output_box.insert("end", f"Nights Stayed: {b['nights']}\n")
        output_box.insert("end", f"Total Bill: ₹{total}\n")
    else:
        messagebox.showinfo("Not Found", "Booking not found for that room.")


frame = ctk.CTkFrame(app)
frame.pack(pady=10)

entry_name = ctk.CTkEntry(frame, placeholder_text="Customer Name")
entry_name.grid(row=0, column=0, padx=10, pady=5)

entry_age = ctk.CTkEntry(frame, placeholder_text="Age")
entry_age.grid(row=0, column=1, padx=10, pady=5)

option_room_type = ctk.CTkOptionMenu(frame, values=list(room_prices.keys()))
option_room_type.grid(row=1, column=0, padx=10, pady=5)

entry_checkin = ctk.CTkEntry(frame, placeholder_text="Check-in Date (YYYY-MM-DD)")
entry_checkin.grid(row=1, column=1, padx=10, pady=5)

entry_checkout = ctk.CTkEntry(frame, placeholder_text="Check-out Date (YYYY-MM-DD)")
entry_checkout.grid(row=2, column=0, padx=10, pady=5)

entry_nights = ctk.CTkEntry(frame, placeholder_text="Nights")
entry_nights.grid(row=2, column=1, padx=10, pady=5)

ctk.CTkButton(app, text="Create Booking", command=create_booking).pack(pady=5)
ctk.CTkButton(app, text="View Bookings", command=view_bookings).pack(pady=5)
ctk.CTkButton(app, text="Check Availability", command=check_availability).pack(pady=5)

entry_bill_room = ctk.CTkEntry(app, placeholder_text="Enter Room No. for Bill")
entry_bill_room.pack(pady=5)

ctk.CTkButton(app, text="Generate Bill", command=generate_bill).pack(pady=5)

output_box=ctk.CTkTextbox(app, width=600, height=200)
output_box.pack(pady=10)

app.mainloop()
