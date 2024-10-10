import cv2
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from PIL import Image
import tkinter as tk
from tkinter import ttk  # สำหรับการสร้าง ComboBox
from PIL import Image, ImageTk
import os

class CameraPage(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.master = master
        self.app = app

        # ขยาย Frame ให้เต็มหน้าจอ
        self.pack(fill=tk.BOTH, expand=True)

        # โหลดภาพพื้นหลัง
        self.bg_img = Image.open(r'E:\Project AI\Project_Ai\Image\BG.png')
        self.bg_img = self.bg_img.resize((1280, 720))
        self.bg_imgtk = ImageTk.PhotoImage(self.bg_img)

        # ใช้ self แทน frame
        self.lbl_home = tk.Label(self, image=self.bg_imgtk)
        self.lbl_home.place(x=0, y=0, relwidth=1, relheight=1)

        # สร้าง Label สำหรับกล้อง
        self.lbl_opencv = tk.Label(self, bg="#FFFFFF", relief="solid", borderwidth=5)  # กำหนด bg เป็นสีขาว
        self.lbl_opencv.pack(pady=10)

        # สร้าง Label สำหรับแสดงภาพถังขยะ
        self.lbl_bin = tk.Label(self)
        self.lbl_bin.place(relx=0.75, rely=0.5, anchor=tk.CENTER)  # อยู่กึ่งกลางแนวตั้งและทางขวา

        # สร้าง Label สำหรับแสดงประเภทของขยะ
        self.lbl_result = tk.Label(
            self, text="", 
            font=("Kanit", 20), 
            fg="black",    # สีข้อความ
            padx=20,       # ระยะห่างในแนวนอน
            pady=10,       # ระยะห่างในแนวตั้ง
        )
        self.lbl_result.place(relx=0.75, rely=0.80, anchor=tk.CENTER)  # อยู่ใต้ถังขยะ

        # สร้างปุ่มสำหรับการทำนายภาพ
        self.btn_predict = tk.Button(
            self, text="ตรวจจับ", 
            command=self.capture_and_predict, 
            font=("Kanit", 20, "bold"),
            bg="#007dff",  # สีพื้นหลังของปุ่ม
            fg="white",    # สีข้อความ
            padx=20,       # ระยะห่างในแนวนอน
            pady=10,       # ระยะห่างในแนวตั้ง
            relief="raised",  # รูปแบบของขอบปุ่ม
            bd=5,           # ความหนาของขอบ
            width=10      # ความกว้างของปุ่ม (จำนวนตัวอักษร)
        )

        # ใช้ place เพื่อจัดตำแหน่งปุ่มตรงกลางด้านล่าง แต่ไม่ติดขอบ
        self.btn_predict.place(relx=0.5, rely=0.9, anchor=tk.CENTER)  # 90% จากด้านบน

        # ปุ่มกลับไปหน้าแรก
        self.btn_back = tk.Button(
            self, text="หน้าแรก", 
            command=self.back_to_home, 
            font=("Kanit", 10 , "bold"),
            padx=20,       # ระยะห่างในแนวนอน
            pady=10,       # ระยะห่างในแนวตั้ง
        )
        self.btn_back.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=(10, 20))  # เพิ่ม padding บนและล่าง

        
        # สร้าง ComboBox สำหรับการเลือกกล้องและตกแต่ง
        self.camera_selection = ttk.Combobox(
            self,
            values=[f"กล้อง {i}" for i in range(4)],
            font=("Kanit", 12),
            state="readonly"  # ทำให้เลือกได้เฉพาะค่าที่กำหนด
        )
        self.camera_selection.current(0)  # ตั้งค่าเริ่มต้นเป็นกล้องตัวแรก
        self.camera_selection.place(relx=0.25, rely=0.73, anchor=tk.CENTER)  # วาง ComboBox ใต้ Label

        # ตกแต่ง ComboBox
        style = ttk.Style()
        style.configure("TCombobox", 
                        font=("Kanit", 12), 
                        background="#ffffff", 
                        foreground="#333333", 
                        padding=5)
        style.map("TCombobox", 
                fieldbackground=[("readonly", "#ffffff")],  # สีพื้นหลังเมื่อเลือก
                background=[("readonly", "#ffffff")])  # สีพื้นหลังเมื่อไม่เลือก

        self.camera_selection.bind("<<ComboboxSelected>>", self.change_camera)  # เรียกเปลี่ยนกล้องเมื่อเลือก

        # เริ่มต้นกล้อง
        self.cap = cv2.VideoCapture(0)
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_resized = cv2.resize(frame, (360, 240))
            img = Image.fromarray(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.lbl_opencv.imgtk = imgtk
            self.lbl_opencv.configure(image=imgtk)

        # วาง opencv ที่กึ่งซ้ายกลาง
        self.lbl_opencv.place(relx=0.25, rely=0.5, anchor=tk.CENTER)  # 25% จากซ้ายและอยู่กึ่งกลางแนวตั้ง

        # เรียกซ้ำเพื่ออัปเดตเฟรมใหม่
        self.lbl_opencv.after(10, self.update_frame)

    def change_camera(self, event):
        # ปล่อยกล้องเก่าก่อน
        self.cap.release()
        # เลือกกล้องจาก ComboBox และเปิดกล้องใหม่
        selected_camera_index = self.camera_selection.current()
        self.cap = cv2.VideoCapture(selected_camera_index)

    def capture_and_predict(self):
        ret, frame = self.cap.read()
        if ret:
            # บันทึกภาพจากกล้องเป็นไฟล์ชั่วคราว
            temp_filename = 'temp_frame.jpg'
            cv2.imwrite(temp_filename, frame)

            # ทำนายหมวดหมู่ภาพด้วยฟังก์ชัน getPrediction
            answer, probability_results, filename = getPrediction(temp_filename)

            # แสดงผลลัพธ์การทำนาย
            print(f"Prediction: {answer}, Probability: {probability_results}")

            # แสดงผลประเภทขยะใน Label
            self.lbl_result.config(text=f"เป็นขยะประเภท : {answer} \n (ความน่าจะเป็น: {probability_results:.2f})")

            # เปลี่ยนรูปถังขยะตามประเภทที่ทำนาย
            if answer == "Recycle":
                bin_image_path = r'E:\Project AI\Project_Ai\Image\Bin\Recycle.png'
            elif answer == "Organic":
                bin_image_path = r'E:\Project AI\Project_Ai\Image\Bin\Organic.png'
            else:
                bin_image_path = r'E:\Project AI\Project_Ai\Image\Bin\General.png'

            # โหลดและแสดงภาพถังขยะใหม่ใน lbl_bin (ไฟล์ PNG โปร่งใส)
            bin_img = Image.open(bin_image_path)
            bin_img = bin_img.resize((300, 300))  # ปรับขนาดถังขยะ
            bin_imgtk = ImageTk.PhotoImage(bin_img)
            self.lbl_bin.imgtk = bin_imgtk
            self.lbl_bin.config(image=bin_imgtk)

            # ลบไฟล์ชั่วคราวหลังจากการทำนายเสร็จสิ้น
            os.remove(temp_filename)

    def release(self):
        self.cap.release()

    def back_to_home(self):
        self.release()
        self.app.show_home()

# ฟังก์ชันการทำนายภาพด้วย TensorFlow
def getPrediction(filename):
    model = tf.keras.models.load_model("E:/Project AI/Project_Ai/Model/final_model_weights.hdf5")

    # โหลดและประมวลผลภาพ
    img = Image.open(filename)
    img = img.resize((180, 180))
    img = img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # ทำนายหมวดหมู่
    category = model.predict(img)
    answer = np.argmax(category, axis=1)[0]

    # ประมวลผลคำตอบและความน่าจะเป็น
    probability_results = category[0][answer]

    # ตรวจสอบหมวดหมู่
    if answer == 1:
        answer = "Recycle"
    elif answer == 0:
        answer = "Organic"
    else:
        answer = "General"

    return str(answer), float(probability_results), filename
