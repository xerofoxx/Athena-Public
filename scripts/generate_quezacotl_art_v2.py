#!/usr/bin/env python3
"""
Generate StepMania title card art for deadmau5 — Quezacotl  (v2)

Art direction (from reference scene):
  - Aztec temple corridor perspective with vanishing point
  - Stone-carved deadmau5 head at center with glowing magenta eyes
  - Neon light pillars: blue-white tops, hot pink/magenta bottoms
  - Starry indigo night sky above
  - Stone floor with perspective grid
  - DDR Japanese arcade aesthetic: bold text, katakana accents,
    speed lines, energy effects
  - Feathered serpent (Quetzalcoatl) motifs

Color palette:
  Deep indigo sky → cyan/blue neons → hot pink/magenta neons
  Stone grays → warm stone tan highlights
"""
import math, random, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops, ImageEnhance

random.seed(42)

# ── Colors ──
SKY_DARK      = (8, 12, 35)
SKY_MID       = (15, 25, 65)
STAR_WHITE    = (220, 225, 255)
NEON_CYAN     = (0, 200, 255)
NEON_BLUE     = (30, 100, 255)
NEON_WHITE    = (220, 240, 255)
NEON_PINK     = (255, 20, 120)
NEON_MAGENTA  = (255, 0, 180)
NEON_HOT      = (255, 60, 160)
STONE_DARK    = (35, 30, 40)
STONE_MID     = (55, 50, 60)
STONE_LIGHT   = (80, 75, 85)
STONE_TAN     = (100, 90, 75)
FLOOR_DARK    = (25, 22, 32)
FLOOR_LIGHT   = (45, 40, 52)
CHROME_LIGHT  = (180, 175, 195)
CHROME_MID    = (110, 105, 125)
EYE_GLOW      = (255, 30, 80)
EYE_CORE      = (255, 200, 220)
GOLD_ACCENT   = (255, 180, 40)
BLACK         = (0, 0, 0)
WHITE         = (255, 255, 255)


def lerp(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(len(c1)))


def draw_starry_sky(draw, w, h, horizon_y):
    """Deep indigo sky with scattered stars above the horizon."""
    for y in range(horizon_y):
        t = y / horizon_y
        c = lerp(SKY_DARK, SKY_MID, t)
        draw.line([(0, y), (w, y)], fill=c)
    # Stars
    for _ in range(300):
        sx = random.randint(0, w - 1)
        sy = random.randint(0, horizon_y - 5)
        brightness = random.randint(100, 255)
        size = random.choice([0, 0, 0, 1])
        sc = (brightness, brightness, min(255, brightness + 20))
        if size == 0:
            draw.point((sx, sy), fill=sc)
        else:
            draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=sc)


def draw_perspective_floor(draw, w, h, horizon_y, vx):
    """Stone floor with perspective grid lines converging to vanishing point."""
    # Floor gradient
    for y in range(horizon_y, h):
        t = (y - horizon_y) / (h - horizon_y)
        c = lerp(FLOOR_DARK, FLOOR_LIGHT, t * 0.5)
        # Add slight warm tone near bottom
        c = lerp(c, (50, 40, 45), t * 0.3)
        draw.line([(0, y), (w, y)], fill=c)
    
    # Horizontal grid lines (perspective spacing)
    for i in range(25):
        t = (i / 25.0) ** 1.8
        y = horizon_y + int((h - horizon_y) * t)
        alpha_color = lerp(STONE_MID, FLOOR_DARK, t)
        draw.line([(0, y), (w, y)], fill=alpha_color, width=1)
    
    # Vertical perspective lines from vanishing point
    for i in range(-15, 16):
        angle = i * 5
        end_x = vx + int(math.tan(math.radians(angle)) * (h - horizon_y) * 2.5)
        c = lerp(STONE_MID, FLOOR_DARK, abs(i) / 15)
        draw.line([(vx, horizon_y), (end_x, h)], fill=c, width=1)


