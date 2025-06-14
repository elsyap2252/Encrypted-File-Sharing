import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def browse_file():
    filepath = filedialog.askopenfilename()
    entry_file.delete(0, tk.END)
    entry_file.insert(0, filepath)

def send_email():
    filepath = entry_file.get()
    receiver = entry_email.get()

    if not filepath or not receiver:
        messagebox.showerror("Error", "Isi semua field terlebih dahulu!")
        return

    # Save file path to 'file_to_encrypt.txt'
    with open("file_to_encrypt.txt", "w") as f:
        with open(filepath, "r") as original_file:
            f.write(original_file.read())

    # Ganti email tujuan di encrypt-send.py sebelum dijalankan
    try:
        with open("encrypt-send.py", "r") as file:
            lines = file.readlines()

        with open("encrypt-send.py", "w") as file:
            for line in lines:
                if line.strip().startswith("EMAIL_RECEIVER"):
                    file.write(f'EMAIL_RECEIVER = "{receiver}"\n')
                else:
                    file.write(line)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal edit email penerima: {e}")
        return

    # Jalankan encrypt-send.py
    try:
        subprocess.run(["python", "encrypt-send.py"], check=True)
        messagebox.showinfo("Sukses", "File berhasil dienkripsi dan dikirim!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Gagal menjalankan encrypt-send.py")

# Setup GUI
window = tk.Tk()
window.title("Encrypted File Sharing via Email")

tk.Label(window, text="Pilih file yang akan dienkripsi:").pack(pady=5)
entry_file = tk.Entry(window, width=50)
entry_file.pack(padx=10)
tk.Button(window, text="Browse", command=browse_file).pack(pady=5)

tk.Label(window, text="Masukkan email tujuan:").pack(pady=5)
entry_email = tk.Entry(window, width=50)
entry_email.pack(padx=10)

tk.Button(window, text="Encrypt & Send", command=send_email, bg="blue", fg="white").pack(pady=20)

window.mainloop()