import tkinter as tk
from PIL import Image, ImageTk

class RulesPage:
    def __init__(self, master, app):
        self.frame = tk.Frame(master)

        # โหลดภาพพื้นหลัง
        self.bg_img = Image.open(r'E:\Project AI\Project_Ai\Image\BG_rules.png')
        self.bg_img = self.bg_img.resize((1280, 720))  # ปรับขนาดภาพให้พอดีกับหน้าจอ
        self.bg_imgtk = ImageTk.PhotoImage(self.bg_img)

        # แสดงภาพพื้นหลัง
        self.lbl_bg = tk.Label(self.frame, image=self.bg_imgtk)
        self.lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)  # แสดงภาพพื้นหลังเต็มจอ

        # ปุ่มกลับไปหน้าแรก
        self.btn_back = tk.Button(
            self.frame, 
            text="หน้าแรก", 
            command=app.show_home,  
            font=("Kanit", 10, "bold"),
            padx=20,       # ระยะห่างในแนวนอน
            pady=10,       # ระยะห่างในแนวตั้ง
        )
        self.btn_back.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=(10, 20))

    def pack(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def clear(self):
        self.frame.pack_forget()
