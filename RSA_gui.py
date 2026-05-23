import tkinter as tk
from tkinter import messagebox
import random
import math

def is_prime(num):
    """Mengecek apakah suatu angka adalah bilangan prima."""
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def generate_prime():
    """Menghasilkan bilangan prima sederhana untuk simulasi."""
    primes = []

    for number in range(100, 300):
        if is_prime(number):
            primes.append(number)

    return random.choice(primes)


def gcd(a, b):
    """Menghitung FPB menggunakan algoritma Euclidean."""
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    """
    Mencari d, yaitu invers modular dari e terhadap phi.
    d memenuhi: (d * e) mod phi = 1
    """
    for d in range(2, phi):
        if (d * e) % phi == 1:
            return d
    return None


def generate_keys():
    """Membangkitkan public key dan private key RSA."""
    p = generate_prime()
    q = generate_prime()

    while q == p:
        q = generate_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 3
    while e < phi:
        if gcd(e, phi) == 1:
            break
        e += 2

    d = mod_inverse(e, phi)

    if d is None:
        raise ValueError("Gagal membangkitkan kunci RSA.")

    public_key = (e, n)
    private_key = (d, n)

    return p, q, n, phi, public_key, private_key


def encrypt_message(message, public_key):
    """Mengenkripsi pesan menggunakan public key RSA."""
    e, n = public_key
    encrypted = []

    for char in message:
        m = ord(char)
        c = pow(m, e, n)
        encrypted.append(c)

    return encrypted


def decrypt_message(ciphertext, private_key):
    """Mendekripsi ciphertext menggunakan private key RSA."""
    d, n = private_key
    decrypted = ""

    for c in ciphertext:
        m = pow(c, d, n)
        decrypted += chr(m)

    return decrypted


public_key = None
private_key = None
ciphertext_global = None


def handle_generate_key():
    global public_key, private_key

    try:
        p, q, n, phi, public_key, private_key = generate_keys()

        label_pq_value.config(text=f"p = {p}, q = {q}")
        label_n_value.config(text=f"n = {n}")
        label_phi_value.config(text=f"φ(n) = {phi}")
        label_public_key_value.config(text=f"Public Key = {public_key}")
        label_private_key_value.config(text=f"Private Key = {private_key}")

        messagebox.showinfo("Berhasil", "Kunci RSA berhasil dibuat.")

    except Exception as error:
        messagebox.showerror("Error", str(error))


def handle_encrypt():
    global ciphertext_global

    if public_key is None:
        messagebox.showwarning("Peringatan", "Silakan generate key terlebih dahulu.")
        return

    plaintext = text_plaintext.get("1.0", tk.END).strip()

    if plaintext == "":
        messagebox.showwarning("Peringatan", "Plaintext tidak boleh kosong.")
        return

    try:
        ciphertext_global = encrypt_message(plaintext, public_key)

        text_ciphertext.delete("1.0", tk.END)
        text_ciphertext.insert(tk.END, str(ciphertext_global))

        messagebox.showinfo("Berhasil", "Pesan berhasil dienkripsi.")

    except Exception as error:
        messagebox.showerror("Error", str(error))


def handle_decrypt():
    global ciphertext_global

    if private_key is None:
        messagebox.showwarning("Peringatan", "Silakan generate key terlebih dahulu.")
        return

    if ciphertext_global is None:
        messagebox.showwarning("Peringatan", "Silakan lakukan enkripsi terlebih dahulu.")
        return

    try:
        decrypted_text = decrypt_message(ciphertext_global, private_key)

        text_decrypted.delete("1.0", tk.END)
        text_decrypted.insert(tk.END, decrypted_text)

        messagebox.showinfo("Berhasil", "Ciphertext berhasil didekripsi.")

    except Exception as error:
        messagebox.showerror("Error", str(error))


def handle_reset():
    global public_key, private_key, ciphertext_global

    public_key = None
    private_key = None
    ciphertext_global = None

    text_plaintext.delete("1.0", tk.END)
    text_ciphertext.delete("1.0", tk.END)
    text_decrypted.delete("1.0", tk.END)

    label_pq_value.config(text="-")
    label_n_value.config(text="-")
    label_phi_value.config(text="-")
    label_public_key_value.config(text="-")
    label_private_key_value.config(text="-")

    messagebox.showinfo("Reset", "Semua data berhasil dihapus.")


