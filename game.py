import tkinter as tk
from tkinter import messagebox, ttk
import random, json, os

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

SAVE_FILE = "savegame.json"
SCORES_FILE = "scores.json"

# ============ КАТАЛОГ КОМПЛЕКТУЮЩИХ ============
MOTHERBOARDS = [
    {"id": "mb_budget", "name": "ASRock H510M",  "socket": "LGA1200", "ram": "DDR4", "max_gpu": 1, "price": 2500,  "power": 30},
    {"id": "mb_mid",    "name": "MSI B550M",     "socket": "AM4",     "ram": "DDR4", "max_gpu": 2, "price": 5500,  "power": 35},
    {"id": "mb_high",   "name": "ASUS Z690",     "socket": "LGA1700", "ram": "DDR5", "max_gpu": 3, "price": 12000, "power": 40},
    {"id": "mb_mining", "name": "Mining B250",   "socket": "LGA1200", "ram": "DDR4", "max_gpu": 6, "price": 15000, "power": 45},
]

CPUS = [
    {"id": "cpu_cel",    "name": "Celeron G5905",  "socket": "LGA1200", "price": 500,   "power": 58},
    {"id": "cpu_ryzen3", "name": "Ryzen 3 3200G",  "socket": "AM4",     "price": 4000,  "power": 65},
    {"id": "cpu_ryzen5", "name": "Ryzen 5 5600",   "socket": "AM4",     "price": 8000,  "power": 65},
    {"id": "cpu_i5",     "name": "Core i5-12400",  "socket": "LGA1700", "price": 12000, "power": 65},
]

RAMS = [
    {"id": "ram_ddr4_8",  "name": "DDR4 8GB",  "type": "DDR4", "price": 1550,  "power": 5},
    {"id": "ram_ddr4_16", "name": "DDR4 16GB", "type": "DDR4", "price": 3000,  "power": 8},
    {"id": "ram_ddr5_16", "name": "DDR5 16GB", "type": "DDR5", "price": 6000,  "power": 10},
    {"id": "ram_ddr5_32", "name": "DDR5 32GB", "type": "DDR5", "price": 12000, "power": 15},
]

PSUS = [
    {"id": "psu_500",  "name": "500W Bronze",     "wattage": 500,  "price": 3500},
    {"id": "psu_750",  "name": "750W Gold",       "wattage": 750,  "price": 6500},
    {"id": "psu_1000", "name": "1000W Gold",      "wattage": 1000, "price": 12000},
    {"id": "psu_1200", "name": "1200W Platinum",  "wattage": 1200, "price": 18000},
    {"id": "psu_1500", "name": "1500W Titanium",  "wattage": 1500, "price": 25000},
]

GPUS = [
    {"id": "gpu_1660", "name": "GTX 1660 Super", "hashrate": 30,  "price": 15000,  "power": 125},
    {"id": "gpu_3060", "name": "RTX 3060",       "hashrate": 35,  "price": 25000,  "power": 130},
    {"id": "gpu_4060", "name": "RTX 4060",       "hashrate": 33,  "price": 31050,  "power": 115},
    {"id": "gpu_4070", "name": "RTX 4070",       "hashrate": 65,  "price": 55000,  "power": 200},
    {"id": "gpu_4090", "name": "RTX 4090",       "hashrate": 130, "price": 150000, "power": 450},
]

# ============ ЗВУК И ИКОНКА ============

def click_sound():
    if HAS_SOUND:
        try: winsound.Beep(800, 40)
        except Exception: pass

def error_sound():
    if HAS_SOUND:
        try: winsound.Beep(300, 120)
        except Exception: pass

def make_icon(root):
    icon = tk.PhotoImage(width=32, height=32)
    icon.put("#1e1e2e", to=(0, 0, 32, 32))
    icon.put("#89b4fa", to=(4, 6, 28, 22))
    icon.put("#181825", to=(7, 9, 25, 19))
    icon.put("#89b4fa", to=(13, 22, 19, 25))
    icon.put("#89b4fa", to=(9, 25, 23, 27))
    icon.put("#a6e3a1", to=(9, 11, 15, 12))
    icon.put("#f9e2af", to=(9, 14, 20, 15))
    icon.put("#f38ba8", to=(9, 17, 13, 18))
    root.iconphoto(True, icon)


