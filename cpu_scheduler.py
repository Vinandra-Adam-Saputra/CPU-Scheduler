import tkinter as tk  # Library utama untuk membuat GUI
from tkinter import ttk, scrolledtext  # Komponen GUI tambahan

# Definisikan kelas untuk merepresentasikan sebuah proses
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid  # ID Proses
        self.arrival_time = arrival_time  # Waktu kedatangan proses
        self.burst_time = burst_time  # Total waktu CPU yang dibutuhkan oleh proses
        self.remaining_time = burst_time  # Waktu yang tersisa untuk menyelesaikan (digunakan dalam Round Robin)
        self.completion_time = 0  # Waktu ketika proses selesai dieksekusi
        self.waiting_time = 0  # Total waktu yang dihabiskan untuk menunggu
        self.turnaround_time = 0  # Total waktu dari kedatangan hingga penyelesaian

# Algoritma penjadwalan First-Come, First-Served (FCFS)
def fcfs_scheduling(processes):
    current_time = 0
    schedule = []
    
    # Urutkan proses berdasarkan waktu kedatangan
    for process in sorted(processes, key=lambda p: p.arrival_time):
        # Jika ada jeda antara proses, majukan waktu saat ini
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        
        # Hitung waktu untuk proses saat ini
        process.completion_time = current_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        
        # Tambahkan proses ke jadwal
        schedule.append((process.pid, current_time, process.completion_time))
        current_time = process.completion_time

    return processes, schedule

# Algoritma penjadwalan Round Robin
def round_robin_scheduling(processes, quantum):
    ready_queue = []  
    time = 0
    completed = 0
    schedule = []
    
    # Urutkan proses berdasarkan waktu kedatangan
    processes = sorted(processes, key=lambda p: p.arrival_time)
    
    while completed < len(processes):
        # Tambahkan proses yang baru tiba ke antrian siap
        for process in processes:
            if process.arrival_time == time and process.remaining_time > 0:
                ready_queue.append(process)
        
        if ready_queue:
            # Mengambil proses dari depan antrian (index 0)
            current_process = ready_queue.pop(0) 
            start_time = time
            
            # Proses dieksekusi selama waktu quantum atau hingga selesai
            if current_process.remaining_time <= quantum:
                time += current_process.remaining_time
                current_process.remaining_time = 0
                completed += 1
                
                # Hitung waktu untuk proses yang telah selesai
                current_process.completion_time = time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            else:
                time += quantum
                current_process.remaining_time -= quantum
                
                # Tambahkan proses yang baru tiba ke antrian siap
                for process in processes:
                    if process.arrival_time > start_time and process.arrival_time <= time and process.remaining_time > 0:
                        ready_queue.append(process)
                
                # Kembalikan proses saat ini ke antrian
                ready_queue.append(current_process)
            
            # Tambahkan eksekusi ke jadwal
            schedule.append((current_process.pid, start_time, time))
        else:
            # Jika tidak ada proses yang siap, majukan waktu
            time += 1
    
    return processes, schedule

