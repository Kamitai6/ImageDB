import re
from pathlib import Path
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
  img = img.resize((1280, 960))
  ImageOps.exif_transpose(img)
  img.save(file.with_suffix(".webp"), quality=95)
  file.unlink()