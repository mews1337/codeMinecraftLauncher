import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from PIL import Image, ImageTk, ImageEnhance
import webbrowser
import threading
import minecraft_launcher_lib
import uuid
import time
import requests
import sys
import subprocess
import tempfile
from os.path import join

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

CONFIG_FILE = "launcher.config.json"
SERVER_URL = "https://online-launcher.onrender.com/ping"
LAUNCHER_SESSION_ID = str(uuid.getnode())
current_online_count = 1
CURRENT_VERSION = "1.0.0"

def update_online_counter():
    global current_online_count
    while True:
        try:
            response = requests.post(
                SERVER_URL, 
                json={"user_id": LAUNCHER_SESSION_ID}, 
                timeout=5
            )
            if response.status_code == 200:
                current_online_count = response.json().get("online", 1)
                root.after(0, update_online_label)
        except Exception:
            pass
        
        time.sleep(30)

def start_online_tracker():
    thread = threading.Thread(target=update_online_counter, daemon=True)
    thread.start()

default_config = {
    "language": "UA",
    "nickname": "Player",
    "version": "1.21.1",
    "ram": "4 GB",
    "loader": "Vanilla",
    "minecraft_dir": os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), ".minecraft")
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**default_config, **json.load(f)}
        except:
            return default_config
    return default_config

def save_config(config_data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)

config = load_config()
if not isinstance(config, dict):
    config = default_config

