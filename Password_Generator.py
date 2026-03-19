import tkinter as tk
from tkinter import messagebox, filedialog
import string
import secrets

# -------------------- FUNCTIONS --------------------

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Please enter a valid password length")
        return

    chars = ""

    if var_upper.get():
        chars += string.ascii_uppercase
    if var_lower.get():
        chars += string.ascii_lowercase
    if var_digits.get():
        chars += string.digits
    if var_symbols.get():
        chars += string.punctuation

    if not chars:
        messagebox.showerror("Error", "Select at least one character type")
        return

    if var_exclude.get():
        similar_chars = "O0l1I"
        chars = ''.join(c for c in chars if c not in similar_chars)

    password = ''.join(secrets.choice(chars) for _ in range(length))
    password_var.set(password)

    check_strength(password)


def check_strength(password):
    strength = 0

    if len(password) >= 8:
        strength += 1
    if any(c.islower() for c in password):
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 1

    if strength <= 2:
        strength_label.config(text="Weak", fg="red")
    elif strength == 3 or strength == 4:
        strength_label.config(text="Medium", fg="orange")
    else:
        strength_label.config(text="Strong", fg="green")


def copy_password():
    password = password_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")


def reset_fields():
    length_entry.delete(0, tk.END)
    password_var.set("")
    strength_label.config(text="")

    var_upper.set(0)
    var_lower.set(0)
    var_digits.set(0)
    var_symbols.set(0)
    var_exclude.set(0)


def save_password():
    password = password_var.get()
    if not password:
        messagebox.showerror("Error", "No password to save")
        return

    file = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text Files", "*.txt")])
    if file:
        with open(file, "a") as f:
            f.write(password + "\n")
        messagebox.showinfo("Saved", "Password saved successfully!")


def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    if dark_mode:
        root.config(bg="#1e1e1e")
        main_frame.config(bg="#1e1e1e")
        for widget in main_frame.winfo_children():
            try:
                widget.config(bg="#1e1e1e", fg="white")
            except:
                pass
    else:
        root.config(bg="white")
        main_frame.config(bg="white")
        for widget in main_frame.winfo_children():
            try:
                widget.config(bg="white", fg="black")
            except:
                pass


# -------------------- UI SETUP --------------------

root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("500x550")
root.resizable(False, False)

dark_mode = False

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# -------------------- VARIABLES --------------------

password_var = tk.StringVar()

var_upper = tk.IntVar()
var_lower = tk.IntVar()
var_digits = tk.IntVar()
var_symbols = tk.IntVar()
var_exclude = tk.IntVar()

# -------------------- UI ELEMENTS --------------------

tk.Label(main_frame, text="Password Length:", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
length_entry = tk.Entry(main_frame, font=("Arial", 12))
length_entry.grid(row=0, column=1, pady=5)

# Checkboxes
tk.Checkbutton(main_frame, text="Uppercase", variable=var_upper).grid(row=1, column=0, sticky="w")
tk.Checkbutton(main_frame, text="Lowercase", variable=var_lower).grid(row=2, column=0, sticky="w")
tk.Checkbutton(main_frame, text="Numbers", variable=var_digits).grid(row=3, column=0, sticky="w")
tk.Checkbutton(main_frame, text="Symbols", variable=var_symbols).grid(row=4, column=0, sticky="w")
tk.Checkbutton(main_frame, text="Exclude Similar (O,0,l,1)", variable=var_exclude).grid(row=5, column=0, columnspan=2, sticky="w")

# Generate Button
tk.Button(main_frame, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white").grid(row=6, column=0, columnspan=2, pady=10)

# Output
tk.Label(main_frame, text="Generated Password:", font=("Arial", 12)).grid(row=7, column=0, sticky="w")
output_entry = tk.Entry(main_frame, textvariable=password_var, font=("Arial", 12), width=30, bd=2, relief="groove")
output_entry.grid(row=8, column=0, columnspan=2, pady=5)

# Strength Label
tk.Label(main_frame, text="Strength:", font=("Arial", 12)).grid(row=9, column=0, sticky="w")
strength_label = tk.Label(main_frame, text="", font=("Arial", 12, "bold"))
strength_label.grid(row=9, column=1, sticky="w")

# Buttons
tk.Button(main_frame, text="Copy", command=copy_password).grid(row=10, column=0, pady=10)
tk.Button(main_frame, text="Reset", command=reset_fields).grid(row=10, column=1)

tk.Button(main_frame, text="Save to File", command=save_password).grid(row=11, column=0, pady=5)
tk.Button(main_frame, text="Toggle Dark Mode", command=toggle_theme).grid(row=11, column=1)

# -------------------- RUN APP --------------------

root.mainloop()