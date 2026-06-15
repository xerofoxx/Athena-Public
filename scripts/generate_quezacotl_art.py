#!/usr/bin/env python3
"""
Generate StepMania title card art for deadmau5 — Quezacotl

Art direction:
  - 2005-era StepMania card aesthetic (bold, glowy, high contrast)
  - Color gradient: golden orange (top) → singularity white → psychic purple (bottom)
  - Neon bars / Tron city lighting
  - Cinema 4D metallic deadmau5 head silhouette, blended into bg
  - Text: "QUEZACOTL" (title), "deadmau5" (artist)

Generates:
  - Quezacotl-bg.png    (640x480 background)
  - Quezacotl.png        (256x80 banner)  [StepMania standard banner]
"""
import math, random, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops, ImageEnhance

random.seed(42)  # reproducible

# ── Colors ──
GOLD_ORANGE   = (255, 165, 30)
DEEP_GOLD     = (200, 120, 0)
SINGULARITY_W = (240, 235, 255)
PSYCHIC_PURPLE = (138, 43, 226)
DEEP_PURPLE    = (60, 10, 100)
NEON_CYAN      = (0, 255, 255)
NEON_MAGENTA   = (255, 0, 180)
NEON_GOLD      = (255, 200, 50)
TRON_BLUE      = (0, 180, 255)
CHROME_LIGHT   = (220, 225, 255)
CHROME_MID     = (140, 145, 170)
CHROME_DARK    = (60, 55, 80)
BLACK          = (0, 0, 0)
WHITE          = (255, 255, 255)


def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_gradient_bg(img):
    """Three-zone vertical gradient: gold → white → purple."""
    w, h = img.size
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        if t < 0.35:
            c = lerp_color(DEEP_GOLD, GOLD_ORANGE, t / 0.35)
        elif t < 0.50:
            c = lerp_color(GOLD_ORANGE, SINGULARITY_W, (t - 0.35) / 0.15)
        elif t < 0.65:
            c = lerp_color(SINGULARITY_W, PSYCHIC_PURPLE, (t - 0.50) / 0.15)
        else:
            c = lerp_color(PSYCHIC_PURPLE, DEEP_PURPLE, (t - 0.65) / 0.35)
        draw.line([(0, y), (w, y)], fill=c)


def draw_tron_city(img):
    """Futuristic city grid lines — Tron-style perspective grid + vertical towers."""
    w, h = img.size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Horizon line in the middle-bottom area
    horizon_y = int(h * 0.55)
    vanishing_x = w // 2
    
    # Horizontal grid lines (perspective)
    for i in range(20):
        t = (i / 20.0) ** 1.5
        y = horizon_y + int((h - horizon_y) * t)
        alpha = int(40 + 60 * (1 - t))
        color = (*TRON_BLUE, alpha)
        draw.line([(0, y), (w, y)], fill=color, width=1)
    
    # Vertical perspective lines radiating from vanishing point
    for i in range(-12, 13):
        angle = i * 7
        end_x = vanishing_x + int(math.tan(math.radians(angle)) * h)
        alpha = max(20, 60 - abs(i) * 4)
        color = (*NEON_CYAN, alpha)
        draw.line([(vanishing_x, horizon_y), (end_x, h)], fill=color, width=1)
    
    # City tower silhouettes
    tower_data = []
    for i in range(30):
        tx = random.randint(0, w)
        tw = random.randint(8, 40)
        th = random.randint(40, 200)
        dist = abs(tx - vanishing_x) / (w / 2)
        th = int(th * (0.3 + 0.7 * (1 - dist)))
        ty = horizon_y - th
        tower_data.append((tx - tw // 2, ty, tx + tw // 2, horizon_y))
    
    for (x1, y1, x2, y2) in tower_data:
        # Dark tower body
        draw.rectangle([x1, y1, x2, y2], fill=(10, 5, 30, 100))
        # Neon edge lines
        edge_color = (*random.choice([NEON_CYAN, TRON_BLUE, NEON_MAGENTA]), 60)
        draw.line([(x1, y1), (x1, y2)], fill=edge_color, width=1)
        draw.line([(x2, y1), (x2, y2)], fill=edge_color, width=1)
        # Random window lights
        for wy in range(y1 + 4, y2 - 2, random.randint(6, 12)):
            if random.random() < 0.4:
                wc = (*random.choice([NEON_CYAN, NEON_GOLD, WHITE]), random.randint(40, 90))
                wx = (x1 + x2) // 2
                draw.rectangle([wx - 1, wy, wx + 1, wy + 1], fill=wc)
    
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))


