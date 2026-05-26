"""裁切封面图：上裁5% 下裁10%（去掉AI生成标记），保留原图和裁切图"""
from PIL import Image
import os

input_path = r"D:\github\zmyAI\zmyAI.github.io\source\_posts\从DeepSeek到TRAE到WorkBuddy\cover_original.png"
cropped_path = r"D:\github\zmyAI\zmyAI.github.io\source\_posts\从DeepSeek到TRAE到WorkBuddy\cover.png"

img = Image.open(input_path)
w, h = img.size
print(f"原图尺寸: {w}x{h}", flush=True)

crop_top = int(h * 0.05)     # 上裁 5%
crop_bottom = int(h * 0.10)  # 下裁 10%
cropped = img.crop((0, crop_top, w, h - crop_bottom))
cropped.save(cropped_path, "PNG")
print(f"裁切: 上 {crop_top}px, 下 {crop_bottom}px", flush=True)
print(f"裁切后尺寸: {cropped.size[0]}x{cropped.size[1]}", flush=True)
print(f"原图保留: {input_path}", flush=True)
print(f"裁切图: {cropped_path}", flush=True)