LANGS = {
    "UA": {
        "title": "Minecraft Launcher",
        "nickname": "Нікнейм:",
        "version": "Версія:",
        "play": "ГРАТИ",
        "status_ready": "Готовий до запуску",
        "server_info": "Версія лаунчера: v{version} | Статус сервера: Онлайн 🟢 | Гравців: {online}",
        "news": "📰 Новини",
        "folder": "📁 Папка",
        "help": "❓ Допомога",
        "settings_title": "⚙️ Налаштування",
        "ram_label": "Оперативна пам'ять (RAM):",
        "loader_label": "Тип запуску (Loader):",
        "dir_label": "Шлях до папки .minecraft:",
        "browse_btn": "Огляд...",
        "check_updates": "🔄 Перевірити оновлення",
        "save_btn": "💾 Зберегти",
        "back_btn": "🔤 Назад",
        "help_msg": "Minecraft Launcher v1.0.0\n\n• Для зміни нікнейму та версії скористайтеся полями на головному екрані.\n• Для налаштування ОЗП та типу запуску перейдіть у Налаштування.",
        "profile_title": "Профіль",
        "profile_msg": "Ваш нікнейм:",
        "downloading": "Завантаження/Перевірка файлів...",
        "version_installed": "Версію встановлено! Натисніть 'ГРАТИ'",
        "success_title": "Успіх",
        "success_msg": "Версію {version} успішно завантажено! Тепер ви можете її запустити.",
        "launching": "Запуск Minecraft...",
        "news_title": "📰 Останні новини сервера",
        "news_text": "📌 Оновлення v1.0.0:\n• Додано інтерактивний лічильник онлайну в реальному часі!\n• Оновлено дизайн Progress Bar та покращено стабільність.",
        "notif_title": "🔔 Сповіщення",
        "notif_text": "Ласкаво просимо до нашого лаунчера!\n\nНаразі важливих системних повідомлень немає.",
        "download_btn": "ЗАВАНТАЖИТИ",
    },
    "RU": {
        "title": "Minecraft Launcher",
        "nickname": "Никнейм:",
        "version": "Версия:",
        "play": "ИГРАТЬ",
        "status_ready": "Готов к запуску",
        "server_info": "Версия лаунчера: v{version} | Статус сервера: Онлайн 🟢 | Игроков: {online}",
        "news": "📰 Новости",
        "folder": "📁 Папка",
        "help": "❓ Помощь",
        "settings_title": "⚙️ Настройки",
        "ram_label": "Оперативная память (RAM):",
        "loader_label": "Тип запуска (Loader):",
        "dir_label": "Путь к папке .minecraft:",
        "browse_btn": "Обзор...",
        "check_updates": "🔄 Проверить обновления",
        "save_btn": "💾 Сохранить",
        "back_btn": "🔤 Назад",
        "help_msg": "Minecraft Launcher v1.0.0\n\n• Для смены никнейма и версии используйте поля на главном экране.\n• Для настройки ОЗУ и типа запуска перейдите в Настройки.",
        "profile_title": "Профиль",
        "profile_msg": "Ваш никнейм:",
        "downloading": "Загрузка/Проверка файлов...",
        "version_installed": "Версия установлена! Нажмите 'ИГРАТЬ'",
        "success_title": "Успех",
        "success_msg": "Версия {version} успешно загружена! Теперь вы можете её запустить.",
        "launching": "Запуск Minecraft...",
        "news_title": "📰 Последние новости сервера",
        "news_text": "📌 Обновление v1.0.0:\n• Добавлен интерактивный счетчик онлайна в реальном времени!\n• Обновлен дизайн Progress Bar и улучшена стабильность.",
        "notif_title": "🔔 Уведомления",
        "notif_text": "Добро пожаловать в наш лаунчер!\n\nНа данный момент важных системных сообщений нет.",
        "download_btn": "СКАЧАТЬ",
    },
    "EN": {
        "title": "Minecraft Launcher",
        "nickname": "Nickname:",
        "version": "Version:",
        "play": "PLAY",
        "status_ready": "Ready to play",
        "server_info": "Launcher version: v{version} | Server Status: Online 🟢 | Players: {online}",
        "news": "📰 News",
        "folder": "📁 Folder",
        "help": "❓ Help",
        "settings_title": "⚙️ Settings",
        "ram_label": "RAM Allocation:",
        "loader_label": "Loader Type:",
        "dir_label": ".minecraft Path:",
        "browse_btn": "Browse...",
        "check_updates": "🔄 Check for updates",
        "save_btn": "💾 Save",
        "back_btn": "🔤 Back",
        "help_msg": "Minecraft Launcher v1.0.0\n\n• Use home screen fields to change nickname/version.\n• Open Settings for RAM and Loader config.",
        "profile_title": "Profile",
        "profile_msg": "Your nickname:",
        "downloading": "Downloading/Checking files...",
        "version_installed": "Version ready! Click 'PLAY'",
        "success_title": "Success",
        "success_msg": "Version {version} downloaded successfully!",
        "launching": "Launching Minecraft...",
        "news_title": "📰 Server News",
        "news_text": "📌 Update v1.0.0:\n• Live online counter added!\n• Updated Progress Bar & stability improvements.",
        "notif_title": "🔔 Notifications",
        "notif_text": "Welcome to our launcher!\n\nNo critical system notifications currently.",
        "download_btn": "DOWNLOAD",
    }
}

def t(key):
    lang = config.get("language", "UA")
    return LANGS.get(lang, LANGS["UA"]).get(key, key)

def update_online_label():
    text_template = t("server_info")
    info_label.config(text=text_template.format(version=CURRENT_VERSION, online=current_online_count))

def change_language():
    current = config.get("language", "UA")
    new_lang = "EN" if current == "UA" else ("RU" if current == "EN" else "UA")
    config["language"] = new_lang
    save_config(config)
    lang_btn.config(text=f"🌐 {new_lang}")
    update_texts()

def check_selected_version_status():
    selected_ver = version_select.get() if 'version_select' in globals() else config.get("version", "1.21.1")
    mc_dir = config.get("minecraft_dir", "")

    installed_versions = []
    if mc_dir and os.path.exists(mc_dir):
        try:
            installed_versions = [v["id"] for v in minecraft_launcher_lib.utils.get_installed_versions(mc_dir)]
        except Exception:
            pass
    if selected_ver in installed_versions:
        play_button.config(text=t("play"))
    else:
        play_button.config(text=t("download_btn"))

