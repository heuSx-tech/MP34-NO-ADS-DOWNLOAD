import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# FFmpeg yolunu ekle (Gerekiyorsa değiştir)
os.environ["PATH"] += os.pathsep + r"C:\mp34\bin"

# İndirilecek klasörü belirlemek için global değişken
download_folder = os.path.expanduser("~/Desktop/oç")

# Klasör yoksa oluştur
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Koyu mod ve açık mod arasındaki renkleri saklayan değişkenler
light_mode = {
    'bg': 'white', 'fg': 'black', 'button_bg': 'lightgrey', 'button_fg': 'black', 'progress_bg': 'lightblue'
}

dark_mode = {
    'bg': 'black', 'fg': 'white', 'button_bg': 'grey', 'button_fg': 'white', 'progress_bg': 'darkgrey'
}

current_mode = light_mode  # Başlangıçta açık modda başlasın

def select_folder():
    global download_folder  # Global olarak kullanacağımızı belirtiyoruz
    folder = filedialog.askdirectory(initialdir=download_folder, title="İndirme Klasörünü Seç")
    if folder:
        download_folder = folder
        folder_label.config(text=f"Klasör: {download_folder}")

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Hata", "Lütfen bir YouTube linki girin!")
        return

    status_label.config(text="İndiriliyor...", fg="blue")
    root.update_idletasks()

    # Seçilen formatı kontrol et (video veya ses)
    is_audio = audio_var.get()
    resolution = resolution_combobox.get()
    audio_quality = audio_quality_combobox.get()

    # Ses veya video seçeneklerine göre format ayarlarını belirle
    if is_audio:
        # Ses kalitesine göre uygun format seçimi
        if audio_quality == 'Yüksek':
            format_selection = 'bestaudio[ext=m4a]'
        elif audio_quality == 'Orta':
            format_selection = 'bestaudio[ext=mp3]/best'
        else:  # Düşük
            format_selection = 'bestaudio[ext=opus]'
    else:
        # Video indirme seçenekleri
        if resolution == 'Yüksek':
            format_selection = 'bestvideo+bestaudio/best'
        elif resolution == 'Orta':
            format_selection = 'bestvideo[height<=720]+bestaudio/best'
        else:  # Düşük
            format_selection = 'bestvideo[height<=480]+bestaudio/best'

    # YDL seçenekleri
    ydl_opts = {
        'format': format_selection,  # Ses veya video formatına göre seçim
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4' if not is_audio else 'mp3',
        'progress_hooks': [progress_hook],  # İlerleme durumu
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_label.config(text="İndirme tamamlandı!", fg="green")
        messagebox.showinfo("Tamamlandı", "İndirme başarıyla tamamlandı.")
    except Exception as e:
        messagebox.showerror("Hata", f"İndirme başarısız: {e}")
        status_label.config(text="İndirme başarısız!", fg="red")

# İlerleme durumu fonksiyonu
def progress_hook(d):
    if d['status'] == 'downloading':
        total_size = d.get('total_bytes', None)
        downloaded = d.get('downloaded_bytes', None)
        download_speed = d.get('speed', 0)  # İndirme hızı (bytes/saniye)
        
        if total_size and downloaded:
            percent = (downloaded / total_size) * 100
            progress_var.set(percent)
            progress_bar.update()

            # Kalan süreyi hesapla (total_size - downloaded) / download_speed
            if download_speed > 0:
                remaining_bytes = total_size - downloaded
                remaining_time = remaining_bytes / download_speed  # saniye cinsinden

                # Kalan süreyi saat:dakika:saniye formatında hesapla
                remaining_minutes, remaining_seconds = divmod(remaining_time, 60)
                remaining_hours, remaining_minutes = divmod(remaining_minutes, 60)
                time_label.config(text=f"Kalan Süre: {int(remaining_hours)}:{int(remaining_minutes)}:{int(remaining_seconds)}")

# Modu değiştirme fonksiyonu
def toggle_mode():
    global current_mode
    if current_mode == light_mode:
        current_mode = dark_mode
    else:
        current_mode = light_mode

    # Renkleri güncelle
    root.config(bg=current_mode['bg'])
    title_label.config(bg=current_mode['bg'], fg=current_mode['fg'])
    url_entry.config(bg=current_mode['bg'], fg=current_mode['fg'])
    folder_button.config(bg=current_mode['button_bg'], fg=current_mode['button_fg'])
    download_button.config(bg=current_mode['button_bg'], fg=current_mode['button_fg'])
    status_label.config(bg=current_mode['bg'], fg=current_mode['fg'])
    progress_bar.config(style='TProgressbar', length=400)

    # Kalan süre etiketini güncelle
    time_label.config(bg=current_mode['bg'], fg=current_mode['fg'])

    # Progress bar stilini güncelle
    style = ttk.Style()
    style.configure("TProgressbar", thickness=20, background=current_mode['progress_bg'])

# Tkinter Arayüzü
root = tk.Tk()
root.title("YouTube Video ve Ses İndirici")
root.geometry("500x500")  # Sabit boyut (genişlik x yükseklik)
root.resizable(False, False)  # Pencereyi sabitle

# Başlık
title_label = tk.Label(root, text="YouTube Video ve Ses İndirici", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

# Video linki etiketi ve giriş kutusu
tk.Label(root, text="YouTube Linki:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Ses veya Video seçenekleri
audio_var = tk.BooleanVar()
audio_check = tk.Checkbutton(root, text="Sadece Ses İndir", variable=audio_var)
audio_check.pack(pady=5)

# Çözünürlük seçenekleri
tk.Label(root, text="Çözünürlük Seçin:").pack(pady=5)
resolution_combobox = ttk.Combobox(root, values=["Düşük", "Orta", "Yüksek"])
resolution_combobox.set("Yüksek")  # Varsayılan çözünürlük
resolution_combobox.pack(pady=5)

# Ses kalitesi seçenekleri
audio_quality_label = tk.Label(root, text="Ses Kalitesi Seçin:")
audio_quality_label.pack(pady=5)

audio_quality_combobox = ttk.Combobox(root, values=["Düşük", "Orta", "Yüksek"])
audio_quality_combobox.set("Yüksek")  # Varsayılan ses kalitesi
audio_quality_combobox.pack(pady=5)

# Klasör seçme butonu
folder_button = tk.Button(root, text="Klasör Seç", command=select_folder)
folder_button.pack(pady=5)

# Klasör yolu etiketi
folder_label = tk.Label(root, text=f"Klasör: {download_folder}", fg="blue")
folder_label.pack(pady=5)

# İndir butonu
download_button = tk.Button(root, text="İndir", command=download_video)
download_button.pack(pady=10)

# Durum etiket
status_label = tk.Label(root, text="", fg="black")
status_label.pack(pady=5)

# İlerleme çubuğu
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
progress_bar.pack(pady=10)

# Kalan süre etiket
time_label = tk.Label(root, text="Kalan Süre: 0:00:00", fg="black")
time_label.pack(pady=5)

# Koyu/açık mod butonu
mode_button = tk.Button(root, text="Koyu/Açık Mod", command=toggle_mode)
mode_button.pack(pady=10)

root.mainloop()
