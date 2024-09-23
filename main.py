import pywhatkit
import pandas as pd
import time
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to browse for the CSV file
def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")], 
        title="Select a CSV File"
    )
    csv_file_var.set(file_path)

# Function to replace placeholders dynamically based on column names
def replace_placeholders(message_template, row):
    # Loop through each column in the CSV row
    for column in row.index:
        placeholder = f"{{{column}}}"  # Placeholder like {parentname}, {childname}, etc.
        # Replace placeholders with the string representation of the value
        message_template = message_template.replace(placeholder, str(row[column]))
    return message_template

# Function to send WhatsApp messages
def send_messages():
    try:
        # Read CSV file
        file_path = csv_file_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a CSV file")
            return

        df = pd.read_csv(file_path)

        # Get the custom message from the text box
        custom_message = message_box.get("1.0", "end-1c")
        if not custom_message:
            messagebox.showerror("Error", "Please enter a custom message")
            return

        # Loop through each row in the DataFrame
        for index, row in df.iterrows():
            phone_number = row['phonenumber']

            # Replace placeholders with actual values from the row
            message = replace_placeholders(custom_message, row)

            # Specify the time to send the message
            pywhatkit.sendwhatmsg(phone_number, message, int(hour_var.get()), int(minute_var.get()))

            # Add a delay to avoid sending messages too quickly
            time.sleep(60)

        messagebox.showinfo("Success", "Messages sent successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("WhatsApp Message Sender")

# CSV file selection
csv_file_var = tk.StringVar()
tk.Label(root, text="Select CSV File:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=csv_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=10)

# Time input (hour)
tk.Label(root, text="Set Hour (24-hour format):").grid(row=1, column=0, padx=10, pady=10)
hour_var = tk.StringVar(value="18")
tk.Entry(root, textvariable=hour_var, width=10).grid(row=1, column=1, padx=10, pady=10)

# Time input (minute)
tk.Label(root, text="Set Minute:").grid(row=2, column=0, padx=10, pady=10)
minute_var = tk.StringVar(value="30")
tk.Entry(root, textvariable=minute_var, width=10).grid(row=2, column=1, padx=10, pady=10)

# Message customization box
tk.Label(root, text="Custom Message (use {column_name} for placeholders):").grid(row=3, column=0, padx=10, pady=10)
message_box = tk.Text(root, height=5, width=40)
message_box.grid(row=3, column=1, padx=10, pady=10)

# Default message example
message_box.insert("1.0", "Hello {parentname}, this is a reminder about the event {eventname} for your child {childname}.")

# Send button
tk.Button(root, text="Send Messages", command=send_messages).grid(row=4, column=1, padx=10, pady=20)

# Start the main event loop
root.mainloop()
