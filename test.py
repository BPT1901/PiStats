import tkinter as tk

app = tk.Tk()
app.geometry("320x240")

frame = tk.Frame(master=app, width=320, height=240)
frame.pack(fill="both", expand=True)

# Create static labels for testing
cpu_label = tk.Label(master=frame, text="CPU Usage: 0%")
cpu_label.pack(pady=10)
ram_label = tk.Label(master=frame, text="RAM Usage: 0%")
ram_label.pack(pady=10)

app.mainloop()