def draw_pillar(img, base_x, horizon_y, h, pillar_w, pillar_h, side, neon_top_color, neon_bot_color):
    """Draw a stone pillar with neon light sections."""
    draw = ImageDraw.Draw(img)
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    
    top_y = horizon_y - pillar_h
    
    # Stone pillar body
    for x in range(pillar_w):
        px = base_x + x
        if 0 <= px < img.size[0]:
            noise = random.randint(-5, 5)
            for y in range(top_y, horizon_y):
                t = (y - top_y) / pillar_h
                sc = lerp(STONE_LIGHT, STONE_DARK, t)
                sc = tuple(max(0, min(255, c + noise)) for c in sc)
                draw.point((px, y), fill=sc)
    
    # Neon light section - top (cyan/blue-white)
    neon_top_y = top_y + int(pillar_h * 0.1)
    neon_top_h = int(pillar_h * 0.25)
    neon_w = max(4, pillar_w - 6)
    neon_x = base_x + 3
    
    # Top neon block
    for glow_r in range(20, 0, -1):
        alpha = int(3 + glow_r * 1.5)
        gc = (*neon_top_color, alpha)
        od.rectangle([neon_x - glow_r, neon_top_y - glow_r,
                      neon_x + neon_w + glow_r, neon_top_y + neon_top_h + glow_r], fill=gc)
    # Core neon
    od.rectangle([neon_x, neon_top_y, neon_x + neon_w, neon_top_y + neon_top_h],
                 fill=(*NEON_WHITE, 240))
    # Gradient overlay on core
    for y in range(neon_top_h):
        t = y / neon_top_h
        c = lerp(NEON_WHITE, neon_top_color, t)
        od.line([(neon_x, neon_top_y + y), (neon_x + neon_w, neon_top_y + y)],
                fill=(*c, 200), width=1)
    
    # Bottom neon block (pink/magenta)
    neon_bot_y = horizon_y - int(pillar_h * 0.35)
    neon_bot_h = int(pillar_h * 0.25)
    
    for glow_r in range(25, 0, -1):
        alpha = int(3 + glow_r * 2)
        gc = (*neon_bot_color, alpha)
        od.rectangle([neon_x - glow_r, neon_bot_y - glow_r,
                      neon_x + neon_w + glow_r, neon_bot_y + neon_bot_h + glow_r], fill=gc)
    od.rectangle([neon_x, neon_bot_y, neon_x + neon_w, neon_bot_y + neon_bot_h],
                 fill=(*NEON_WHITE, 240))
    for y in range(neon_bot_h):
        t = y / neon_bot_h
        c = lerp(NEON_WHITE, neon_bot_color, t)
        od.line([(neon_x, neon_bot_y + y), (neon_x + neon_w, neon_bot_y + y)],
                fill=(*c, 200), width=1)
    
    # Floor reflection glow
    reflect_y = horizon_y
    for glow_r in range(30, 0, -2):
        alpha = int(2 + glow_r)
        gc = (*neon_bot_color, alpha)
        od.ellipse([base_x - glow_r, reflect_y - 5,
                    base_x + pillar_w + glow_r, reflect_y + glow_r * 2], fill=gc)
    
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))


