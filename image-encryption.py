import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Generate chaotic sequence based on logistic map
def generate_chaotic_sequence(length, seed=0.5, r=3.99):
    seq = []
    x = seed
    for _ in range(length):
        x = r * x * (1 - x)
        seq.append(int(x * 256) % 256)
    return seq

# Convert password string to seed value between 0 and 1
def password_to_seed(password):
    total = sum(ord(char) for char in password)
    return (total % 1000) / 1000.0 or 0.5

# XOR-based encryption/decryption using chaotic sequence
def chaotic_xor_encrypt_decrypt(image, password):
    pixels = image.load()
    width, height = image.size
    seed = password_to_seed(password)
    chaotic_seq = generate_chaotic_sequence(width * height * 3, seed)
    
    index = 0
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y][:3]
            r ^= chaotic_seq[index]
            g ^= chaotic_seq[index + 1]
            b ^= chaotic_seq[index + 2]
            pixels[x, y] = (r, g, b)
            index += 3
    return image

class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryption Tool - Chaotic XOR Based")
        self.root.configure(bg='#1e1e1e')

        self.original_img_label = tk.Label(root, text="Original Image", fg='white', bg='#1e1e1e')
        self.original_img_label.grid(row=0, column=0)

        self.encrypted_img_label = tk.Label(root, text="Processed Image", fg='white', bg='#1e1e1e')
        self.encrypted_img_label.grid(row=0, column=1)

        self.original_canvas = tk.Label(root, bg='#1e1e1e')
        self.original_canvas.grid(row=1, column=0, padx=10, pady=10)

        self.result_canvas = tk.Label(root, bg='#1e1e1e')
        self.result_canvas.grid(row=1, column=1, padx=10, pady=10)

        self.upload_btn = tk.Button(root, text="Upload Image", command=self.upload_image, bg='#333', fg='white')
        self.upload_btn.grid(row=2, column=0, columnspan=2, pady=5)

        tk.Label(root, text="Enter Password:", fg='white', bg='#1e1e1e').grid(row=3, column=0, sticky='e')
        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.grid(row=3, column=1, sticky='w')

        self.encrypt_btn = tk.Button(root, text="Encrypt", command=self.encrypt_image, bg='#007acc', fg='white')
        self.encrypt_btn.grid(row=4, column=0, pady=10)

        self.decrypt_btn = tk.Button(root, text="Decrypt", command=self.decrypt_image, bg='#007acc', fg='white')
        self.decrypt_btn.grid(row=4, column=1, pady=10)

        self.save_btn = tk.Button(root, text="Save Output", command=self.save_output, bg='#444', fg='white')
        self.save_btn.grid(row=5, column=0, columnspan=2)

        self.status_label = tk.Label(root, text="Status: Ready", fg='lightgreen', bg='#1e1e1e')
        self.status_label.grid(row=6, column=0, columnspan=2)

        self.original_image = None
        self.processed_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.original_image = Image.open(file_path).convert('RGB')
            self.display_image(self.original_image, self.original_canvas)
            self.status_label.config(text="Status: Image loaded")

    def display_image(self, image, canvas):
        image_resized = image.resize((250, 250))
        photo = ImageTk.PhotoImage(image_resized)
        canvas.image = photo
        canvas.config(image=photo)

    def encrypt_image(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Please upload an image first.")
            return
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return
        self.processed_image = chaotic_xor_encrypt_decrypt(self.original_image.copy(), password)
        self.display_image(self.processed_image, self.result_canvas)
        self.status_label.config(text="Status: Image encrypted")

    def decrypt_image(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Please upload an image first.")
            return
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return
        self.processed_image = chaotic_xor_encrypt_decrypt(self.original_image.copy(), password)
        self.display_image(self.processed_image, self.result_canvas)
        self.status_label.config(text="Status: Image decrypted")

    def save_output(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.processed_image.save(file_path)
                self.status_label.config(text=f"Image saved: {os.path.basename(file_path)}")
        else:
            messagebox.showerror("Error", "No image to save.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
