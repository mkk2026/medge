"""Generate MedEdge cover image for Kaggle submission."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1600, 900
BG = (15, 23, 42)        # --bg: #0f172a
SURFACE = (30, 41, 59)   # --surface: #1e293b
ACCENT = (56, 189, 248)  # --accent: #38bdf8
RED = (239, 68, 68)
YELLOW = (245, 158, 11)
GREEN = (34, 197, 94)
WHITE = (241, 245, 249)
MUTED = (148, 163, 184)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# Background accent strip
draw.rectangle([0, 0, W, 6], fill=ACCENT)

# Try to load a good font, fall back to default
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    badge_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
except:
    title_font = ImageFont.load_default()
    sub_font = title_font
    body_font = title_font
    badge_font = title_font
    small_font = title_font

# Logo area - use text cross instead of emoji
draw.text((80, 55), "+", fill=ACCENT, font=title_font)

# Title
draw.text((80, 150), "MedEdge", fill=WHITE, font=title_font)

# Subtitle
draw.text((80, 250), "AI-Powered Triage Assistant for Community Health Workers", fill=ACCENT, font=sub_font)

# Description
draw.text((80, 310), "Gemma 4 multimodal analysis · Native function calling · Agentic reasoning", fill=MUTED, font=body_font)

# Triage level cards
card_y = 420
card_w = 440
card_h = 120
gap = 30

# RED card
rx = 80
draw.rounded_rectangle([rx, card_y, rx + card_w, card_y + card_h], radius=12, fill=(69, 10, 10), outline=RED, width=2)
draw.text((rx + 20, card_y + 16), ">>> RED — REFER URGENTLY", fill=RED, font=badge_font)
draw.text((rx + 20, card_y + 50), "Emergency transport within 1 hour", fill=MUTED, font=small_font)
draw.text((rx + 20, card_y + 76), "Stabilize airway, breathing, circulation", fill=MUTED, font=small_font)

# YELLOW card
yx = 80 + card_w + gap
draw.rounded_rectangle([yx, card_y, yx + card_w, card_y + card_h], radius=12, fill=(69, 26, 3), outline=YELLOW, width=2)
draw.text((yx + 20, card_y + 16), "(!!) YELLOW — MONITOR CLOSELY", fill=YELLOW, font=badge_font)
draw.text((yx + 20, card_y + 50), "Refer within 24 hours if needed", fill=MUTED, font=small_font)
draw.text((yx + 20, card_y + 76), "Monitor vitals every 30 minutes", fill=MUTED, font=small_font)

# GREEN card
gx = 80 + 2 * (card_w + gap)
draw.rounded_rectangle([gx, card_y, gx + card_w, card_y + card_h], radius=12, fill=(20, 83, 45), outline=GREEN, width=2)
draw.text((gx + 20, card_y + 16), "[OK] GREEN — MANAGE LOCALLY", fill=GREEN, font=badge_font)
draw.text((gx + 20, card_y + 50), "Appropriate first aid on-site", fill=MUTED, font=small_font)
draw.text((gx + 20, card_y + 76), "Follow up in 48-72 hours", fill=MUTED, font=small_font)

# Tool pipeline
pipe_y = 600
draw.text((80, pipe_y), "Agentic Pipeline", fill=WHITE, font=badge_font)

tools = [
    ("1. Image Analysis", "Multimodal"),
    ("2. search_medical_protocols()", "ChromaDB / WHO+MSF"),
    ("3. assess_vital_signs()", "Clinical Thresholds"),
    ("4. get_referral_guidance()", "Transfer Protocol"),
    ("5. Triage Report", "9 Languages"),
]

tx = 80
for i, (name, desc) in enumerate(tools):
    bw = 270
    draw.rounded_rectangle([tx, pipe_y + 35, tx + bw, pipe_y + 95], radius=8, fill=SURFACE, outline=(51, 65, 85), width=1)
    draw.text((tx + 12, pipe_y + 44), name, fill=ACCENT, font=small_font)
    draw.text((tx + 12, pipe_y + 68), desc, fill=MUTED, font=small_font)
    if i < len(tools) - 1:
        arrow_x = tx + bw + 5
        draw.text((arrow_x, pipe_y + 52), "→", fill=MUTED, font=body_font)
    tx += bw + 28

# Bottom bar
draw.rectangle([0, H - 55, W, H], fill=SURFACE)
draw.text((80, H - 40), "Gemma 4 Good Hackathon · Health & Sciences Track · Built in Freetown, Sierra Leone", fill=MUTED, font=small_font)
draw.text((W - 300, H - 40), "Core Brim Tech · 2026", fill=MUTED, font=small_font)

# Accent line above bottom bar
draw.rectangle([0, H - 57, W, H - 55], fill=ACCENT)

out_path = os.path.join(os.path.dirname(__file__), "cover.png")
img.save(out_path, "PNG", quality=95)
print(f"Saved cover image to {out_path}")
print(f"Size: {W}x{H}")