def draw_mau5_head_stone(img, cx, cy, radius):
    """Stone-carved deadmau5 head with glowing magenta eyes — temple centerpiece."""
    w, h = img.size
    r = radius
    ear_r = int(r * 0.48)
    ear_ox = int(r * 0.68)
    ear_oy = int(r * 0.78)
    
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    
    # Outer glow (subtle magenta/cyan aura)
    for expand in range(30, 0, -2):
        alpha = int(2 + expand)
        gc = (*lerp(NEON_PINK, NEON_CYAN, expand / 30), alpha)
        od.ellipse([cx - r - expand, cy - r - expand,
                    cx + r + expand, cy + r + expand], fill=gc)
    
    # Stone head body — concentric rings with stone texture
    for ring in range(r, 0, -1):
        t = 1.0 - (ring / r)
        # Stone gradient: edges dark, mid lighter, center mid-dark
        if t < 0.05:
            c = lerp(STONE_DARK, (30, 25, 38), t / 0.05)
        elif t < 0.3:
            c = lerp(STONE_DARK, STONE_MID, (t - 0.05) / 0.25)
        elif t < 0.6:
            c = lerp(STONE_MID, STONE_LIGHT, (t - 0.3) / 0.3)
        elif t < 0.8:
            c = lerp(STONE_LIGHT, STONE_TAN, (t - 0.6) / 0.2)
        else:
            c = lerp(STONE_TAN, STONE_MID, (t - 0.8) / 0.2)
        od.ellipse([cx - ring, cy - ring, cx + ring, cy + ring], fill=(*c, 230))
    
    # Ears (stone)
    for (ecx, ecy) in [(cx - ear_ox, cy - ear_oy), (cx + ear_ox, cy - ear_oy)]:
        # Ear glow
        for expand in range(15, 0, -2):
            alpha = int(2 + expand)
            od.ellipse([ecx - ear_r - expand, ecy - ear_r - expand,
                        ecx + ear_r + expand, ecy + ear_r + expand],
                       fill=(*NEON_CYAN, alpha))
        # Ear stone body
        for ring in range(ear_r, 0, -1):
            t = 1.0 - (ring / ear_r)
            if t < 0.3:
                c = lerp(STONE_DARK, STONE_MID, t / 0.3)
            elif t < 0.6:
                c = lerp(STONE_MID, STONE_LIGHT, (t - 0.3) / 0.3)
            else:
                c = lerp(STONE_LIGHT, STONE_MID, (t - 0.6) / 0.4)
            od.ellipse([ecx - ring, ecy - ring, ecx + ring, ecy + ring], fill=(*c, 230))
    
    # Feathered serpent crown detail (zigzag pattern around head top)
    crown_r = r + 8
    for i in range(0, 360, 12):
        angle_rad = math.radians(i - 90)
        if -60 < (i - 180) < 60:  # only on top half
            continue
        px = cx + int(crown_r * math.cos(angle_rad))
        py = cy + int(crown_r * math.sin(angle_rad))
        # Small stone protrusion
        for pr in range(5, 0, -1):
            od.ellipse([px - pr, py - pr, px + pr, py + pr],
                       fill=(*STONE_TAN, 150 + pr * 15))
    
    # Stone edge outline
    for ow in range(3, 0, -1):
        oc = (*STONE_DARK, 100 + ow * 40)
        od.ellipse([cx - r, cy - r, cx + r, cy + r], outline=oc, width=ow)
        od.ellipse([cx - ear_ox - ear_r, cy - ear_oy - ear_r,
                    cx - ear_ox + ear_r, cy - ear_oy + ear_r], outline=oc, width=ow)
        od.ellipse([cx + ear_ox - ear_r, cy - ear_oy - ear_r,
                    cx + ear_ox + ear_r, cy - ear_oy + ear_r], outline=oc, width=ow)
    
    # ── GLOWING EYES ──
    eye_y = cy + int(r * 0.0)
    eye_lx = cx - int(r * 0.32)
    eye_rx = cx + int(r * 0.32)
    eye_sz = int(r * 0.22)
    
    for (ex, ey) in [(eye_lx, eye_y), (eye_rx, eye_y)]:
        # Big outer glow
        for gr in range(25, 0, -1):
            alpha = int(5 + gr * 4)
            gc = (*EYE_GLOW, alpha)
            od.ellipse([ex - eye_sz - gr, ey - eye_sz - gr,
                        ex + eye_sz + gr, ey + eye_sz + gr], fill=gc)
        # Eye shape (slightly oval)
        od.ellipse([ex - eye_sz, ey - int(eye_sz * 0.7),
                    ex + eye_sz, ey + int(eye_sz * 0.7)],
                   fill=(*EYE_GLOW, 255))
        # Bright core
        core_sz = int(eye_sz * 0.5)
        od.ellipse([ex - core_sz, ey - int(core_sz * 0.6),
                    ex + core_sz, ey + int(core_sz * 0.6)],
                   fill=(*EYE_CORE, 255))
    
    # Mouth (carved line)
    mouth_y = cy + int(r * 0.5)
    mouth_w = int(r * 0.45)
    od.arc([cx - mouth_w, mouth_y - int(r * 0.08),
            cx + mouth_w, mouth_y + int(r * 0.08)],
           start=10, end=170, fill=(*STONE_DARK, 200), width=3)
    
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))


