import tkinter as tk
from tkinter import messagebox
import random
import json
import os

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

SAVE_FILE = "savegame.json"
SCORES_FILE = "scores.json"


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


# ---------- СТАРТОВОЕ МЕНЮ ----------
class StartMenu:
    def __init__(self, root, on_start, on_continue, on_scores):
        self.root = root
        self.frame = tk.Frame(root, bg="#1e1e2e")
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="🖥️", font=("Segoe UI Emoji", 64),
                 bg="#1e1e2e", fg="#89b4fa").pack(pady=(40, 0))
        tk.Label(self.frame, text="КОМПЬЮТЕРЩИК 2.0",
                 font=("Consolas", 28, "bold"), bg="#1e1e2e", fg="#cdd6f4").pack(pady=5)
        tk.Label(self.frame, text="Крипто-ветка: майнинг, балкон, гараж, налоговая",
                 font=("Consolas", 13), bg="#1e1e2e", fg="#a6adc8").pack(pady=(0, 20))

        has_save = os.path.exists(SAVE_FILE)

        tk.Button(self.frame, text="▶ НОВАЯ ИГРА", command=on_start,
                  bg="#89b4fa", fg="#1e1e2e", font=("Consolas", 14, "bold"),
                  relief="flat", padx=30, pady=12, cursor="hand2",
                  activebackground="#b4befe").pack(pady=8)

        btn_cont = tk.Button(self.frame, text="📂 ПРОДОЛЖИТЬ", command=on_continue,
                             bg="#a6e3a1", fg="#1e1e2e", font=("Consolas", 14, "bold"),
                             relief="flat", padx=30, pady=12, cursor="hand2",
                             activebackground="#94e2d5")
        if has_save:
            btn_cont.pack(pady=8)
        else:
            btn_cont.config(state="disabled", bg="#313244", fg="#585b70")

        tk.Button(self.frame, text="🏆 РЕКОРДЫ", command=on_scores,
                  bg="#f9e2af", fg="#1e1e2e", font=("Consolas", 13, "bold"),
                  relief="flat", padx=30, pady=10, cursor="hand2",
                  activebackground="#fab387").pack(pady=8)

        tk.Button(self.frame, text="Выход", command=root.quit,
                  bg="#313244", fg="#cdd6f4", font=("Consolas", 11),
                  relief="flat", padx=20, pady=6, cursor="hand2",
                  activebackground="#45475a").pack(pady=10)

        tk.Label(self.frame, text="v2.1 • Tkinter edition • с сохранениями",
                 font=("Consolas", 9), bg="#1e1e2e", fg="#585b70").pack(side="bottom", pady=8)


