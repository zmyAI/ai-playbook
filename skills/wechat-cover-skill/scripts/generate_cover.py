"""公众号封面图生成工具

核心职责：调用火山引擎 SeeDream 模型生图 + 裁切至 2.35:1 + 保存 prompt。

封面图裁切策略：
- 从画面中心裁切，上下均等裁去相同像素至 2.35:1（左右不裁）
- 从裁切图中心裁 1:1 正方形作为缩略图
- prompt 文本保存为 {basename}_prompt.txt，方便排查

使用方式：
  python generate_cover.py <文章目录> --prompt "<AI编写的提示词>" [--size 2640x1404] [--basename cover]
"""
import requests, json, base64, sys, os, argparse, re
from PIL import Image

API_KEY = "ark-4ecd14b5-e28d-43a2-af09-f9cf4ceebb34-d39a2"
URL = "https://ark.cn-beijing.volces.com/api/plan/v3/images/generations"
MODEL = "doubao-seedream-5.0-lite"
CROP_TOP_PCT = 0.08
# 封面裁切比例：上下各裁 10%，对称裁至 2.35:1
CROP_PCT = 0.10
DEFAULT_SIZE = "2640x1404"
AUTHOR = "Python与AI未来"

# 公共裁切安全提示词（封面图：2.35:1，上下各裁 10%）
COVER_CROP_SAFETY_PREFIX = "【构图】所有文字和视觉元素集中在画面中央区域。顶部和底部各留约10%的等高空白背景边距，不放置任何文字或视觉元素。\n"

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS_DIR = os.path.join(SKILL_DIR, "prompts")

# ===== 预设风格（旧模式保留向后兼容） =====
STYLES = {
    "deep-tech": {"name": "深蓝科技信息图", "size": DEFAULT_SIZE, "prompt_file": "deep-tech.prompt"},
    "pixel-window": {"name": "像素窗口风", "size": DEFAULT_SIZE, "prompt_file": "pixel-window.prompt"},
    "particle-future": {"name": "未来科技粒子", "size": DEFAULT_SIZE, "prompt_file": "particle-future.prompt"},
    "clean-blue": {"name": "清爽科技蓝白", "size": DEFAULT_SIZE, "prompt_file": "clean-blue.prompt"},
    "summary-card": {"name": "文章总结卡", "size": "1080x1920", "prompt_file": "summary-card.prompt"},
}


def load_prompt(prompt_file, title, theme, points, author):
    """旧模式：从文件读取 prompt 模板并填入参数"""
    path = os.path.join(PROMPTS_DIR, prompt_file)
    if not os.path.exists(path):
        print(f"错误：未找到 prompt 文件 {path}", flush=True)
        return None
    with open(path, "r", encoding="utf-8") as f:
        tmpl = f.read()
    result = tmpl.format(
        title=title, theme=theme, author=author,
        points="、".join(points[:4]) if points else theme,
    )
    # 自动注入公共裁切安全提示词（summary 卡使用单独的四周8%裁切，不注入）
    if prompt_file != "summary-card.prompt":
        result = COVER_CROP_SAFETY_PREFIX + result
    return result


def extract_article_info(content):
    """从文章内容提取标题、主题、关键点"""
    title = ""
    theme = ""
    points = []

    for line in content.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break

    paragraphs = []
    in_body = False
    for line in content.split("\n"):
        if line.startswith("# ") and title:
            in_body = True
            continue
        if in_body and line.strip() and not line.startswith("#") and not line.startswith("!"):
            paragraphs.append(line.strip())
            if len(paragraphs) >= 5:
                break
    theme = " ".join(paragraphs[:3])[:200]

    for line in content.split("\n"):
        if line.startswith("## ") and not line.startswith("### "):
            pt = line[3:].strip()
            pt = re.sub(r"[【\[\<].*?[】\]\>]", "", pt).strip()
            if pt:
                points.append(pt)

    return title or "文章", theme, points[:6]


def generate_image(prompt, size):
    """调用火山引擎 SeeDream 模型生图"""
    payload = {"model": MODEL, "prompt": prompt, "n": 1, "size": size, "response_format": "b64_json"}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    resp = requests.post(URL, json=payload, headers=headers)
    if not resp.ok:
        print(f"错误: {resp.text}", flush=True)
        return None
    return base64.b64decode(resp.json()["data"][0]["b64_json"])


