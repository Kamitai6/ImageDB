import re
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

# ディレクトリを取得
cwd = Path.cwd()
print(cwd)

# 再帰的にディレクトリ内のpngとjpgの画像を検索
images = sorted([p for p in cwd.glob('**/*') if re.search('/*\.(jpg|jpeg|png)', str(p))])
for file in images:
  print(file)
  # 画像を読み込む
  img = Image.open(file)
  img.convert("RGB")
  # 背景画像を作成
  small_img = img.resize((100, 100))
  color_arr = np.array(small_img)
  w_size, h_size, n_color = color_arr.shape
  color_arr = color_arr.reshape(w_size * h_size, n_color)
  color_mean = np.mean(color_arr, axis=0)
  color_mean = color_mean.astype(int)
  color_mean = tuple(color_mean)
  bg = Image.new('RGB', (1280, 960), color_mean)
  # リサイズ
  height = 960
  width = round(img.width * height / img.height)
  if(width > 1280): width = 1280
  img = img.resize((width, height))
  ImageOps.exif_transpose(img)
  # 重ねる
  x = (1280 - img.width) / 2
  y = 0
  bg.paste(img, (x, y))
  bg.save(file.with_suffix(".webp"), quality=95)
  file.unlink()