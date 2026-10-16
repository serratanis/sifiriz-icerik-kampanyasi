from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "source"
FINAL = ROOT / "assets" / "final"
FINAL.mkdir(parents=True, exist_ok=True)

FOREST = "#173F3A"
SAGE = "#A7C4A0"
APRICOT = "#E76F51"
CREAM = "#F5F0E6"
CHARCOAL = "#20332E"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def square_crop(path: Path, size: int = 1080) -> Image.Image:
    image = Image.open(path).convert("RGB")
    return ImageOps.fit(image, (size, size), method=Image.Resampling.LANCZOS)


def add_brand(draw: ImageDraw.ImageDraw, xy: tuple[int, int], color: str, dark_mark: bool = True) -> None:
    x, y = xy
    mark_color = FOREST if dark_mark else CREAM
    draw.rounded_rectangle((x, y, x + 56, y + 56), radius=18, fill=mark_color)
    draw.arc((x + 13, y + 12, x + 43, y + 43), 200, 520, fill=APRICOT if dark_mark else SAGE, width=4)
    draw.line((x + 20, y + 39, x + 38, y + 21), fill=APRICOT if dark_mark else SAGE, width=4)
    draw.text((x + 70, y + 9), "Sıfırİz", font=font(32, True), fill=color)


def draw_multiline(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, size: int, fill: str, spacing: int = 8) -> None:
    draw.multiline_text(xy, text, font=font(size, True), fill=fill, spacing=spacing)


def build_visual_1() -> None:
    image = square_crop(SOURCE / "01-ikinci-tur-kaynak.png")
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rounded_rectangle((52, 55, 590, 477), radius=34, fill=(245, 240, 230, 232))
    add_brand(draw, (90, 91), FOREST)
    draw.text((92, 187), "BUGÜNÜN KÜÇÜK ADIMI", font=font(19, True), fill=APRICOT)
    draw_multiline(draw, (88, 232), "BİR NESNEYE\nİKİNCİ BİR TUR.", 57, FOREST, 2)
    draw.text((91, 393), "Biriktirmek değil, ömrünü uzatmak.", font=font(23), fill=CHARCOAL)
    draw.rounded_rectangle((72, 947, 378, 1018), radius=35, fill=(23, 63, 58, 238))
    draw.text((103, 968), "#BugünBirAdım", font=font(24, True), fill=CREAM)
    image.save(FINAL / "01-ikinci-tur.png", quality=96)