def draw_corridor_neon_bars(img, vx, horizon_y, h):
    """Vertical neon accent bars receding toward vanishing point (blue pillars of light)."""
    w_img = img.size[0]
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    
    # Pairs of blue neon bars at various depths
    depths = [0.2, 0.35, 0.5, 0.65, 0.8]
    for depth in depths:
        # Bar position based on perspective depth
        spread = int((1.0 - depth) * w_img * 0.35)
        bar_h = int((1.0 - depth) * (horizon_y * 0.5))
        bar_w = max(2, int((1.0 - depth) * 6))
        bar_y = horizon_y - bar_h
        alpha = int(40 + (1.0 - depth) * 80)
        
        for side in [-1, 1]:
            bx = vx + side * spread
            # Glow
            for gr in range(12, 0, -1):
                gc = (*NEON_BLUE, int(alpha * gr / 24))
                od.rectangle([bx - bar_w - gr, bar_y - gr,
                              bx + bar_w + gr, horizon_y + gr], fill=gc)
            # Core
            od.rectangle([bx - bar_w, bar_y, bx + bar_w, horizon_y],
                         fill=(*NEON_CYAN, alpha))
    
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))


def draw_ddr_text_elements(img):
    """DDR Japanese-influenced text: bold title, katakana accents, speed lines."""
    w, h = img.size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    
    # Speed lines radiating from center (DDR energy effect)
    vx, vy = w // 2, int(h * 0.42)
    for i in range(60):
        angle = random.uniform(0, 2 * math.pi)
        start_r = random.randint(80, 130)
        end_r = random.randint(150, 300)
        sx = vx + int(start_r * math.cos(angle))
        sy = vy + int(start_r * math.sin(angle))
        ex = vx + int(end_r * math.cos(angle))
        ey = vy + int(end_r * math.sin(angle))
        alpha = random.randint(15, 50)
        c = random.choice([NEON_CYAN, NEON_PINK, WHITE])
        od.line([(sx, sy), (ex, ey)], fill=(*c, alpha), width=1)
    
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))
    
    # ── Title: QUEZACOTL ──
    title_font = get_font(68, bold=True)
    # Multiple layers for DDR-style outlined text
    text_glow(img, "QUEZACOTL", w // 2, int(h * 0.10), title_font,
              fill=WHITE, outline=NEON_CYAN, glow=NEON_BLUE, glow_r=8)
    
    # ── Japanese subtitle: ケツァルコアトル (Quetzalcoatl in katakana) ──
    jp_font = get_font(20)
    text_glow(img, "ケツァルコアトル", w // 2, int(h * 0.18), jp_font,
              fill=GOLD_ACCENT, outline=None, glow=NEON_PINK, glow_r=4)
    
    # ── Artist: deadmau5 ──
    artist_font = get_font(36, bold=True)
    text_glow(img, "deadmau5", w // 2, int(h * 0.88), artist_font,
              fill=WHITE, outline=NEON_PINK, glow=NEON_MAGENTA, glow_r=6)
    
    # ── Subtitle ──
    sub_font = get_font(16)
    text_glow(img, "— EFFORTLESS FLOW EDIT —", w // 2, int(h * 0.95), sub_font,
              fill=NEON_CYAN, outline=None, glow=NEON_BLUE, glow_r=3)
    
    # ── DDR-style difficulty badge area (small decorative text) ──
    tiny_font = get_font(12)
    text_glow(img, "DANCE DANCE CHALLENGE", w // 2, int(h * 0.03), tiny_font,
              fill=(*NEON_PINK,), outline=None, glow=NEON_MAGENTA, glow_r=2)


