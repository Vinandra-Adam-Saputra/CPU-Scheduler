# CPU Scheduler

## Deskripsi
CPU Scheduler adalah aplikasi berbasis Python yang memungkinkan pengguna untuk mensimulasikan algoritma penjadwalan proses First-Come, First-Served (FCFS) dan Round Robin (RR) dengan antarmuka grafis yang interaktif menggunakan Tkinter. Aplikasi ini memvisualisasikan eksekusi proses menggunakan diagram Gantt.

## Fitur
- **Dukungan Algoritma Penjadwalan**:
  - First-Come, First-Served (FCFS)
  - Round Robin (RR) dengan input quantum
- **Antarmuka Grafis Interaktif**:
  - Input data proses secara dinamis
  - Pemilihan algoritma penjadwalan
  - Tampilan hasil dalam bentuk tabel dan diagram Gantt
  - Kemampuan reset input
  
## Instalasi dan Penggunaan
1. **Clone repositori ini**:
   ```bash
   git clone https://github.com/username/repository.git
   cd repository
   ```
2. **Jalankan skrip Python**:
   ```bash
   python scheduler_gui.py
   ```
3. **Gunakan antarmuka**:
   - Tambahkan proses dengan mengisi PID, waktu kedatangan, dan burst time.
   - Pilih algoritma penjadwalan.
   - Jika memilih Round Robin, tentukan nilai quantum.
   - Klik "Run Scheduling" untuk melihat hasil simulasi.
   - Hasil akan ditampilkan dalam tabel serta diagram Gantt.
   - Klik "Reset" untuk menghapus semua input.

## Struktur Proyek
```
repository/
│── cpu_scheduler.py  # Skrip utama dengan antarmuka GUI
│── README.md         # Dokumentasi proyek
```

## Lisensi
[LICENSE]

## Kontribusi
Kontribusi sangat diterima! Silakan lakukan pull request atau laporkan issue jika menemukan bug atau memiliki saran perbaikan.