def build_visual_2() -> None:
    image = square_crop(SOURCE / "02-once-elindekine-bak-kaynak.png")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    o = ImageDraw.Draw(overlay, "RGBA")
    o.rectangle((0, 0, 1080, 380), fill=(23, 63, 58, 229))
    overlay = overlay.filter(ImageFilter.GaussianBlur(0.2))
    image = Image.alpha_composite(image.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(image, "RGBA")
    add_brand(draw, (72, 54), CREAM, dark_mark=False)
    draw.text((74, 155), "ALIŞVERİŞTEN ÖNCE 60 SANİYE", font=font(19, True), fill=SAGE)
    draw_multiline(draw, (69, 198), "ÖNCE ELİNDEKİNE\nBAK.", 59, CREAM, 0)
    draw.rounded_rectangle((650, 958, 1013, 1024), radius=33, fill=(245, 240, 230, 235))
    draw.text((687, 978), "Öne al · Planla · Tüket", font=font(21, True), fill=FOREST)
    image.convert("RGB").save(FINAL / "02-once-elindekine-bak.png", quality=96)


def build_visual_3() -> None:
    image = square_crop(SOURCE / "03-mahallede-dongu-kaynak.png")
    draw = ImageDraw.Draw(image, "RGBA")
    draw.ellipse((292, 292, 788, 788), fill=(245, 240, 230, 240), outline=(167, 196, 160, 255), width=6)
    draw.text((438, 390), "ONAR", font=font(18, True), fill=APRICOT)
    bbox = draw.multiline_textbbox((0, 0), "MAHALLEDE\nDÖNGÜ VAR.", font=font(47, True), spacing=3, align="center")
    text_w = bbox[2] - bbox[0]
    draw.multiline_text(((1080 - text_w) / 2, 443), "MAHALLEDE\nDÖNGÜ VAR.", font=font(47, True), fill=FOREST, spacing=3, align="center")
    draw.text((405, 585), "Paylaş · Doldur · Uzat", font=font(20), fill=CHARCOAL)
    add_brand(draw, (64, 956), CREAM, dark_mark=True)
    image.save(FINAL / "03-mahallede-dongu.png", quality=96)


def build_brand_card() -> None:
    canvas = Image.new("RGB", (1600, 900), CREAM)
    draw = ImageDraw.Draw(canvas)
    add_brand(draw, (90, 74), FOREST)
    draw.text((90, 176), "Atıksız şehir yaşamı için\nküçük ve uygulanabilir adımlar.", font=font(49, True), fill=FOREST, spacing=8)
    draw.text((90, 312), "MARKA KİMLİĞİ", font=font(18, True), fill=APRICOT)
    colors = [(FOREST, "Orman"), (SAGE, "Adaçayı"), (APRICOT, "Kayısı"), (CREAM, "Kâğıt"), (CHARCOAL, "Kömür")]
    for i, (color, name) in enumerate(colors):
        x = 90 + i * 167
        draw.rounded_rectangle((x, 354, x + 140, 467), radius=18, fill=color, outline="#D4D7CE", width=1)
        text_fill = CREAM if color in (FOREST, CHARCOAL) else FOREST
        draw.text((x + 13, 421), name, font=font(17, True), fill=text_fill)
    draw.text((90, 535), "SES", font=font(18, True), fill=APRICOT)
    draw.text((90, 575), "Pratik · sakin · yargılamayan · şeffaf", font=font(29, True), fill=FOREST)
    draw.text((90, 636), "KELİMELER", font=font(18, True), fill=APRICOT)
    draw.text((90, 676), "ikinci tur   küçük adım   yeniden kullan   paylaş   onar", font=font(25), fill=CHARCOAL)
    draw.rounded_rectangle((1050, 72, 1510, 828), radius=38, fill=FOREST)
    draw.text((1102, 124), "BUGÜN", font=font(22, True), fill=SAGE)
    draw_multiline(draw, (1097, 172), "BİR\nADIMLA\nBAŞLA.", 70, CREAM, 8)
    draw.arc((1125, 520, 1435, 830), 205, 510, fill=APRICOT, width=13)
    draw.line((1200, 723, 1359, 564), fill=APRICOT, width=13)
    canvas.save(FINAL / "00-marka-kimligi-karti.png", quality=96)


def build_contact_sheet() -> None:
    files = [FINAL / "01-ikinci-tur.png", FINAL / "02-once-elindekine-bak.png", FINAL / "03-mahallede-dongu.png"]
    canvas = Image.new("RGB", (2220, 780), "#E9E9E2")
    for index, path in enumerate(files):
        image = Image.open(path).convert("RGB").resize((700, 700), Image.Resampling.LANCZOS)
        canvas.paste(image, (30 + index * 730, 30))
    canvas.save(FINAL / "kampanya-gorselleri-onizleme.png", quality=94)


def build_video_frames() -> None:
    frame_dir = ROOT / "tmp" / "media" / "frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    specs = [
        ("01-ikinci-tur.png", CREAM, FOREST, "ATIKSIZ YAŞAM,\nKUSURSUZLUK DEĞİL."),
        ("02-once-elindekine-bak.png", FOREST, CREAM, "ÖNCE ELİNDEKİNE BAK."),
        ("03-mahallede-dongu.png", CREAM, FOREST, "KÜÇÜK SEÇİMLER\nDÖNGÜ YARATIR."),
    ]
    for index, (filename, background, text_color, title) in enumerate(specs, start=1):
        frame = Image.new("RGB", (1080, 1920), background)
        draw = ImageDraw.Draw(frame)
        draw.text((74, 92), "SIFIRİZ · BUGÜN BİR ADIM", font=font(21, True), fill=APRICOT if background == CREAM else SAGE)
        draw.multiline_text((70, 154), title, font=font(52, True), fill=text_color, spacing=5)
        visual = Image.open(FINAL / filename).convert("RGB").resize((980, 980), Image.Resampling.LANCZOS)
        frame.paste(visual, (50, 420))
        draw.text((73, 1492), "Yeniden kullan · Onar · Paylaş", font=font(31, True), fill=text_color)
        draw.rounded_rectangle((70, 1583, 1010, 1774), radius=32, fill=SAGE if background == CREAM else "#24574F")
        draw.text((113, 1634), "Küçük bir seçim,\ntekrarlanabilir bir alışkanlık.", font=font(37, True), fill=FOREST if background == CREAM else CREAM, spacing=7)
        frame.save(frame_dir / f"frame-{index}.png", quality=96)

    end = Image.new("RGB", (1080, 1920), FOREST)
    draw = ImageDraw.Draw(end)
    draw.ellipse((232, 380, 848, 996), outline=SAGE, width=8)
    draw.arc((318, 463, 765, 910), 200, 515, fill=APRICOT, width=18)
    draw.line((414, 785, 665, 534), fill=APRICOT, width=18)
    bbox = draw.textbbox((0, 0), "Sıfırİz", font=font(96, True))
    draw.text(((1080 - (bbox[2] - bbox[0])) / 2, 1070), "Sıfırİz", font=font(96, True), fill=CREAM)
    bbox2 = draw.textbbox((0, 0), "BUGÜN BİR ADIMLA BAŞLA.", font=font(31, True))
    draw.text(((1080 - (bbox2[2] - bbox2[0])) / 2, 1210), "BUGÜN BİR ADIMLA BAŞLA.", font=font(31, True), fill=SAGE)
    end.save(frame_dir / "frame-4.png", quality=96)


if __name__ == "__main__":
    build_visual_1()
    build_visual_2()
    build_visual_3()
    build_brand_card()
    build_contact_sheet()
    build_video_frames()
    for path in sorted(FINAL.glob("*.png")):
        print(path)