def update_texts():
    title_label.config(text=t("title"))
    nik_label.config(text=t("nickname"))
    version_label.config(text=t("version"))
    
    check_selected_version_status()
    
    news_btn.config(text=t("news"))
    folder_btn.config(text=t("folder"))
    help_btn.config(text=t("help"))
    update_online_label()
    profile_btn.config(text=f"👤 {config.get('nickname', 'Player')}")

def open_notifications():
    messagebox.showinfo(
        t("notif_title"), 
        t("notif_text")
    )

def open_profile():
    new_nick = username_entry.get().strip()
    if new_nick:
        config['nickname'] = new_nick
        save_config(config)
        profile_btn.config(text=f"👤 {new_nick}")
    else:
        new_nick = config.get('nickname', 'Player')
    messagebox.showinfo(t("profile_title"), f"{t('profile_msg')} {new_nick}")

def open_minecraft_folder():
    mc_dir = config.get("minecraft_dir", "")
    if os.path.exists(mc_dir):
        os.startfile(mc_dir)
    else:
        messagebox.showerror("Помилка", f"Папку не знайдено:\n{mc_dir}")

def open_news():
    news_win = tk.Toplevel(root)
    news_win.title(t("news"))
    news_win.geometry("500x350")
    news_win.configure(bg="#222222")
    news_win.resizable(False, False)
    news_win.transient(root)
    news_win.grab_set()

    
    tk.Label(
        news_win,
        text=t("news_title"),
        font=("Segoe UI", 12, "bold"),
        fg="white",
        bg="#222222"
    ).pack(anchor="w", padx=20, pady=(15, 10))

    
    news_text = tk.Text(
        news_win,
        bg="#1a1a1a",
        fg="#d0d0d0",
        font=("Segoe UI", 9),
        wrap="word",
        bd=0,
        padx=10,
        pady=10
    )
    news_text.pack(fill="both", expand=True, padx=20, pady=(0, 15))
    
    news_text.insert("1.0", "Завантаження новин з сервера...")
    news_text.config(state="disabled")

    def fetch_news():
        try:
            
            response = requests.get("https://online-launcher.onrender.com/news", timeout=5)
            if response.status_code == 200:
                data = response.json()
                content = data.get("news", t("news_text"))
            else:
                content = t("news_text")
        except Exception:
        
            content = t("news_text")

        def update_ui():
            if news_win.winfo_exists():
                news_text.config(state="normal")
                news_text.delete("1.0", tk.END)
                news_text.insert("1.0", content)
                news_text.config(state="disabled")

        root.after(0, update_ui)

    threading.Thread(target=fetch_news, daemon=True).start()

    
    news_text.insert("1.0", t("news_text"))
    news_text.config(state="disabled") 

def open_help():
    messagebox.showinfo(
        t("help"),
        t("help_msg")
    )

def start_game_thread():
    thread = threading.Thread(target=launch_game, daemon=True)
    thread.start()

def get_ram_arguments():
    ram_str = config.get("ram", "4 GB")
    ram_gb = "".join(filter(str.isdigit, ram_str))
    if not ram_gb:
        ram_gb = "2"
    return [f"-Xmx{ram_gb}G", f"-Xms{ram_gb}G"]

def set_status(status: str):
    info_label.config(text=status)

current_max = 1

def set_max(new_max: int):
    global current_max
    current_max = new_max if new_max > 0 else 1

def set_progress(value: int):
    percent = int((value / current_max) * 100)

    progress_canvas.delete("all")

    progress_canvas.create_rectangle(0, 0, 320, 18, fill="#2b2b2b", outline="")

    fill_width = int((percent / 100) * 320)
    if fill_width > 0:
        progress_canvas.create_rectangle(0, 0, fill_width, 18, fill="#388E3C", outline="")

    progress_canvas.create_text(160, 9, text=f"{percent}%", fill="white", font=("Segoe UI", 9, "bold"))

    info_label.config(text=f"{t('downloading')} {percent}%")
    root.update_idletasks()
 
