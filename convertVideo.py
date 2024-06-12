import tkinter as tk
from tkinter import filedialog, ttk
import moviepy.editor as mp

def select_file_and_output_format():
    root = tk.Tk()
    root.withdraw()
    
    file_paths = filedialog.askopenfilenames(
        title="変換したいファイルを選択",
        filetypes=[("動画ファイル", "*.mp4 *.avi *.mov *.gif")]
    )
    
    if not file_paths:
        print("ファイルが選択されませんでした")
        return None, None
    
    output_format = None
    
    # 出力形式を選択するためのウィンドウを表示
    format_window = tk.Toplevel(root)
    format_window.title("出力形式の選択")
    
    tk.Label(format_window, text="出力形式を選択してください:").pack(pady=10)
    
    formats = ["mp4", "avi", "webm", "mov", "gif", "mkv", "flv", "wmv", "ogv", "ogg", "mpeg"]
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

def convert_to_specified_format(file_paths, output_format):
    for file_path in file_paths:
        try:
            codec = 'libx264'
            if output_format.lower() == 'avi':
                codec = 'png'
            elif output_format.lower() == 'webm':
                codec = 'libvpx'
            elif output_format.lower() == 'gif':
                codec = 'gif'
            elif output_format.lower() == 'flv':
                codec = 'flv1'
            elif output_format.lower() == 'wmv':
                codec = 'wmv2'
            elif output_format.lower() in ['ogv', 'ogg']:
                codec = 'libtheora'
            # 拡張子を置き換えて出力パスを作成
            output_path = '.'.join(file_path.split('.')[:-1]) + '.' + output_format.lower()
            clip = mp.VideoFileClip(file_path)
            clip.write_videofile(output_path, codec=codec)
            clip.close()
            print(f"{file_path} を {output_format} 形式に変換しました: {output_path}")
        except Exception as e:
            print(f"{file_path} の変換に失敗しました: {e}")

if __name__ == "__main__":
    file_paths, output_format = select_file_and_output_format()
    if file_paths is not None and output_format is not None:
        convert_to_specified_format(file_paths, output_format)
    else:
        print("ファイルが選択されなかったか、変換形式が指定されませんでした")