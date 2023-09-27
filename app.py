import psutil
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to update CPU and RAM usage
def update_usage():
    # Get CPU usage and display it
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")

    # Get RAM usage and display it
    ram = psutil.virtual_memory()
    ram_label.config(text=f"RAM Usage: {ram.percent}%")

    # Get the process using the most CPU
    processes = [proc.info for proc in psutil.process_iter(attrs=['name', 'cpu_percent'])]
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    most_used_process_label.config(text=f"Most CPU Usage: {processes[0]['name']} ({processes[0]['cpu_percent']}%)")

    # Update the usage plot
    cpu_usage_data.append(cpu_usage)
    ram_usage_data.append(ram.percent)
    if len(cpu_usage_data) > 10:
        cpu_usage_data.pop(0)
        ram_usage_data.pop(0)

    ax.clear()
    ax.plot(range(len(cpu_usage_data)), cpu_usage_data, label='CPU Usage')
    ax.plot(range(len(ram_usage_data)), ram_usage_data, label='RAM Usage')
    ax.legend(loc="upper right")
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Usage (%)')
    ax.set_title('CPU and RAM Usage')

    canvas.draw()

    # Schedule the function to run again after 1 second
    root.after(1000, update_usage)

# Create the main application window
root = tk.Tk()
root.title("Resource Monitor")

# Create labels for CPU and RAM usage
cpu_label = ttk.Label(root, text="CPU Usage: ")
cpu_label.pack()
ram_label = ttk.Label(root, text="RAM Usage: ")
ram_label.pack()
most_used_process_label = ttk.Label(root, text="Most CPU Usage: ")
most_used_process_label.pack()

# Create a plot to display CPU and RAM usage
fig, ax = plt.subplots(figsize=(6, 3))
cpu_usage_data = []
ram_usage_data = []
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Start monitoring the usage
update_usage()

# Run the application
root.mainloop()