root = tk.Tk()
root.title("Aplikasi Simulasi RSA")
root.geometry("760x720")
root.resizable(False, False)

label_title = tk.Label(
    root,
    text="Aplikasi Desktop Sederhana\nSimulasi Enkripsi dan Dekripsi Pesan Menggunakan RSA",
    font=("Arial", 16, "bold"),
    justify="center"
)
label_title.pack(pady=15)

frame_main = tk.Frame(root)
frame_main.pack(padx=20, pady=10, fill="both")

label_plaintext = tk.Label(frame_main, text="Plaintext / Pesan Asli:", font=("Arial", 11, "bold"))
label_plaintext.pack(anchor="w")

text_plaintext = tk.Text(frame_main, height=4, width=85)
text_plaintext.pack(pady=5)

frame_buttons = tk.Frame(frame_main)
frame_buttons.pack(pady=10)

button_generate = tk.Button(
    frame_buttons,
    text="Generate Key",
    width=18,
    command=handle_generate_key
)
button_generate.grid(row=0, column=0, padx=5)

button_encrypt = tk.Button(
    frame_buttons,
    text="Enkripsi",
    width=18,
    command=handle_encrypt
)
button_encrypt.grid(row=0, column=1, padx=5)

button_decrypt = tk.Button(
    frame_buttons,
    text="Dekripsi",
    width=18,
    command=handle_decrypt
)
button_decrypt.grid(row=0, column=2, padx=5)

button_reset = tk.Button(
    frame_buttons,
    text="Reset",
    width=18,
    command=handle_reset
)
button_reset.grid(row=0, column=3, padx=5)

frame_key = tk.LabelFrame(frame_main, text="Informasi Kunci RSA", padx=10, pady=10)
frame_key.pack(fill="x", pady=10)

label_pq = tk.Label(frame_key, text="Bilangan Prima:", font=("Arial", 10, "bold"))
label_pq.grid(row=0, column=0, sticky="w")
label_pq_value = tk.Label(frame_key, text="-")
label_pq_value.grid(row=0, column=1, sticky="w")

label_n = tk.Label(frame_key, text="Nilai n:", font=("Arial", 10, "bold"))
label_n.grid(row=1, column=0, sticky="w")
label_n_value = tk.Label(frame_key, text="-")
label_n_value.grid(row=1, column=1, sticky="w")

label_phi = tk.Label(frame_key, text="Nilai φ(n):", font=("Arial", 10, "bold"))
label_phi.grid(row=2, column=0, sticky="w")
label_phi_value = tk.Label(frame_key, text="-")
label_phi_value.grid(row=2, column=1, sticky="w")

label_public_key = tk.Label(frame_key, text="Public Key:", font=("Arial", 10, "bold"))
label_public_key.grid(row=3, column=0, sticky="w")
label_public_key_value = tk.Label(frame_key, text="-")
label_public_key_value.grid(row=3, column=1, sticky="w")

label_private_key = tk.Label(frame_key, text="Private Key:", font=("Arial", 10, "bold"))
label_private_key.grid(row=4, column=0, sticky="w")
label_private_key_value = tk.Label(frame_key, text="-")
label_private_key_value.grid(row=4, column=1, sticky="w")

label_ciphertext = tk.Label(frame_main, text="Ciphertext / Hasil Enkripsi:", font=("Arial", 11, "bold"))
label_ciphertext.pack(anchor="w", pady=(10, 0))

text_ciphertext = tk.Text(frame_main, height=5, width=85)
text_ciphertext.pack(pady=5)

label_decrypted = tk.Label(frame_main, text="Hasil Dekripsi:", font=("Arial", 11, "bold"))
label_decrypted.pack(anchor="w", pady=(10, 0))

text_decrypted = tk.Text(frame_main, height=4, width=85)
text_decrypted.pack(pady=5)

label_note = tk.Label(
    root,
    text="Catatan: Aplikasi ini merupakan simulasi pembelajaran RSA dan bukan sistem keamanan nyata.",
    font=("Arial", 9, "italic")
)
label_note.pack(pady=10)

root.mainloop()