def draw_neon_bars(img):
    """Horizontal neon accent bars across the image."""
    w, h = img.size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    bar_positions = [
        (0.12, NEON_GOLD, 3, 80),
        (0.18, NEON_CYAN, 2, 50),
        (0.28, NEON_MAGENTA, 2, 60),
        (0.42, WHITE, 1, 40),
        (0.58, NEON_CYAN, 2, 50),
        (0.72, NEON_MAGENTA, 3, 70),
        (0.78, PSYCHIC_PURPLE, 2, 55),
        (0.85, NEON_GOLD, 2, 45),
        (0.92, TRON_BLUE, 1, 35),
    ]
    
    for (pos, color, width, alpha) in bar_positions:
        y = int(h * pos)
        # Main bar
        draw.line([(0, y), (w, y)], fill=(*color, alpha), width=width)
        # Glow around bar
        for offset in range(1, 6):
            glow_alpha = max(0, alpha - offset * 15)
            draw.line([(0, y - offset), (w, y - offset)], 
                     fill=(*color, glow_alpha), width=1)
            draw.line([(0, y + offset), (w, y + offset)], 
                     fill=(*color, glow_alpha), width=1)
    
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))


def draw_deadmau5_head(img, cx, cy, radius):
    """Draw a stylized metallic deadmau5 head using shape-based rendering.
    
    Fast approach: draw filled shapes with outline glows rather than per-pixel.
    """
    w, h = img.size
    r = radius
    ear_r = int(r * 0.45)
    ear_offset_x = int(r * 0.65)
    ear_offset_y = int(r * 0.75)
    
    ear_l_cx = cx - ear_offset_x
    ear_l_cy = cy - ear_offset_y
    ear_r_cx = cx + ear_offset_x
    ear_r_cy = cy - ear_offset_y
    
    # -- Outer glow layer (big soft glow behind head) --
    glow_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    for expand in range(20, 0, -2):
        alpha = int(8 + expand * 2)
        gc = (*lerp_color(NEON_CYAN, PSYCHIC_PURPLE, expand / 20), alpha)
        gd.ellipse([cx - r - expand, cy - r - expand, cx + r + expand, cy + r + expand], fill=gc)
        gd.ellipse([ear_l_cx - ear_r - expand, ear_l_cy - ear_r - expand,
                     ear_l_cx + ear_r + expand, ear_l_cy + ear_r + expand], fill=gc)
        gd.ellipse([ear_r_cx - ear_r - expand, ear_r_cy - ear_r - expand,
                     ear_r_cx + ear_r + expand, ear_r_cy + ear_r + expand], fill=gc)
    
    # -- Chrome body: dark base with bright outline --
    body_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body_layer)
    
    # Fill body with a vertical chrome gradient using concentric rings
    for ring in range(r, 0, -1):
        t = 1.0 - (ring / r)
        # Chrome: dark edges, bright middle band, dark center
        if t < 0.15:
            c = lerp_color(CHROME_DARK, (40, 30, 70), t / 0.15)
        elif t < 0.3:
            c = lerp_color((40, 30, 70), CHROME_MID, (t - 0.15) / 0.15)
        elif t < 0.5:
            c = lerp_color(CHROME_MID, CHROME_LIGHT, (t - 0.3) / 0.2)
        elif t < 0.7:
            c = lerp_color(CHROME_LIGHT, CHROME_MID, (t - 0.5) / 0.2)
        else:
            c = lerp_color(CHROME_MID, CHROME_DARK, (t - 0.7) / 0.3)
        bd.ellipse([cx - ring, cy - ring, cx + ring, cy + ring], fill=(*c, 220))
    
    # Ears with similar gradient
    for (ecx, ecy) in [(ear_l_cx, ear_l_cy), (ear_r_cx, ear_r_cy)]:
        for ring in range(ear_r, 0, -1):
            t = 1.0 - (ring / ear_r)
            if t < 0.2:
                c = lerp_color(CHROME_DARK, CHROME_MID, t / 0.2)
            elif t < 0.5:
                c = lerp_color(CHROME_MID, CHROME_LIGHT, (t - 0.2) / 0.3)
            else:
                c = lerp_color(CHROME_LIGHT, CHROME_MID, (t - 0.5) / 0.5)
            bd.ellipse([ecx - ring, ecy - ring, ecx + ring, ecy + ring], fill=(*c, 220))
    
    # Bright outline (neon edge)
    for outline_w in range(4, 0, -1):
        oc = (*NEON_CYAN, 40 + outline_w * 30)
        bd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=oc, width=outline_w)
        bd.ellipse([ear_l_cx - ear_r, ear_l_cy - ear_r,
                     ear_l_cx + ear_r, ear_l_cy + ear_r], outline=oc, width=outline_w)
        bd.ellipse([ear_r_cx - ear_r, ear_r_cy - ear_r,
                     ear_r_cx + ear_r, ear_r_cy + ear_r], outline=oc, width=outline_w)
    
    # -- Eyes: X marks --
    eye_y = cy + int(r * 0.05)
    eye_l_x = cx - int(r * 0.3)
    eye_r_x = cx + int(r * 0.3)
    eye_size = int(r * 0.20)
    
    for (ex, ey) in [(eye_l_x, eye_y), (eye_r_x, eye_y)]:
        s = eye_size
        # Glow behind X
        for gw in range(6, 0, -1):
            gc = (*NEON_CYAN, 15 + gw * 8)
            bd.line([(ex - s, ey - s), (ex + s, ey + s)], fill=gc, width=gw + 3)
            bd.line([(ex + s, ey - s), (ex - s, ey + s)], fill=gc, width=gw + 3)
        # Dark X
        bd.line([(ex - s, ey - s), (ex + s, ey + s)], fill=(*BLACK, 240), width=4)
        bd.line([(ex + s, ey - s), (ex - s, ey + s)], fill=(*BLACK, 240), width=4)
        # Bright X center line
        bd.line([(ex - s, ey - s), (ex + s, ey + s)], fill=(*DEEP_PURPLE, 180), width=2)
        bd.line([(ex + s, ey - s), (ex - s, ey + s)], fill=(*DEEP_PURPLE, 180), width=2)
    
    # -- Mouth: curved line --
    mouth_y = cy + int(r * 0.45)
    mouth_w = int(r * 0.5)
    bd.arc([cx - mouth_w, mouth_y - int(r * 0.12),
            cx + mouth_w, mouth_y + int(r * 0.12)],
           start=10, end=170, fill=(*BLACK, 200), width=3)
    
    # -- Specular highlight (bright spot upper-left for 3D feel) --
    spec_cx = cx - int(r * 0.25)
    spec_cy = cy - int(r * 0.3)
    for spec_r in range(int(r * 0.3), 0, -1):
        alpha = int(15 * (1 - spec_r / (r * 0.3)))
        bd.ellipse([spec_cx - spec_r, spec_cy - spec_r,
                     spec_cx + spec_r, spec_cy + spec_r], 
                   fill=(255, 255, 255, alpha))
    
    # -- Composite everything --
    img_rgba = img.convert('RGBA')
    result = Image.alpha_composite(img_rgba, glow_layer)
    result = Image.alpha_composite(result, body_layer)
    img.paste(result.convert('RGB'))


