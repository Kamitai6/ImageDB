import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
import pillow_avif  # AVIFサポートを追加

def select_files_and_format():
    # ルートウィンドウを作成し、表示しない
    root = tk.Tk()
    root.withdraw()
    
    # ファイル選択ダイアログを表示
    file_paths = filedialog.askopenfilenames(
        title="画像ファイルを選択",
        # filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp *.ico *.pdf *.eps *.svg *.jfif *.ppm *.pbm *.pgm *.pnm *.avif")]
        filetypes=[("画像ファイル", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp *.ico *.pdf *.eps *.svg *.jfif *.ppm *.pbm *.pgm *.pnm *.avif")]
    )
    
    # ファイルが選択されなかった場合は終了
    if not file_paths:
        print("ファイルが選択されませんでした")  # 追加
        return None, None
    
    # 新しいウィンドウを作成して変換形式を選択
    format_window = tk.Toplevel(root)
    format_window.title("変換形式の選択")
    
    tk.Label(format_window, text="変換形式を選択してください:").pack(pady=10)
    formats = ['JPEG', 'PNG', 'BMP', 'GIF', 'TIFF', 'WEBP', 'ICO', 'JFIF', 'PPM', 'PBM', 'PGM', 'PNM', 'AVIF']
    selected_format = tk.StringVar(value=formats[0])
    option_menu = ttk.OptionMenu(format_window, selected_format, formats[0], *formats)
    option_menu.pack(pady=20)
    
    button_frame = tk.Frame(format_window)
    button_frame.pack(pady=10)
    
    def on_select():
        format_window.quit()
    
    ok_button = ttk.Button(button_frame, text="OK", command=on_select)
    ok_button.pack(side="left", padx=5)
    
    cancel_button = ttk.Button(button_frame, text="キャンセル", command=lambda: format_window.quit())
    cancel_button.pack(side="right", padx=5)
    
    format_window.mainloop()
    
    if selected_format.get():
        format_window.destroy()
        return file_paths, selected_format.get()
    else:
        format_window.destroy()
        return None, None

def convert_images(file_paths, output_format):
    for file_path in file_paths:
        try:
            image = Image.open(file_path)
            image.load()
            
            # パレットモードの場合はRGBAモードに変換
            if image.mode == 'P':
                image = image.convert('RGBA')
            
            # 透明なPNG画像の場合
            if image.mode == 'RGBA':
                # 透明な部分を白で塗りつぶす
                image_with_white_background = Image.new("RGBA", image.size, (255, 255, 255, 0))
                image_with_white_background.paste(image, (0, 0), image)
                image = image_with_white_background
                image = image.convert('RGB')
            
            output_path = file_path.rsplit('.', 1)[0] + '.' + output_format.lower()
            image.save(output_path, output_format.upper())
            print(f"画像が {output_format} 形式に変換されました: {output_path}")
        except Exception as e:
            print(f"{file_path} の画像の変換に失敗しました: {e}")

if __name__ == "__main__":
    file_paths, output_format = select_files_and_format()
    if file_paths is not None and output_format is not None:
        convert_images(file_paths, output_format)
    else:
        print("ファイルが選択されなかったか、変換形式が指定されませんでした")