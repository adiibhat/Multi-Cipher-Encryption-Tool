import tkinter as tk
from tkinter import messagebox, ttk
import string

# 🔐 Character set for Caesar and Vigenère
CHARSET = string.ascii_letters + string.digits + string.punctuation + " "

# ===================== #
# 🔸 Caesar Cipher Logic
# ===================== #
def caesar_cipher(text, shift, mode):
    result = ''
    for char in text:
        if char in CHARSET:
            idx = CHARSET.index(char)
            shifted_idx = (idx + shift) % len(CHARSET) if mode == 'encrypt' else (idx - shift) % len(CHARSET)
            result += CHARSET[shifted_idx]
        else:
            result += char
    return result

# ======================== #
# 🔸 Vigenère Cipher Logic
# ======================== #
def vigenere_cipher(text, key, mode):
    result = ''
    key_indices = [CHARSET.index(k) for k in key if k in CHARSET]
    if not key_indices:
        return "Invalid key."

    for i, char in enumerate(text):
        if char in CHARSET:
            key_index = key_indices[i % len(key_indices)]
            char_index = CHARSET.index(char)
            new_index = (char_index + key_index) % len(CHARSET) if mode == 'encrypt' else (char_index - key_index) % len(CHARSET)
            result += CHARSET[new_index]
        else:
            result += char
    return result

# ========================= #
# 🔸 Playfair Cipher Helpers
# ========================= #
def generate_playfair_matrix(key):
    matrix = []
    used = set()
    key = ''.join([c.upper() for c in key if c.upper() in string.ascii_uppercase])
    key += ''.join([c for c in string.ascii_uppercase if c not in key and c != 'J'])

    for char in key:
        if char not in used:
            matrix.append(char)
            used.add(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]

def prepare_playfair_text(text, for_encryption=True):
    text = ''.join([c.upper() for c in text if c.upper() in string.ascii_uppercase])
    text = text.replace('J', 'I')

    prepared = ''
    i = 0
    while i < len(text):
        char1 = text[i]
        char2 = text[i + 1] if i + 1 < len(text) else 'X'
        if char1 == char2:
            prepared += char1 + 'X'
            i += 1
        else:
            prepared += char1 + char2
            i += 2

    if len(prepared) % 2 != 0:
        prepared += 'X'

    return prepared

def playfair_cipher(text, key, mode):
    matrix = generate_playfair_matrix(key)
    coords = {matrix[r][c]: (r, c) for r in range(5) for c in range(5)}
    text = prepare_playfair_text(text)

    result = ''
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        ra, ca = coords[a]
        rb, cb = coords[b]

        if ra == rb:
            result += matrix[ra][(ca + 1) % 5] if mode == 'encrypt' else matrix[ra][(ca - 1) % 5]
            result += matrix[rb][(cb + 1) % 5] if mode == 'encrypt' else matrix[rb][(cb - 1) % 5]
        elif ca == cb:
            result += matrix[(ra + 1) % 5][ca] if mode == 'encrypt' else matrix[(ra - 1) % 5][ca]
            result += matrix[(rb + 1) % 5][cb] if mode == 'encrypt' else matrix[(rb - 1) % 5][cb]
        else:
            result += matrix[ra][cb] + matrix[rb][ca]

    return result

# ================== #
# 🎨 GUI Setup
# ================== #
def create_gui():
    root = tk.Tk()
    root.title("🔐 Multi-Cipher Encryption Tool")
    root.geometry("700x600")
    root.configure(bg="#2b2b2b")

    style = {
        "bg": "#2b2b2b",
        "fg": "#ffffff",
        "font": ("Segoe UI", 11)
    }

    tk.Label(root, text="Multi-Cipher Encryption Tool", font=("Helvetica", 18, "bold"), bg="#2b2b2b", fg="#00e6ac").pack(pady=10)

    # Cipher Selection
    cipher_var = tk.StringVar(value="Caesar")
    tk.Label(root, text="Choose Cipher:", **style).pack()
    cipher_menu = ttk.Combobox(root, textvariable=cipher_var, values=["Caesar", "Vigenère", "Playfair"], state="readonly", font=("Segoe UI", 10))
    cipher_menu.pack(pady=5)

    # Mode Selection
    mode_var = tk.StringVar(value="encrypt")
    mode_frame = tk.Frame(root, bg="#2b2b2b")
    mode_frame.pack(pady=5)
    tk.Radiobutton(mode_frame, text="Encrypt", variable=mode_var, value="encrypt", **style, selectcolor="#2b2b2b").grid(row=0, column=0, padx=10)
    tk.Radiobutton(mode_frame, text="Decrypt", variable=mode_var, value="decrypt", **style, selectcolor="#2b2b2b").grid(row=0, column=1, padx=10)

    # Input Text
    tk.Label(root, text="Enter Text:", **style).pack()
    input_text = tk.Text(root, height=5, width=70, font=("Consolas", 11), bg="#3c3f41", fg="#ffffff", insertbackground="white")
    input_text.pack(pady=5)

    # Key/Shift Entry
    key_label = tk.Label(root, text="Enter Key / Shift:", **style)
    key_label.pack()
    key_entry = tk.Entry(root, font=("Consolas", 11), bg="#3c3f41", fg="white", insertbackground="white")
    key_entry.pack(pady=5)

    # Output Text
    tk.Label(root, text="Result:", **style).pack()
    result_box = tk.Text(root, height=5, width=70, font=("Consolas", 11), bg="#1f1f1f", fg="#00ff88", state="disabled")
    result_box.pack(pady=10)

    # 🔘 Process & Clear
    def process():
        text = input_text.get("1.0", tk.END).strip()
        key = key_entry.get()
        mode = mode_var.get()
        cipher = cipher_var.get()

        if not text:
            messagebox.showwarning("Input Missing", "Please enter some text.")
            return

        if cipher == "Caesar":
            if not key.isdigit():
                messagebox.showerror("Invalid Shift", "Shift must be a number.")
                return
            shift = int(key)
            result = caesar_cipher(text, shift, mode)

        elif cipher == "Vigenère":
            if not key:
                messagebox.showerror("Key Missing", "Please enter a Vigenère key.")
                return
            result = vigenere_cipher(text, key, mode)

        elif cipher == "Playfair":
            if not key:
                messagebox.showerror("Key Missing", "Please enter a Playfair key.")
                return
            result = playfair_cipher(text, key, mode)

        result_box.config(state='normal')
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, result)
        result_box.config(state='disabled')

    def clear():
        input_text.delete("1.0", tk.END)
        key_entry.delete(0, tk.END)
        result_box.config(state='normal')
        result_box.delete("1.0", tk.END)
        result_box.config(state='disabled')

    btn_frame = tk.Frame(root, bg="#2b2b2b")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Process", command=process, bg="#00e6ac", fg="black", font=("Segoe UI", 11, "bold"), width=12).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Clear", command=clear, bg="#ff5f5f", fg="white", font=("Segoe UI", 11, "bold"), width=12).grid(row=0, column=1, padx=10)

    root.mainloop()

# Run the app
if __name__ == "__main__":
    create_gui()