def text_glow(img, text, x, y, font, fill, outline, glow, glow_r):
    """Draw text with glow, outline, and shadow — DDR arcade style."""
    w, h = img.size
    
    # Glow layer
    gl = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gl)
    gd.text((x, y), text, font=font, fill=(*glow, 200), anchor='mm')
    gl = gl.filter(ImageFilter.GaussianBlur(glow_r))
    gl2 = gl.copy()
    gl = Image.alpha_composite(gl, gl2)
    
    # Text layer
    tl = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tl)
    # Shadow
    td.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 180), anchor='mm')
    # Outline (draw text offset in 8 directions)
    if outline:
        for dx in [-2, 0, 2]:
            for dy in [-2, 0, 2]:
                if dx or dy:
                    td.text((x + dx, y + dy), text, font=font,
                            fill=(*outline, 200), anchor='mm')
    # Main text
    td.text((x, y), text, font=font, fill=(*fill, 255), anchor='mm')
    
    img_rgba = img.convert('RGBA')
    result = Image.alpha_composite(img_rgba, gl)
    result = Image.alpha_composite(result, tl)
    img.paste(result.convert('RGB'))


def get_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ] if bold else [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/msgothic.ttc",  # Japanese support
    ]
    # For Japanese text, try fonts with CJK support
    jp_candidates = [
        "C:/Windows/Fonts/msgothic.ttc",
        "C:/Windows/Fonts/meiryo.ttc",
        "C:/Windows/Fonts/YuGothR.ttc",
        "C:/Windows/Fonts/msmincho.ttc",
    ]
    all_candidates = candidates + jp_candidates
    for fp in all_candidates:
        if os.path.exists(fp):
            try:
                f = ImageFont.truetype(fp, size)
                return f
            except Exception:
                continue
    return ImageFont.load_default()


def get_jp_font(size):
    """Get a font that supports Japanese characters."""
    jp_paths = [
        "C:/Windows/Fonts/msgothic.ttc",
        "C:/Windows/Fonts/meiryo.ttc",
        "C:/Windows/Fonts/YuGothR.ttc",
        "C:/Windows/Fonts/YuGothB.ttc",
        "C:/Windows/Fonts/msmincho.ttc",
    ]
    for fp in jp_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return get_font(size)


def add_scanlines(img, alpha=10):
    w, h = img.size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(0, h, 2):
        draw.line([(0, y), (w, y)], fill=(0, 0, 0, alpha), width=1)
    result = Image.alpha_composite(img.convert('RGBA'), overlay)
    img.paste(result.convert('RGB'))


def add_vignette(img, strength=0.6):
    """Dark edges vignette for dramatic focus."""
    w, h = img.size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    cx, cy = w // 2, h // 2
    max_dist = math.sqrt(cx * cx + cy * cy)
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            dx = (x - cx) / cx
            dy = (y - cy) / cy
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0.5:
                alpha = int((dist - 0.5) * 2 * 255 * strength)
                alpha = min(200, alpha)
                od.rectangle([x, y, x + 1, y + 1], fill=(0, 0, 0, alpha))
    result = Image.alpha_composite(img.convert('RGBA'), overlay)
    img.paste(result.convert('RGB'))


# ═══════════════════════════════════════════════════════════
# MAIN GENERATION
# ═══════════════════════════════════════════════════════════

