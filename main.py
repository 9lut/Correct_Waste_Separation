import tkinter as tk
from home import HomePage
from camera import CameraPage
from rules import RulesPage

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Correct Waste Separation")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        # สร้างหน้าเริ่มต้น
        self.home_page = HomePage(self.root, self)  # ส่งตัวเองเป็นพารามิเตอร์
        self.camera_page = None
        self.rules_page = None

        self.show_home()

    def show_home(self):
        self.clear_frame()
        self.home_page.pack()

    def show_camera(self):
        self.clear_frame()
        self.camera_page = CameraPage(self.root, self)  # ส่งตัวเองเป็นพารามิเตอร์
        self.camera_page.pack()

    def show_rules(self):
        self.clear_frame()
        self.rules_page = RulesPage(self.root, self)  # ส่งตัวเองเป็นพารามิเตอร์
        self.rules_page.pack()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    app.show_home()
    root.mainloop()