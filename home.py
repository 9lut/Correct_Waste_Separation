import tkinter as tk
from PIL import Image, ImageTk
import pygame  # เพิ่ม pygame เพื่อเล่นเพลง

class HomePage:
    def __init__(self, master, app):
        self.frame = tk.Frame(master)
        
        # เริ่มต้น pygame สำหรับเสียง
        pygame.mixer.init()

        self.label = tk.Label(self.frame, text="Welcome to the Home Page", font=("Arial", 24))
        self.label.pack(pady=20)

        # โหลดภาพพื้นหลัง
        self.bg_img = Image.open(r'E:\Project AI\Project_Ai\Image\BG_home.png')  # ใช้ r เพื่อเส้นทางแบบดิบ
        self.bg_img = self.bg_img.resize((1280, 720))  # ลบ Image.ANTIALIAS
        self.bg_imgtk = ImageTk.PhotoImage(self.bg_img)

        # ใช้ self.frame แทน self
        self.lbl_home = tk.Label(self.frame, image=self.bg_imgtk)
        self.lbl_home.place(x=0, y=0)

        # ปุ่มไปที่กล้อง
        self.btn_camera = tk.Button(
            self.frame, 
            text="เริ่มกันเลย", 
            command=lambda: self.go_to_page(app.show_camera),  # เรียกฟังก์ชัน go_to_page ก่อนเปลี่ยนหน้า
            font=("Kanit", 20 , "bold"),
            bg="#4CAF50", 
            fg="white", 
            padx=20, 
            pady=10, 
            borderwidth=5, 
        )
        
        self.btn_camera.pack(expand=True, padx=20, pady=20)  # ใช้ expand=True เพื่อให้ปุ่มอยู่กึ่งกลาง

        # ปุ่มไปที่กฎ
        self.btn_rules = tk.Button(
            self.frame,
            text="ความรู้เกี่ยวกับถังขยะ",
            command=lambda: self.go_to_page(app.show_rules),  # เรียกฟังก์ชัน go_to_page ก่อนเปลี่ยนหน้า
            font=("Kanit", 15 , "bold"),
            bg="#007dff",  # สีพื้นหลังของปุ่ม
            fg="white",    # สีข้อความ
            padx=20,       # ระยะห่างในแนวนอน
            pady=10,       # ระยะห่างในแนวตั้ง
            relief="raised",  # รูปแบบของขอบปุ่ม
            bd=5,           # ความหนาของขอบ
            width=25      # ความกว้างของปุ่ม (จำนวนตัวอักษร)
        )
        self.btn_rules.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=(10, 20))  # เพิ่ม padding บนและล่าง

        # สถานะของเพลง (เล่นหรือหยุด)
        self.music_playing = False

        # โหลดไอคอน
        self.play_icon = Image.open(r'E:\Project AI\Project_Ai\Image\unmute.png')  # ไอคอนเล่น
        self.stop_icon = Image.open(r'E:\Project AI\Project_Ai\Image\mute.png')  # ไอคอนหยุด
        self.play_icon = self.play_icon.resize((50, 50))
        self.stop_icon = self.stop_icon.resize((50, 50))

        self.play_icon_tk = ImageTk.PhotoImage(self.play_icon)
        self.stop_icon_tk = ImageTk.PhotoImage(self.stop_icon)

        # ปุ่มเปิด/ปิดเพลงที่มุมขวาล่าง
        self.music_btn = tk.Button(
            self.frame, 
            image=self.play_icon_tk,  # เริ่มด้วยไอคอนเล่นเพลง
            command=self.toggle_music,  # เชื่อมโยงกับฟังก์ชัน toggle_music
            bd=0  # ไม่มีขอบ
        )
        self.music_btn.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)  # จัดให้อยู่มุมขวาล่าง

        # เล่นเพลงทันทีเมื่อเปิดหน้า
        self.play_music()  # เพิ่มการเล่นเพลงเมื่อหน้า HomePage โหลด

    def play_music(self):
        """ ฟังก์ชันเล่นเพลง """
        pygame.mixer.music.load(r'E:\Project AI\Project_Ai\Image\song.mp3')  # ระบุเส้นทางไฟล์เพลง
        pygame.mixer.music.play(-1)  # เล่นเพลงวนไปเรื่อยๆ (-1)
        self.music_btn.config(image=self.stop_icon_tk)  # เปลี่ยนไอคอนเป็นหยุด
        self.music_playing = True

    def stop_music(self):
        """ ฟังก์ชันหยุดเพลง """
        pygame.mixer.music.stop()  # หยุดเพลง
        self.music_btn.config(image=self.play_icon_tk)  # เปลี่ยนไอคอนเป็นเล่น
        self.music_playing = False

    def toggle_music(self):
        """ ฟังก์ชันเปิด/ปิดเพลง """
        if self.music_playing:
            self.stop_music()
        else:
            self.play_music()

    def go_to_page(self, next_page_func):
        """ ฟังก์ชันนี้จะหยุดเพลงก่อนแล้วจึงไปยังหน้าถัดไป """
        self.stop_music()  # หยุดเพลงก่อนเปลี่ยนหน้า
        next_page_func()    # ไปยังหน้าถัดไปที่กำหนด

    def pack(self):
        self.play_music()  # เล่นเพลงใหม่ทุกครั้งเมื่อเปิดหน้า HomePage
        self.frame.pack(fill=tk.BOTH, expand=True)


    def clear(self):
        self.frame.pack_forget()