def generate_background(path):
    W, H = 640, 480
    img = Image.new('RGB', (W, H), BLACK)
    draw = ImageDraw.Draw(img)
    
    vx = W // 2        # vanishing point x
    horizon_y = int(H * 0.48)  # horizon line
    
    print("  Starry sky...")
    draw_starry_sky(draw, W, H, horizon_y)
    
    print("  Floor grid...")
    draw_perspective_floor(draw, W, H, horizon_y, vx)
    
    print("  Corridor neon bars...")
    draw_corridor_neon_bars(img, vx, horizon_y, H)
    
    print("  Stone pillars with neon...")
    # Large foreground pillars (left & right)
    draw_pillar(img, 20, horizon_y, H, 50, 260, -1, NEON_CYAN, NEON_PINK)
    draw_pillar(img, W - 70, horizon_y, H, 50, 260, 1, NEON_CYAN, NEON_PINK)
    # Medium pillars
    draw_pillar(img, 100, horizon_y, H, 35, 200, -1, NEON_BLUE, NEON_HOT)
    draw_pillar(img, W - 135, horizon_y, H, 35, 200, 1, NEON_BLUE, NEON_HOT)
    # Small background pillars
    draw_pillar(img, 165, horizon_y, H, 22, 140, -1, NEON_BLUE, NEON_MAGENTA)
    draw_pillar(img, W - 187, horizon_y, H, 22, 140, 1, NEON_BLUE, NEON_MAGENTA)
    # Tiny far pillars
    draw_pillar(img, 215, horizon_y, H, 14, 90, -1, NEON_BLUE, NEON_MAGENTA)
    draw_pillar(img, W - 229, horizon_y, H, 14, 90, 1, NEON_BLUE, NEON_MAGENTA)
    
    print("  Deadmau5 head (stone carved)...")
    draw_mau5_head_stone(img, vx, int(H * 0.36), int(H * 0.14))
    
    print("  DDR text elements...")
    # Override jp font for katakana
    draw_ddr_text_full(img, W, H)
    
    print("  Post-processing...")
    add_vignette(img, strength=0.5)
    add_scanlines(img, alpha=8)
    
    img.save(path, 'PNG')
    print(f"  ✓ Background: {path} ({os.path.getsize(path):,} bytes)")


def draw_ddr_text_full(img, w, h):
    """All text rendering with proper Japanese font handling."""
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    
    # Speed lines
    vx, vy = w // 2, int(h * 0.36)
    for i in range(80):
        angle = random.uniform(0, 2 * math.pi)
        start_r = random.randint(70, 120)
        end_r = random.randint(140, 280)
        sx = vx + int(start_r * math.cos(angle))
        sy = vy + int(start_r * math.sin(angle) * 0.6)
        ex = vx + int(end_r * math.cos(angle))
        ey = vy + int(end_r * math.sin(angle) * 0.6)
        alpha = random.randint(10, 40)
        c = random.choice([NEON_CYAN, NEON_PINK, WHITE])
        od.line([(sx, sy), (ex, ey)], fill=(*c, alpha), width=1)
    
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))
    
    # Title
    title_font = get_font(64, bold=True)
    text_glow(img, "QUEZACOTL", w // 2, int(h * 0.09), title_font,
              fill=WHITE, outline=NEON_CYAN, glow=NEON_BLUE, glow_r=8)
    
    # Katakana subtitle
    jp_font = get_jp_font(18)
    text_glow(img, "ケツァルコアトル", w // 2, int(h * 0.17), jp_font,
              fill=GOLD_ACCENT, outline=None, glow=NEON_PINK, glow_r=3)
    
    # Artist
    artist_font = get_font(34, bold=True)
    text_glow(img, "deadmau5", w // 2, int(h * 0.87), artist_font,
              fill=WHITE, outline=NEON_PINK, glow=NEON_MAGENTA, glow_r=6)
    
    # Subtitle
    sub_font = get_font(14)
    text_glow(img, "— EFFORTLESS  FLOW  EDIT —", w // 2, int(h * 0.94), sub_font,
              fill=NEON_CYAN, outline=None, glow=NEON_BLUE, glow_r=3)
    
    # DDR badge
    tiny_font = get_font(11)
    text_glow(img, "DANCE ★ DANCE ★ CHALLENGE", w // 2, int(h * 0.03), tiny_font,
              fill=NEON_PINK, outline=None, glow=NEON_MAGENTA, glow_r=2)


