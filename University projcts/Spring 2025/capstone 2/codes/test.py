import tkinter as tk
import random

class BughesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bughes - Vulnerability Scanner")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.title_label = tk.Label(root, text="BUGHES", fg="#00FF00", bg="black",
                                    font=("Courier", 32, "bold"))
        self.title_label.place(x=300, y=20)

        self.scan_button = tk.Button(root, text="Start Scan", command=self.scan_vulnerabilities,
                                     fg="white", bg="#444444", font=("Courier", 14))
        self.scan_button.place(x=350, y=80)

        self.result_text = tk.Text(root, bg="black", fg="white", font=("Courier", 12),
                                   insertbackground="white", borderwidth=0)
        self.result_text.place(x=50, y=130, width=700, height=400)

        # Start animation of glitch lines
        self.animate_lines()

    def animate_lines(self):
        self.canvas.delete("glitch")
        for _ in range(20):  # Number of bugged lines
            y = random.randint(0, 600)
            x1 = random.randint(0, 400)
            x2 = random.randint(400, 800)
            color = random.choice(["#00FF00", "#FF0000", "#00FFFF", "#FFFFFF"])
            self.canvas.create_line(x1, y, x2, y, fill=color, width=random.randint(1, 3), tags="glitch")
        self.root.after(100, self.animate_lines)  # Refresh glitch every 100ms

    def scan_vulnerabilities(self):
        # Simulate scanning
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Scanning for vulnerabilities...\n")
        self.root.after(1000, self.show_results)

    def show_results(self):
        fake_results = [
            "[!] Buffer Overflow in main()",
            "[!] Use of deprecated system call: int 0x80",
            "[!] Dangerous syscall pattern detected: execve",
            "[*] Heuristic match: suspicious control flow",
        ]
        for line in fake_results:
            self.result_text.insert(tk.END, f"{line}\n")


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BughesGUI(root)
    root.mainloop()