def launch_game():
    global mc_dir

    loader_widget = globals().get("loader_select") or globals().get("loader_combobox")
    version_widget = globals().get("version_select") or globals().get("version_combobox")
    nickname_widget = globals().get("username_entry") or globals().get("nickname_entry")

    selected_loader = loader_widget.get() if loader_widget else config.get("loader", "Vanilla")
    version = version_widget.get() if version_widget else config.get("version", "1.21.1")
    username = nickname_widget.get().strip() if nickname_widget else config.get("nickname", "Player")

    mc_dir = config.get("minecraft_dir", minecraft_launcher_lib.utils.get_minecraft_directory())

    if not username:
        messagebox.showwarning(t("title"), "Введіть нікнейм!")
        return

    
    java_executable = minecraft_launcher_lib.utils.get_java_executable() or "java"

    try:
        
        set_status(f"Перевірка та завантаження бібліотек {version}...")
        minecraft_launcher_lib.install.install_minecraft_version(version, mc_dir)

        
        if selected_loader == "Fabric":
            set_status("Перевірка / встановлення Fabric...")
            minecraft_launcher_lib.fabric.install_fabric(version, mc_dir)
        elif selected_loader == "Forge":
            set_status("Перевірка / встановлення Forge...")
            minecraft_launcher_lib.forge.install_forge_version(version, mc_dir)

        
        installed_versions = [v["id"] for v in minecraft_launcher_lib.utils.get_installed_versions(mc_dir)]
        target_version_id = version

        if selected_loader != "Vanilla":
            for inst_v in installed_versions:
                if version in inst_v and selected_loader.lower() in inst_v.lower():
                    target_version_id = inst_v
                    break

        
        set_status(f"{t('launching')} ({target_version_id})")
        ram_args = get_ram_arguments()

        options = {
            "username": username,
            "uuid": str(uuid.uuid4()),
            "token": "",
            "executablePath": java_executable,
            "jvmArguments": ["-Dfile.encoding=UTF-8"] + ram_args,
            "clientid": "",
            "xuid": ""
        }

        command = minecraft_launcher_lib.command.get_minecraft_command(target_version_id, mc_dir, options)

        print("Команда запуску:", " ".join(command))
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        
        set_status("Гра запускається...")

        def log_reader():
            for line in process.stdout:
                print(f"[Minecraft] {line.strip()}")

        threading.Thread(target=log_reader, daemon=True).start()

    except Exception as e:
        print(f"ПОМИЛКА ЗАПУСКУ: {e}")
        messagebox.showerror(t("title"), f"Не вдалося виконати операцію:\n{e}")
        set_status(t("status_ready"))
    finally:
        play_button.config(state="normal")