class StartMenu:
    def __init__(self, root, on_start, on_continue, on_scores):
        self.root = root
        self.frame = tk.Frame(root, bg="#1e1e2e")
        self.frame.pack(fill="both", expand=True)
        tk.Label(self.frame, text="КОМПЬЮТЕРЩИК 2.0", font=("Consolas", 28, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=(60, 5))
        tk.Label(self.frame, text="Сборка фермы: совместимость, мощность, реальные цены",
                 font=("Consolas", 12), bg="#1e1e2e", fg="#a6adc8").pack(pady=(0, 25))

        has_save = os.path.exists(SAVE_FILE)
        tk.Button(self.frame, text="НОВАЯ ИГРА", command=on_start, bg="#89b4fa", fg="#1e1e2e",
                  font=("Consolas", 14, "bold"), relief="flat", padx=30, pady=12, cursor="hand2").pack(pady=6)
        btn = tk.Button(self.frame, text="ПРОДОЛЖИТЬ", command=on_continue, bg="#a6e3a1", fg="#1e1e2e",
                        font=("Consolas", 14, "bold"), relief="flat", padx=30, pady=12, cursor="hand2")
        if has_save:
            btn.pack(pady=6)
        else:
            btn.config(state="disabled", bg="#313244", fg="#585b70"); btn.pack(pady=6)
        tk.Button(self.frame, text="РЕКОРДЫ", command=on_scores, bg="#f9e2af", fg="#1e1e2e",
                  font=("Consolas", 13, "bold"), relief="flat", padx=30, pady=10, cursor="hand2").pack(pady=6)
        tk.Button(self.frame, text="Выход", command=root.quit, bg="#313244", fg="#cdd6f4",
                  font=("Consolas", 11), relief="flat", padx=20, pady=6, cursor="hand2").pack(pady=10)


class GameGUI:
    def __init__(self, root, load=False):
        self.root = root
        self.root.title("Компьютерщик 2.0")
        self.root.geometry("1000x900")
        self.root.configure(bg="#1e1e2e")
        self.root.minsize(900, 800)

        self.bg = "#1e1e2e"; self.fg = "#cdd6f4"; self.accent = "#89b4fa"
        self.green = "#a6e3a1"; self.red = "#f38ba8"; self.yellow = "#f9e2af"
        self.surface = "#313244"; self.dark = "#181825"

        self.init_state()
        if load: self.load_game()

        self.anim_progress = 1.0
        self.anim_target = 1.0
        self.shop_win = None

        self.build_ui()
        self.update_ui()
        self.animate_chart()
        self.log_msg(f"--- ДЕНЬ {self.day} ---")
        self.log_msg("Открой МАГАЗИН и собери ферму: плата, CPU, RAM, БП, GPU.")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def init_state(self):
        self.day = 1
        self.money = 15000
        self.energy = 100
        self.stress = 20
        self.crypto_balance = 0.0
        self.btc_price_rub = 5386778.85
        self.price_history = [self.btc_price_rub] * 14
        self.trend = 0.0
        self.volatility = 0.02
        self.neighbor_patience = 100
        self.balcony = False
        self.garage = False
        self.wiring_ok = True
        self.legal = False
        self.tax_risk = 0
        self.ended = False
        self.mb = None
        self.cpu = None
        self.ram = None
        self.psu = None
        self.gpus = []
        self.hashrate = 0.0

    def on_close(self):
        if not self.ended:
            self.save_game()
        self.root.destroy()

    # ---- Сохранение ----
    def save_game(self):
        data = {k: v for k, v in self.__dict__.items()
                if k not in ("root", "bg", "fg", "accent", "green", "red", "yellow",
                             "surface", "dark", "anim_progress", "anim_target", "log",
                             "chart", "bar_energy", "bar_stress", "bar_neighbor",
                             "lbl_day", "lbl_money", "lbl_energy", "lbl_stress",
                             "lbl_farm", "lbl_crypto", "shop_win")}
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_msg(f"Ошибка сохранения: {e}")

    def load_game(self):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.items():
                if hasattr(self, k): setattr(self, k, v)
            self.hashrate = sum(g["hashrate"] for g in self.gpus)
        except Exception as e:
            print("Ошибка загрузки:", e)

    # ---- Расчёты ----
    def calc_power(self, mb=None, cpu=None, ram=None, extra_gpu=None):
        power = 20
        m = mb if mb is not None else self.mb
        c = cpu if cpu is not None else self.cpu
        r = ram if ram is not None else self.ram
        if m: power += m["power"]
        if c: power += c["power"]
        if r: power += r["power"]
        for g in self.gpus: power += g["power"]
        if extra_gpu: power += extra_gpu["power"]
        return power

    def check_compatibility(self, cat, item):
        if cat == "mb":
            if self.cpu and self.cpu["socket"] != item["socket"]:
                return False, f"CPU {self.cpu['socket']} ≠ {item['socket']}"
            if self.ram and self.ram["type"] != item["ram"]:
                return False, f"RAM {self.ram['type']} ≠ {item['ram']}"
            if len(self.gpus) > item["max_gpu"]:
                return False, f"Карт {len(self.gpus)} > слотов {item['max_gpu']}"
            if self.psu:
                p = self.calc_power(mb=item)
                if p > self.psu["wattage"] * 0.85:
                    return False, f"БП {self.psu['wattage']}W не потянет {p}W"
        elif cat == "cpu":
            if not self.mb: return False, "Сначала купите плату"
            if self.mb["socket"] != item["socket"]:
                return False, f"Сокет {item['socket']} ≠ {self.mb['socket']}"
            if self.psu:
                p = self.calc_power(cpu=item)
                if p > self.psu["wattage"] * 0.85:
                    return False, f"БП не потянет {p}W"
        elif cat == "ram":
            if not self.mb: return False, "Сначала купите плату"
            if self.mb["ram"] != item["type"]:
                return False, f"Плата {self.mb['ram']} ≠ {item['type']}"
            if self.psu:
                p = self.calc_power(ram=item)
                if p > self.psu["wattage"] * 0.85:
                    return False, f"БП не потянет {p}W"
        elif cat == "psu":
            p = self.calc_power()
            if p > item["wattage"] * 0.85:
                return False, f"Нужно ≥{p/0.85:.0f}W"
        elif cat == "gpu":
            if not self.mb: return False, "Сначала купите плату"
            if len(self.gpus) >= self.mb["max_gpu"]:
                return False, f"Слотов: {self.mb['max_gpu']}, занято: {len(self.gpus)}"
            if not self.psu: return False, "Сначала купите БП"
            p = self.calc_power(extra_gpu=item)
            if p > self.psu["wattage"] * 0.85:
                return False, f"БП не потянет ({p}W)"
        return True, ""

    # ---- Покупки ----
    def buy_component(self, cat, item):
        compat, reason = self.check_compatibility(cat, item)
        if not compat:
            error_sound(); self.log_msg(f"Нельзя: {reason}"); return
        if self.money < item["price"]:
            error_sound(); self.log_msg("Мало денег"); return
        self.money -= item["price"]
        if cat in ("mb", "cpu", "ram", "psu"):
            old = getattr(self, cat)
            if old:
                refund = old["price"] // 2
                self.money += refund
                self.log_msg(f"Старый {old['name']} продан за {refund}₽")
            setattr(self, cat, item)
        elif cat == "gpu":
            self.gpus.append(item)
        self.hashrate = sum(g["hashrate"] for g in self.gpus)
        self.log_msg(f"Куплено: {item['name']} ({item['price']}₽)")
        self.update_ui()
        self.build_shop()

    def sell_component(self, cat):
        item = getattr(self, cat) if cat in ("mb", "cpu", "ram", "psu") else None
        if not item: return
        refund = item["price"] // 2
        self.money += refund
        setattr(self, cat, None)
        self.log_msg(f"{item['name']} продан за {refund}₽")
        self.update_ui()
        self.build_shop()

    def sell_gpu(self, gpu):
        if gpu in self.gpus:
            refund = gpu["price"] // 2
            self.gpus.remove(gpu)
            self.money += refund
            self.hashrate = sum(g["hashrate"] for g in self.gpus)
            self.log_msg(f"{gpu['name']} продан за {refund}₽")
            self.update_ui()
            self.build_shop()

    # ---- UI ----
    def build_ui(self):
        top = tk.Frame(self.root, bg=self.bg)
        top.pack(fill="x", padx=12, pady=6)
        self.lbl_day = tk.Label(top, text="", fg=self.accent, bg=self.bg, font=("Consolas", 13, "bold"))
        self.lbl_day.pack(side="left")
        self.lbl_money = tk.Label(top, text="", fg=self.green, bg=self.bg, font=("Consolas", 13))
        self.lbl_money.pack(side="left", padx=22)
        self.lbl_energy = tk.Label(top, text="", fg=self.yellow, bg=self.bg, font=("Consolas", 13))
        self.lbl_energy.pack(side="left", padx=22)
        self.lbl_stress = tk.Label(top, text="", fg=self.red, bg=self.bg, font=("Consolas", 13))
        self.lbl_stress.pack(side="left", padx=22)

        bars = tk.Frame(self.root, bg=self.bg)
        bars.pack(fill="x", padx=12, pady=4)
        self.bar_energy = self._make_bar(bars, "ЭНЕРГИЯ", self.yellow)
        self.bar_stress = self._make_bar(bars, "СТРЕСС", self.red)
        self.bar_neighbor = self._make_bar(bars, "СОСЕД", self.accent)

        info = tk.Frame(self.root, bg=self.bg)
        info.pack(fill="x", padx=12, pady=6)
        self.lbl_farm = tk.Label(info, text="", fg=self.fg, bg=self.bg, font=("Consolas", 11), justify="left")
        self.lbl_farm.pack(side="left")
        self.lbl_crypto = tk.Label(info, text="", fg=self.accent, bg=self.bg, font=("Consolas", 11), justify="right")
        self.lbl_crypto.pack(side="right")

        self.chart = tk.Canvas(self.root, height=180, bg=self.dark, highlightthickness=0)
        self.chart.pack(fill="x", padx=12, pady=6)

        btns = tk.Frame(self.root, bg=self.bg)
        btns.pack(fill="x", padx=12, pady=6)
        actions = [
            ("Работать (+5000)", lambda: self.action(self.work)),
            ("Отдохнуть", lambda: self.action(self.rest)),
            ("МАГАЗИН", self.open_shop),
            ("Майнить", lambda: self.action(self.mine)),
            ("Продать BTC", lambda: self.action(self.sell_crypto)),
            ("Балкон (20000)", lambda: self.action(self.build_balcony)),
            ("Гараж (80000)", lambda: self.action(self.build_garage)),
            ("Самозанятость (10000)", lambda: self.action(self.legalize)),
            ("Сохранить", self.save_game),
        ]
        for i, (t, c) in enumerate(actions):
            tk.Button(btns, text=t, command=c, bg=self.surface, fg=self.fg,
                      font=("Consolas", 10), relief="flat", padx=8, pady=6,
                      cursor="hand2").grid(row=i//3, column=i%3, padx=3, pady=3, sticky="ew")
        for c in range(3): btns.grid_columnconfigure(c, weight=1)

        self.log = tk.Text(self.root, height=7, bg=self.dark, fg=self.fg, font=("Consolas", 10),
                           relief="flat", state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True, padx=12, pady=6)

    def _make_bar(self, parent, label, color):
        f = tk.Frame(parent, bg=self.bg); f.pack(fill="x", pady=2)
        tk.Label(f, text=label, fg=color, bg=self.bg, width=10, anchor="w", font=("Consolas", 9)).pack(side="left")
        c = tk.Canvas(f, height=16, bg=self.surface, highlightthickness=0)
        c.pack(side="left", fill="x", expand=True)
        return c

    def open_shop(self):
        if self.shop_win and self.shop_win.winfo_exists():
            self.shop_win.lift(); self.build_shop(); return
        self.shop_win = tk.Toplevel(self.root)
        self.shop_win.title("Магазин комплектующих")
        self.shop_win.geometry("1050x680")
        self.shop_win.configure(bg=self.bg)
        self.build_shop()

    def build_shop(self):
        if not (self.shop_win and self.shop_win.winfo_exists()):
            return
        for w in self.shop_win.winfo_children(): w.destroy()

        hdr = tk.Frame(self.shop_win, bg=self.dark); hdr.pack(fill="x", padx=10, pady=5)
        total_p = self.calc_power()
        psu_str = f"{self.psu['name']} ({self.psu['wattage']}W)" if self.psu else "—"
        head_text = (
            f"Плата: {self.mb['name'] + ' [' + self.mb['socket'] + '/' + self.mb['ram'] + ']' if self.mb else '—'}\n"
            f"CPU: {self.cpu['name'] + ' [' + self.cpu['socket'] + ']' if self.cpu else '—'}\n"
            f"RAM: {self.ram['name'] if self.ram else '—'}\n"
            f"БП: {psu_str}\n"
            f"Видеокарт: {len(self.gpus)}/{self.mb['max_gpu'] if self.mb else 0}\n"
            f"Потребление: {total_p} Вт"
            + (f" / {self.psu['wattage']} Вт (запас {100-total_p/self.psu['wattage']*100:.0f}%)" if self.psu else "")
        )
        tk.Label(hdr, text=head_text, bg=self.dark, fg=self.fg, font=("Consolas", 10),
                 justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        nb = ttk.Notebook(self.shop_win); nb.pack(fill="both", expand=True, padx=10, pady=5)
        for cat, items, label in [("mb", MOTHERBOARDS, "Платы"), ("cpu", CPUS, "Процессоры"),
                                   ("ram", RAMS, "Память"), ("psu", PSUS, "БП"),
                                   ("gpu", GPUS, "Видеокарты")]:
            frame = tk.Frame(nb, bg=self.bg)
            nb.add(frame, text=label)
            self.render_shop(frame, cat, items)

    def render_shop(self, frame, cat, items):
        owned = []
        if cat == "mb" and self.mb: owned = [self.mb]
        elif cat == "cpu" and self.cpu: owned = [self.cpu]
        elif cat == "ram" and self.ram: owned = [self.ram]
        elif cat == "psu" and self.psu: owned = [self.psu]
        elif cat == "gpu": owned = self.gpus[:]

        if owned:
            tk.Label(frame, text="— Установлено —", bg=self.bg, fg=self.green,
                     font=("Consolas", 10, "bold")).pack(anchor="w", padx=10, pady=(8, 3))
            for o in owned:
                r = tk.Frame(frame, bg=self.bg); r.pack(fill="x", padx=10, pady=2)
                tk.Label(r, text=self._describe(cat, o), bg=self.bg, fg=self.green,
                         font=("Consolas", 10), anchor="w").pack(side="left", fill="x", expand=True)
                if cat == "gpu":
                    tk.Button(r, text="Продать (50%)", command=lambda g=o: self.sell_gpu(g),
                              bg="#45475a", fg=self.fg, font=("Consolas", 9),
                              relief="flat", cursor="hand2").pack(side="right")
                else:
                    tk.Button(r, text="Продать (50%)", command=lambda c=cat: self.sell_component(c),
                              bg="#45475a", fg=self.fg, font=("Consolas", 9),
                              relief="flat", cursor="hand2").pack(side="right")

        tk.Label(frame, text="— Доступно —", bg=self.bg, fg=self.accent,
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=10, pady=(12, 3))
        for item in items:
            row = tk.Frame(frame, bg=self.bg); row.pack(fill="x", padx=10, pady=2)
            tk.Label(row, text=self._describe(cat, item), bg=self.bg, fg=self.fg,
                     font=("Consolas", 10), anchor="w").pack(side="left", fill="x", expand=True)

            is_owned = (
                (cat == "mb" and self.mb and self.mb["id"] == item["id"]) or
                (cat == "cpu" and self.cpu and self.cpu["id"] == item["id"]) or
                (cat == "ram" and self.ram and self.ram["id"] == item["id"]) or
                (cat == "psu" and self.psu and self.psu["id"] == item["id"])
            )
            if is_owned:
                tk.Button(row, text="Установлено", state="disabled", bg=self.surface,
                          fg=self.green, font=("Consolas", 9, "bold")).pack(side="right")
                continue

            compat, reason = self.check_compatibility(cat, item)
            if not compat:
                tk.Label(row, text=reason, bg=self.bg, fg=self.red,
                         font=("Consolas", 8)).pack(side="right", padx=5)
                tk.Button(row, text="Несовм.", state="disabled", bg=self.surface,
                          fg="#585b70", font=("Consolas", 9)).pack(side="right")
            elif self.money < item["price"]:
                tk.Button(row, text=f"{item['price']}₽", state="disabled", bg=self.surface,
                          fg="#585b70", font=("Consolas", 9)).pack(side="right")
            else:
                tk.Button(row, text=f"Купить {item['price']}₽",
                          command=lambda c=cat, it=item: self.buy_component(c, it),
                          bg=self.green, fg=self.bg, font=("Consolas", 9, "bold"),
                          relief="flat", cursor="hand2").pack(side="right")

    def _describe(self, cat, item):
        if cat == "mb":
            return f"{item['name']}  |  {item['socket']}/{item['ram']}  |  GPU×{item['max_gpu']}  |  {item['power']}Вт"
        if cat == "cpu":
            return f"{item['name']}  |  {item['socket']}  |  {item['power']}Вт"
        if cat == "ram":
            return f"{item['name']}  |  {item['type']}  |  {item['power']}Вт"
        if cat == "psu":
            return f"{item['name']}  |  {item['wattage']}Вт"
        if cat == "gpu":
            return f"{item['name']}  |  {item['hashrate']} MH/s  |  {item['power']}Вт"
        return item["name"]

    # ---- День ----
    def action(self, func):
        if self.ended: return
        func()
        if not self.ended: self.end_day()

    def end_day(self):
        self.day += 1
        self.update_price()
        self.apply_electricity_bill()
        self.process_random_event()
        self.refresh_chart()
        if self.day > 30:
            self.final(); return
        self.check_end()
        self.update_ui()
        self.save_game()
        if not self.ended:
            self.log_msg(f"--- ДЕНЬ {self.day} ---")

    def apply_electricity_bill(self):
        p = self.calc_power()
        bill = int(p / 1000 * 24 * 4.72) if p > 0 else 0
        if bill > 0:
            self.money -= bill
            self.log_msg(f"Свет ({p}Вт × 24ч × 4.72₽): -{bill}₽")

    # ---- Действия ----
    def work(self):
        self.money += 5000
        self.energy -= 20
        self.stress += 10
        self.log_msg("Работа: +5000₽, -20 энергии, +10 стресса")

    def rest(self):
        self.energy = min(100, self.energy + 30)
        self.stress = max(0, self.stress - 20)
        self.log_msg("Отдых: +30 энергии, -20 стресса")

    def mine(self):
        if not (self.mb and self.cpu and self.ram and self.psu and self.gpus):
            error_sound(); self.log_msg("Ферма не собрана: нужны плата, CPU, RAM, БП и хотя бы одна GPU"); return
        p = self.calc_power()
        if p > self.psu["wattage"] * 0.85:
            error_sound(); self.log_msg(f"БП перегружен: {p}Вт при {self.psu['wattage']}Вт"); return
        btc = self.hashrate * 0.00002
        self.crypto_balance += btc
        self.energy -= 10
        self.stress += 5
        self.log_msg(f"Намайнено {btc:.8f} BTC ({self.hashrate:.0f} MH/s)")
        risk = 0.25 if self.balcony else 0.0
        if self.garage: risk = 0.40
        if risk > 0 and not self.wiring_ok and random.random() < risk:
            error_sound()
            if self.gpus:
                g = self.gpus.pop()
                self.hashrate -= g["hashrate"]
                self.log_msg(f"Проводка не выдержала! Сгорела {g['name']}")

    def sell_crypto(self):
        if self.crypto_balance <= 0:
            self.log_msg("Нечего продавать"); return
        rev = int(self.crypto_balance * self.btc_price_rub)
        self.money += rev
        self.log_msg(f"Продано {self.crypto_balance:.8f} BTC за {rev}₽")
        self.crypto_balance = 0

    def build_balcony(self):
        if self.balcony: self.log_msg("Балкон уже есть"); return
        if self.money >= 20000:
            self.money -= 20000; self.balcony = True
            self.log_msg("Балкон оборудован")
        else: error_sound(); self.log_msg("Нужно 20000₽")

    def build_garage(self):
        if self.garage: self.log_msg("Гараж уже есть"); return
        if not self.balcony: error_sound(); self.log_msg("Сначала балкон"); return
        if self.money >= 80000:
            self.money -= 80000; self.garage = True
            self.log_msg("Гараж оборудован (больше места, но риск кражи)")
        else: error_sound(); self.log_msg("Нужно 80000₽")

    def legalize(self):
        if self.legal: self.log_msg("Уже легален"); return
        if self.money >= 10000:
            self.money -= 10000; self.legal = True
            self.tax_risk = max(0, self.tax_risk - 30)
            self.log_msg("Самозанятость оформлена")
        else: error_sound(); self.log_msg("Нужно 10000₽")

    # ---- Рынок ----
    def update_price(self):
        if random.random() < 0.20:
            self.trend = random.uniform(-0.8, 0.8)
            self.volatility = random.uniform(0.02, 0.08)
        drift = self.trend * 0.02
        shock = random.gauss(0, self.volatility)
        if random.random() < 0.04:
            shock += random.choice([-1, 1]) * random.uniform(0.10, 0.25)
        self.btc_price_rub *= (1 + drift + shock)
        self.btc_price_rub = max(1000000, self.btc_price_rub)
        self.price_history.append(self.btc_price_rub)
        if len(self.price_history) > 14: self.price_history.pop(0)

    def process_random_event(self):
        evs = [self.ev_bro, self.ev_neighbor, self.ev_cooler, self.ev_tax]
        if abs(self.trend) > 0.5 and random.random() < 0.5: evs.append(self.ev_news)
        if self.garage: evs.append(self.ev_theft)
        if random.random() < 0.6:
            random.choice(evs)()

    def ev_bro(self):
        self.log_msg("Крипто-бро: мем-коин x10!")
        if random.random() < 0.4:
            self.crypto_balance += 0.0001
            self.log_msg("  +0.0001 BTC")
        else:
            self.money -= 3000
            self.log_msg("  -3000₽")

    def ev_neighbor(self):
        self.neighbor_patience -= 20
        self.log_msg("Сосед: «Это что, самолёт?» -20 терпения")

    def ev_cooler(self):
        if self.gpus:
            self.hashrate = max(0, self.hashrate - 1)
            self.log_msg("Кулер загудел, -1 MH/s")

    def ev_tax(self):
        self.tax_risk += 10
        if self.legal:
            self.tax_risk = max(0, self.tax_risk - 20)
            self.log_msg("Налоговая: легален, всё в порядке")
        elif random.random() < self.tax_risk / 100:
            self.money -= 20000
            error_sound()
            self.log_msg("Налоговая: штраф 20000₽")
        else:
            self.log_msg("Налоговая: пронесло")

    def ev_news(self):
        if self.trend > 0.3:
            self.btc_price_rub *= 1.10
            self.log_msg("Новость: BTC +10%")
        else:
            self.btc_price_rub *= 0.90
            self.log_msg("Новость: BTC -10%")
        self.price_history[-1] = self.btc_price_rub

    def ev_theft(self):
        if random.random() < 0.3 and self.gpus:
            g = self.gpus.pop()
            self.hashrate -= g["hashrate"]
            error_sound()
            self.log_msg(f"Гараж вскрыли! Украдена {g['name']}")
        else:
            self.log_msg("Кто-то у гаража, но обошлось")

    # ---- UI update ----
    def update_ui(self):
        self.lbl_day.config(text=f"День {self.day}/30")
        self.lbl_money.config(text=f"{self.money}₽")
        self.lbl_energy.config(text=f"Энергия: {self.energy}")
        self.lbl_stress.config(text=f"Стресс: {self.stress}")
        self.draw_bar(self.bar_energy, self.energy, self.yellow)
        self.draw_bar(self.bar_stress, self.stress, self.red)
        self.draw_bar(self.bar_neighbor, self.neighbor_patience, self.accent)

        comps = []
        if self.mb: comps.append("плата")
        if self.cpu: comps.append("CPU")
        if self.ram: comps.append("RAM")
        if self.psu: comps.append(f"БП {self.psu['wattage']}W")
        comp_str = ", ".join(comps) if comps else "—"
        loc = "гараж" if self.garage else ("балкон" if self.balcony else "комната")
        p = self.calc_power()
        self.lbl_farm.config(text=(
            f"Карт: {len(self.gpus)} | Хешрейт: {self.hashrate:.0f} MH/s | {loc}\n"
            f"Компоненты: {comp_str} | Потребление: {p} Вт\n"
            f"Легально: {'да' if self.legal else 'нет'} | Риск налоговой: {self.tax_risk}%"
        ))
        trend = "бычий" if self.trend > 0.3 else "медвежий" if self.trend < -0.3 else "боковик"
        self.lbl_crypto.config(text=(
            f"Баланс: {self.crypto_balance:.8f} BTC\n"
            f"Курс: {self.btc_price_rub:,.0f}₽\n"
            f"Тренд: {trend}"
        ))

    def draw_bar(self, c, v, color):
        c.delete("all"); c.update_idletasks()
        w = c.winfo_width() or 800; h = int(c.cget("height"))
        c.create_rectangle(0, 0, int(w * max(0, min(100, v)) / 100), h, fill=color, outline="")

    def animate_chart(self):
        if self.anim_progress < self.anim_target:
            self.anim_progress = min(self.anim_target, self.anim_progress + 0.08)
            self.draw_chart(self.anim_progress)
        self.root.after(30, self.animate_chart)

    def draw_chart(self, progress=1.0):
        c = self.chart; c.delete("all"); c.update_idletasks()
        w = c.winfo_width() or 800; h = int(c.cget("height"))
        hist = self.price_history; lo, hi = min(hist), max(hist)
        if hi - lo < 1: hi = lo + 1
        pad = 14; points = []
        for i, p in enumerate(hist):
            x = pad + (w - 2*pad) * i / (len(hist) - 1)
            y = h - pad - (h - 2*pad) * (p - lo) / (hi - lo)
            points.append((x, y))
        n = max(2, int(len(points) * progress))
        poly = [(points[0][0], h-pad)] + points[:n] + [(points[n-1][0], h-pad)]
        c.create_polygon(poly, fill="#1e2a3a", outline="")
        for i in range(n-1):
            c.create_line(points[i], points[i+1], fill=self.accent, width=2)
        c.create_text(10, 10, text=f"{hi:,.0f}", fill=self.fg, anchor="nw", font=("Consolas", 9))
        c.create_text(10, h-10, text=f"{lo:,.0f}", fill=self.fg, anchor="sw", font=("Consolas", 9))
        ch = (hist[-1] / hist[0] - 1) * 100
        c.create_text(w-10, 10, text=f"{ch:+.1f}% / 14д",
                      fill=(self.green if ch >= 0 else self.red), anchor="ne",
                      font=("Consolas", 10, "bold"))

    def refresh_chart(self):
        self.anim_progress = 0.0; self.anim_target = 1.0

    def log_msg(self, t):
        self.log.config(state="normal"); self.log.insert("end", t + "\n")
        self.log.see("end"); self.log.config(state="disabled")

    # ---- Конец ----
    def check_end(self):
        if self.ended: return
        if self.money < -50000:
            self.ended = True; error_sound()
            messagebox.showinfo("Конец", "Долговая яма")
            self.save_score("Долговая яма", self.money); self.restart_prompt()
        if self.stress >= 100:
            self.ended = True; error_sound()
            messagebox.showinfo("Конец", "Выгорание")
            self.save_score("Выгорание", self.money); self.restart_prompt()

    def final(self):
        self.ended = True
        if self.crypto_balance * self.btc_price_rub > 200000:
            msg, t = "Крипто-магнат: квартира есть, но графики не отпускают.", "Крипто-магнат"
        elif self.legal and len(self.gpus) >= 3 and self.money > 50000:
            msg, t = "Легальный фермер: платишь налоги, спишь спокойно.", "Легальный фермер"
        elif self.money < 0:
            msg, t = "Отрицательный баланс, положительный опыт.", "Долговая яма"
        else:
            msg, t = "Тихая гавань: работаешь, майнишь потихоньку.", "Тихая гавань"
        messagebox.showinfo("Итоги 30 дней", msg)
        self.save_score(t, self.money)
        if os.path.exists(SAVE_FILE):
            try: os.remove(SAVE_FILE)
            except Exception: pass
        self.restart_prompt()

    def save_score(self, title, money):
        scores = []
        if os.path.exists(SCORES_FILE):
            try:
                with open(SCORES_FILE, "r", encoding="utf-8") as f: scores = json.load(f)
            except Exception: scores = []
        scores.append({"title": title, "money": money, "day": self.day,
                       "cards": len(self.gpus),
                       "crypto": round(self.crypto_balance * self.btc_price_rub)})
        scores = sorted(scores, key=lambda x: x["money"], reverse=True)[:10]
        try:
            with open(SCORES_FILE, "w", encoding="utf-8") as f:
                json.dump(scores, f, ensure_ascii=False, indent=2)
        except Exception: pass

    def restart_prompt(self):
        if messagebox.askyesno("Ещё раз?", "Сыграем заново?"):
            self.root.destroy(); main()


def show_scores(root):
    win = tk.Toplevel(root); win.title("Рекорды"); win.geometry("650x400"); win.configure(bg="#1e1e2e")
    tk.Label(win, text="РЕКОРДЫ", font=("Consolas", 18, "bold"), bg="#1e1e2e", fg="#f9e2af").pack(pady=10)
    scores = []
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f: scores = json.load(f)
        except Exception: pass
    if not scores:
        tk.Label(win, text="Пока пусто", bg="#1e1e2e", fg="#cdd6f4", font=("Consolas", 12)).pack(pady=30)
    else:
        f = tk.Frame(win, bg="#1e1e2e"); f.pack(fill="both", expand=True, padx=20, pady=10)
        for i, h in enumerate(["#", "Концовка", "Деньги", "День", "Карт", "Крипта"]):
            tk.Label(f, text=h, bg="#1e1e2e", fg="#89b4fa", font=("Consolas", 11, "bold")).grid(row=0, column=i, padx=8, pady=4)
        for r, s in enumerate(scores, 1):
            for c, v in enumerate([r, s["title"], f"{s['money']}₽", s["day"], s["cards"], f"{s['crypto']}₽"]):
                tk.Label(f, text=str(v), bg="#1e1e2e", fg="#cdd6f4", font=("Consolas", 10)).grid(row=r, column=c, padx=8, pady=2)
    tk.Button(win, text="Закрыть", command=win.destroy, bg="#313244", fg="#cdd6f4",
              font=("Consolas", 11), relief="flat", padx=20, pady=6).pack(pady=10)


def main():
    root = tk.Tk()
    make_icon(root)

    def start_new():
        for w in root.winfo_children(): w.destroy()
        GameGUI(root, load=False)

    def continue_game():
        for w in root.winfo_children(): w.destroy()
        GameGUI(root, load=True)

    def open_scores(): show_scores(root)

    StartMenu(root, start_new, continue_game, open_scores)
    root.mainloop()


if __name__ == "__main__":
    main()
