"""裁切封面图/总结卡：四周各裁10%，保留原图和裁切图
用法：
  python crop_cover.py <input.png> [--output <output.png>]
  python crop_cover.py <input.png> --crop 0.08
"""
import argparse
from PIL import Image
import os

def main():
    parser = argparse.ArgumentParser(description="裁切图片：四周各裁指定比例")
    parser.add_argument("input", help="输入图片路径")
    parser.add_argument("--output", help="输出图片路径（默认: 输入文件名加 _cropped 后缀）")
    parser.add_argument("--crop", type=float, default=0.08, help="裁切比例（默认0.08即8%）")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"错误：文件不存在 {args.input}", flush=True)
        return

    output = args.output or args.input.replace(".png", "_cropped.png").replace(".jpg", "_cropped.jpg")
    c = args.crop

    img = Image.open(args.input)
    w, h = img.size
    left = int(w * c)
    top = int(h * c)
    right = int(w * (1 - c))
    bottom = int(h * (1 - c))
    cropped = img.crop((left, top, right, bottom))
    cropped.save(output, "PNG")

    print(f"原图: {args.input} ({w}x{h})", flush=True)
    print(f"裁切: 四周各 {c*100:.0f}%", flush=True)
    print(f"输出: {output} ({cropped.size[0]}x{cropped.size[1]})", flush=True)

if __name__ == "__main__":
    main()