# ---------- ИГРА ----------
class GameGUI:
    def __init__(self, root, load=False):
        self.root = root
        self.root.title("Компьютерщик 2.0: Крипто-ветка")
        self.root.geometry("940x800")
        self.root.configure(bg="#1e1e2e")
        self.root.minsize(820, 720)

        self.init_state()
        if load:
            self.load_game()

        self.bg = "#1e1e2e"
        self.fg = "#cdd6f4"
        self.accent = "#89b4fa"
        self.green = "#a6e3a1"
        self.red = "#f38ba8"
        self.yellow = "#f9e2af"
        self.surface = "#313244"
        self.dark = "#181825"

        self.anim_progress = 1.0
        self.anim_target = 1.0

        self.build_ui()
        self.update_ui()
        self.animate_chart()

    def init_state(self):
        self.day = 1
        self.money = 15000
        self.energy = 100
        self.stress = 20
        self.cards = 0
        self.hashrate = 0
        self.crypto_balance = 0.0
        self.crypto_price = 100.0
        self.price_history = [100.0] * 14
        self.trend = 0.0
        self.volatility = 0.02
        self.neighbor_patience = 100
        self.balcony = False
        self.garage = False
        self.wiring_ok = True
        self.legal = False
        self.tax_risk = 0
        self.ended = False

    # ---------- СОХРАНЕНИЕ ----------
    def save_game(self):
        data = {k: v for k, v in self.__dict__.items()
                if k not in ("root", "bg", "fg", "accent", "green", "red",
                             "yellow", "surface", "dark", "anim_progress",
                             "anim_target", "log", "chart", "bar_energy",
                             "bar_stress", "bar_neighbor", "lbl_day",
                             "lbl_money", "lbl_energy", "lbl_stress",
                             "lbl_farm", "lbl_crypto")}
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.log_msg("💾 Игра сохранена.")
        except Exception as e:
            self.log_msg(f"❌ Ошибка сохранения: {e}")

    def load_game(self):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.items():
                if hasattr(self, k):
                    setattr(self, k, v)
        except Exception as e:
            print("Не удалось загрузить сохранение:", e)

    # ---------- UI ----------
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
        self.bar_energy = tk.Canvas(bars, height=18, bg=self.surface, highlightthickness=0)
        self.bar_energy.pack(fill="x", pady=2)
        self.bar_stress = tk.Canvas(bars, height=18, bg=self.surface, highlightthickness=0)
        self.bar_stress.pack(fill="x", pady=2)
        self.bar_neighbor = tk.Canvas(bars, height=18, bg=self.surface, highlightthickness=0)
        self.bar_neighbor.pack(fill="x", pady=2)

        info = tk.Frame(self.root, bg=self.bg)
        info.pack(fill="x", padx=12, pady=6)
        self.lbl_farm = tk.Label(info, text="", fg=self.fg, bg=self.bg,
                                 font=("Consolas", 11), justify="left")
        self.lbl_farm.pack(side="left")
        self.lbl_crypto = tk.Label(info, text="", fg=self.accent, bg=self.bg,
                                   font=("Consolas", 11), justify="right")
        self.lbl_crypto.pack(side="right")

        self.chart = tk.Canvas(self.root, height=190, bg=self.dark, highlightthickness=0)
        self.chart.pack(fill="x", padx=12, pady=6)

        btns = tk.Frame(self.root, bg=self.bg)
        btns.pack(fill="x", padx=12, pady=6)
        actions = [
            ("💼 Работать", self.work),
            ("🖥️ Купить карту (30к)", self.buy_card),
            ("🏠 Балкон (20к)", self.build_balcony),
            ("🏭 Гараж (80к)", self.build_garage),
            ("⚡ Проводка (15к)", self.upgrade_wiring),
            ("⛏️ Майнить", self.mine),
            ("💰 Продать крипту", self.sell_crypto),
            ("😴 Отдохнуть", self.rest),
            ("🧾 Самозанятость (10к)", self.legalize),
            ("💾 Сохранить", self.save_game),
            ("📅 Завершить день", self.end_day),
        ]
        for i, (text, cmd) in enumerate(actions):
            b = tk.Button(btns, text=text, command=lambda c=cmd: self._btn(c),
                          bg=self.surface, fg=self.fg,
                          activebackground=self.accent, activeforeground=self.bg,
                          font=("Consolas", 10), relief="flat", padx=8, pady=8,
                          cursor="hand2")
            b.grid(row=i // 3, column=i % 3, padx=4, pady=4, sticky="ew")
        for c in range(3):
            btns.grid_columnconfigure(c, weight=1)

        self.log = tk.Text(self.root, height=7, bg=self.dark, fg=self.fg,
                           font=("Consolas", 10), relief="flat", state="disabled",
                           wrap="word")
        self.log.pack(fill="both", expand=True, padx=12, pady=6)

    def _btn(self, cmd):
        click_sound()
        cmd()

    # ---------- ОБНОВЛЕНИЕ ----------
    def update_ui(self):
        self.lbl_day.config(text=f"📅 День {self.day}/30")
        self.lbl_money.config(text=f"💰 {self.money} ₽")
        self.lbl_energy.config(text=f"⚡ {self.energy}")
        self.lbl_stress.config(text=f"😰 {self.stress}")

        self.draw_bar(self.bar_energy, self.energy, self.green)
        self.draw_bar(self.bar_stress, self.stress, self.red)
        self.draw_bar(self.bar_neighbor, self.neighbor_patience, self.accent)

        loc = "балкон" if self.balcony else "комната"
        if self.garage:
            loc = "гараж"
        self.lbl_farm.config(
            text=f"🖥️ Карт: {self.cards} | ⛏️ Хешрейт: {self.hashrate} | 📍 {loc}\n"
                 f"⚡ Проводка: {'ок' if self.wiring_ok else 'риск'}\n"
                 f"🧾 Легально: {'да' if self.legal else 'нет'} | Риск налоговой: {self.tax_risk}%"
        )
        trend_icon = "🐂" if self.trend > 0.3 else "🐻" if self.trend < -0.3 else "🦀"
        self.lbl_crypto.config(
            text=f"🪙 Баланс: {self.crypto_balance:.6f}\n"
                 f"💵 Курс: {self.crypto_price:.1f}\n"
                 f"🧭 Тренд: {trend_icon}"
        )

    def draw_bar(self, canvas, value, color):
        canvas.delete("all")
        canvas.update_idletasks()
        w = canvas.winfo_width() or 800
        h = int(canvas.cget("height"))
        fill = int(w * max(0, min(100, value)) / 100)
        canvas.create_rectangle(0, 0, fill, h, fill=color, outline="")

    def animate_chart(self):
        if self.anim_progress < self.anim_target:
            self.anim_progress = min(self.anim_target, self.anim_progress + 0.08)
            self.draw_chart(self.anim_progress)
        self.root.after(30, self.animate_chart)

    def draw_chart(self, progress=1.0):
        c = self.chart
        c.delete("all")
        c.update_idletasks()
        w = c.winfo_width() or 800
        h = int(c.cget("height"))
        hist = self.price_history
        lo, hi = min(hist), max(hist)
        if hi - lo < 0.01:
            hi = lo + 1
        pad = 14
        points = []
        for i, p in enumerate(hist):
            x = pad + (w - 2 * pad) * i / (len(hist) - 1)
            y = h - pad - (h - 2 * pad) * (p - lo) / (hi - lo)
            points.append((x, y))
        n = max(2, int(len(points) * progress))
        poly = [(points[0][0], h - pad)] + points[:n] + [(points[n - 1][0], h - pad)]
        c.create_polygon(poly, fill="#1e2a3a", outline="")
        for i in range(n - 1):
            c.create_line(points[i], points[i + 1], fill=self.accent, width=2)
        if n >= 2:
            c.create_oval(points[n - 1][0] - 4, points[n - 1][1] - 4,
                          points[n - 1][0] + 4, points[n - 1][1] + 4,
                          fill=self.accent, outline="")
        c.create_text(10, 10, text=f"{hi:.1f}", fill=self.fg, anchor="nw", font=("Consolas", 9))
        c.create_text(10, h - 10, text=f"{lo:.1f}", fill=self.fg, anchor="sw", font=("Consolas", 9))
        change = (hist[-1] / hist[0] - 1) * 100
        color = self.green if change >= 0 else self.red
        c.create_text(w - 10, 10, text=f"{change:+.1f}% за 14 дней",
                      fill=color, anchor="ne", font=("Consolas", 10, "bold"))

    def refresh_chart(self):
        self.anim_progress = 0.0
        self.anim_target = 1.0

    def log_msg(self, text):
        self.log.config(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    # ---------- ДЕЙСТВИЯ ----------
    def work(self):
        self.money += 5000
        self.energy -= 20
        self.stress += 10
        self.log_msg("💼 Работа: +5000 ₽, энергия -20, стресс +10.")
        self.check_end()
        self.update_ui()

    def buy_card(self):
        if self.money >= 30000:
            self.money -= 30000
            self.cards += 1
            self.hashrate += 2
            self.log_msg("🖥️ Купил карту. Хешрейт +2.")
        else:
            error_sound()
            self.log_msg("❌ Не хватает денег (нужно 30000 ₽).")
        self.update_ui()

    def build_balcony(self):
        if self.balcony:
            self.log_msg("Балкон уже оборудован.")
        elif self.money >= 20000:
            self.money -= 20000
            self.balcony = True
            self.log_msg("🏠 Оборудовал ферму на балконе.")
        else:
            error_sound()
            self.log_msg("❌ Нужно 20000 ₽.")
        self.update_ui()

    def build_garage(self):
        if self.garage:
            self.log_msg("Гараж уже оборудован.")
        elif not self.balcony:
            error_sound()
            self.log_msg("❌ Сначала оборудуй балкон.")
        elif self.money >= 80000:
            self.money -= 80000
            self.garage = True
            self.hashrate += 5
            self.log_msg("🏭 Оборудовал гараж! Хешрейт +5, но и расходы выросли.")
        else:
            error_sound()
            self.log_msg("❌ Нужно 80000 ₽.")
        self.update_ui()

    def upgrade_wiring(self):
        if self.wiring_ok:
            self.log_msg("Проводка уже в порядке.")
        elif self.money >= 15000:
            self.money -= 15000
            self.wiring_ok = True
            self.log_msg("⚡ Провёл отдельную линию.")
        else:
            error_sound()
            self.log_msg("❌ Нужно 15000 ₽.")
        self.update_ui()

    def mine(self):
        if self.cards == 0:
            error_sound()
            self.log_msg("❌ Нет карт.")
            return
        mined = self.hashrate * 0.001 * random.uniform(0.8, 1.2)
        self.crypto_balance += mined
        self.energy -= 10
        self.stress += 5
        self.log_msg(f"⛏️ Намайнил {mined:.6f}.")
        # Риск проводки: балкон 25%, гараж 40% если не починена
        risk = 0.25 if self.balcony else 0.0
        if self.garage:
            risk = 0.40
        if risk > 0 and not self.wiring_ok and random.random() < risk:
            error_sound()
            self.log_msg("🔥 Проводка не выдержала! Карта сгорела.")
            self.cards = max(0, self.cards - 1)
            self.hashrate = max(0, self.hashrate - 2)
            self.money -= 5000
        self.check_end()
        self.update_ui()

    def sell_crypto(self):
        if self.crypto_balance <= 0:
            self.log_msg("Нечего продавать.")
        else:
            revenue = int(self.crypto_balance * self.crypto_price)
            self.money += revenue
            self.log_msg(f"💰 Продал за {revenue} ₽.")
            self.crypto_balance = 0
        self.update_ui()

    def rest(self):
        self.energy = min(100, self.energy + 30)
        self.stress = max(0, self.stress - 20)
        self.log_msg("😴 Отдых: энергия +30, стресс -20.")
        self.update_ui()

    def legalize(self):
        if self.legal:
            self.log_msg("Ты уже легален.")
        elif self.money >= 10000:
            self.money -= 10000
            self.legal = True
            self.tax_risk = max(0, self.tax_risk - 30)
            self.log_msg("🧾 Оформил самозанятость.")
        else:
            error_sound()
            self.log_msg("❌ Нужно 10000 ₽.")
        self.update_ui()

    # ---------- ДЕНЬ ----------
    def end_day(self):
        if self.ended:
            return
        self.day += 1
        self.update_price()
        if self.neighbor_patience <= 0:
            error_sound()
            self.log_msg("🚨 Сосед вызвал полицию. Ферму выключили.")
            self.neighbor_patience = 50
            self.hashrate = max(0, self.hashrate - 2)
        self.random_event()
        self.refresh_chart()
        if self.day > 30:
            self.final()
            return
        self.check_end()
        self.update_ui()
        self.save_game()

    def update_price(self):
        if random.random() < 0.15:
            self.trend = random.uniform(-1, 1)
            self.volatility = random.uniform(0.01, 0.06)
        drift = self.trend * 0.03
        shock = random.gauss(0, self.volatility)
        if random.random() < 0.03:
            shock += random.choice([-1, 1]) * random.uniform(0.15, 0.35)
        self.crypto_price *= (1 + drift + shock)
        self.crypto_price = max(1.0, self.crypto_price)
        self.price_history.append(self.crypto_price)
        if len(self.price_history) > 14:
            self.price_history.pop(0)

    def random_event(self):
        events = [self.ev_bro, self.ev_neighbor, self.ev_bill, self.ev_cooler, self.ev_tax]
        if abs(self.trend) > 0.5 and random.random() < 0.5:
            events.append(self.ev_news)
        if self.garage:
            events.append(self.ev_theft)
        random.choice(events)()

    def ev_bro(self):
        self.log_msg("⚡ Крипто-бро: «Мем-коин, x10!»")
        if random.random() < 0.4:
            self.crypto_balance += 20
            self.log_msg("   Повезло! +20 монет.")
        else:
            self.money -= 3000
            self.log_msg("   Не повезло. -3000 ₽.")

    def ev_neighbor(self):
        self.neighbor_patience -= 20
        self.log_msg("⚡ Сосед стучит: «Это что, самолёт?» Терпение -20.")

    def ev_bill(self):
        bill = self.cards * 1500 + (1000 if self.balcony else 0) + (3000 if self.garage else 0)
        self.money -= bill
        self.log_msg(f"⚡ Счёт за свет: -{bill} ₽.")

    def ev_cooler(self):
        if self.cards > 0:
            self.hashrate = max(0, self.hashrate - 1)
            self.log_msg("⚡ Кулер загудел. Хешрейт -1.")

    def ev_tax(self):
        self.tax_risk += 10
        if self.legal:
            self.tax_risk = max(0, self.tax_risk - 20)
            self.log_msg("⚡ Налоговая: ты легален, отделался испугом.")
        elif random.random() < self.tax_risk / 100:
            self.money -= 20000
            error_sound()
            self.log_msg("⚡ Налоговая: штраф 20000 ₽.")
        else:
            self.log_msg("⚡ Налоговая: пока пронесло.")

    def ev_news(self):
        if self.trend > 0.3:
            self.crypto_price *= 1.1
            self.log_msg("⚡ Новость: фонд покупает. Курс +10%.")
        else:
            self.crypto_price *= 0.9
            self.log_msg("⚡ Новость: регулятор давит. Курс -10%.")
        self.price_history[-1] = self.crypto_price

    def ev_theft(self):
        if random.random() < 0.3:
            error_sound()
            self.cards = max(0, self.cards - 1)
            self.hashrate = max(0, self.hashrate - 2)
            self.log_msg("🚨 Гараж вскрыли! Одна карта украдена.")
        else:
            self.log_msg("🚨 Кто-то крутился у гаража, но обошлось.")

    # ---------- КОНЕЦ ----------
    def check_end(self):
        if self.ended:
            return
        if self.money < -50000:
            self.ended = True
            error_sound()
            messagebox.showinfo("Конец", "💀 Долговая яма. Игра окончена.")
            self.save_score("Долговая яма", self.money)
            self.restart_prompt()
        if self.stress >= 100:
            self.ended = True
            error_sound()
            messagebox.showinfo("Конец", "💀 Выгорание. Игра окончена.")
            self.save_score("Выгорание", self.money)
            self.restart_prompt()

    def final(self):
        self.ended = True
        if self.crypto_balance * self.crypto_price > 200000:
            msg, title = "🏆 «Крипто-магнат»: квартира есть, но графики не отпускают.", "Крипто-магнат"
        elif self.legal and self.cards >= 3 and self.money > 50000:
            msg, title = "🏆 «Легальный фермер»: платишь налоги, спишь спокойно.", "Легальный фермер"
        elif self.money < 0:
            msg, title = "💀 «Отрицательный баланс, положительный опыт».", "Долговая яма"
        else:
            msg, title = "🏆 «Тихая гавань»: работаешь, майнишь потихоньку.", "Тихая гавань"
        messagebox.showinfo("Итоги 30 дней", msg)
        self.save_score(title, self.money)
        if os.path.exists(SAVE_FILE):
            try: os.remove(SAVE_FILE)
            except Exception: pass
        self.restart_prompt()

    def save_score(self, title, money):
        scores = []
        if os.path.exists(SCORES_FILE):
            try:
                with open(SCORES_FILE, "r", encoding="utf-8") as f:
                    scores = json.load(f)
            except Exception:
                scores = []
        scores.append({"title": title, "money": money, "day": self.day,
                       "cards": self.cards, "crypto": round(self.crypto_balance * self.crypto_price)})
        scores = sorted(scores, key=lambda x: x["money"], reverse=True)[:10]
        try:
            with open(SCORES_FILE, "w", encoding="utf-8") as f:
                json.dump(scores, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def restart_prompt(self):
        if messagebox.askyesno("Ещё раз?", "Сыграем заново?"):
            self.root.destroy()
            main()


# ---------- РЕКОРДЫ ----------
def show_scores(root):
    win = tk.Toplevel(root)
    win.title("🏆 Таблица рекордов")
    win.geometry("600x400")
    win.configure(bg="#1e1e2e")
    tk.Label(win, text="🏆 РЕКОРДЫ", font=("Consolas", 18, "bold"),
             bg="#1e1e2e", fg="#f9e2af").pack(pady=10)
    scores = []
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                scores = json.load(f)
        except Exception:
            pass
    if not scores:
        tk.Label(win, text="Пока пусто. Сыграй первую игру!",
                 bg="#1e1e2e", fg="#cdd6f4", font=("Consolas", 12)).pack(pady=30)
    else:
        frame = tk.Frame(win, bg="#1e1e2e")
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        headers = ["#", "Концовка", "Деньги", "День", "Карт", "Крипта"]
        for i, h in enumerate(headers):
            tk.Label(frame, text=h, bg="#1e1e2e", fg="#89b4fa",
                     font=("Consolas", 11, "bold")).grid(row=0, column=i, padx=8, pady=4)
        for r, s in enumerate(scores, 1):
            vals = [r, s["title"], f"{s['money']} ₽", s["day"], s["cards"], f"{s['crypto']} ₽"]
            for c, v in enumerate(vals):
                tk.Label(frame, text=str(v), bg="#1e1e2e", fg="#cdd6f4",
                         font=("Consolas", 10)).grid(row=r, column=c, padx=8, pady=2)
    tk.Button(win, text="Закрыть", command=win.destroy, bg="#313244", fg="#cdd6f4",
              font=("Consolas", 11), relief="flat", padx=20, pady=6).pack(pady=10)


def main():
    root = tk.Tk()
    make_icon(root)

    def start_new():
        for w in root.winfo_children():
            w.destroy()
        GameGUI(root, load=False)

    def continue_game():
        for w in root.winfo_children():
            w.destroy()
        GameGUI(root, load=True)

    def open_scores():
        show_scores(root)

    StartMenu(root, start_new, continue_game, open_scores)
    root.mainloop()


if __name__ == "__main__":
    main()