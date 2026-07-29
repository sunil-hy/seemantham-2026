"""scripts/generate_photo_circle.py

Generates an 800x800 circular PNG with transparent background from
assets/photo.jpg and writes assets/photo-circle.png.

Usage:
  pip install pillow
  python scripts/generate_photo_circle.py [input_path] [output_path] [size]

Defaults:
  input: assets/photo.jpg
  output: assets/photo-circle.png
  size: 800

Notes:
 - This script centers the crop on the image center. If the faces are
   off-center you can pass a 4-tuple crop box or adjust the code.
 - Feather (soft) edges are created with a Gaussian blur on the alpha mask.
 - Color grading: subtle warm tint and light contrast/color boost applied.
"""

from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import sys
import os

def generate_circle(input_path='assets/photo.jpg', output_path='assets/photo-circle.png', size=800, feather=18):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    img = Image.open(input_path).convert('RGBA')

    # Resize to fill the square box, preserving aspect ratio
    w, h = img.size
    scale = max(size / w, size / h)
    new_w, new_h = int(w * scale), int(h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # Center crop to square
    left = (new_w - size) // 2
    top = (new_h - size) // 2
    img = img.crop((left, top, left + size, top + size))

    # Subtle color grade: warm tint + contrast + color boost
    # Warm overlay
    warm = Image.new('RGBA', (size, size), (255, 195, 140, 0))
    img = Image.blend(img, warm, alpha=0.06)  # very subtle warm tone

    # Enhance color and contrast slightly
    img = ImageEnhance.Color(img).enhance(1.08)
    img = ImageEnhance.Contrast(img).enhance(1.06)

    # Create circular mask with feathered edge
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    # Draw a solid ellipse slightly inset to keep a small transparent margin
    inset = int(size * 0.0)
    draw.ellipse((inset, inset, size - inset, size - inset), fill=255)

    # Feather the mask by Gaussian blur
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather))

    # Apply mask as alpha channel
    img.putalpha(mask)

    # Save as PNG with transparency
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, format='PNG')
    print(f"Saved circular image to: {output_path}")


if __name__ == '__main__':
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'assets/photo.jpg'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'assets/photo-circle.png'
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 800
    try:
        generate_circle(input_path, output_path, size)
    except Exception as e:
        print('Error:', e)
        sys.exit(1)