def draw_x_eye(draw, cx, cy, size):
    """Draw an X-shaped eye (deadmau5 signature)."""
    color = (*BLACK, 220)
    s = size
    draw.line([(cx - s, cy - s), (cx + s, cy + s)], fill=color, width=3)
    draw.line([(cx + s, cy - s), (cx - s, cy + s)], fill=color, width=3)
    # Glow around X
    glow_color = (*NEON_CYAN, 60)
    draw.line([(cx - s - 1, cy - s - 1), (cx + s + 1, cy + s + 1)], fill=glow_color, width=5)
    draw.line([(cx + s + 1, cy - s - 1), (cx - s - 1, cy + s + 1)], fill=glow_color, width=5)


def draw_text_with_glow(img, text, x, y, font, fill, glow_color, glow_radius=4):
    """Draw text with a neon glow effect behind it."""
    w, h = img.size
    # Glow layer
    glow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.text((x, y), text, font=font, fill=(*glow_color, 180), anchor='mm')
    glow = glow.filter(ImageFilter.GaussianBlur(glow_radius))
    # Stack glow twice for intensity
    glow2 = glow.copy()
    glow = Image.alpha_composite(glow, glow2)
    
    # Text layer
    text_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_layer)
    # Shadow
    text_draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 150), anchor='mm')
    # Main text
    text_draw.text((x, y), text, font=font, fill=(*fill, 255), anchor='mm')
    
    # Composite
    img_rgba = img.convert('RGBA')
    result = Image.alpha_composite(img_rgba, glow)
    result = Image.alpha_composite(result, text_layer)
    img.paste(result.convert('RGB'))


