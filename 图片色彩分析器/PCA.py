import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image
from colorthief import ColorThief
import numpy as np

# 手动维护的颜色名称到 HEX 值的字典
COLOR_NAMES = {
    '#000000': '黑色',
    '#FFFFFF': '白色',
    '#FF0000': '红色',
    '#00FF00': '绿色',
    '#0000FF': '蓝色',
    '#FFFF00': '黄色',
    '#00FFFF': '青色',
    '#FF00FF': '品红',
    '#C0C0C0': '银色',
    '#808080': '灰色',
    '#800000': '褐色',
    '#808000': '橄榄色',
    '#008000': '深绿色',
    '#800080': '紫色',
    '#008080': '青绿色',
    '#000080': '海军蓝',
    '#FFA500': '橙色',
    '#A52A2A': '棕色',
    '#8B0000': '深红色',
    '#8B4513': '马鞍棕',
    '#2E8B57': '海洋绿',
    '#A9A9A9': '深灰色',
    '#F5F5DC': '米色',
    '#FFE4C4': '小麦色',
    '#00CED1': '暗青色',
    '#4682B4': '钢蓝色',
    '#D2691E': '巧克力色',
    '#9ACD32': '黄绿色',
    '#F0E68C': '卡其色',
    '#DA70D6': '兰花色',
    '#EEE8AA': '苍金麒麟色',
    '#98FB98': '苍绿色',
    '#AFEEEE': '苍白绿宝石色',
    '#DB7093': '苍紫红色',
    '#FFD700': '金色',
    '#D3D3D3': '亮灰色',
    '#F08080': '亮珊瑚色',
    '#20B2AA': '浅海绿色',
    '#87CEFA': '亮天蓝色',
    '#778899': '浅石板灰',
    '#B0C4DE': '淡钢蓝色',
    '#FFFFE0': '亮黄色',
    '#FFB6C1': '亮粉红色',
    '#32CD32': '酸橙绿',
    '#FAFAD2': '淡金色',
    '#FFA07A': '淡珊瑚色',
    '#E6E6FA': '淡紫色',
    '#7FFFD4': '绿宝石色',
    '#FFEBCD': '杏仁色'
}


class ColorAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("颜色分析工具 - 微软化风格")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # 自定义 Win10 风格的 ttk 主题
        style = ttk.Style()
        style.theme_use('clam')  # 选择基础主题
        style.configure('TButton', font=('Segoe UI', 10), background='#0078D7', foreground='#ffffff', padding=6, relief='flat')
        style.map('TButton', background=[('active', '#005A9E')], relief=[('pressed', 'sunken')])

        style.configure('TLabel', font=('Segoe UI', 10), background='#f0f0f0')
        style.configure('TNotebook.Tab', font=('Segoe UI', 10))

        # Segoe UI 字体设置
        self.default_font = ('Segoe UI', 10)

        self.image_path = None

        # 创建选项卡
        self.tab_control = ttk.Notebook(root)

        # 上传图片选项卡
        self.upload_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.upload_tab, text='上传图片')

        # 颜色显示选项卡
        self.colors_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.colors_tab, text='颜色显示')

        # 结果显示选项卡
        self.results_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.results_tab, text='结果显示')

        self.tab_control.pack(expand=1, fill='both')

        # 上传图片界面
        self.upload_button = ttk.Button(self.upload_tab, text="上传图片", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.image_label = tk.Label(self.upload_tab, bg='#f0f0f0')
        self.image_label.pack(pady=10)

        # 重新分析按钮
        self.analyze_button = ttk.Button(self.upload_tab, text="分析", command=self.analyze_colors, state=tk.DISABLED)
        self.analyze_button.pack(pady=10)

        # 颜色显示界面
        self.colors_frame = tk.Frame(self.colors_tab, bg="#f0f0f0")
        self.colors_frame.pack(pady=10)

        # 选择比较方法
        self.comparison_method = tk.StringVar(value='euclidean')
        method_frame = tk.Frame(self.colors_tab, bg="#f0f0f0")
        method_frame.pack(pady=10)
        tk.Label(method_frame, text="选择比较方法：", bg="#f0f0f0", font=self.default_font).pack(side=tk.LEFT)
        ttk.Radiobutton(method_frame, text="欧几里得距离", variable=self.comparison_method, value='euclidean').pack(side=tk.LEFT)
        ttk.Radiobutton(method_frame, text="曼哈顿距离", variable=self.comparison_method, value='manhattan').pack(side=tk.LEFT)
        ttk.Radiobutton(method_frame, text="余弦相似度", variable=self.comparison_method, value='cosine').pack(side=tk.LEFT)

        # 结果显示界面
        self.result_text = tk.Text(self.results_tab, height=20, width=90, wrap=tk.WORD, bg="#ffffff", fg="#000000", font=self.default_font)
        self.result_text.pack(pady=10)

        self.error_label = tk.Label(self.results_tab, text="", fg="red", bg="#f0f0f0", font=self.default_font)
        self.error_label.pack(pady=5)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return

        self.image_path = file_path
        self.display_image()
        self.analyze_colors()
        self.analyze_button.config(state=tk.NORMAL)  # 启用重新分析按钮

    def display_image(self):
        image = Image.open(self.image_path)
        image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.photo = photo

    def analyze_colors(self):
        try:
            num_colors = 10  # 调整为分析更多的颜色
            dominant_colors = self.get_dominant_colors(self.image_path, num_colors)
            self.display_colors(dominant_colors)
            self.display_results(dominant_colors)
        except Exception as e:
            self.error_label.config(text=f"错误: {str(e)}")

    def get_dominant_colors(self, image_path, num_colors=10):
        color_thief = ColorThief(image_path)
        return color_thief.get_palette(color_count=num_colors)

    def display_colors(self, colors):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()

        for color in colors:
            color_hex = self.rgb_to_hex(color)
            color_name = self.closest_color(color)
            color_label = tk.Label(self.colors_frame, text=f"{color_hex} - {color_name}", bg=color_hex, fg="white", padx=10, pady=5, font=self.default_font)
            color_label.pack(pady=2)

    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def closest_color(self, requested_color):
        requested_color_hex = self.rgb_to_hex(requested_color)
        if requested_color_hex in COLOR_NAMES:
            return COLOR_NAMES[requested_color_hex]

        min_colors = {}
        for color_hex, name in COLOR_NAMES.items():
            r, g, b = self.hex_to_rgb(color_hex)
            rd = (r - requested_color[0]) ** 2
            gd = (g - requested_color[1]) ** 2
            bd = (b - requested_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def display_results(self, colors):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "分析结果:\n")
        for color in colors:
            color_hex = self.rgb_to_hex(color)
            color_name = self.closest_color(color)
            self.result_text.insert(tk.END, f"颜色: {color_name} - {color_hex}\n")

    def compare_colors(self, color1, color2, method):
        if method == 'euclidean':
            return np.linalg.norm(np.array(color1) - np.array(color2))
        elif method == 'manhattan':
            return np.abs(np.array(color1) - np.array(color2)).sum()
        elif method == 'cosine':
            return 1 - np.dot(color1, color2) / (np.linalg.norm(color1) * np.linalg.norm(color2))
        return None


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorAnalyzerApp(root)
    root.mainloop()
