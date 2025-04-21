import customtkinter as ctk
import psutil
import platform
import threading
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    import cpuinfo
except ImportError:
    cpuinfo = None

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PerformanceMonitor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PC Performance Monitor")
        self.geometry("1600x900")
        self.minsize(1400, 800)

        self.num_cores = psutil.cpu_count(logical=True)

        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(1, weight=1)

        self.create_widgets()
        self.update_stats()
        self.update_graphs()

    def create_widgets(self):
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 5))

        self.sys_info = ctk.CTkLabel(self.info_frame, text=self.get_system_info(), justify="left", font=("Consolas", 13))
        self.sys_info.pack(padx=10, pady=10, anchor="w")

        self.stats_frame = ctk.CTkFrame(self, corner_radius=15)
        self.stats_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(5, 10))

        self.stats_frame.grid_rowconfigure(6, weight=1)

        self.stats_title = ctk.CTkLabel(self.stats_frame, text="Performance Stats", font=("Arial", 20, "bold"))
        self.stats_title.pack(pady=(15, 25))

        def add_stat_row(parent, label_text):
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.pack(fill="x", padx=20, pady=5)
            label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14))
            label.pack(side="left")
            value = ctk.CTkLabel(frame, text="", font=("Arial", 14))
            value.pack(side="right")
            return value

        self.cpu_label = add_stat_row(self.stats_frame, "CPU Usage:")
        self.temp_label = add_stat_row(self.stats_frame, "CPU Temp:")
        self.ram_label = add_stat_row(self.stats_frame, "RAM Usage:")
        self.disk_label = add_stat_row(self.stats_frame, "Disk Usage:")
        self.net_label = add_stat_row(self.stats_frame, "Network I/O:")

        self.graph_frame = ctk.CTkFrame(self, corner_radius=15)
        self.graph_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(5, 10))

        self.fig = Figure(figsize=(12, 6), dpi=100, facecolor='#1e1e1e')
        self.ax_cpu = self.fig.add_subplot(231, facecolor='#2e2e2e')
        self.ax_ram = self.fig.add_subplot(232, facecolor='#2e2e2e')
        self.ax_disk = self.fig.add_subplot(233, facecolor='#2e2e2e')
        self.ax_net = self.fig.add_subplot(234, facecolor='#2e2e2e')
        self.ax_cores = self.fig.add_subplot(235, facecolor='#2e2e2e')

        self.cpu_usage_history = []
        self.ram_usage_history = []
        self.disk_read_history = []
        self.net_sent_history = []
        self.core_usage_current = [0 for _ in range(self.num_cores)]

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def get_system_info(self):
        uname = platform.uname()
        return f"System: {uname.system}\nNode: {uname.node}\nRelease: {uname.release}\nVersion: {uname.version}\nMachine: {uname.machine}\nProcessor: {uname.processor}"

    def get_temperature(self):
        try:
            temps = psutil.sensors_temperatures()
            for name, entries in temps.items():
                for entry in entries:
                    if entry.label.lower() in ["package id 0", "core 0", "cpu"] or entry.label == '':
                        return f"{entry.current} °C"
            return "N/A"
        except Exception:
            return "Not Supported"

    def update_stats(self):
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        ram = psutil.virtual_memory()
        disk = psutil.disk_io_counters()
        net = psutil.net_io_counters()

        self.cpu_label.configure(text=f"{sum(cpu_percent)/len(cpu_percent):.1f}% ({cpu_percent})")
        self.temp_label.configure(text=self.get_temperature())
        self.ram_label.configure(text=f"{ram.percent}% ({self.convert_bytes(ram.used)}/{self.convert_bytes(ram.total)})")
        self.disk_label.configure(text=f"R {self.convert_bytes(disk.read_bytes)} / W {self.convert_bytes(disk.write_bytes)}")
        self.net_label.configure(text=f"Sent {self.convert_bytes(net.bytes_sent)} / Recv {self.convert_bytes(net.bytes_recv)}")

        self.after(1000, self.update_stats)

    def update_graphs(self):
        cpu_percents = psutil.cpu_percent(percpu=True)
        self.cpu_usage_history.append(sum(cpu_percents)/len(cpu_percents))
        self.ram_usage_history.append(psutil.virtual_memory().percent)
        self.disk_read_history.append(psutil.disk_io_counters().read_bytes)
        self.net_sent_history.append(psutil.net_io_counters().bytes_sent)
        self.core_usage_current = cpu_percents

        if len(self.cpu_usage_history) > 60:
            self.cpu_usage_history.pop(0)
            self.ram_usage_history.pop(0)
            self.disk_read_history.pop(0)
            self.net_sent_history.pop(0)

        self.ax_cpu.clear()
        self.ax_cpu.plot(self.cpu_usage_history, label="CPU %", color="cyan")
        self.ax_cpu.set_title("CPU Usage", color="white")
        self.ax_cpu.set_ylim(0, 100)
        self.ax_cpu.tick_params(axis='x', colors='white')
        self.ax_cpu.tick_params(axis='y', colors='white')

        self.ax_ram.clear()
        self.ax_ram.plot(self.ram_usage_history, label="RAM %", color="green")
        self.ax_ram.set_title("RAM Usage", color="white")
        self.ax_ram.set_ylim(0, 100)
        self.ax_ram.tick_params(axis='x', colors='white')
        self.ax_ram.tick_params(axis='y', colors='white')

        self.ax_disk.clear()
        self.ax_disk.plot(self.disk_read_history, label="Disk Read", color="orange")
        self.ax_disk.set_title("Disk Read", color="white")
        self.ax_disk.tick_params(axis='x', colors='white')
        self.ax_disk.tick_params(axis='y', colors='white')

        self.ax_net.clear()
        self.ax_net.plot(self.net_sent_history, label="Net Sent", color="purple")
        self.ax_net.set_title("Network Sent", color="white")
        self.ax_net.tick_params(axis='x', colors='white')
        self.ax_net.tick_params(axis='y', colors='white')

        self.ax_cores.clear()
        self.ax_cores.bar(range(self.num_cores), self.core_usage_current, color="skyblue")
        self.ax_cores.set_title("Per-Core CPU Usage (%)", color="white")
        self.ax_cores.set_ylim(0, 100)
        self.ax_cores.set_xticks(range(self.num_cores))
        self.ax_cores.set_xticklabels([f"Core {i}" for i in range(self.num_cores)], rotation=45, ha="right")
        self.ax_cores.tick_params(axis='x', colors='white')
        self.ax_cores.tick_params(axis='y', colors='white')

        self.fig.tight_layout()
        self.canvas.draw()

        self.after(1000, self.update_graphs)

    def convert_bytes(self, num):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return f"{num:.2f} {unit}"
            num /= 1024.0

if __name__ == '__main__':
    app = PerformanceMonitor()
    app.mainloop()