def get_font(size, bold=False):
    """Try to load a good font, fall back to default."""
    font_paths = [
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    if bold:
        font_paths = [
            "C:/Windows/Fonts/impact.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
        ] + font_paths
    
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()


def add_scanlines(img, alpha=15):
    """Add CRT-style scanlines for that 2005 aesthetic."""
    w, h = img.size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(0, h, 2):
        draw.line([(0, y), (w, y)], fill=(0, 0, 0, alpha), width=1)
    img_rgba = img.convert('RGBA')
    result = Image.alpha_composite(img_rgba, overlay)
    img.paste(result.convert('RGB'))


def add_bloom(img, intensity=1.2):
    """Add a subtle bloom/glow to bright areas."""
    bright = img.copy()
    bright = ImageEnhance.Brightness(bright).enhance(1.5)
    bright = bright.filter(ImageFilter.GaussianBlur(15))
    return ImageChops.add(img, bright, scale=2, offset=0)


# ═══════════════════════════════════════════════════════════
# MAIN GENERATION
# ═══════════════════════════════════════════════════════════

def generate_background(path):
    """Generate the 640x480 background image."""
    W, H = 640, 480
    img = Image.new('RGB', (W, H), BLACK)
    
    print("  Drawing gradient...")
    draw_gradient_bg(img)
    
    print("  Drawing Tron city...")
    draw_tron_city(img)
    
    print("  Drawing neon bars...")
    draw_neon_bars(img)
    
    print("  Drawing deadmau5 head...")
    draw_deadmau5_head(img, W // 2, int(H * 0.42), int(H * 0.22))
    
    print("  Adding text...")
    # Title: QUEZACOTL
    title_font = get_font(72, bold=True)
    draw_text_with_glow(img, "QUEZACOTL", W // 2, int(H * 0.15),
                        title_font, WHITE, NEON_GOLD, glow_radius=6)
    
    # Artist: deadmau5
    artist_font = get_font(32, bold=True)
    draw_text_with_glow(img, "deadmau5", W // 2, int(H * 0.82),
                        artist_font, SINGULARITY_W, PSYCHIC_PURPLE, glow_radius=4)
    
    # Subtitle
    sub_font = get_font(18)
    draw_text_with_glow(img, "~ Effortless Flow Edit ~", W // 2, int(H * 0.90),
                        sub_font, NEON_CYAN, TRON_BLUE, glow_radius=3)
    
    print("  Post-processing...")
    img = add_bloom(img)
    add_scanlines(img, alpha=12)
    
    img.save(path, 'PNG')
    print(f"  ✓ Background: {path} ({os.path.getsize(path):,} bytes)")


def generate_banner(path):
    """Generate the 256x80 banner image."""
    W, H = 256, 80
    img = Image.new('RGB', (W, H), BLACK)
    
    # Gradient
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        if t < 0.3:
            c = lerp_color(DEEP_GOLD, GOLD_ORANGE, t / 0.3)
        elif t < 0.5:
            c = lerp_color(GOLD_ORANGE, SINGULARITY_W, (t - 0.3) / 0.2)
        elif t < 0.7:
            c = lerp_color(SINGULARITY_W, PSYCHIC_PURPLE, (t - 0.5) / 0.2)
        else:
            c = lerp_color(PSYCHIC_PURPLE, DEEP_PURPLE, (t - 0.7) / 0.3)
        draw.line([(0, y), (W, y)], fill=c)
    
    # Neon bars (simplified)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for (pos, color, alpha) in [(0.15, NEON_GOLD, 50), (0.5, NEON_CYAN, 40),
                                 (0.85, NEON_MAGENTA, 50)]:
        y = int(H * pos)
        od.line([(0, y), (W, y)], fill=(*color, alpha), width=1)
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))
    
    # Small deadmau5 head on the left
    head_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_layer)
    hx, hy, hr = 45, 42, 20
    ear_r = 9
    # Head
    hd.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], 
               fill=(*CHROME_MID, 160), outline=(*NEON_CYAN, 120), width=1)
    # Ears
    for ex in [hx - 13, hx + 13]:
        ey = hy - 16
        hd.ellipse([ex - ear_r, ey - ear_r, ex + ear_r, ey + ear_r],
                   fill=(*CHROME_MID, 160), outline=(*NEON_CYAN, 120), width=1)
    # X eyes
    for ex in [hx - 7, hx + 7]:
        ey = hy + 2
        hd.line([(ex - 3, ey - 3), (ex + 3, ey + 3)], fill=(*BLACK, 200), width=2)
        hd.line([(ex + 3, ey - 3), (ex - 3, ey + 3)], fill=(*BLACK, 200), width=2)
    
    img_rgba = img.convert('RGBA')
    result = Image.alpha_composite(img_rgba, head_layer)
    img = result.convert('RGB')
    
    # Text
    title_font = get_font(28, bold=True)
    artist_font = get_font(14, bold=True)
    draw_text_with_glow(img, "QUEZACOTL", 158, 30,
                        title_font, WHITE, NEON_GOLD, glow_radius=3)
    draw_text_with_glow(img, "deadmau5", 158, 55,
                        artist_font, SINGULARITY_W, PSYCHIC_PURPLE, glow_radius=2)
    
    add_scanlines(img, alpha=10)
    img.save(path, 'PNG')
    print(f"  ✓ Banner: {path} ({os.path.getsize(path):,} bytes)")


if __name__ == '__main__':
    folder = r'c:\Program Files (x86)\StepMania\Songs\_Dance Dance Challenge\Quezacotl'
    
    print("Generating Quezacotl art...")
    print()
    
    bg_path = os.path.join(folder, 'Quezacotl-bg.png')
    print("Background (640x480):")
    generate_background(bg_path)
    print()
    
    banner_path = os.path.join(folder, 'Quezacotl-banner.png')
    print("Banner (256x80):")
    generate_banner(banner_path)
    print()
    
    print("Done! Update .sm file references to use new images.")
