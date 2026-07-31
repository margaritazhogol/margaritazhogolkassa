import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime


class SelfServiceCheckout:
    def __init__(self, root):
        self.root = root
        self.root.title("Касса самообслуживания | Дипломный проект")

        # 2. Увеличенное окно и минимальный размер
        self.root.geometry("900x650")
        self.root.minsize(900, 650)
        self.root.configure(bg="#eef2f7")  # 12. Главный фон обновлен

        # Настройка стилей для ttk виджетов
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background="#eef2f7", foreground="#000000")
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.style.configure("Treeview", font=("Segoe UI", 10), background="#ffffff", foreground="#000000")

        self.db_file = "inventory.json"
        self.receipts_dir = "receipts"
        self.password = "123456"
        self.cart = {}
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_products)  # 7. Живой поиск

        if not os.path.exists(self.receipts_dir):
            os.makedirs(self.receipts_dir)

        self.inventory = self.load_data()
        self.main_menu()

    def load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not data:  # 8. Добавляем эмодзи, если файл пуст
                        return {"🍞 Хлеб": [50, 10], "🥛 Молоко": [90, 5], "🍎 Яблоки": [120, 20], "🥚 Яйца": [110, 15]}
                    return data
            except Exception:
                return {"🍞 Хлеб": [50, 10], "🥛 Молоко": [90, 5], "🍎 Яблоки": [120, 20], "🥚 Яйца": [110, 15]}
        return {"🍞 Хлеб": [50, 10], "🥛 Молоко": [90, 5], "🍎 Яблоки": [120, 20], "🥚 Яйца": [110, 15]}

    def save_data(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.inventory, f, ensure_ascii=False, indent=4)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_scrollable_container(self):
        """Создает область с прокруткой (с исправленной прокруткой колесиком мыши)"""
        container = tk.Frame(self.root, bg="#eef2f7")
        container.pack(fill="both", expand=True, padx=15, pady=10)

        canvas = tk.Canvas(container, bg="#eef2f7", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#eef2f7")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)


        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return self.scrollable_frame

    # --- ГЛАВНОЕ МЕНЮ ---
    def main_menu(self):
        self.clear_window()
        self.root.configure(bg="#eef2f7")
        self.root.unbind_all("<MouseWheel>")  # Сбрасываем скролл при выходе

        # 3. Красивая шапка
        tk.Label(self.root, text="🛒 Smart Checkout", font=("Segoe UI", 32, "bold"),
                 bg="#eef2f7", fg="#000000").pack(pady=(40, 0))

        tk.Label(self.root, text="Касса самообслуживания", font=("Segoe UI", 16),
                 bg="#eef2f7", fg="#000000").pack(pady=(5, 0))

        tk.Label(self.root, text="Дипломный проект", font=("Segoe UI", 10),
                 bg="#eef2f7", fg="#000000").pack(pady=(5, 30))

        # 13. Одинаковые кнопки
        btn_customer = tk.Button(self.root, text="🛒  Я покупатель", font=("Segoe UI", 12, "bold"),
                                 bg="#27ae60", fg="#000000", activebackground="#2ecc71",
                                 width=25, height=2, relief="flat", cursor="hand2",
                                 command=self.customer_menu)
        btn_customer.pack(pady=10)

        btn_staff = tk.Button(self.root, text="👤  Я сотрудник", font=("Segoe UI", 12, "bold"),
                              bg="#2980b9", fg="#000000", activebackground="#3498db",
                              width=25, height=2, relief="flat", cursor="hand2",
                              command=self.staff_login)
        btn_staff.pack(pady=10)

        # 11. Нижний статус
        tk.Label(self.root, text="Авторы: Жоголь Маргарита и Егор Семкин | Python • Tkinter | 2026",
                 font=("Segoe UI", 9), bg="#eef2f7", fg="#000000").pack(side="bottom", pady=15)

    # --- ЛОГИКА СОТРУДНИКА ---
    def staff_login(self):
        pwd = simpledialog.askstring("Авторизация", "Введите пароль сотрудника:", show='*')
        if pwd == self.password:
            self.staff_menu()
        elif pwd is not None:
            messagebox.showerror("⚠ Ошибка", "Неверный пароль!")

    def staff_menu(self):
        self.clear_window()
        self.root.configure(bg="#eef2f7")
        self.root.unbind_all("<MouseWheel>")

        ttk.Label(self.root, text="⚙ Управление складом", style="Header.TLabel").pack(pady=15)

        tree_frame = tk.Frame(self.root, bg="#eef2f7")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("name", "price", "qty")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

        self.tree.heading("name", text="Название товара")
        self.tree.heading("price", text="Цена (руб.)")
        self.tree.heading("qty", text="Остаток (шт.)")

        self.tree.column("name", width=350)
        self.tree.column("price", width=150, anchor="center")
        self.tree.column("qty", width=150, anchor="center")

        for name, data in self.inventory.items():
            # 9. Статус товара цветом (упрощенно через эмодзи для студента)
            status = "🟢" if data[1] > 10 else "🟡" if data[1] > 3 else "🔴"
            self.tree.insert("", "end", values=(name, f"{data[0]} руб.", f"{status} {data[1]} шт."))

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_frame = tk.Frame(self.root, bg="#eef2f7")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="➕ Добавить товар", bg="#27ae60", fg="#000000", font=("Segoe UI", 10, "bold"),
                  width=20, relief="flat", cursor="hand2", command=self.add_item).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="🗑 Удалить выбранное", bg="#e74c3c", fg="#000000", font=("Segoe UI", 10, "bold"),
                  width=20, relief="flat", cursor="hand2", command=self.delete_selected_item).grid(row=0, column=1,
                                                                                                   padx=10)

        tk.Button(self.root, text="← Назад в главное меню", bg="#5d6d7e", fg="#000000", font=("Segoe UI", 10, "bold"),
                  width=25, relief="flat", cursor="hand2", command=self.main_menu).pack(pady=10)

    def delete_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("⚠ Внимание", "Выберите товар в таблице для удаления!")
            return

        item_values = self.tree.item(selected[0], "values")
        name = item_values[0]

        if messagebox.askyesno("Подтверждение", f"Удалить товар '{name}' со склада?"):
            del self.inventory[name]
            self.save_data()
            self.staff_menu()

    def add_item(self):
        name = simpledialog.askstring("Новый товар", "Название (можно с эмодзи):")
        if not name: return
        try:
            p = int(simpledialog.askstring("Цена", "Цена за штуку (руб.):"))
            q = int(simpledialog.askstring("Количество", "Количество на складе (шт.):"))
            self.inventory[name] = [p, q]
            self.save_data()
            self.staff_menu()
        except (ValueError, TypeError):
            messagebox.showerror("⚠ Ошибка", "Введите корректные целые числа!")

    # --- ЛОГИКА ПОКУПАТЕЛЯ ---
    def customer_menu(self):
        self.clear_window()
        self.root.configure(bg="#eef2f7")

        # Шапка
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🛒 Витрина магазина", font=("Segoe UI", 16, "bold"),
                 bg="#2c3e50", fg="#ffffff").pack(side="left", padx=20, pady=10)

        # 7. Поиск
        search_frame = tk.Frame(header, bg="#2c3e50")
        search_frame.pack(side="left", padx=20, pady=10)
        tk.Label(search_frame, text="🔍", font=("Segoe UI", 12), bg="#2c3e50", fg="#ffffff").pack(side="left",
                                                                                                 padx=(0, 5))
        tk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 10), width=25, bg="#ffffff",
                 fg="#000000").pack(side="left")

        # Основной контейнер: Слева товары, Справа корзина (Пункт 6)
        main_container = tk.Frame(self.root, bg="#eef2f7")
        main_container.pack(fill="both", expand=True, padx=15, pady=10)

        left_frame = tk.Frame(main_container, bg="#eef2f7", width=600)
        left_frame.pack(side="left", fill="both", expand=True)

        right_frame = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=1, width=250)
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        right_frame.pack_propagate(False)

        # Правая панель: Корзина
        tk.Label(right_frame, text="🛒 Ваша корзина", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#000000").pack(
            pady=15)

        self.cart_text = tk.Text(right_frame, font=("Segoe UI", 11), bg="#ffffff", fg="#000000",
                                 relief="flat", wrap="word", state="disabled")
        self.cart_text.pack(fill="both", expand=True, padx=10, pady=5)

        self.update_cart_display()

        # Левая панель: Товары
        self.create_scrollable_container()  # Создаст self.scrollable_frame
        self.filter_products()  # Заполнит товарами

        # Нижняя панель
        bottom_frame = tk.Frame(self.root, bg="#eef2f7")
        bottom_frame.pack(fill="x", side="bottom", pady=15)

        tk.Button(bottom_frame, text="💳 Оплатить и получить чек", bg="#27ae60", fg="#000000",
                  font=("Segoe UI", 11, "bold"), width=25, height=2, relief="flat", cursor="hand2",
                  command=self.show_receipt).pack(side="left", padx=10)

        tk.Button(bottom_frame, text="🗑 Очистить корзину", bg="#e74c3c", fg="#000000",
                  font=("Segoe UI", 10, "bold"), width=18, relief="flat", cursor="hand2",
                  command=self.clear_cart).pack(side="left", padx=5)

        tk.Button(bottom_frame, text="← Назад", bg="#5d6d7e", fg="#000000",
                  font=("Segoe UI", 10, "bold"), width=12, relief="flat", cursor="hand2", command=self.main_menu).pack(
            side="right", padx=10)

    def filter_products(self, *args):
        """Очищает и перерисовывает товары на основе поиска"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        query = self.search_var.get().lower()

        found = False
        for name, data in self.inventory.items():
            if data[1] > 0 and query in name.lower():
                found = True
                self.create_product_card(self.scrollable_frame, name, data)

        if not found:
            tk.Label(self.scrollable_frame, text="😕 Товары не найдены", font=("Segoe UI", 14), bg="#eef2f7",
                     fg="#000000").pack(pady=50)

    def create_product_card(self, parent, name, data):
        # 4. Карточки товаров: белый фон, рамка, отступы
        card = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        card.pack(fill="x", pady=8, padx=15, ipady=10, ipadx=10)

        info_frame = tk.Frame(card, bg="#ffffff")
        info_frame.pack(side="left", padx=15, fill="x", expand=True)

        # Текст везде черный
        tk.Label(info_frame, text=name, font=("Segoe UI", 13, "bold"), bg="#ffffff", fg="#000000").pack(anchor="w",
                                                                                                        pady=(0, 5))

        # 9. Статус остатка цветом (эмодзи)
        status = "🟢" if data[1] > 10 else "🟡" if data[1] > 3 else "🔴"
        tk.Label(info_frame, text=f"{data[0]} руб. | Остаток: {status} {data[1]} шт.",
                 font=("Segoe UI", 11), bg="#ffffff", fg="#000000").pack(anchor="w")

        tk.Button(card, text="В корзину ➕", bg="#2980b9", fg="#000000",
                  font=("Segoe UI", 11, "bold"), relief="raised", bd=1, cursor="hand2",
                  padx=15, pady=5,
                  command=lambda n=name: self.add_to_cart(n)).pack(side="right", padx=15)

    def add_to_cart(self, name):
        max_qty = self.inventory[name][1]
        qty = simpledialog.askinteger("Добавление в корзину", f"Сколько '{name}' добавить?\n(Максимум: {max_qty})",
                                      minvalue=1, maxvalue=max_qty)
        if qty is not None:  # Исправление: корректная обработка отмены (None)
            price = self.inventory[name][0]
            if name in self.cart:
                self.cart[name]['qty'] += qty
            else:
                self.cart[name] = {'qty': qty, 'price': price}

            self.inventory[name][1] -= qty
            self.save_data()
            self.update_cart_display()
            self.filter_products()  # Обновляем экран

    def update_cart_display(self):
        """Обновляет правую панель корзины"""
        self.cart_text.config(state="normal")
        self.cart_text.delete("1.0", tk.END)

        if not self.cart:
            self.cart_text.insert(tk.END, "Корзина пуста 🛒")
        else:
            total = 0
            for name, data in self.cart.items():
                cost = data['price'] * data['qty']
                total += cost
                self.cart_text.insert(tk.END, f"{name}\n")
                self.cart_text.insert(tk.END, f"  {data['qty']} x {data['price']} ₽ = {cost} ₽\n\n")

            self.cart_text.insert(tk.END, "-" * 25 + "\n")
            self.cart_text.insert(tk.END, f"ИТОГО: {total} ₽", ("bold",))

        self.cart_text.config(state="disabled")

    def clear_cart(self):
        if not self.cart:
            messagebox.showinfo("ℹ Информация", "Корзина уже пуста!")
            return
        if messagebox.askyesno("Очистка", "Вы уверены, что хотите очистить корзину?\nТовары вернутся на склад."):
            for name, data in self.cart.items():
                # Исправление ошибки №1: безопасное возвращение товара, даже если его удалили со склада
                if name in self.inventory:
                    self.inventory[name][1] += data['qty']
            self.save_data()
            self.cart = {}
            self.update_cart_display()
            self.filter_products()

    def show_receipt(self):
        if not self.cart:
            messagebox.showwarning("⚠ Пустая корзина", "Добавьте товары в корзину перед оплатой!")
            return

        payment_method = simpledialog.askstring("Оплата", "Выберите способ оплаты (1 - Наличные, 2 - Карта):")
        if payment_method not in ["1", "2"]:
            return
        pay_text = "Наличные" if payment_method == "1" else "Банковская карта"

        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # 10. Красивый чек с эмодзи и форматированием
        receipt_text = "══════════════════════════\n"
        receipt_text += "      🛒 SMART CHECKOUT\n"
        receipt_text += "══════════════════════════\n"
        receipt_text += f"Дата: {now}\n"
        receipt_text += f"Оплата: {pay_text}\n"
        receipt_text += "──────────────────────────\n"

        total = 0
        for name, data in self.cart.items():
            cost = data['price'] * data['qty']
            total += cost
            receipt_text += f"{name}\n"
            receipt_text += f"{data['qty']} x {data['price']} ₽\n"
            receipt_text += f"{cost} ₽\n\n"

        receipt_text += "──────────────────────────\n"
        receipt_text += f"ИТОГО: {total} ₽\n"
        receipt_text += "══════════════════════════\n"
        receipt_text += "  СПАСИБО ЗА ПОКУПКУ! 😊\n"
        receipt_text += "══════════════════════════\n"

        file_name = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = os.path.join(self.receipts_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(receipt_text)

        messagebox.showinfo("✅ Оплата прошла успешно!", f"Чек сохранен в файл:\n{file_path}\n\n{receipt_text}")

        self.cart = {}
        self.main_menu()


if __name__ == "__main__":
    root = tk.Tk()
    root.update_idletasks()
    width = 900
    height = 650
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    app = SelfServiceCheckout(root)
    root.mainloop()