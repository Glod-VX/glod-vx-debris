import tkinter as tk
from tkinter import messagebox

class UnicodeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Unicode 互译器")
        self.root.geometry("400x200")
        self.root.configure(bg="#f5f5f5")

        # 标签和输入框
        self.label = tk.Label(root, text="输入字符或Unicode编码:", bg="#f5f5f5", font=("Arial", 12))
        self.label.pack(pady=10)

        self.input_field = tk.Entry(root, font=("Arial", 12))
        self.input_field.pack(pady=5)

        # 按钮
        self.to_unicode_button = tk.Button(root, text="字符转Unicode编码", command=self.char_to_unicode, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.to_unicode_button.pack(pady=5)

        self.to_char_button = tk.Button(root, text="Unicode编码转字符", command=self.unicode_to_char, bg="#2196F3", fg="white", font=("Arial", 12))
        self.to_char_button.pack(pady=5)

        # 结果显示
        self.result_label = tk.Label(root, text="转换结果:", bg="#f5f5f5", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.result_field = tk.Entry(root, font=("Arial", 12), state="readonly")
        self.result_field.pack(pady=5)

    def char_to_unicode(self):
        user_input = self.input_field.get()
        if len(user_input) == 1:
            unicode_value = f"\\u{ord(user_input):04x}"
            self.result_field.config(state="normal")
            self.result_field.delete(0, tk.END)
            self.result_field.insert(0, unicode_value)
            self.result_field.config(state="readonly")
        else:
            messagebox.showerror("错误", "请输入一个字符！")

    def unicode_to_char(self):
        user_input = self.input_field.get()
        try:
            code_point = int(user_input, 16)
            character = chr(code_point)
            self.result_field.config(state="normal")
            self.result_field.delete(0, tk.END)
            self.result_field.insert(0, character)
            self.result_field.config(state="readonly")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的Unicode编码！")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnicodeConverter(root)
    root.mainloop()