def open_settings():
    print("Відкриття налаштувань...")
    settings_win = tk.Toplevel(root)
    settings_win.title(t("settings_title"))
    settings_win.geometry("500x420")
    settings_win.configure(bg="#222222")
    settings_win.resizable(False, False)
    settings_win.transient(root)
    settings_win.grab_set()

    tk.Label(settings_win, text=t("ram_label"), font=("Segoe UI", 10), fg="#cccccc", bg="#222222").pack(anchor="w", padx=30, pady=(10, 2))
    
    current_ram_str = config.get("ram", "4 GB")
    try:
        init_ram_val = int("".join(filter(str.isdigit, current_ram_str)))
    except ValueError:
        init_ram_val = 4

    ram_val_label = tk.Label(settings_win, text=f"{init_ram_val} GB", font=("Segoe UI", 10, "bold"), fg="#388E3C", bg="#222222")
    ram_val_label.pack(anchor="w", padx=30)

    def on_ram_scale_change(val):
        ram_val_label.config(text=f"{int(float(val))} GB")

    ram_scale = tk.Scale(
        settings_win,
        from_=2,
        to=16,
        orient="horizontal",
        resolution=1,
        showvalue=False,
        bg="#222222",
        fg="#ffffff",
        troughcolor="#2b2b2b",
        activebackground="#388E3C",
        highlightthickness=0,
        bd=0,
        command=on_ram_scale_change
    )
    ram_scale.set(init_ram_val)
    ram_scale.pack(fill="x", padx=30, pady=(0, 10))

    
    tk.Label(settings_win, text=t("loader_label"), font=("Segoe UI", 10), fg="#cccccc", bg="#222222").pack(anchor="w", padx=30, pady=(10, 2))
    loader_var = tk.StringVar(value=config.get("loader", "Vanilla"))
    loader_combo = ttk.Combobox(settings_win, textvariable=loader_var, values=["Vanilla", "Fabric", "Forge", "Quilt", "NeoForge"], state="readonly", width=35)
    loader_combo.pack(padx=30)

    
    tk.Label(settings_win, text=t("dir_label"), font=("Segoe UI", 10), fg="#cccccc", bg="#222222").pack(anchor="w", padx=30, pady=(10, 2))
    dir_frame = tk.Frame(settings_win, bg="#222222")
    dir_frame.pack(fill="x", padx=30)

    dir_entry = tk.Entry(dir_frame, font=("Segoe UI", 9), bg="#2b2b2b", fg="white", insertbackground="white", relief="flat", bd=3)
    dir_entry.insert(0, config.get("minecraft_dir", ""))
    dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

    def browse_folder():
        selected_dir = filedialog.askdirectory(initialdir=dir_entry.get())
        if selected_dir:
            dir_entry.delete(0, tk.END)
            dir_entry.insert(0, selected_dir)

    browse_btn = tk.Button(dir_frame, text=t("browse_btn"), font=("Segoe UI", 8), fg="white", bg="#3c3c3c", activebackground="#4c4c4c", relief="flat", command=browse_folder)
    browse_btn.pack(side="right")

    
    update_btn = tk.Button(settings_win, text=t("check_updates"), font=("Segoe UI", 9), fg="white", bg="#2b2b2b", activebackground="#3c3c3c", relief="flat", command=lambda: threading.Thread(target=check_launcher_update, daemon=True).start())
    update_btn.pack(pady=15)

    
    btn_frame = tk.Frame(settings_win, bg="#222222")
    btn_frame.pack(side="bottom", fill="x", padx=30, pady=20)

    def save_and_close():
        selected_ram = ram_scale.get()
        config["ram"] = f"{selected_ram} GB"
        config["loader"] = loader_var.get()
        config["minecraft_dir"] = dir_entry.get()
        save_config(config)
        settings_win.destroy()

    save_btn = tk.Button(
        btn_frame, 
        text=t("save_btn"), 
        font=("Segoe UI", 10, "bold"), 
        fg="white", 
        bg="#388E3C", 
        activebackground="#4CAF50", 
        relief="flat", 
        padx=15, 
        pady=5, 
        command=save_and_close
    )
    save_btn.pack(side="right")

def start_game():
    nickname = username_entry.get()
    selected_ver = version_select.get()
    print(f"Запуск гри з нікнеймом: {nickname} та версією: {selected_ver}")


root = tk.Tk()
try:
    root.iconbitmap(resource_path("icon.ico"))
except Exception:
    pass
root.title("Minecraft Launcher TEST")
root.geometry("1024x600")
root.resizable(False, False)


style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", 
    fieldbackground="#2b2b2b", 
    background="#3c3c3c", 
    foreground="white",
    arrowcolor="white",
    selectbackground="#2b2b2b",
    selectforeground="white"
)
style.map("TCombobox",
    fieldbackground=[("readonly", "#2b2b2b")],
    selectbackground=[("readonly", "#2b2b2b")],
    selectforeground=[("readonly", "white")],
    foreground=[("readonly", "white")]
)


bg_image_path = resource_path("bg.jpg")

try:
    img = Image.open(bg_image_path)
    img = img.resize((1024, 600), Image.Resampling.LANCZOS)
    
    
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.5)  
    
    bg_photo = ImageTk.PhotoImage(img)
    print("Картинка 'bg.jpg' завантажена успішно!")
