import tkinter as tk
from tkinter import messagebox
import random, json, os, math

try:
    import ttkbootstrap as tb
    HAS_BOOTSTRAP = True
except ImportError:
    HAS_BOOTSTRAP = False
    from tkinter import ttk

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

SAVE_FILE = "savegame.json"
SCORES_FILE = "scores.json"

# ============ КАТАЛОГ ============
MOTHERBOARDS = [
    {"id": "mb_budget", "name": "ASRock H510M", "socket": "LGA1200", "ram": "DDR4", "max_gpu": 1, "price": 2500,  "power": 30},
    {"id": "mb_mid",    "name": "MSI B550M",    "socket": "AM4",     "ram": "DDR4", "max_gpu": 2, "price": 5500,  "power": 35},
    {"id": "mb_high",   "name": "ASUS Z690",    "socket": "LGA1700", "ram": "DDR5", "max_gpu": 3, "price": 12000, "power": 40},
    {"id": "mb_mining", "name": "Mining B250",  "socket": "LGA1200", "ram": "DDR4", "max_gpu": 6, "price": 15000, "power": 45},
]
CPUS = [
    {"id": "cpu_cel",    "name": "Celeron G5905", "socket": "LGA1200", "price": 500,   "power": 58},
    {"id": "cpu_ryzen3", "name": "Ryzen 3 3200G", "socket": "AM4",     "price": 4000,  "power": 65},
    {"id": "cpu_ryzen5", "name": "Ryzen 5 5600",  "socket": "AM4",     "price": 8000,  "power": 65},
    {"id": "cpu_i5",     "name": "Core i5-12400", "socket": "LGA1700", "price": 12000, "power": 65},
]
RAMS = [
    {"id": "ram_ddr4_8",  "name": "DDR4 8GB",  "type": "DDR4", "price": 1550,  "power": 5},
    {"id": "ram_ddr4_16", "name": "DDR4 16GB", "type": "DDR4", "price": 3000,  "power": 8},
    {"id": "ram_ddr5_16", "name": "DDR5 16GB", "type": "DDR5", "price": 6000,  "power": 10},
    {"id": "ram_ddr5_32", "name": "DDR5 32GB", "type": "DDR5", "price": 12000, "power": 15},
]
PSUS = [
    {"id": "psu_500",  "name": "500W Bronze",    "wattage": 500,  "price": 3500},
    {"id": "psu_750",  "name": "750W Gold",      "wattage": 750,  "price": 6500},
    {"id": "psu_1000", "name": "1000W Gold",     "wattage": 1000, "price": 12000},
    {"id": "psu_1200", "name": "1200W Platinum", "wattage": 1200, "price": 18000},
    {"id": "psu_1500", "name": "1500W Titanium", "wattage": 1500, "price": 25000},
]
# === ОБНОВЛЕНО: реальные хешрейты Ethash и потребление ===
GPUS = [
    {"id": "gpu_1660",  "name": "GTX 1660 Super", "hashrate": 31,  "price": 15000,  "power": 80},
    {"id": "gpu_3060",  "name": "RTX 3060",       "hashrate": 36,  "price": 22000,  "power": 116},
    {"id": "gpu_3060ti","name": "RTX 3060 Ti",    "hashrate": 61,  "price": 28000,  "power": 130},
    {"id": "gpu_3070",  "name": "RTX 3070",       "hashrate": 62,  "price": 33000,  "power": 130},
    {"id": "gpu_3080",  "name": "RTX 3080",       "hashrate": 98,  "price": 48000,  "power": 240},
    {"id": "gpu_3090",  "name": "RTX 3090",       "hashrate": 121, "price": 75000,  "power": 290},
    {"id": "gpu_4060",  "name": "RTX 4060",       "hashrate": 34,  "price": 31050,  "power": 80},
    {"id": "gpu_4070",  "name": "RTX 4070",       "hashrate": 62,  "price": 55000,  "power": 130},
    {"id": "gpu_4090",  "name": "RTX 4090",       "hashrate": 135, "price": 150000, "power": 275},
    {"id": "gpu_6600xt","name": "RX 6600 XT",     "hashrate": 32,  "price": 18000,  "power": 55},
    {"id": "gpu_6700xt","name": "RX 6700 XT",     "hashrate": 46,  "price": 26000,  "power": 100},
    {"id": "gpu_6800xt","name": "RX 6800 XT",     "hashrate": 65,  "price": 40000,  "power": 110},
    {"id": "gpu_7900xtx","name": "RX 7900 XTX",   "hashrate": 100, "price": 90000,  "power": 220},
]

SYNC_PRICE = 5000
MAX_PSU = 2  # максимум БП на ферму

def click_sound():
    if HAS_SOUND:
        try: winsound.Beep(800, 40)
        except: pass

def error_sound():
    if HAS_SOUND:
        try: winsound.Beep(300, 120)
        except: pass

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


class Farm:
    def __init__(self, idx, location, setup_cost=0):
        self.idx = idx
        self.location = location
        self.setup_cost = setup_cost
        self.unlocked = (setup_cost == 0)
        self.mb = None
        self.cpu = None
        self.ram = None
        self.psus = []
        self.synchronizer = False
        self.gpus = []
        self.wiring_ok = True

    @property
    def name(self):
        return {"room": "Комната", "balcony": "Балкон", "garage": "Гараж"}[self.location]

    @property
    def location_icon(self):
        return {"room": "🏠", "balcony": "🪟", "garage": "🏭"}[self.location]

    def total_wattage(self):
        return sum(p["wattage"] for p in self.psus)

    def power_draw(self):
        p = 20
        if self.mb: p += self.mb["power"]
        if self.cpu: p += self.cpu["power"]
        if self.ram: p += self.ram["power"]
        for g in self.gpus: p += g["power"]
        return p

    def hashrate(self):
        return sum(g["hashrate"] for g in self.gpus)

    def is_complete(self):
        return (self.mb and self.cpu and self.ram and self.psus and self.gpus
                and self.power_draw() <= self.total_wattage() * 0.85)

    def max_slots(self):
        return self.mb["max_gpu"] if self.mb else 0

    def to_dict(self):
        return {
            "idx": self.idx, "location": self.location, "setup_cost": self.setup_cost,
            "unlocked": self.unlocked, "mb": self.mb, "cpu": self.cpu, "ram": self.ram,
            "psus": self.psus, "synchronizer": self.synchronizer,
            "gpus": self.gpus, "wiring_ok": self.wiring_ok,
        }

    @classmethod
    def from_dict(cls, d):
        f = cls(d["idx"], d["location"], d["setup_cost"])
        for k, v in d.items():
            setattr(f, k, v)
        return f


