from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image as PILImage
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


PROJECT = Path(__file__).resolve().parent.parent
OUTPUT = PROJECT / "deliverables" / "SifirIz-Ornek-Icerik-Portfolyosu.pdf"
W, H = A4

FOREST = HexColor("#173F3A")
SAGE = HexColor("#A7C4A0")
APRICOT = HexColor("#E76F51")
CREAM = HexColor("#F5F0E6")
CHARCOAL = HexColor("#20332E")
MIST = HexColor("#EAF0EA")
GRAY = HexColor("#66736F")
LINE = HexColor("#D4DDD8")
WHITE = white

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
pdfmetrics.registerFont(TTFont("Sifiriz", str(FONT_DIR / "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Sifiriz-Bold", str(FONT_DIR / "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("Sifiriz-Italic", str(FONT_DIR / "Arial Italic.ttf")))


def wrap_lines(text: str, font: str, size: float, width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if pdfmetrics.stringWidth(candidate, font, size) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_text(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    *,
    font: str = "Sifiriz",
    size: float = 10,
    color=CHARCOAL,
    leading: float | None = None,
    max_lines: int | None = None,
) -> float:
    leading = leading or size * 1.35
    lines = wrap_lines(text, font, size, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_image_cover(c: canvas.Canvas, image_path: Path, x: float, y: float, w: float, h: float) -> None:
    image = PILImage.open(image_path).convert("RGB")
    src_ratio = image.width / image.height
    dst_ratio = w / h
    if src_ratio > dst_ratio:
        crop_width = int(image.height * dst_ratio)
        left = (image.width - crop_width) // 2
        image = image.crop((left, 0, left + crop_width, image.height))
    else:
        crop_height = int(image.width / dst_ratio)
        top = (image.height - crop_height) // 2
        image = image.crop((0, top, image.width, top + crop_height))
    c.drawImage(ImageReader(image), x, y, width=w, height=h, mask="auto")


def draw_image_contain(c: canvas.Canvas, image_path: Path, x: float, y: float, w: float, h: float, fill=WHITE) -> None:
    image = PILImage.open(image_path).convert("RGB")
    c.setFillColor(fill)
    c.rect(x, y, w, h, fill=1, stroke=0)
    scale = min(w / image.width, h / image.height)
    draw_w = image.width * scale
    draw_h = image.height * scale
    draw_x = x + (w - draw_w) / 2
    draw_y = y + (h - draw_h) / 2
    c.drawImage(ImageReader(image), draw_x, draw_y, width=draw_w, height=draw_h, mask="auto")


def rounded_panel(c: canvas.Canvas, x: float, y: float, w: float, h: float, fill=CREAM, stroke=LINE, radius: float = 12) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def pill(c: canvas.Canvas, text: str, x: float, y: float, fill=APRICOT, color=WHITE) -> float:
    c.setFont("Sifiriz-Bold", 8)
    width = pdfmetrics.stringWidth(text, "Sifiriz-Bold", 8) + 18
    c.setFillColor(fill)
    c.roundRect(x, y - 3, width, 18, 9, fill=1, stroke=0)
    c.setFillColor(color)
    c.drawString(x + 9, y + 2, text)
    return width


def page_header(c: canvas.Canvas, number: int, kicker: str, title: str, subtitle: str = "") -> float:
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(FOREST)
    c.rect(0, H - 18, W, 18, fill=1, stroke=0)
    c.setFont("Sifiriz-Bold", 8)
    c.setFillColor(APRICOT)
    c.drawString(48, H - 52, kicker.upper())
    y = draw_text(c, title, 48, H - 88, W - 96, font="Sifiriz-Bold", size=22, color=FOREST, leading=25, max_lines=2)
    y -= 2
    if subtitle:
        y = draw_text(c, subtitle, 48, y, W - 96, font="Sifiriz", size=10.5, color=GRAY, leading=14)
    c.setFillColor(LINE)
    c.rect(48, y - 8, W - 96, 1, fill=1, stroke=0)
    c.setFont("Sifiriz", 8)
    c.setFillColor(GRAY)
    c.drawRightString(W - 48, 26, f"Sıfırİz  •  İçerik Üretimi Final Projesi  •  {number}/8")
    return y - 30


def check(c: canvas.Canvas, text: str, x: float, y: float, width: float) -> float:
    c.setFillColor(SAGE)
    c.circle(x + 6, y + 3, 6, fill=1, stroke=0)
    c.setFont("Sifiriz-Bold", 8)
    c.setFillColor(FOREST)
    c.drawCentredString(x + 6, y, "✓")
    return draw_text(c, text, x + 20, y + 6, width - 20, size=9.5, color=CHARCOAL, leading=13)


def finish_page(c: canvas.Canvas) -> None:
    c.showPage()


def cover(c: canvas.Canvas) -> None:
    c.setFillColor(FOREST)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(APRICOT)
    c.circle(W - 42, H - 36, 82, fill=1, stroke=0)
    c.setFillColor(SAGE)
    c.circle(18, 48, 100, fill=1, stroke=0)
    c.setFont("Sifiriz-Bold", 11)
    c.setFillColor(SAGE)
    c.drawString(48, H - 74, "YAPAY ZEKÂ İLE İÇERİK ÜRETİMİ  •  FINAL PROJESİ")
    c.setFont("Sifiriz-Bold", 48)
    c.setFillColor(WHITE)
    c.drawString(48, H - 144, "Sıfırİz")
    c.setFont("Sifiriz-Bold", 22)
    c.setFillColor(CREAM)
    c.drawString(48, H - 180, "Atıksız Şehir Yaşamı")
    c.setFont("Sifiriz", 13)
    c.setFillColor(WHITE)
    c.drawString(48, H - 208, "7 günlük çok formatlı içerik kampanyası")

    brand = PROJECT / "assets" / "final" / "00-marka-kimligi-karti.png"
    draw_image_cover(c, brand, 48, 292, W - 96, 282)

    c.setFillColor(WHITE)
    c.setFont("Sifiriz-Bold", 15)
    c.drawString(48, 252, "Bugün bir adımla başla.")
    c.setFont("Sifiriz", 10)
    c.setFillColor(CREAM)
    c.drawString(48, 229, "Strateji • blog • sosyal medya • görsel üretim • video • TTS • şeffaf AI süreci")
    c.setFillColor(SAGE)
    c.rect(48, 186, 104, 4, fill=1, stroke=0)
    c.setFont("Sifiriz", 9)
    c.setFillColor(WHITE)
    c.drawString(48, 162, "TNC Group proje yönergesine göre hazırlanmıştır  •  2026")
    c.showPage()


def strategy_page(c: canvas.Canvas) -> None:
    y = page_header(
        c,
        2,
        "01 / Marka stratejisi",
        "Küçük adımların büyük vaatlarden daha inandırıcı olduğu bir içerik markası",
        "Sıfırİz, şehirde yaşayan kişilere suçluluk yüklemeden aynı gün uygulanabilecek atık azaltma ve yeniden kullanım davranışları önerir.",
    )
    metrics = [("7", "günlük plan"), ("1", "SEO blog"), ("3", "sosyal gönderi"), ("3", "özgün görsel"), ("18 sn", "dikey video"), ("1", "TTS kayıt")]
    box_w = (W - 96 - 25) / 3
    for idx, (value, label) in enumerate(metrics):
        col = idx % 3
        row = idx // 3
        x = 48 + col * (box_w + 12.5)
        by = y - 78 - row * 82
        rounded_panel(c, x, by, box_w, 64, fill=WHITE)
        c.setFont("Sifiriz-Bold", 20)
        c.setFillColor(FOREST)
        c.drawString(x + 14, by + 32, value)
        c.setFont("Sifiriz", 9)
        c.setFillColor(GRAY)
        c.drawString(x + 14, by + 16, label)

    y2 = y - 194
    rounded_panel(c, 48, y2 - 160, 236, 146, fill=MIST)
    c.setFont("Sifiriz-Bold", 13)
    c.setFillColor(FOREST)
    c.drawString(64, y2 - 38, "Kime sesleniyor?")
    draw_text(c, "Derya, 28 — kentte yaşayan, yoğun çalışan, çevreye duyarlı; ama uzun raporlar ve kusursuz yaşam örnekleri yerine iki dakikada anlayıp aynı gün deneyebileceği öneriler arıyor.", 64, y2 - 61, 204, size=9.5, leading=14)

    rounded_panel(c, 300, y2 - 160, W - 348, 146, fill=WHITE)
    c.setFont("Sifiriz-Bold", 13)
    c.setFillColor(FOREST)
    c.drawString(316, y2 - 38, "Marka sesi")
    voice_y = y2 - 62
    for text in [
        "Pratik: tek ve açık eylem",
        "Sakin: suçluluk ve korku yok",
        "Kaynaklı: kesin iddia yok",
        "Yerel: ev, mahalle, tamir, paylaşım",
    ]:
        voice_y = check(c, text, 316, voice_y, W - 380) - 5

    pillar_y = y2 - 204
    c.setFont("Sifiriz-Bold", 14)
    c.setFillColor(FOREST)
    c.drawString(48, pillar_y, "İçerik sütunları")
    pillars = [
        ("Evde 10 Dakika", "Buzdolabı, yeniden doldurma, ev içi mikro görevler"),
        ("Mahallede Döngü", "Tamir, ikinci el, paylaşım ve yerel noktalar"),
        ("Etikete Değil Alışkanlığa", "Yeşil iddiaları sade dille sorgulama"),
        ("Paylaş ve Çoğalt", "Tamamlanan görevler ve topluluk çağrıları"),
    ]
    py = pillar_y - 28
    for idx, (title, desc) in enumerate(pillars):
        x = 48 if idx % 2 == 0 else 306
        if idx == 2:
            py -= 70
        by = py - (idx // 2) * 0
        rounded_panel(c, x, by - 50, 241, 52, fill=WHITE)
        c.setFont("Sifiriz-Bold", 10)
        c.setFillColor(FOREST)
        c.drawString(x + 12, by - 18, title)
        draw_text(c, desc, x + 12, by - 34, 216, size=8, color=GRAY, leading=10, max_lines=2)
    finish_page(c)


def calendar_page(c: canvas.Canvas) -> None:
    y = page_header(
        c,
        3,
        "02 / İçerik planı",
        "Her gün farklı bir görev, her format aynı marka sözü",
        "Takvim; kanal, format, amaç, eylem çağrısı, kanıt dosyası ve insan kontrolü durumunu tek görünümde izler.",
    )
    preview = PROJECT / "tmp" / "xlsx-render" / "7-gunluk-takvim.png"
    draw_image_cover(c, preview, 48, y - 250, W - 96, 210)
    c.setFont("Sifiriz-Italic", 8.5)
    c.setFillColor(GRAY)
    c.drawString(48, y - 266, "Excel teslimindeki canlı takvim: filtrelenebilir durum alanları ve otomatik özet formülleri içerir.")

    days = [
        ("Pzt", "İkinci tur", "Carousel"),
        ("Sal", "7 gerçekçi adım", "Blog"),
        ("Çar", "Elindekine bak", "Görsel"),
        ("Per", "Mahallede döngü", "LinkedIn"),
        ("Cum", "Kullan–tamir et–paylaş", "Video"),
        ("Cmt", "Mükemmellik değil tekrar", "X"),
        ("Paz", "Haftanın mikro görevi", "TTS"),
    ]
    start_y = y - 318
    for idx, (day, topic, fmt) in enumerate(days):
        row = idx // 2
        col = idx % 2
        x = 48 + col * 258
        by = start_y - row * 74
        rounded_panel(c, x, by - 50, 241, 56, fill=WHITE)
        pill(c, day, x + 10, by - 17, fill=APRICOT)
        c.setFont("Sifiriz-Bold", 9.5)
        c.setFillColor(FOREST)
        c.drawString(x + 58, by - 13, topic)
        c.setFont("Sifiriz", 8)
        c.setFillColor(GRAY)
        c.drawString(x + 58, by - 31, fmt)
    finish_page(c)


def blog_page(c: canvas.Canvas) -> None:
    y = page_header(
        c,
        4,
        "03 / Uzun biçim",
        "Blog: Atıksız şehir yaşamı için 7 gerçekçi adım",
        "SEO uyumlu, kaynaklı ve okuru tek bir küçük davranış seçmeye çağıran rehber içerik.",
    )
    rounded_panel(c, 48, y - 98, W - 96, 86, fill=FOREST, stroke=FOREST)
    c.setFont("Sifiriz-Bold", 10)
    c.setFillColor(SAGE)
    c.drawString(64, y - 36, "ARAMA NİYETİ")
    c.setFont("Sifiriz-Bold", 16)
    c.setFillColor(WHITE)
    c.drawString(64, y - 61, "“Atıksız yaşamı nereden ve nasıl başlatabilirim?”")
    c.setFont("Sifiriz", 8.5)
    c.setFillColor(CREAM)
    c.drawString(64, y - 80, "Odak anahtar kelime: atıksız yaşam  •  Ton: cesaretlendirici  •  CTA: bir adım seç")

    steps = [
        "Çöp kutusuna değil, alışveriş kararına bak",
        "Buzdolabını görünür hâle getir",
        "Tek kullanımlık ürünü tek seferde değiştirme",
        "Tamir ve bakım için bekleme listesi oluştur",
        "Mahallendeki döngü noktalarını haritala",
        "Bir eşyayı ikinci tura çıkar",
        "İlerlemeni çöple değil, tekrarla ölç",
    ]
    sy = y - 135
    c.setFont("Sifiriz-Bold", 13)
    c.setFillColor(FOREST)
    c.drawString(48, sy, "Yedi adımlık editoryal omurga")
    sy -= 28
    for idx, step in enumerate(steps, start=1):
        c.setFillColor(APRICOT)
        c.circle(58, sy + 3, 10, fill=1, stroke=0)
        c.setFont("Sifiriz-Bold", 9)
        c.setFillColor(WHITE)
        c.drawCentredString(58, sy, str(idx))
        c.setFont("Sifiriz", 10)
        c.setFillColor(CHARCOAL)
        c.drawString(78, sy, step)
        sy -= 34

    rounded_panel(c, 48, 106, W - 96, 122, fill=MIST)
    c.setFont("Sifiriz-Bold", 12)
    c.setFillColor(FOREST)
    c.drawString(64, 200, "Editoryal karar")
    excerpt = (
        "Atıksız yaşam, bir gecede değişen kusursuz bir hayat değil; aynı küçük seçimi yeterince kolay olduğu için tekrar edebilmektir. "
        "Bu nedenle içerik büyük vaat yerine uygulanabilir davranışı, soyut çevre kaygısı yerine bugünün kararını öne çıkarır."
    )
    draw_text(c, excerpt, 64, 178, W - 128, size=10, leading=15)
    c.setFont("Sifiriz-Italic", 8.5)
    c.setFillColor(GRAY)
    c.drawString(64, 124, "Tam metin: content/blog-yazisi.md  •  Kaynaklar içerik sonunda açıkça listelenmiştir.")
    finish_page(c)


def social_page(c: canvas.Canvas) -> None:
    y = page_header(
        c,
        5,
        "04 / Sosyal medya",
        "Aynı fikir, üç platforma özgü anlatım",
        "Metinler aynı marka sesini korurken biçim, uzunluk ve eylem çağrısı platform davranışına göre değişir.",
    )
    posts = [
        ("INSTAGRAM", "Kaydırmalı gönderi", "Eşyaya ikinci tur", "Kullanmadığın bir eşya çöp olmak zorunda değil. Bugün tek bir parçayı seç: kullan, tamir et ya da paylaş. #Sıfırİz"),
        ("LINKEDIN", "Düşünce liderliği", "Mahallede döngü", "Sürdürülebilirlik yalnızca büyük kurum hedefleri değildir. Tamirci, paylaşım dolabı ve yerel üretici; döngüsel ekonominin mahalledeki görünür yüzüdür."),
        ("X", "Üçlü kısa seri", "Mükemmellik değil tekrar", "Atıksız yaşam için 30 yeni ürün gerekmiyor. Önce elindekine bak. Sonra bir davranışı kolaylaştır. En iyi adım, yarın da tekrarlayabildiğindir."),
    ]
    card_h = 148
    for idx, (platform, fmt, title, body) in enumerate(posts):
        by = y - 145 - idx * 165
        rounded_panel(c, 48, by, W - 96, card_h, fill=WHITE)
        pill(c, platform, 64, by + card_h - 31, fill=FOREST)
        c.setFont("Sifiriz", 8)
        c.setFillColor(GRAY)
        c.drawString(160, by + card_h - 27, fmt)
        c.setFont("Sifiriz-Bold", 15)
        c.setFillColor(FOREST)
        c.drawString(64, by + card_h - 61, title)
        draw_text(c, body, 64, by + card_h - 84, W - 128, size=9.5, leading=14, max_lines=4)
        c.setFont("Sifiriz-Bold", 8.5)
        c.setFillColor(APRICOT)
        c.drawString(64, by + 18, "CTA: Bugün bir adım seç, kaydet ve paylaş.")
    finish_page(c)


def visuals_page(c: canvas.Canvas) -> None:
    y = page_header(
        c,
        6,
        "05 / Görsel üretim",
        "Üç parçalık tutarlı kampanya serisi",
        "Doğal ışık, geri dönüştürülmüş kâğıt dokusu ve sıcak gündelik nesneler; yaprak klişesine düşmeden ortak bir dünya kurar.",
    )
    images = [
        (PROJECT / "assets" / "final" / "01-ikinci-tur.png", "01", "Eşyaya ikinci tur", "Tamir ve paylaşım"),
        (PROJECT / "assets" / "final" / "02-once-elindekine-bak.png", "02", "Önce elindekine bak", "Gıda değerlendirme"),
        (PROJECT / "assets" / "final" / "03-mahallede-dongu.png", "03", "Mahallede döngü", "Yerel dayanışma"),
    ]
    gap = 14
    iw = (W - 96 - gap * 2) / 3
    ih = 250
    for idx, (path, number, title, note) in enumerate(images):
        x = 48 + idx * (iw + gap)
        draw_image_contain(c, path, x, y - ih, iw, ih, fill=WHITE)
        c.setFillColor(FOREST)
        c.rect(x, y - ih - 78, iw, 70, fill=1, stroke=0)
        c.setFont("Sifiriz-Bold", 8)
        c.setFillColor(SAGE)
        c.drawString(x + 10, y - ih - 30, f"KAMPANYA {number}")
        draw_text(c, title, x + 10, y - ih - 47, iw - 20, font="Sifiriz-Bold", size=10, color=WHITE, leading=12, max_lines=2)
        c.setFont("Sifiriz", 7.5)
        c.setFillColor(CREAM)
        c.drawString(x + 10, y - ih - 67, note)

    rounded_panel(c, 48, 75, W - 96, 108, fill=MIST)
    c.setFont("Sifiriz-Bold", 11)
    c.setFillColor(FOREST)
    c.drawString(64, 157, "Üretim notu")
    note = (
        "Kaynak sahneler yapay zekâ ile üretildi; kompozisyon seçimi, kırpma, tipografi, marka renkleri ve son düzen insan eliyle tamamlandı. "
        "Gerçek kişi, kurum logosu veya telifli karakter taklit edilmedi."
    )
    draw_text(c, note, 64, 136, W - 128, size=9.5, leading=14)
    finish_page(c)


def video_audio_page(c: canvas.Canvas) -> None:
    y = page_header(
        c,
        7,
        "06 / Video ve ses",
        "18 saniyede tek bir davranış zinciri",
        "Dikey format, okunabilir altyazı ve Türkçe TTS; sesi kapalı izleyen kullanıcıyı da kapsar.",
    )
    frames = [PROJECT / "tmp" / "media" / f"video-check-0{i}.png" for i in range(1, 5)]
    labels = ["0–4 sn", "4–9 sn", "9–14 sn", "14–18 sn"]
    gap = 12
    fw = (W - 96 - 3 * gap) / 4
    fh = 250
    for idx, (frame, label) in enumerate(zip(frames, labels)):
        x = 48 + idx * (fw + gap)
        draw_image_contain(c, frame, x, y - fh, fw, fh, fill=CREAM)
        c.setFillColor(FOREST)
        c.rect(x, y - fh, fw, 25, fill=1, stroke=0)
        c.setFont("Sifiriz-Bold", 8)
        c.setFillColor(WHITE)
        c.drawCentredString(x + fw / 2, y - fh + 8, label)

    rounded_panel(c, 48, y - 386, W - 96, 104, fill=WHITE)
    c.setFont("Sifiriz-Bold", 12)
    c.setFillColor(FOREST)
    c.drawString(64, y - 310, "Video anlatı akışı")
    script = "Bir eşya artık işine yaramıyor mu? Önce kullanmayı dene. Olmuyorsa tamir et. Hâlâ olmuyorsa paylaş. Sıfırİz — bugün bir adımla başla."
    draw_text(c, script, 64, y - 334, W - 128, size=9.5, leading=14)
    c.setFont("Sifiriz", 8.5)
    c.setFillColor(GRAY)
    c.drawString(64, y - 372, "1080 × 1920  •  H.264 + AAC  •  18.000 sn  •  ayrı SRT altyazı dosyası")

    rounded_panel(c, 48, 92, W - 96, 142, fill=FOREST, stroke=FOREST)
    c.setFont("Sifiriz-Bold", 12)
    c.setFillColor(SAGE)
    c.drawString(64, 204, "TTS SES KANITI")
    c.setFont("Sifiriz-Bold", 18)
    c.setFillColor(WHITE)
    c.drawString(64, 176, "Türkçe seslendirme • 12,4 saniye")
    draw_text(c, "Sakin, anlaşılır ve marka tonuyla uyumlu mikro görev kaydı. Metin–ses karşılaştırması ve süre kontrolü tamamlandı.", 64, 151, W - 128, size=9.5, color=CREAM, leading=14)
    c.setFont("Sifiriz", 8)
    c.setFillColor(SAGE)
    c.drawString(64, 111, "audio/SifirIz-TTS-Seslendirme.m4a")
    finish_page(c)


def process_page(c: canvas.Canvas) -> None:
    y = page_header(
        c,
        8,
        "07 / Sorumlu üretim",
        "Yapay zekâ hızlandırdı; editoryal sorumluluk insanda kaldı",
        "Her çıktı marka sesi, doğruluk, telif, kapsayıcılık ve uygulanabilirlik açısından insan kontrolünden geçirildi.",
    )
    rounded_panel(c, 48, y - 176, 244, 160, fill=WHITE)
    c.setFont("Sifiriz-Bold", 13)
    c.setFillColor(FOREST)
    c.drawString(64, y - 45, "Prompt tasarım sistemi")
    prompt = (
        "Rol + hedef kitle + tek amaç + marka sesi + format + somut kısıtlar + kaçınılacaklar + kontrol ölçütü. "
        "Örnek: ‘Suçluluk dili kullanma; doğrulanmamış sayı üretme; tek bir uygulanabilir davranış öner.’"
    )
    draw_text(c, prompt, 64, y - 70, 212, size=9.5, leading=14)

    rounded_panel(c, 304, y - 176, W - 352, 160, fill=MIST)
    c.setFont("Sifiriz-Bold", 13)
    c.setFillColor(FOREST)
    c.drawString(320, y - 45, "Kontrol kapıları")
    cy = y - 72
    for item in ["Marka sesi", "Kaynak ve iddia", "Telif ve özgünlük", "Erişilebilirlik", "İnsan onayı"]:
        cy = check(c, item, 320, cy, W - 384) - 3

    c.setFont("Sifiriz-Bold", 14)
    c.setFillColor(FOREST)
    c.drawString(48, y - 220, "Yönerge kapsama özeti")
    checklist = [
        "1–2 sayfalık marka stratejisi belgesi",
        "7 günlük Excel içerik takvimi",
        "1 özgün ve SEO uyumlu blog yazısı",
        "3 platforma özgü sosyal medya gönderisi",
        "3 tutarlı kampanya görseli",
        "15–20 saniye aralığında dikey video",
        "Türkçe TTS seslendirme kanıtı",
        "Prompt kütüphanesi, AI kullanım raporu ve otomasyon akışı",
    ]
    left_y = y - 252
    right_y = left_y
    for idx, item in enumerate(checklist):
        if idx < 4:
            left_y = check(c, item, 48, left_y, 240) - 6
        else:
            right_y = check(c, item, 306, right_y, 240) - 6

    rounded_panel(c, 48, 96, W - 96, 150, fill=FOREST, stroke=FOREST)
    c.setFont("Sifiriz-Bold", 12)
    c.setFillColor(SAGE)
    c.drawString(64, 220, "DOĞRULAMA KAYNAKLARI")
    sources = [
        "sifiratik.gov.tr — Sıfır Atık yaklaşımı",
        "wwf.org.tr — Sahil Sahiplen programı",
        "fazla.com — gıda fazlası çözümleri",
        "toogoodtogo.com — gıda israfı hareketi",
        "unep.org — Zero Waste 101",
    ]
    sy = 196
    for source in sources:
        c.setFillColor(APRICOT)
        c.circle(67, sy + 2, 2.5, fill=1, stroke=0)
        c.setFont("Sifiriz", 8.5)
        c.setFillColor(CREAM)
        c.drawString(76, sy, source)
        sy -= 20
    c.setFont("Sifiriz-Italic", 7.5)
    c.setFillColor(SAGE)
    c.drawRightString(W - 64, 112, "Erişim ve kullanım ayrıntıları Excel kaynak sekmesindedir.")
    finish_page(c)


def build() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("Sıfırİz — Atıksız Şehir Yaşamı İçerik Kampanyası")
    c.setAuthor("TNC Group Yapay Zekâ ile İçerik Üretimi Final Projesi")
    c.setSubject("Marka stratejisi, içerik takvimi ve çok formatlı kampanya portföyü")
    cover(c)
    strategy_page(c)
    calendar_page(c)
    blog_page(c)
    social_page(c)
    visuals_page(c)
    video_audio_page(c)
    process_page(c)
    c.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