except Exception as e:
    print(f"Помилка завантаження 'bg.jpg': {e}")
    
    img = Image.new("RGB", (1024, 600), "#181818")
    bg_photo = ImageTk.PhotoImage(img)


canvas = tk.Canvas(root, width=1024, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)


canvas.create_image(0, 0, image=bg_photo, anchor="nw")
canvas.image = bg_photo  


canvas.create_image(0, 0, image=bg_photo, anchor="nw")

canvas.image = bg_photo 


top_frame = tk.Frame(root, bg="#2b2b2b")

lang_btn = tk.Button(top_frame, text=f"🌐 {config.get('language', 'UA')}", font=("Segoe UI", 9, "bold"), fg="white", bg="#2b2b2b", activebackground="#3c3c3c", relief="flat", cursor="hand2", padx=8, pady=3, command=change_language)
lang_btn.pack(side="left", padx=4)

notif_btn = tk.Button(top_frame, text="🔔", font=("Segoe UI", 9, "bold"), fg="white", bg="#2b2b2b", activebackground="#3c3c3c", relief="flat", cursor="hand2", padx=8, pady=3, command=open_notifications)
notif_btn.pack(side="left", padx=4)

settings_top_btn = tk.Button(top_frame, text="⚙", font=("Segoe UI", 9, "bold"), fg="white", bg="#2b2b2b", activebackground="#3c3c3c", relief="flat", cursor="hand2", padx=8, pady=3, command=open_settings)
settings_top_btn.pack(side="left", padx=4)

profile_btn = tk.Button(top_frame, text=f"👤 {config.get('nickname', 'Player')}", font=("Segoe UI", 9, "bold"), fg="white", bg="#2b2b2b", activebackground="#3c3c3c", relief="flat", cursor="hand2", padx=8, pady=3, command=open_profile)
profile_btn.pack(side="left", padx=4)

canvas.create_window(1004, 20, window=top_frame, anchor="ne")


title_label = tk.Label(root, text=t("title"), font=("Segoe UI", 20, "bold"), fg="#FFFFFF", bg="#181818")
canvas.create_window(512, 45, window=title_label, anchor="n")


nik_label = tk.Label(root, text=t("nickname"), font=("Segoe UI", 10, "bold"), fg="#ABABAB", bg="#181818")
canvas.create_window(512, 80, window=nik_label, anchor="n")

username_entry = tk.Entry(root, font=("Segoe UI", 11), width=20, bg="#2b2b2b", fg="white", insertbackground="white", relief="flat")
username_entry.insert(0, config.get("nickname", "Player"))
canvas.create_window(512, 100, window=username_entry, anchor="n")


try:
    all_v = minecraft_launcher_lib.utils.get_version_list()
    versions = [v["id"] for v in all_v if v["type"] == "release"]
except Exception:
    versions = ["1.21.1", "1.20.1", "1.19.4", "1.16.5", "1.12.2"]


loader_label = tk.Label(root, text="Loader:", font=("Segoe UI", 10, "bold"), fg="#ABABAB", bg="#181818")
canvas.create_window(512, 140, window=loader_label, anchor="n")

loaders = ["Vanilla", "Fabric", "Forge", "OptiFine"]
loader_select = ttk.Combobox(root, values=loaders, state="readonly", width=18, font=("Segoe UI", 11))
loader_select.set(config.get("loader", "Vanilla"))
canvas.create_window(512, 160, window=loader_select, anchor="n")


version_label = tk.Label(root, text=t("version"), font=("Segoe UI", 10, "bold"), fg="#ABABAB", bg="#181818")
canvas.create_window(512, 200, window=version_label, anchor="n")

version_select = ttk.Combobox(root, values=versions, state="readonly", width=18, font=("Segoe UI", 11))
version_select.set(config.get("version", "1.21.1"))
canvas.create_window(512, 220, window=version_select, anchor="n")


def auto_save_main_options(event=None):
    config["nickname"] = username_entry.get().strip()
    config["loader"] = loader_select.get()
    config["version"] = version_select.get()
    save_config(config)