def generate_banner(path):
    W, H = 256, 80
    img = Image.new('RGB', (W, H), BLACK)
    draw = ImageDraw.Draw(img)
    
    # Gradient background
    for y in range(H):
        t = y / H
        if t < 0.3:
            c = lerp(SKY_DARK, SKY_MID, t / 0.3)
        elif t < 0.6:
            c = lerp(SKY_MID, (25, 15, 50), (t - 0.3) / 0.3)
        else:
            c = lerp((25, 15, 50), FLOOR_DARK, (t - 0.6) / 0.4)
        draw.line([(0, y), (W, y)], fill=c)
    
    # Neon accent lines
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for (pos, color, alpha) in [(0.12, NEON_CYAN, 50), (0.5, NEON_BLUE, 30),
                                 (0.88, NEON_PINK, 50)]:
        y = int(H * pos)
        od.line([(0, y), (W, y)], fill=(*color, alpha), width=1)
        for gr in range(1, 4):
            od.line([(0, y - gr), (W, y - gr)], fill=(*color, alpha // (gr + 1)), width=1)
            od.line([(0, y + gr), (W, y + gr)], fill=(*color, alpha // (gr + 1)), width=1)
    img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))
    
    # Small mau5 head silhouette on left
    head_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_overlay)
    hx, hy, hr = 38, 42, 18
    ear_r = 8
    # Glow
    for gr in range(10, 0, -1):
        hd.ellipse([hx - hr - gr, hy - hr - gr, hx + hr + gr, hy + hr + gr],
                   fill=(*NEON_PINK, gr * 2))
    # Stone body
    hd.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(*STONE_MID, 200))
    # Ears
    for ex in [hx - 12, hx + 12]:
        ey = hy - 14
        hd.ellipse([ex - ear_r, ey - ear_r, ex + ear_r, ey + ear_r],
                   fill=(*STONE_MID, 200))
    # Glowing eyes
    for ex in [hx - 6, hx + 6]:
        ey = hy + 1
        for gr in range(6, 0, -1):
            hd.ellipse([ex - gr, ey - gr, ex + gr, ey + gr],
                       fill=(*EYE_GLOW, 10 + gr * 15))
        hd.ellipse([ex - 3, ey - 2, ex + 3, ey + 2], fill=(*EYE_GLOW, 255))
    
    img.paste(Image.alpha_composite(img.convert('RGBA'), head_overlay).convert('RGB'))
    
    # Text
    title_font = get_font(24, bold=True)
    text_glow(img, "QUEZACOTL", 152, 28, title_font,
              fill=WHITE, outline=NEON_CYAN, glow=NEON_BLUE, glow_r=3)
    
    artist_font = get_font(13, bold=True)
    text_glow(img, "deadmau5", 152, 50, artist_font,
              fill=WHITE, outline=NEON_PINK, glow=NEON_MAGENTA, glow_r=2)
    
    jp_font = get_jp_font(10)
    text_glow(img, "ケツァルコアトル", 152, 67, jp_font,
              fill=GOLD_ACCENT, outline=None, glow=NEON_PINK, glow_r=2)
    
    add_scanlines(img, alpha=8)
    img.save(path, 'PNG')
    print(f"  ✓ Banner: {path} ({os.path.getsize(path):,} bytes)")


if __name__ == '__main__':
    folder = r'c:\Program Files (x86)\StepMania\Songs\_Dance Dance Challenge\Quezacotl'
    
    print("Generating Quezacotl art v2...")
    print()
    
    bg_path = os.path.join(folder, 'Quezacotl-bg.png')
    print("Background (640x480):")
    generate_background(bg_path)
    print()
    
    banner_path = os.path.join(folder, 'Quezacotl-banner.png')
    print("Banner (256x80):")
    generate_banner(banner_path)
    print()
    
    print("✓ Done!")
