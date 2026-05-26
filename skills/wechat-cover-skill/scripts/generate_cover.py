"""生成并裁切公众号封面图：保留原图和裁切图"""
import requests, json, base64, sys, os
from PIL import Image

API_KEY = "ark-4ecd14b5-e28d-43a2-af09-f9cf4ceebb34-d39a2"
URL = "https://ark.cn-beijing.volces.com/api/plan/v3/images/generations"
MODEL = "doubao-seedream-5.0-lite"
CROP_TOP_PCT = 0.05   # 上裁 5%
CROP_BOTTOM_PCT = 0.10  # 下裁 10%

def generate_image(prompt, size="1920x1920", out_dir="."):
    payload = {"model": MODEL, "prompt": prompt, "n": 1, "size": size, "response_format": "b64_json"}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    print(f"[1/4] 调用 SeeDream 生成图片...", flush=True)
    resp = requests.post(URL, json=payload, headers=headers)
    print(f"[2/4] 响应状态码: {resp.status_code}", flush=True)
    if not resp.ok:
        print(f"错误: {resp.text}", flush=True)
        sys.exit(1)

    data = resp.json()
    b64 = data["data"][0]["b64_json"]
    img_bytes = base64.b64decode(b64)
    return img_bytes

def crop_image(img_bytes, crop_top_pct, crop_bottom_pct, out_dir, basename):
    """保存原图和裁切图"""
    os.makedirs(out_dir, exist_ok=True)

    # 保存原图（后缀 _original）
    orig_path = os.path.join(out_dir, f"{basename}_original.png")
    with open(orig_path, "wb") as f:
        f.write(img_bytes)
    print(f"[3/4] 原图保存: {orig_path}", flush=True)

    # 裁切并保存
    img = Image.open(orig_path)
    w, h = img.size
    crop_top = int(h * crop_top_pct)
    crop_bottom = int(h * crop_bottom_pct)
    cropped = img.crop((0, crop_top, w, h - crop_bottom))
    cropped_path = os.path.join(out_dir, f"{basename}.png")
    cropped.save(cropped_path, "PNG")
    print(f"[4/4] 裁切图保存: {cropped_path} ({w}x{h-crop_top-crop_bottom})", flush=True)

if __name__ == "__main__":
    prompt = (
        "公众号封面图，主题：AI工具演进路线。"
        "视觉元素：从左到右排列四个工具的图标或符号——DeepSeek（蓝色菱形）、TRAE（绿色箭头）、"
        "OpenClaw（龙虾轮廓）、WorkBuddy（橙色圆形），中间用流动的线条连接。"
        "背景：深蓝到深灰渐变，科技感。"
        "文字标题：从DeepSeek到WorkBuddy，副标题：我的AI工具折腾史。"
        "风格：简洁、现代、科技感，适合微信公众号封面。尺寸：1920x1920，方形。"
    )

    out_dir = r"D:\github\zmyAI\zmyAI.github.io\source\_posts\从DeepSeek到TRAE到WorkBuddy"
    img_bytes = generate_image(prompt)
    crop_image(img_bytes, CROP_TOP_PCT, CROP_BOTTOM_PCT, out_dir, "cover")

    print("完成：原图和裁切图均已保存", flush=True)