class SchedulerGUI:
    def __init__(self, master):
        self.master = master  
        master.title("PROGRAM SISOP") 
        master.geometry("800x600")  # Ukuran jendela

        # Membuat frame utama dengan padding
        self.mainframe = ttk.Frame(master, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        master.columnconfigure(0, weight=1)  # Memungkinkan kolom untuk meregang
        master.rowconfigure(0, weight=1)  # Memungkinkan baris untuk meregang

        self.algorithm_var = tk.StringVar(value="FCFS")  # Variabel untuk menyimpan pilihan algoritma
        self.setup_algorithm_selection()  # Menyiapkan pemilihan algoritma
        self.setup_quantum_input()  # Menyiapkan input quantum
        self.setup_process_input()  # Menyiapkan input proses
        self.setup_run_button()  # Menyiapkan tombol run
        self.setup_reset_button()  # Menyiapkan tombol reset
        self.setup_canvas()  # Menyiapkan canvas untuk diagram Gantt
        self.setup_result_text()  # Menyiapkan area teks untuk hasil

    def setup_algorithm_selection(self):
        # Label untuk pemilihan algoritma
        ttk.Label(self.mainframe, text="Algorithm:").grid(column=1, row=1, sticky=tk.W)
        # Radio button untuk FCFS
        ttk.Radiobutton(self.mainframe, text="FCFS", variable=self.algorithm_var, value="FCFS").grid(column=2, row=1, sticky=tk.W)
        # Radio button untuk Round Robin
        ttk.Radiobutton(self.mainframe, text="Round Robin", variable=self.algorithm_var, value="RR").grid(column=3, row=1, sticky=tk.W)

    def setup_quantum_input(self):
        # Label untuk input quantum
        self.quantum_label = ttk.Label(self.mainframe, text="Quantum:")
        self.quantum_label.grid(column=1, row=2, sticky=tk.W)
        # Entry untuk input quantum
        self.quantum_entry = ttk.Entry(self.mainframe, width=7)
        self.quantum_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))
        self.quantum_entry.insert(0, "2")  # Mengatur nilai default quantum
        
        # Menambahkan trace pada variabel algoritma untuk mengubah visibilitas quantum
        self.algorithm_var.trace("w", self.toggle_quantum_visibility)
        self.toggle_quantum_visibility()  # Memanggil fungsi untuk mengatur visibilitas awal

    def toggle_quantum_visibility(self, *args):
        # Menampilkan atau menyembunyikan input quantum berdasarkan algoritma yang dipilih
        if self.algorithm_var.get() == "RR":
            self.quantum_label.grid()
            self.quantum_entry.grid()
        else:
            self.quantum_label.grid_remove()
            self.quantum_entry.grid_remove()

    def setup_process_input(self):
        # Membuat frame untuk input proses
        self.process_frame = ttk.LabelFrame(self.mainframe, text="Process Input", padding="10 10 10 10")
        self.process_frame.grid(column=1, row=3, columnspan=3, sticky=(tk.W, tk.E))
        self.mainframe.columnconfigure(1, weight=1)

        # Label untuk kolom input proses
        ttk.Label(self.process_frame, text="PID").grid(column=1, row=1, sticky=tk.W)
        ttk.Label(self.process_frame, text="Arrival Time").grid(column=2, row=1, sticky=tk.W)
        ttk.Label(self.process_frame, text="Burst Time").grid(column=3, row=1, sticky=tk.W)

        self.process_entries = []  # List untuk menyimpan entry proses
        self.add_process_row()  # Menambahkan baris input proses pertama

        # Tombol untuk menambah proses baru
        ttk.Button(self.process_frame, text="Add Process", command=self.add_process_row).grid(column=1, row=1000, columnspan=3, pady=10)

    def add_process_row(self):
        # Menentukan nomor baris baru
        row = len(self.process_entries) + 2
        entries = []
        # Membuat 3 entry untuk PID, Arrival Time, dan Burst Time
        for col in range(1, 4):
            entry = ttk.Entry(self.process_frame, width=10)
            entry.grid(column=col, row=row, padx=5, pady=2)
            entries.append(entry)
        self.process_entries.append(entries)  # Menambahkan entries ke list

    def setup_run_button(self):
        # Tombol untuk menjalankan simulasi
        ttk.Button(self.mainframe, text="Run Scheduling", command=self.run_scheduling).grid(column=1, row=4, columnspan=2, pady=10)

    def setup_reset_button(self):
        # Tombol untuk mereset simulator
        ttk.Button(self.mainframe, text="Reset", command=self.reset_scheduler).grid(column=3, row=4, pady=10)

    def setup_canvas(self):
        # Membuat frame untuk canvas
        self.canvas_frame = ttk.Frame(self.mainframe)
        self.canvas_frame.grid(column=1, row=5, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.mainframe.rowconfigure(5, weight=1)

        # Membuat canvas untuk menggambar Gantt Chart
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def setup_result_text(self):
        # Membuat area teks dengan scrollbar untuk menampilkan hasil
        self.result_text = scrolledtext.ScrolledText(self.mainframe, wrap=tk.WORD, width=50, height=10)
        self.result_text.grid(column=1, row=6, columnspan=3, sticky=(tk.W, tk.E))

    def draw_gantt_chart(self, schedule, title):
        self.canvas.delete("all")
        self.canvas.create_text(300, 20, text=title, font=("Arial", 16))
        
        y_start = 50
        height = 40
        x_scale = 20
        colors = ["#FF9999", "#66B2FF", "#99FF99", "#FFCC99", "#FF99CC", "#99CCFF"]
        
        max_time = max(end for _, _, end in schedule)
        canvas_width = (max_time * x_scale) + 100
        self.canvas.config(width=canvas_width, scrollregion=(0, 0, canvas_width, 200))
        
        for i, (pid, start, end) in enumerate(schedule):
            x1 = start * x_scale + 50
            x2 = end * x_scale + 50
            color = colors[i % len(colors)]
            
            self.canvas.create_rectangle(x1, y_start, x2, y_start + height, fill=color)
            self.canvas.create_text((x1 + x2) / 2, y_start + height / 2, text=f"P{pid}")
            self.canvas.create_text(x1, y_start + height + 10, text=str(start), anchor="n")
        
        self.canvas.create_text(canvas_width - 50, y_start + height + 10, text=str(max_time), anchor="n")

        # Add horizontal scrollbar
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(xscrollcommand=scrollbar.set)

    def run_scheduling(self):
        algorithm = self.algorithm_var.get()
        processes = []
        
        for entries in self.process_entries:
            try:
                pid = int(entries[0].get())
                arrival_time = int(entries[1].get())
                burst_time = int(entries[2].get())
                processes.append(Process(pid, arrival_time, burst_time))
            except ValueError:
                continue  # Skip invalid entries
        
        if not processes:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, "Error: No valid processes entered.")
            return
        
        if algorithm == "FCFS":
            completed_processes, schedule = fcfs_scheduling(processes)
            title = "FCFS Gantt Chart"
        else:  # Round Robin
            try:
                quantum = int(self.quantum_entry.get())
            except ValueError:
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert(tk.END, "Error: Invalid quantum time.")
                return
            completed_processes, schedule = round_robin_scheduling(processes, quantum)
            title = f"Round Robin Gantt Chart (Quantum: {quantum})"
        
        self.draw_gantt_chart(schedule, title)
        
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "PID\tArrival\tBurst\tCompletion\tWaiting\tTurnaround\n")
        total_waiting = 0
        total_turnaround = 0
        for p in completed_processes:
            self.result_text.insert(tk.END, f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.completion_time}\t\t{p.waiting_time}\t{p.turnaround_time}\n")
            total_waiting += p.waiting_time
            total_turnaround += p.turnaround_time
        
        avg_waiting = total_waiting / len(completed_processes)
        avg_turnaround = total_turnaround / len(completed_processes)
        self.result_text.insert(tk.END, f"\nAverage Waiting Time: {avg_waiting:.2f}")
        self.result_text.insert(tk.END, f"\nAverage Turnaround Time: {avg_turnaround:.2f}")

    def reset_scheduler(self):
        # Reset algorithm selection
        self.algorithm_var.set("FCFS")
        self.toggle_quantum_visibility()

        # Reset quantum input
        self.quantum_entry.delete(0, tk.END)
        self.quantum_entry.insert(0, "2")

        # Clear process entries
        for entries in self.process_entries:
            for entry in entries:
                entry.delete(0, tk.END)

        # Remove additional process rows
        while len(self.process_entries) > 1:
            for entry in self.process_entries[-1]:
                entry.destroy()
            self.process_entries.pop()

        # Clear canvas
        self.canvas.delete("all")

        # Clear result text
        self.result_text.delete('1.0', tk.END)

        # Reset canvas scrollregion
        self.canvas.config(scrollregion=(0, 0, 800, 200))


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()