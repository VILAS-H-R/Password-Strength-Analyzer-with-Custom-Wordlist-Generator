import tkinter as tk
from tkinter import messagebox, filedialog
from zxcvbn import zxcvbn
import itertools

# Common substitutions
LEET_MAP = {
    'a': ['@', '4'],
    'e': ['3'],
    'i': ['1', '!'],
    'o': ['0'],
    's': ['$', '5'],
    't': ['7']
}

# Generate leetspeak variants
def generate_variants(word):
    variants = set([word])
    for i in range(1, len(word) + 1):
        for combo in itertools.combinations(range(len(word)), i):
            for replacements in itertools.product(*[LEET_MAP.get(word[j], [word[j]]) for j in combo]):
                temp = list(word)
                for idx, r in zip(combo, replacements):
                    temp[idx] = r
                variants.add(''.join(temp))
    return variants

# Generate wordlist
def generate_wordlist(inputs):
    base_words = [w.lower() for w in inputs if w]
    variants = set()
    for word in base_words:
        variants.update(generate_variants(word))
        for year in range(2000, 2026):
            variants.add(word + str(year))
            variants.add(str(year) + word)
    return sorted(variants)

# GUI App
class PasswordApp:
    def __init__(self, root):
        self.root = root
        root.title("Password Strength Analyzer & Wordlist Generator")
        root.geometry("500x500")

        # Password input
        tk.Label(root, text="Enter Password:").pack()
        self.password_entry = tk.Entry(root, show='*', width=40)
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Analyze Strength", command=self.analyze_password).pack(pady=5)

        self.result_label = tk.Label(root, text="", fg="blue", wraplength=400)
        self.result_label.pack(pady=10)

        # Wordlist generation inputs
        tk.Label(root, text="Custom Info for Wordlist").pack(pady=10)
        self.name_var = tk.StringVar()
        self.pet_var = tk.StringVar()
        self.date_var = tk.StringVar()

        tk.Entry(root, textvariable=self.name_var, width=40).pack(pady=2)
        tk.Entry(root, textvariable=self.pet_var, width=40).pack(pady=2)
        tk.Entry(root, textvariable=self.date_var, width=40).pack(pady=2)

        tk.Button(root, text="Generate Wordlist", command=self.generate_and_export).pack(pady=10)

    def analyze_password(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return
        result = zxcvbn(password)
        score = result['score']
        crack_time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
        feedback = result['feedback']['warning'] or "No major issues."

        msg = f"Score: {score}/4\nCrack Time (slow hash): {crack_time}\nFeedback: {feedback}"
        self.result_label.config(text=msg)

    def generate_and_export(self):
        info = [self.name_var.get(), self.pet_var.get(), self.date_var.get()]
        wordlist = generate_wordlist(info)

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Wordlist",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                f.write("\n".join(wordlist))
            messagebox.showinfo("Success", f"Wordlist saved to:\n{file_path}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()