class GameGUI:
    def __init__(self, root, load=False):
        self.root = root
        self.root.title("Компьютерщик 2.0 — 3 фермы")
        self.root.geometry("1240x980")
        self.root.minsize(1150, 900)

        self.bg = "#1e1e2e"; self.fg = "#cdd6f4"; self.accent = "#89b4fa"
        self.green = "#a6e3a1"; self.red = "#f38ba8"; self.yellow = "#f9e2af"
        self.surface = "#313244"; self.dark = "#181825"; self.gray = "#585b70"

        self.init_state()
        if load: self.load_game()

        self.anim_progress = 1.0
        self.anim_target = 1.0
        self.fan_angle = 0
        self.shop_win = None
        self.farm_canvases = []

        self.build_ui()
        self.update_ui()
        self.animate()
        self.log_msg(f"--- ДЕНЬ {self.day} ---")
        self.log_msg("Максимум 2 БП на ферму. Для второго нужен синхронизатор (5 000 ₽).")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def init_state(self):
        self.day = 1
        self.money = 15000
        self.energy = 100
        self.stress = 20
        self.crypto_balance = 0.0
        self.btc_price_rub = 5386778.85
        self.price_history = [self.btc_price_rub] * 30
        self.market_phase = "neutral"
        self.phase_days_left = random.randint(20, 60)
        self.trend_strength = 0.0
        self.base_volatility = 0.022
        self.neighbor_patience = 100
        self.legal = False
        self.tax_risk = 0
        self.ended = False
        self.active_farm = 0
        self.farms = [
            Farm(0, "room", 0),
            Farm(1, "balcony", 20000),
            Farm(2, "garage", 80000),
        ]

    def on_close(self):
        if not self.ended: self.save_game()
        self.root.destroy()

    def save_game(self):
        data = {
            "day": self.day, "money": self.money, "energy": self.energy,
            "stress": self.stress, "crypto_balance": self.crypto_balance,
            "btc_price_rub": self.btc_price_rub, "price_history": self.price_history,
            "market_phase": self.market_phase, "phase_days_left": self.phase_days_left,
            "trend_strength": self.trend_strength, "base_volatility": self.base_volatility,
            "neighbor_patience": self.neighbor_patience, "legal": self.legal,
            "tax_risk": self.tax_risk, "active_farm": self.active_farm,
            "farms": [f.to_dict() for f in self.farms],
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_msg(f"Ошибка сохранения: {e}")

    def load_game(self):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
            for k, v in d.items():
                if k == "farms":
                    self.farms = [Farm.from_dict(fd) for fd in v]
                elif hasattr(self, k):
                    setattr(self, k, v)
        except Exception as e:
            print("Ошибка загрузки:", e)

    def build_ui(self):
        top = tk.Frame(self.root, bg=self.bg); top.pack(fill="x", padx=12, pady=6)
        self.lbl_day = tk.Label(top, text="", fg=self.accent, bg=self.bg, font=("Consolas", 14, "bold"))
        self.lbl_day.pack(side="left")
        self.lbl_money = tk.Label(top, text="", fg=self.green, bg=self.bg, font=("Consolas", 14))
        self.lbl_money.pack(side="left", padx=22)
        self.lbl_energy = tk.Label(top, text="", fg=self.yellow, bg=self.bg, font=("Consolas", 14))
        self.lbl_energy.pack(side="left", padx=22)
        self.lbl_stress = tk.Label(top, text="", fg=self.red, bg=self.bg, font=("Consolas", 14))
        self.lbl_stress.pack(side="left", padx=22)
        self.lbl_active = tk.Label(top, text="", fg=self.accent, bg=self.bg, font=("Consolas", 12, "italic"))
        self.lbl_active.pack(side="right")

        bars = tk.Frame(self.root, bg=self.bg); bars.pack(fill="x", padx=12, pady=4)
        self.bar_energy = self._make_bar(bars, "ЭНЕРГИЯ", self.yellow)
        self.bar_stress = self._make_bar(bars, "СТРЕСС", self.red)
        self.bar_neighbor = self._make_bar(bars, "СОСЕД", self.accent)

        farms_frame = tk.Frame(self.root, bg=self.bg)
        farms_frame.pack(fill="x", padx=12, pady=8)
        self.farm_canvases = []
        for i, farm in enumerate(self.farms):
            c = tk.Canvas(farms_frame, width=390, height=210, bg=self.dark, highlightthickness=0)
            c.grid(row=0, column=i, padx=5, sticky="nsew")
            c.bind("<Button-1>", lambda e, idx=i: self.select_farm(idx))
            self.farm_canvases.append(c)
        for i in range(3):
            farms_frame.grid_columnconfigure(i, weight=1)

        self.chart = tk.Canvas(self.root, height=170, bg=self.dark, highlightthickness=0)
        self.chart.pack(fill="x", padx=12, pady=6)

        btns = tk.Frame(self.root, bg=self.bg); btns.pack(fill="x", padx=12, pady=6)
        actions = [
            ("💼 Работать (+5000)", lambda: self.action(self.work)),
            ("😴 Отдохнуть", lambda: self.action(self.rest)),
            ("🛒 МАГАЗИН", self.open_shop),
            ("⛏️ Майнить всё", lambda: self.action(self.mine_all)),
            ("💰 Продать BTC", lambda: self.action(self.sell_crypto)),
            ("🪟 Открыть балкон (20к)", lambda: self.action(lambda: self.unlock_farm(1))),
            ("🏭 Открыть гараж (80к)", lambda: self.action(lambda: self.unlock_farm(2))),
            ("🧾 Самозанятость (10к)", lambda: self.action(self.legalize)),
            ("💾 Сохранить", self.save_game),
        ]
        for i, (t, c) in enumerate(actions):
            tk.Button(btns, text=t, command=c, bg=self.surface, fg=self.fg,
                      font=("Consolas", 10), relief="flat", padx=6, pady=6,
                      cursor="hand2", activebackground=self.accent).grid(
                          row=i//3, column=i%3, padx=3, pady=3, sticky="ew")
        for c in range(3): btns.grid_columnconfigure(c, weight=1)

        self.log = tk.Text(self.root, height=7, bg=self.dark, fg=self.fg, font=("Consolas", 10),
                           relief="flat", state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True, padx=12, pady=6)

    def _make_bar(self, parent, label, color):
        f = tk.Frame(parent, bg=self.bg); f.pack(fill="x", pady=2)
        tk.Label(f, text=label, fg=color, bg=self.bg, width=12, anchor="w", font=("Consolas", 9)).pack(side="left")
        c = tk.Canvas(f, height=16, bg=self.surface, highlightthickness=0)
        c.pack(side="left", fill="x", expand=True)
        return c

    def select_farm(self, idx):
        if not self.farms[idx].unlocked:
            self.log_msg(f"Ферма {self.farms[idx].name} не открыта (нужно {self.farms[idx].setup_cost}₽)")
            return
        self.active_farm = idx
        click_sound()
        self.update_ui()

    def log_msg(self, t):
        self.log.config(state="normal"); self.log.insert("end", t + "\n")
        self.log.see("end"); self.log.config(state="disabled")

    def draw_farm(self, canvas, farm, angle, active):
        canvas.delete("all")
        w, h = 390, 210
        border = self.accent if active else "#45475a"
        canvas.create_rectangle(2, 2, w-2, h-2, outline=border, width=3 if active else 2)

        if not farm.unlocked:
            canvas.create_text(w//2, 50, text=f"🔒 {farm.location_icon} {farm.name}",
                               font=("Consolas", 14, "bold"), fill=self.gray)
            canvas.create_text(w//2, 90, text=f"Открыть за {farm.setup_cost:,}₽",
                               font=("Consolas", 12), fill=self.yellow)
            canvas.create_text(w//2, 130, text="(кнопка внизу)",
                               font=("Consolas", 9), fill=self.gray)
            return

        canvas.create_text(10, 8, text=f"{farm.location_icon} {farm.name}",
                           font=("Consolas", 13, "bold"), fill=self.accent, anchor="nw")

        comps = []
        comps.append(("MB", farm.mb is not None))
        comps.append(("CPU", farm.cpu is not None))
        comps.append(("RAM", farm.ram is not None))
        x = 10
        for name, ok in comps:
            color = self.green if ok else self.red
            canvas.create_text(x, 30, text=f"{name}:{'✓' if ok else '✗'}",
                               font=("Consolas", 10), fill=color, anchor="nw")
            x += 65

        if farm.psus:
            psu_str = f"БП: {'+'.join(str(p['wattage']) for p in farm.psus)}W = {farm.total_wattage()}W"
            if farm.synchronizer: psu_str += " 🔗"
            psu_color = self.green if farm.power_draw() <= farm.total_wattage() * 0.85 else self.red
        else:
            psu_str = "БП: нет"
            psu_color = self.gray
        canvas.create_text(10, 50, text=psu_str, font=("Consolas", 10), fill=psu_color, anchor="nw")

        draw = farm.power_draw()
        canvas.create_text(10, 68, text=f"Потребление: {draw}W", font=("Consolas", 10),
                           fill=self.fg, anchor="nw")

        canvas.create_text(w-10, 8, text=f"⛏ {farm.hashrate():.0f} MH/s",
                           font=("Consolas", 12, "bold"), fill=self.yellow, anchor="ne")

        max_s = farm.max_slots()
        if max_s > 0:
            slot_w = min(55, (w - 30) // max_s)
            for i in range(max_s):
                sx = 10 + i * (slot_w + 3)
                sy = 95
                if i < len(farm.gpus):
                    gpu = farm.gpus[i]
                    canvas.create_rectangle(sx, sy, sx+slot_w, sy+slot_w,
                                            fill="#1e3a2f", outline=self.green, width=1)
                    cx, cy = sx + slot_w/2, sy + slot_w/2
                    canvas.create_oval(cx-12, cy-12, cx+12, cy+12, outline=self.gray)
                    ang = math.radians(angle)
                    for off in (0, math.pi):
                        bx = cx + 11 * math.cos(ang + off)
                        by = cy + 11 * math.sin(ang + off)
                        canvas.create_line(cx, cy, bx, by, fill=self.green, width=2)
                    canvas.create_text(cx, sy + slot_w + 8, text=f"{gpu['hashrate']}M",
                                       font=("Consolas", 8), fill=self.fg)
                else:
                    canvas.create_rectangle(sx, sy, sx+slot_w, sy+slot_w,
                                            fill=self.dark, outline=self.gray, dash=(2, 2))
                    canvas.create_text(sx+slot_w/2, sy+slot_w/2, text="—",
                                       font=("Consolas", 10), fill=self.gray)
        elif farm.unlocked:
            canvas.create_text(10, 100, text="Купи материнскую плату →",
                               font=("Consolas", 10, "italic"), fill=self.gray, anchor="nw")

        if active:
            canvas.create_text(w-10, h-10, text="[АКТИВНА]",
                               font=("Consolas", 9, "bold"), fill=self.accent, anchor="se")

    def animate(self):
        self.fan_angle = (self.fan_angle + 10) % 360
        if self.anim_progress < self.anim_target:
            self.anim_progress = min(self.anim_target, self.anim_progress + 0.06)
        self.draw_chart(self.anim_progress)
        for i, farm in enumerate(self.farms):
            if i < len(self.farm_canvases):
                self.draw_farm(self.farm_canvases[i], farm, self.fan_angle, i == self.active_farm)
        self.root.after(80, self.animate)

    def draw_chart(self, progress=1.0):
        c = self.chart; c.delete("all"); c.update_idletasks()
        w = c.winfo_width() or 800; h = int(c.cget("height"))
        hist = self.price_history
        if len(hist) < 2: return
        lo, hi = min(hist), max(hist)
        if hi - lo < 1: hi = lo + 1
        pad = 18; pts = []
        for i, p in enumerate(hist):
            x = pad + (w - 2*pad) * i / (len(hist) - 1)
            y = h - pad - (h - 2*pad) * (p - lo) / (hi - lo)
            pts.append((x, y))
        n = max(2, int(len(pts) * progress))
        poly = [(pts[0][0], h-pad)] + pts[:n] + [(pts[n-1][0], h-pad)]
        c.create_polygon(poly, fill="#1e2a3a", outline="")
        for i in range(n-1):
            c.create_line(pts[i], pts[i+1], fill=self.accent, width=2)
        for frac in [0.25, 0.5, 0.75]:
            y = pad + (h - 2*pad) * frac
            c.create_line(pad, y, w-pad, y, fill="#2a2a4a", dash=(2, 4))
        c.create_text(10, 8, text=f"BTC: {hi:,.0f}₽", fill=self.fg, anchor="nw", font=("Consolas", 10, "bold"))
        ch = (hist[-1] / hist[0] - 1) * 100
        c.create_text(w-10, 8, text=f"{ch:+.1f}% / 30д",
                      fill=(self.green if ch >= 0 else self.red), anchor="ne",
                      font=("Consolas", 11, "bold"))

    # ---------- Магазин ----------
    def open_shop(self):
        if not self.farms[self.active_farm].unlocked:
            self.log_msg("Ферма не открыта"); return
        if self.shop_win and self.shop_win.winfo_exists():
            self.shop_win.lift(); self.build_shop(); return
        self.shop_win = tk.Toplevel(self.root)
        self.shop_win.title("Магазин")
        self.shop_win.geometry("1100x750")
        self.shop_win.configure(bg=self.bg)
        self.build_shop()

    def build_shop(self):
        if not (self.shop_win and self.shop_win.winfo_exists()): return
        for w in self.shop_win.winfo_children(): w.destroy()
        farm = self.farms[self.active_farm]

        sel = tk.Frame(self.shop_win, bg=self.dark); sel.pack(fill="x", padx=10, pady=6)
        tk.Label(sel, text="Ферма:", bg=self.dark, fg=self.fg, font=("Consolas", 11, "bold")).pack(side="left", padx=5)
        for i, f in enumerate(self.farms):
            state = "normal" if f.unlocked else "disabled"
            bg = self.accent if i == self.active_farm else self.surface
            btn = tk.Button(sel, text=f"{f.location_icon} {f.name}", state=state,
                            command=lambda idx=i: self._shop_switch(idx),
                            bg=bg, fg=self.bg, font=("Consolas", 10, "bold"),
                            relief="flat", padx=10, pady=4, cursor="hand2")
            btn.pack(side="left", padx=3)

        hdr = tk.Frame(self.shop_win, bg=self.dark); hdr.pack(fill="x", padx=10, pady=4)
        info = (
            f"{farm.name}: MB={farm.mb['name'] if farm.mb else '—'} | "
            f"CPU={farm.cpu['name'] if farm.cpu else '—'} | "
            f"RAM={farm.ram['name'] if farm.ram else '—'} | "
            f"БП={len(farm.psus)}×{'='+str(farm.total_wattage())+'W' if farm.psus else '0'} | "
            f"GPU={len(farm.gpus)}/{farm.max_slots()} | "
            f"Draw={farm.power_draw()}W"
        )
        tk.Label(hdr, text=info, bg=self.dark, fg=self.fg, font=("Consolas", 10),
                 justify="left", anchor="w").pack(fill="x", padx=6, pady=4)

        if HAS_BOOTSTRAP: nb = tb.Notebook(self.shop_win, bootstyle="dark")
        else: nb = ttk.Notebook(self.shop_win)
        nb.pack(fill="both", expand=True, padx=10, pady=6)
        for cat, items, label in [("mb", MOTHERBOARDS, "Платы"), ("cpu", CPUS, "Процессоры"),
                                   ("ram", RAMS, "Память"), ("psu", PSUS, "БП (синхрон)"),
                                   ("gpu", GPUS, "Видеокарты")]:
            frame = tk.Frame(nb, bg=self.bg); nb.add(frame, text=label)
            if cat == "psu": self.render_psu_tab(frame, farm)
            else: self.render_generic(frame, farm, cat, items)

    def _shop_switch(self, idx):
        if not self.farms[idx].unlocked: return
        self.active_farm = idx
        self.update_ui()
        self.build_shop()

    def render_generic(self, frame, farm, cat, items):
        owned = None
        if cat == "mb": owned = farm.mb
        elif cat == "cpu": owned = farm.cpu
        elif cat == "ram": owned = farm.ram

        if cat == "gpu" and farm.gpus:
            tk.Label(frame, text="— Установлено —", bg=self.bg, fg=self.green,
                     font=("Consolas", 10, "bold")).pack(anchor="w", padx=12, pady=(8, 3))
            for g in farm.gpus:
                r = tk.Frame(frame, bg=self.bg); r.pack(fill="x", padx=12, pady=2)
                tk.Label(r, text=self._describe(cat, g), bg=self.bg, fg=self.green,
                         font=("Consolas", 10), anchor="w").pack(side="left", fill="x", expand=True)
                tk.Button(r, text="Снять (50%)", command=lambda gg=g: self.sell_gpu(farm, gg),
                          bg=self.surface, fg=self.fg, font=("Consolas", 9),
                          relief="flat", cursor="hand2").pack(side="right")
        elif owned:
            tk.Label(frame, text="— Установлено —", bg=self.bg, fg=self.green,
                     font=("Consolas", 10, "bold")).pack(anchor="w", padx=12, pady=(8, 3))
            r = tk.Frame(frame, bg=self.bg); r.pack(fill="x", padx=12, pady=2)
            tk.Label(r, text=self._describe(cat, owned), bg=self.bg, fg=self.green,
                     font=("Consolas", 10), anchor="w").pack(side="left", fill="x", expand=True)
            tk.Button(r, text="Снять (50%)", command=lambda c=cat: self.sell_component(farm, c),
                      bg=self.surface, fg=self.fg, font=("Consolas", 9),
                      relief="flat", cursor="hand2").pack(side="right")

        tk.Label(frame, text="— Доступно —", bg=self.bg, fg=self.accent,
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=12, pady=(14, 3))
        for item in items:
            row = tk.Frame(frame, bg=self.bg); row.pack(fill="x", padx=12, pady=2)
            tk.Label(row, text=self._describe(cat, item), bg=self.bg, fg=self.fg,
                     font=("Consolas", 10), anchor="w").pack(side="left", fill="x", expand=True)

            if cat != "gpu" and owned and owned["id"] == item["id"]:
                tk.Button(row, text="Установлено", state="disabled", bg=self.surface,
                          fg=self.green, font=("Consolas", 9, "bold")).pack(side="right")
                continue

            ok, reason = self.check_compat(farm, cat, item)
            if not ok:
                tk.Label(row, text=reason, bg=self.bg, fg=self.red,
                         font=("Consolas", 8)).pack(side="right", padx=5)
                tk.Button(row, text="Несовм.", state="disabled", bg=self.surface,
                          fg=self.gray, font=("Consolas", 9)).pack(side="right")
            elif self.money < item["price"]:
                tk.Button(row, text=f"{item['price']:,}₽", state="disabled", bg=self.surface,
                          fg=self.gray, font=("Consolas", 9)).pack(side="right")
            else:
                tk.Button(row, text=f"Купить {item['price']:,}₽",
                          command=lambda c=cat, it=item: self.buy_component(farm, c, it),
                          bg=self.green, fg=self.bg, font=("Consolas", 9, "bold"),
                          relief="flat", cursor="hand2").pack(side="right")

    def render_psu_tab(self, frame, farm):
        if farm.psus:
            tk.Label(frame, text="— Подключённые БП —", bg=self.bg, fg=self.green,
                     font=("Consolas", 10, "bold")).pack(anchor="w", padx=12, pady=(8, 3))
            for p in farm.psus:
                r = tk.Frame(frame, bg=self.bg); r.pack(fill="x", padx=12, pady=2)
                tk.Label(r, text=f"{p['name']} ({p['wattage']}W)", bg=self.bg, fg=self.green,
                         font=("Consolas", 10), anchor="w").pack(side="left", fill="x", expand=True)
                tk.Button(r, text="Отключить (50%)", command=lambda pp=p: self.sell_psu(farm, pp),
                          bg=self.surface, fg=self.fg, font=("Consolas", 9),
                          relief="flat", cursor="hand2").pack(side="right")

        tk.Label(frame, text="— Синхронизатор БП (add2psu) —", bg=self.bg, fg=self.accent,
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=12, pady=(14, 3))
        sync_row = tk.Frame(frame, bg=self.bg); sync_row.pack(fill="x", padx=12, pady=2)
        if farm.synchronizer:
            tk.Label(sync_row, text="✓ Установлен — можно подключить 2-й БП",
                     bg=self.bg, fg=self.green, font=("Consolas", 10)).pack(side="left")
        else:
            tk.Label(sync_row, text="Нужен для подключения 2-го БП",
                     bg=self.bg, fg=self.fg, font=("Consolas", 10)).pack(side="left")
            if self.money >= SYNC_PRICE:
                tk.Button(sync_row, text=f"Купить {SYNC_PRICE:,}₽",
                          command=lambda: self.buy_sync(farm),
                          bg=self.yellow, fg=self.bg, font=("Consolas", 9, "bold"),
                          relief="flat", cursor="hand2").pack(side="right")
            else:
                tk.Button(sync_row, text=f"{SYNC_PRICE:,}₽", state="disabled",
                          bg=self.surface, fg=self.gray, font=("Consolas", 9)).pack(side="right")

        tk.Label(frame, text="— Доступные БП —", bg=self.bg, fg=self.accent,
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=12, pady=(14, 3))
        for psu in PSUS:
            row = tk.Frame(frame, bg=self.bg); row.pack(fill="x", padx=12, pady=2)
            tk.Label(row, text=f"{psu['name']} — {psu['wattage']}W — {psu['price']:,}₽",
                     bg=self.bg, fg=self.fg, font=("Consolas", 10), anchor="w").pack(side="left", fill="x", expand=True)

            if len(farm.psus) >= MAX_PSU:
                tk.Button(row, text=f"Макс. {MAX_PSU} БП", state="disabled", bg=self.surface,
                          fg=self.gray, font=("Consolas", 9)).pack(side="right")
            elif len(farm.psus) >= 1 and not farm.synchronizer:
                tk.Button(row, text="Нужен синхр.", state="disabled", bg=self.surface,
                          fg=self.gray, font=("Consolas", 9)).pack(side="right")
            elif self.money < psu["price"]:
                tk.Button(row, text=f"{psu['price']:,}₽", state="disabled", bg=self.surface,
                          fg=self.gray, font=("Consolas", 9)).pack(side="right")
            else:
                tk.Button(row, text=f"Добавить {psu['price']:,}₽",
                          command=lambda p=psu: self.buy_psu(farm, p),
                          bg=self.green, fg=self.bg, font=("Consolas", 9, "bold"),
                          relief="flat", cursor="hand2").pack(side="right")

    def _describe(self, cat, item):
        if cat == "mb": return f"{item['name']} | {item['socket']}/{item['ram']} | GPU×{item['max_gpu']} | {item['power']}Вт"
        if cat == "cpu": return f"{item['name']} | {item['socket']} | {item['power']}Вт"
        if cat == "ram": return f"{item['name']} | {item['type']} | {item['power']}Вт"
        if cat == "psu": return f"{item['name']} | {item['wattage']}Вт"
        if cat == "gpu": return f"{item['name']} | {item['hashrate']} MH/s | {item['power']}Вт"
        return item["name"]

    def check_compat(self, farm, cat, item):
        if cat == "mb":
            if farm.cpu and farm.cpu["socket"] != item["socket"]:
                return False, f"CPU {farm.cpu['socket']}≠{item['socket']}"
            if farm.ram and farm.ram["type"] != item["ram"]:
                return False, f"RAM {farm.ram['type']}≠{item['ram']}"
            if len(farm.gpus) > item["max_gpu"]:
                return False, f"Карт {len(farm.gpus)}>{item['max_gpu']}"
            if farm.psus:
                p = farm.power_draw()
                old_mb_power = farm.mb["power"] if farm.mb else 0
                p = p - old_mb_power + item["power"]
                if p > farm.total_wattage() * 0.85:
                    return False, f"БП {farm.total_wattage()}W не тянет {p}W"
        elif cat == "cpu":
            if not farm.mb: return False, "Сначала плата"
            if farm.mb["socket"] != item["socket"]:
                return False, f"Сокет {item['socket']}≠{farm.mb['socket']}"
        elif cat == "ram":
            if not farm.mb: return False, "Сначала плата"
            if farm.mb["ram"] != item["type"]:
                return False, f"Плата {farm.mb['ram']}≠{item['type']}"
        elif cat == "gpu":
            if not farm.mb: return False, "Сначала плата"
            if len(farm.gpus) >= farm.mb["max_gpu"]:
                return False, f"Слотов {farm.mb['max_gpu']}, занято {len(farm.gpus)}"
            if not farm.psus: return False, "Сначала БП"
            p = farm.power_draw() + item["power"]
            if p > farm.total_wattage() * 0.85:
                return False, f"БП не тянет ({p}W)"
        return True, ""

    def buy_component(self, farm, cat, item):
        ok, reason = self.check_compat(farm, cat, item)
        if not ok:
            error_sound(); self.log_msg(f"Нельзя: {reason}"); return
        if self.money < item["price"]:
            error_sound(); self.log_msg("Мало денег"); return
        self.money -= item["price"]
        if cat in ("mb", "cpu", "ram"):
            old = getattr(farm, cat)
            if old:
                refund = old["price"] // 2
                self.money += refund
                self.log_msg(f"Старый {old['name']} → {refund}₽")
            setattr(farm, cat, item)
        elif cat == "gpu":
            farm.gpus.append(item)
        self.log_msg(f"{farm.name}: куплено {item['name']} ({item['price']:,}₽)")
        self.update_ui(); self.build_shop()

    def buy_psu(self, farm, psu):
        if len(farm.psus) >= MAX_PSU:
            error_sound(); self.log_msg(f"Максимум {MAX_PSU} БП на ферму"); return
        if len(farm.psus) >= 1 and not farm.synchronizer:
            error_sound(); self.log_msg("Нужен синхронизатор для 2-го БП"); return
        if self.money < psu["price"]:
            error_sound(); self.log_msg("Мало денег"); return
        self.money -= psu["price"]
        farm.psus.append(psu)
        self.log_msg(f"{farm.name}: добавлен БП {psu['name']} (всего {farm.total_wattage()}W)")
        self.update_ui(); self.build_shop()

    def buy_sync(self, farm):
        if farm.synchronizer:
            self.log_msg("Синхронизатор уже есть"); return
        if self.money < SYNC_PRICE:
            error_sound(); self.log_msg(f"Нужно {SYNC_PRICE}₽"); return
        self.money -= SYNC_PRICE
        farm.synchronizer = True
        self.log_msg(f"{farm.name}: синхронизатор установлен")
        self.update_ui(); self.build_shop()

    def sell_component(self, farm, cat):
        item = getattr(farm, cat)
        if not item: return
        refund = item["price"] // 2
        self.money += refund
        setattr(farm, cat, None)
        self.log_msg(f"{farm.name}: {item['name']} снят за {refund}₽")
        self.update_ui(); self.build_shop()

    def sell_gpu(self, farm, gpu):
        if gpu in farm.gpus:
            refund = gpu["price"] // 2
            farm.gpus.remove(gpu)
            self.money += refund
            self.log_msg(f"{farm.name}: {gpu['name']} снят за {refund}₽")
            self.update_ui(); self.build_shop()

    def sell_psu(self, farm, psu):
        if psu in farm.psus:
            refund = psu["price"] // 2
            farm.psus.remove(psu)
            self.money += refund
            self.log_msg(f"{farm.name}: БП {psu['name']} отключён за {refund}₽")
            self.update_ui(); self.build_shop()

    def action(self, func):
        if self.ended: return
        func()
        if not self.ended: self.end_day()

    def work(self):
        self.money += 5000; self.energy -= 20; self.stress += 10
        self.log_msg("Работа: +5000₽, -20 энергии, +10 стресса")

    def rest(self):
        self.energy = min(100, self.energy + 30)
        self.stress = max(0, self.stress - 20)
        self.log_msg("Отдых: +30 энергии, -20 стресса")

    def mine_all(self):
        total = 0; any_ok = False
        for farm in self.farms:
            if not farm.unlocked or not farm.is_complete(): continue
            btc = farm.hashrate() * 0.00002
            total += btc; any_ok = True
            risk = {"room": 0.0, "balcony": 0.25, "garage": 0.40}.get(farm.location, 0.0)
            if risk > 0 and not farm.wiring_ok and random.random() < risk:
                if farm.gpus:
                    g = farm.gpus.pop()
                    error_sound()
                    self.log_msg(f"{farm.name}: проводка не выдержала! Сгорела {g['name']}")
        if not any_ok:
            error_sound(); self.log_msg("Нет готовых ферм"); return
        self.crypto_balance += total
        self.energy -= 10; self.stress += 5
        self.log_msg(f"Намайнено всего {total:.8f} BTC")

    def sell_crypto(self):
        if self.crypto_balance <= 0:
            self.log_msg("Нечего продавать"); return
        rev = int(self.crypto_balance * self.btc_price_rub)
        self.money += rev
        self.log_msg(f"Продано {self.crypto_balance:.8f} BTC за {rev:,}₽")
        self.crypto_balance = 0

    def unlock_farm(self, idx):
        farm = self.farms[idx]
        if farm.unlocked:
            self.log_msg("Уже открыто"); return
        if self.money < farm.setup_cost:
            error_sound(); self.log_msg(f"Нужно {farm.setup_cost:,}₽"); return
        self.money -= farm.setup_cost
        farm.unlocked = True
        self.active_farm = idx
        self.log_msg(f"Ферма '{farm.name}' открыта!")

    def legalize(self):
        if self.legal: self.log_msg("Уже легален"); return
        if self.money >= 10000:
            self.money -= 10000; self.legal = True
            self.tax_risk = max(0, self.tax_risk - 30)
            self.log_msg("Самозанятость оформлена")
        else: error_sound(); self.log_msg("Нужно 10000₽")

    def end_day(self):
        self.day += 1
        self.update_price()
        total_w = sum(f.power_draw() for f in self.farms if f.unlocked)
        if total_w > 0:
            bill = int(total_w / 1000 * 24 * 4.72)
            self.money -= bill
            self.log_msg(f"Свет ({total_w}Вт×24ч×4.72₽): -{bill}₽")
        self.process_event()
        self.anim_progress = 0.0; self.anim_target = 1.0
        self.check_end()
        self.update_ui()
        self.save_game()
        if not self.ended:
            self.log_msg(f"--- ДЕНЬ {self.day} ---")

    def update_price(self):
        if self.phase_days_left <= 0:
            roll = random.random()
            if roll < 0.35:
                self.market_phase = "bull"; self.trend_strength = random.uniform(0.0005, 0.003)
                self.base_volatility = random.uniform(0.015, 0.030)
            elif roll < 0.60:
                self.market_phase = "bear"; self.trend_strength = random.uniform(-0.003, -0.0005)
                self.base_volatility = random.uniform(0.020, 0.040)
            else:
                self.market_phase = "neutral"; self.trend_strength = random.uniform(-0.0003, 0.0003)
                self.base_volatility = random.uniform(0.010, 0.025)
            self.phase_days_left = random.randint(14, 42)
        self.phase_days_left -= 1
        ret = self.trend_strength + random.gauss(0, self.base_volatility)
        roll = random.random()
        if roll < 0.003:
            ret += random.choice([-1, 1]) * random.uniform(0.08, 0.15)
            self.log_msg("⚡ Резкое движение BTC!")
        elif roll < 0.015:
            ret += random.choice([-1, 1]) * random.uniform(0.04, 0.08)
            self.log_msg("📊 Сильное движение BTC")
        elif roll < 0.040:
            ret += random.choice([-1, 1]) * random.uniform(0.025, 0.04)
        ret = max(-0.20, min(0.20, ret))
        self.btc_price_rub *= (1 + ret)
        self.btc_price_rub = max(500000, self.btc_price_rub)
        self.price_history.append(self.btc_price_rub)
        if len(self.price_history) > 30: self.price_history.pop(0)

    def process_event(self):
        evs = [self.ev_bro, self.ev_neighbor, self.ev_cooler, self.ev_tax, self.ev_news]
        if random.random() < 0.5:
            random.choice(evs)()

    def ev_bro(self):
        self.log_msg("Крипто-бро: мем-коин x10!")
        if random.random() < 0.4:
            self.crypto_balance += 0.0001; self.log_msg("  +0.0001 BTC")
        else:
            self.money -= 3000; self.log_msg("  -3000₽")

    def ev_neighbor(self):
        self.neighbor_patience -= 20
        self.log_msg("Сосед: -20 терпения")

    def ev_cooler(self):
        for f in self.farms:
            if f.gpus and random.random() < 0.3:
                f.gpus.pop()
                self.log_msg(f"{f.name}: кулер отказал — карта вышла из строя")
                return

    def ev_tax(self):
        self.tax_risk += 10
        if self.legal:
            self.tax_risk = max(0, self.tax_risk - 20)
            self.log_msg("Налоговая: легален, всё ок")
        elif random.random() < self.tax_risk / 100:
            self.money -= 20000; error_sound()
            self.log_msg("Налоговая: штраф 20000₽")
        else:
            self.log_msg("Налоговая: пронесло")

    def ev_news(self):
        if self.market_phase == "bull":
            self.btc_price_rub *= 1.05; self.log_msg("Новость: BTC +5%")
        elif self.market_phase == "bear":
            self.btc_price_rub *= 0.95; self.log_msg("Новость: BTC -5%")
        self.price_history[-1] = self.btc_price_rub

    def update_ui(self):
        self.lbl_day.config(text=f"День {self.day}")
        self.lbl_money.config(text=f"{self.money:,}₽")
        self.lbl_energy.config(text=f"Энергия: {self.energy}")
        self.lbl_stress.config(text=f"Стресс: {self.stress}")
        farm = self.farms[self.active_farm]
        self.lbl_active.config(text=f"Активна: {farm.location_icon} {farm.name}")
        self.draw_bar(self.bar_energy, self.energy, self.yellow)
        self.draw_bar(self.bar_stress, self.stress, self.red)
        self.draw_bar(self.bar_neighbor, self.neighbor_patience, self.accent)

    def draw_bar(self, c, v, color):
        c.delete("all"); c.update_idletasks()
        w = c.winfo_width() or 800; h = int(c.cget("height"))
        c.create_rectangle(0, 0, int(w * max(0, min(100, v)) / 100), h, fill=color, outline="")

    def check_end(self):
        if self.ended: return
        if self.money < -50000:
            self.ended = True; error_sound()
            messagebox.showinfo("Конец", "💀 Долговая яма")
            self.save_score("Долговая яма"); self.restart()
        if self.stress >= 100:
            self.ended = True; error_sound()
            messagebox.showinfo("Конец", "💀 Выгорание")
            self.save_score("Выгорание"); self.restart()

    def save_score(self, title):
        scores = []
        if os.path.exists(SCORES_FILE):
            try:
                with open(SCORES_FILE, "r", encoding="utf-8") as f: scores = json.load(f)
            except: scores = []
        total_farms = sum(1 for f in self.farms if f.unlocked)
        total_gpus = sum(len(f.gpus) for f in self.farms)
        scores.append({"title": title, "money": self.money, "day": self.day,
                       "cards": total_gpus, "farms": total_farms,
                       "crypto": round(self.crypto_balance * self.btc_price_rub)})
        scores = sorted(scores, key=lambda x: x["money"], reverse=True)[:10]
        try:
            with open(SCORES_FILE, "w", encoding="utf-8") as f:
                json.dump(scores, f, ensure_ascii=False, indent=2)
        except: pass

    def restart(self):
        if messagebox.askyesno("Ещё раз?", "Начать новую игру?"):
            self.root.destroy(); main()


def show_scores(root):
    win = tk.Toplevel(root); win.title("Рекорды"); win.geometry("700x420"); win.configure(bg="#1e1e2e")
    tk.Label(win, text="🏆 РЕКОРДЫ", font=("Consolas", 18, "bold"), bg="#1e1e2e", fg="#f9e2af").pack(pady=10)
    scores = []
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f: scores = json.load(f)
        except: pass
    if not scores:
        tk.Label(win, text="Пока пусто", bg="#1e1e2e", fg="#cdd6f4", font=("Consolas", 12)).pack(pady=30)
    else:
        f = tk.Frame(win, bg="#1e1e2e"); f.pack(fill="both", expand=True, padx=20, pady=10)
        for i, h in enumerate(["#", "Концовка", "Деньги", "День", "Ферм", "Карт", "Крипта"]):
            tk.Label(f, text=h, bg="#1e1e2e", fg="#89b4fa", font=("Consolas", 10, "bold")).grid(row=0, column=i, padx=6, pady=4)
        for r, s in enumerate(scores, 1):
            vals = [r, s["title"], f"{s['money']:,}₽", s["day"], s.get("farms", 1), s["cards"], f"{s['crypto']:,}₽"]
            for c, v in enumerate(vals):
                tk.Label(f, text=str(v), bg="#1e1e2e", fg="#cdd6f4", font=("Consolas", 10)).grid(row=r, column=c, padx=6, pady=2)
    tk.Button(win, text="Закрыть", command=win.destroy, bg="#313244", fg="#cdd6f4",
              font=("Consolas", 11), relief="flat", padx=20, pady=6).pack(pady=10)


def main():
    if HAS_BOOTSTRAP:
        root = tb.Window(themename="darkly")
    else:
        root = tk.Tk(); root.configure(bg="#1e1e2e")
    make_icon(root)

    def start_new():
        for w in root.winfo_children(): w.destroy()
        GameGUI(root, load=False)

    def continue_game():
        for w in root.winfo_children(): w.destroy()
        GameGUI(root, load=True)

    frame = tk.Frame(root, bg="#1e1e2e"); frame.pack(fill="both", expand=True)
    tk.Label(frame, text="🖥️ КОМПЬЮТЕРЩИК 2.0", font=("Consolas", 30, "bold"),
             bg="#1e1e2e", fg="#cdd6f4").pack(pady=(80, 5))
    tk.Label(frame, text="3 фермы • 2 БП • реальные хешрейты",
             font=("Consolas", 13), bg="#1e1e2e", fg="#a6adc8").pack(pady=(0, 30))

    tk.Button(frame, text="▶ НОВАЯ ИГРА", command=start_new, bg="#89b4fa", fg="#1e1e2e",
              font=("Consolas", 14, "bold"), relief="flat", padx=40, pady=12, cursor="hand2").pack(pady=8)
    btn_c = tk.Button(frame, text="📂 ПРОДОЛЖИТЬ", command=continue_game, bg="#a6e3a1", fg="#1e1e2e",
                      font=("Consolas", 14, "bold"), relief="flat", padx=40, pady=12, cursor="hand2")
    if os.path.exists(SAVE_FILE): btn_c.pack(pady=8)
    else: btn_c.config(state="disabled", bg="#313244", fg="#585b70"); btn_c.pack(pady=8)
    tk.Button(frame, text="🏆 РЕКОРДЫ", command=lambda: show_scores(root), bg="#f9e2af", fg="#1e1e2e",
              font=("Consolas", 13, "bold"), relief="flat", padx=40, pady=10, cursor="hand2").pack(pady=8)
    tk.Button(frame, text="Выход", command=root.quit, bg="#313244", fg="#cdd6f4",
              font=("Consolas", 11), relief="flat", padx=20, pady=6, cursor="hand2").pack(pady=20)
    root.mainloop()


if __name__ == "__main__":
    main()