loader_select.bind("<<ComboboxSelected>>", auto_save_main_options)
version_select.bind("<<ComboboxSelected>>", auto_save_main_options)
username_entry.bind("<FocusOut>", auto_save_main_options)


play_button = tk.Button(
    root,
    text=t("play"),
    command=start_game_thread,
    bg="#388E3C",
    activebackground="#4CAF50",
    fg="white",
    font=("Segoe UI", 13, "bold"),
    width=18,
    pady=6,
    relief="flat",
    cursor="hand2"
)
canvas.create_window(512, 270, window=play_button, anchor="n")


bottom_frame = tk.Frame(root, bg="#2b2b2b")

news_btn = tk.Button(bottom_frame, text=t("news"), font=("Segoe UI", 9, "bold"), fg="#D0D0D0", bg="#2b2b2b", activebackground="#3c3c3c", relief="flat", cursor="hand2", padx=10, pady=5, command=open_news)
news_btn.pack(side="left", padx=2)

folder_btn = tk.Button(bottom_frame, text=t("folder"), font=("Segoe UI", 9, "bold"), fg="#D0D0D0", bg="#2b2b2b", activebackground="#3c3c3c", relief="flat", cursor="hand2", padx=10, pady=5, command=open_minecraft_folder)
folder_btn.pack(side="left", padx=2)

help_btn = tk.Button(bottom_frame, text=t("help"), font=("Segoe UI", 9, "bold"), fg="#D0D0D0", bg="#2b2b2b", activebackground="#3c3c3c", relief="flat", cursor="hand2", padx=10, pady=5, command=open_help)
help_btn.pack(side="left", padx=2)

canvas.create_window(1004, 570, window=bottom_frame, anchor="se")

progress_canvas = tk.Canvas(root, width=320, height=18, bg="#1a1a1a", highlightthickness=0)


info_label = tk.Label(
    root,
    text=t("server_info"),
    font=("Segoe UI", 9),
    fg="#888888",
    bg="#181818"
)
canvas.create_window(20, 570, window=info_label, anchor="sw")

def show_update_dialog(latest_version):
    answer = messagebox.askyesno(
        "🚀 Оновлення лаунчера", 
        f"Вийшла нова версія лаунчера (v{latest_version})!\nПоточна версія: v{CURRENT_VERSION}\n\nБажаєте оновити зараз?"
    )
    if answer:
        try:
            update_url = "https://online-launcher.onrender.com/download"
            print("Завантаження оновлення...")
            response = requests.get(update_url, stream=True)
            if response.status_code == 200:
                temp_dir = tempfile.gettempdir()
                new_exe_path = os.path.join(temp_dir, "launcher_update.exe")
                
                with open(new_exe_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                bat_path = os.path.join(temp_dir, "update.bat")
                current_exe = sys.executable 
                
                bat_content = f"""
                @echo off
                timeout /t 2 /nobreak > nul
                del /f /q "{current_exe}"
                move /y "{new_exe_path}" "{current_exe}"
                start "" "{current_exe}"
                del "%~f0"
                """
                
                with open(bat_path, "w", encoding="cp1251") as bat_file:
                    bat_file.write(bat_content)
                
                subprocess.Popen(bat_path, shell=True)
                sys.exit()
            else:
                messagebox.showerror("Помилка", "Не вдалося завантажити файл оновлення з сервера.")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка під час оновлення: {e}")

def check_launcher_update():
    print("-> Запуск перевірки оновлень...")
    latest_version = "1.0.0"
    try:
        response = requests.get("https://online-launcher.onrender.com/version", timeout=3)
        if response.status_code == 200:
            latest_version = response.json().get("version", "1.0.0")
    except Exception:
        pass

    if latest_version != CURRENT_VERSION:
        root.after(0, lambda: show_update_dialog(latest_version))

start_online_tracker()
threading.Thread(target=check_launcher_update, daemon=True).start()

check_selected_version_status()

root.mainloop()