def crop_and_save(img_bytes, out_dir, basename, mode="cover"):
    """
    裁切保存图片。

    封面模式（mode="cover"）：
    - 上下均等裁切至 2.35:1（从画面中心取）
    - 左右不裁
    - 额外输出 1:1 中心裁切的缩略图

    总结卡模式（mode="summary"）：
    - 四周 8% 裁切
    """
    os.makedirs(out_dir, exist_ok=True)
    orig_path = os.path.join(out_dir, f"{basename}_original.png")
    with open(orig_path, "wb") as f:
        f.write(img_bytes)
    img = Image.open(orig_path)
    w, h = img.size

    if mode == "summary":
        # 总结卡：四周 8% 等比例裁切
        c = CROP_TOP_PCT
        left = int(w * c)
        top = int(h * c)
        right = int(w * (1 - c))
        bottom = int(h * (1 - c))
        cropped = img.crop((left, top, right, bottom))
        cropped_path = os.path.join(out_dir, f"{basename}.png")
        cropped.save(cropped_path, "PNG")
        print(f"  原图: {orig_path}", flush=True)
        print(f"  裁切: {cropped_path} ({cropped.size[0]}x{cropped.size[1]})", flush=True)
        return orig_path, cropped_path, None

    # === 封面模式：上下各裁 10% 至 2.35:1 ===
    crop_px = int(h * CROP_PCT)  # 上下各裁的比例
    top = crop_px
    bottom = crop_px

    print(f"  裁切策略: 上下各 {CROP_PCT*100:.0f}%, 上 {top}px, 下 {bottom}px, 左右不裁",
          flush=True)
    print(f"  目标比例: 2.35:1 ({w}x{h - 2*crop_px})", flush=True)

    cropped = img.crop((0, top, w, h - bottom))
    cw, ch = cropped.size
    cropped_path = os.path.join(out_dir, f"{basename}.png")
    cropped.save(cropped_path, "PNG")

    # 1:1 缩略图（从裁切图中心取）
    s = min(cw, ch)
    l = (cw - s) // 2
    t = (ch - s) // 2
    thumb = cropped.crop((l, t, l + s, t + s))
    thumb_path = os.path.join(out_dir, f"{basename}_thumbnail.png")
    thumb.save(thumb_path, "PNG")

    print(f"  原图: {orig_path} ({w}x{h})", flush=True)
    print(f"  裁切(2.35:1): {cropped_path} ({cw}x{ch})", flush=True)
    print(f"  缩略图(1:1): {thumb_path} ({s}x{s})", flush=True)

    return orig_path, cropped_path, thumb_path


def main():
    parser = argparse.ArgumentParser(
        description="公众号封面图/总结卡生成工具（基于火山引擎 SeeDream）")
    parser.add_argument("article_dir", help="文章目录（含 .md 文件）")
    # ---- 核心参数：AI 直接提供 prompt ----
    parser.add_argument("--prompt", help="生图提示词（AI 根据文章内容动态生成）")
    parser.add_argument("--size", default=DEFAULT_SIZE,
                        help="生图尺寸，格式 宽x高，默认 " + DEFAULT_SIZE)
    parser.add_argument("--basename", default="cover",
                        help="输出文件名前缀（不含扩展名），默认 'cover'")
    # ---- 旧模式参数（向后兼容） ----
    parser.add_argument("--styles", nargs="+", default=None,
                        help="[旧模式] 要生成的预设风格列表")
    parser.add_argument("--type", choices=["cover", "summary"], default=None,
                        help="[旧模式] cover: 封面图, summary: 总结卡")
    parser.add_argument("--author", default=AUTHOR,
                        help=f"公众号/作者名，默认{AUTHOR}")
    args = parser.parse_args()

    # ---- 读取文章 ----
    article_path = None
    for f in os.listdir(args.article_dir):
        if f.endswith(".md"):
            article_path = os.path.join(args.article_dir, f)
            break
    if not article_path:
        print("错误：未在目录中找到 .md 文件", flush=True)
        sys.exit(1)

    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()

    title, theme, points = extract_article_info(content)
    print(f"文章: {title}", flush=True)
    print(f"关键点: {points}", flush=True)

    # ===== 模式1（推荐）：AI 自定义提示词 =====
    if args.prompt:
        print(f"\n[自定义模式]", flush=True)
        print(f"尺寸: {args.size}", flush=True)
        # 根据尺寸判断模式：竖版 1080x1920 走 summary 裁切
        mode = "summary" if args.size == "1080x1920" else "cover"
        img_bytes = generate_image(args.prompt, args.size)
        if not img_bytes:
            sys.exit(1)
        crop_and_save(img_bytes, args.article_dir, args.basename, mode=mode)
        # 保存 prompt 文本
        prompt_path = os.path.join(args.article_dir, f"{args.basename}_prompt.txt")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(args.prompt)
        print(f"  prompt: {prompt_path}", flush=True)
        return

    # ===== 模式2（旧）：预设风格轮询 =====
    style_keys = args.styles or list(STYLES.keys())
    if args.type == "summary":
        style_keys = [s for s in style_keys if STYLES.get(s, {}).get("size") == "1080x1920"]
    elif args.type == "cover":
        style_keys = [s for s in style_keys if STYLES.get(s, {}).get("size") != "1080x1920"]

    results = []
    for sk in style_keys:
        if sk not in STYLES:
            print(f"跳过未知风格: {sk}", flush=True)
            continue
        info = STYLES[sk]
        print(f"\n[{sk}] 生成 {info['name']} ({info['size']})...", flush=True)
        prompt = load_prompt(info["prompt_file"], title, theme, points, args.author)
        if not prompt:
            continue
        img_bytes = generate_image(prompt, info["size"])
        if not img_bytes:
            continue
        mode = "summary" if info["size"] == "1080x1920" else "cover"
        orig, cropped, thumb = crop_and_save(
            img_bytes, args.article_dir, f"cover_{sk}", mode=mode)
        results.append((sk, info["name"], orig, cropped, thumb))

    if not results:
        print("未生成任何图片", flush=True)
        sys.exit(1)

    print("\n=== 结果汇总 ===", flush=True)
    for sk, sn, orig, cropped, thumb in results:
        line = f"  [{sk}] {sn}: {cropped}"
        if thumb:
            line += f" 缩略图: {thumb}"
        print(line, flush=True)
    print(f"\n共生成 {len(results)} 张", flush=True)


if __name__ == "__main__":
    main()
