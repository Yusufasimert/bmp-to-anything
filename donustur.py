import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMP Format Dönüştürücü")
        self.root.geometry("450x380")
        self.root.resizable(False, False)

        # Variables
        self.input_files = []
        self.output_dir = ""
        self.target_format = tk.StringVar(value="JPG")

        # Styling
        style = ttk.Style()
        style.theme_use('clam')

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Kaynak Dosya Seçimi
        ttk.Label(main_frame, text="1. Dönüştürülecek BMP Dosyaları:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        btn_select_input = ttk.Button(main_frame, text="Resimleri Seç", command=self.select_input_files)
        btn_select_input.pack(fill=tk.X, pady=(0, 5))
        
        self.lbl_input = ttk.Label(main_frame, text="Henüz dosya seçilmedi", foreground="gray")
        self.lbl_input.pack(anchor=tk.W, pady=(0, 15))

        # 2. Hedef Klasör Seçimi
        ttk.Label(main_frame, text="2. Kaydedilecek Hedef Klasör:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        btn_select_output = ttk.Button(main_frame, text="Klasör Seç", command=self.select_output_dir)
        btn_select_output.pack(fill=tk.X, pady=(0, 5))
        
        self.lbl_output = ttk.Label(main_frame, text="Henüz klasör seçilmedi", foreground="gray")
        self.lbl_output.pack(anchor=tk.W, pady=(0, 15))

        # 3. Format Seçimi
        ttk.Label(main_frame, text="3. Hedef Format:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        format_frame = ttk.Frame(main_frame)
        format_frame.pack(fill=tk.X, pady=(0, 15))
        
        formats = ["JPG", "JPEG", "PNG", "WEBP", "TIFF"]
        combo = ttk.Combobox(format_frame, textvariable=self.target_format, values=formats, state="readonly")
        combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Dönüştür Butonu
        self.btn_convert = ttk.Button(main_frame, text="DÖNÜŞTÜR", command=self.convert_images, style="Action.TButton")
        self.btn_convert.pack(fill=tk.X, pady=(10, 10))

        # İlerleme Çubuğu
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X)

        self.lbl_status = ttk.Label(main_frame, text="", font=("Arial", 9))
        self.lbl_status.pack(pady=(5, 0))

    def select_input_files(self):
        files = filedialog.askopenfilenames(
            title="Dönüştürülecek BMP dosyalarını seçin",
            filetypes=[("BMP Dosyaları", "*.bmp"), ("Tüm Dosyalar", "*.*")]
        )
        if files:
            self.input_files = files
            self.lbl_input.config(text=f"{len(files)} dosya seçildi", foreground="green")

    def select_output_dir(self):
        dir_name = filedialog.askdirectory(title="Kaydedilecek Klasörü Seçin")
        if dir_name:
            self.output_dir = dir_name
            self.lbl_output.config(text=dir_name, foreground="green")

    def convert_images(self):
        if not self.input_files:
            messagebox.showwarning("Uyarı", "Lütfen en az bir resim seçin!")
            return
        if not self.output_dir:
            messagebox.showwarning("Uyarı", "Lütfen resimlerin kaydedileceği hedef klasörü seçin!")
            return

        fmt = self.target_format.get()
        extension = fmt.lower()
        
        pil_format = fmt
        if fmt == "JPG":
            pil_format = "JPEG"
            extension = "jpg"
        elif fmt == "JPEG":
            pil_format = "JPEG"
            extension = "jpeg"

        total_files = len(self.input_files)
        success_count = 0
        
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        self.btn_convert.config(state=tk.DISABLED)

        for idx, file_path in enumerate(self.input_files):
            try:
                self.lbl_status.config(text=f"İşleniyor: {os.path.basename(file_path)}")
                self.root.update_idletasks()

                with Image.open(file_path) as img:
                    # JPEG ve formatları için RGBA/P modunu desteklemez, RGB'ye dönüştür
                    if pil_format == "JPEG" and img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                        
                    basename = os.path.basename(file_path)
                    name, _ = os.path.splitext(basename)
                    
                    new_filename = f"{name}.{extension}"
                    out_path = os.path.join(self.output_dir, new_filename)
                    
                    img.save(out_path, format=pil_format)
                    success_count += 1
                    
            except Exception as e:
                messagebox.showerror("Hata", f"{os.path.basename(file_path)} dönüştürülürken hata oluştu:\n{str(e)}")
            
            self.progress['value'] = idx + 1
            self.root.update_idletasks()

        self.lbl_status.config(text=f"Tamamlandı! {success_count}/{total_files} dosya dönüştürüldü.")
        self.btn_convert.config(state=tk.NORMAL)
        messagebox.showinfo("Başarılı", f"İşlem tamamlandı!\n{success_count} dosya {fmt} formatına dönüştürüldü.")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Custom style for action button
    style = ttk.Style()
    style.configure("Action.TButton", font=("Arial", 11, "bold"), padding=10)
    
    app = ConverterApp(root)
    root.mainloop()
