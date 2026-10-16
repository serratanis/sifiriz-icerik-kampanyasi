import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const projectDir = path.resolve(import.meta.dirname, "..");
const outputDir = path.join(projectDir, "deliverables");
const renderDir = path.join(projectDir, "tmp", "xlsx-render");
await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(renderDir, { recursive: true });

const colors = {
  forest: "#173F3A",
  sage: "#A7C4A0",
  apricot: "#E76F51",
  cream: "#F5F0E6",
  charcoal: "#20332E",
  mist: "#EAF0EA",
  white: "#FFFFFF",
  gray: "#66736F",
  line: "#D4DDD8",
};
const font = "Arial";

const workbook = Workbook.create();
const calendar = workbook.worksheets.add("7 Günlük Takvim");
const control = workbook.worksheets.add("Kontrol ve Kaynaklar");

calendar.showGridLines = false;
calendar.tabColor = colors.apricot;
calendar.freezePanes.freezeRows(7);

calendar.mergeCells("A1:J1");
calendar.getRange("A1").values = [["Sıfırİz — 7 Günlük İçerik Takvimi"]];
calendar.getRange("A1:J1").format = {
  fill: colors.forest,
  font: { name: font, size: 22, bold: true, color: colors.white },
  verticalAlignment: "center",
};
calendar.getRange("A1:J1").format.rowHeight = 42;

calendar.mergeCells("A2:J2");
calendar.getRange("A2").values = [[
  "Kampanya: Bugün bir adımla başla.  •  Dönem: 19–25 Ekim 2026  •  Amaç: küçük ve tekrarlanabilir atıksız yaşam davranışları",
]];
calendar.getRange("A2:J2").format = {
  fill: colors.cream,
  font: { name: font, size: 11, italic: true, color: colors.charcoal },
  wrapText: true,
  verticalAlignment: "center",
};
calendar.getRange("A2:J2").format.rowHeight = 35;

calendar.getRange("A4:B4").values = [["TOPLAM İÇERİK", null]];
calendar.getRange("C4:D4").values = [["ONAYLANAN", null]];
calendar.getRange("E4:F4").values = [["GÖRSEL ODAKLI", null]];
calendar.getRange("G4:H4").values = [["VİDEO", null]];
calendar.getRange("I4:J4").values = [["SESLİ İÇERİK", null]];
calendar.mergeCells("A4:B4");
calendar.mergeCells("C4:D4");
calendar.mergeCells("E4:F4");
calendar.mergeCells("G4:H4");
calendar.mergeCells("I4:J4");
calendar.getRange("A4:J4").format = {
  fill: colors.sage,
  font: { name: font, size: 9, bold: true, color: colors.charcoal },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};

calendar.getRange("A5:B5").formulas = [["=COUNTA(A8:A14)", null]];
calendar.getRange("C5:D5").formulas = [["=COUNTIF(J8:J14,\"Onaylandı\")", null]];
calendar.getRange("E5:F5").formulas = [["=COUNTIF(F8:F14,\"Carousel\")+COUNTIF(F8:F14,\"Tek görsel\")", null]];
calendar.getRange("G5:H5").formulas = [["=COUNTIF(F8:F14,\"Dikey video\")", null]];
calendar.getRange("I5:J5").formulas = [["=COUNTIF(F8:F14,\"TTS ses\")", null]];
calendar.mergeCells("A5:B5");
calendar.mergeCells("C5:D5");
calendar.mergeCells("E5:F5");
calendar.mergeCells("G5:H5");
calendar.mergeCells("I5:J5");
calendar.getRange("A5:J5").format = {
  fill: colors.white,
  font: { name: font, size: 20, bold: true, color: colors.forest },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  borders: { preset: "all", style: "thin", color: colors.line },
};
calendar.getRange("A5:J5").format.rowHeight = 32;

const headers = [[
  "Gün", "Tarih", "İçerik Sütunu", "Konu", "Kanal", "Format",
  "Amaç", "Ana CTA", "Dosya / Kanıt", "Kontrol Durumu",
]];
calendar.getRange("A7:J7").values = headers;
calendar.getRange("A7:J7").format = {
  fill: colors.forest,
  font: { name: font, size: 10, bold: true, color: colors.white },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: colors.white },
};
calendar.getRange("A7:J7").format.rowHeight = 34;

const calendarRows = [
  ["Pazartesi", new Date(2026, 9, 19), "Mahallede Döngü", "Eşyaya ikinci tur: tamir ve paylaşım", "Instagram", "Carousel", "Farkındalık", "Bugün bir eşyayı ikinci tura çıkar.", "assets/final/01-ikinci-tur.png", "Onaylandı"],
  ["Salı", new Date(2026, 9, 20), "Etikete Değil Alışkanlığa", "Atıksız şehir yaşamı için 7 gerçekçi adım", "Web sitesi", "Blog", "Bilgilendirme", "Yedi adımdan birini seç.", "content/blog-yazisi.md", "Onaylandı"],
  ["Çarşamba", new Date(2026, 9, 21), "Evde 10 Dakika", "Satın almadan önce elindekine bak", "Instagram", "Tek görsel", "Etkileşim", "Dolabında bir unutulanı değerlendir.", "assets/final/02-once-elindekine-bak.png", "Onaylandı"],
  ["Perşembe", new Date(2026, 9, 22), "Mahallede Döngü", "Tamir, paylaşım ve yerel dayanışma", "LinkedIn", "Metin gönderisi", "Güven", "Mahallendeki bir döngü noktasını paylaş.", "content/sosyal-medya-gonderileri.md", "Onaylandı"],
  ["Cuma", new Date(2026, 9, 23), "Paylaş ve Çoğalt", "Bir eşya, üç seçenek: kullan, tamir et, paylaş", "Reels / Shorts", "Dikey video", "Erişim", "Videoyu kaydet; hafta sonu birini uygula.", "video/SifirIz-18sn-Tanitim.mp4", "Onaylandı"],
  ["Cumartesi", new Date(2026, 9, 24), "Etikete Değil Alışkanlığa", "Mükemmellik değil tekrar", "X", "Kısa seri", "Topluluk", "Bugünün küçük adımını yanıtla.", "content/sosyal-medya-gonderileri.md", "Onaylandı"],
  ["Pazar", new Date(2026, 9, 25), "Paylaş ve Çoğalt", "Haftanın sesli mikro görevi", "Podcast / Story", "TTS ses", "Hatırlatma", "Bir sonraki haftanın adımını seç.", "audio/SifirIz-TTS-Seslendirme.m4a", "Onaylandı"],
];
calendar.getRange("A8:J14").values = calendarRows;
calendar.getRange("A8:J14").format = {
  font: { name: font, size: 10, color: colors.charcoal },
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: colors.line },
};
calendar.getRange("B8:B14").setNumberFormat("dd/mm/yyyy");
calendar.getRange("A8:J14").format.rowHeight = 54;
for (const row of [8, 10, 12, 14]) {
  calendar.getRange(`A${row}:J${row}`).format.fill = colors.mist;
}
calendar.getRange("J8:J14").dataValidation = {
  rule: { type: "list", values: ["Taslak", "Kontrolde", "Onaylandı"] },
};
calendar.getRange("J8:J14").conditionalFormats.add("containsText", {
  text: "Onaylandı",
  format: { fill: "#DDEFD9", font: { color: colors.forest, bold: true } },
});

const calendarWidths = [15, 16, 24, 34, 18, 18, 18, 35, 38, 18];
calendarWidths.forEach((width, index) => {
  calendar.getRangeByIndexes(0, index, 14, 1).format.columnWidth = width;
});

control.showGridLines = false;
control.tabColor = colors.sage;
control.freezePanes.freezeRows(5);
control.mergeCells("A1:G1");
control.getRange("A1").values = [["Sıfırİz — İçerik Kontrolü ve Kaynak İzleme"]];
control.getRange("A1:G1").format = {
  fill: colors.forest,
  font: { name: font, size: 20, bold: true, color: colors.white },
  verticalAlignment: "center",
};
control.getRange("A1:G1").format.rowHeight = 42;
control.mergeCells("A2:G2");
control.getRange("A2").values = [[
  "Her içerik insan kontrolünden geçti; istatistik, telif ve kesin sonuç iddiaları kaynaklandırılmadan kullanılmadı.",
]];
control.getRange("A2:G2").format = {
  fill: colors.cream,
  font: { name: font, size: 11, italic: true, color: colors.charcoal },
  wrapText: true,
  verticalAlignment: "center",
};
control.getRange("A2:G2").format.rowHeight = 34;

control.getRange("A4:G4").values = [[
  "İçerik", "Tür", "Marka Sesi", "Telif", "Kaynak / Doğruluk", "İnsan Kontrolü", "Durum",
]];
control.getRange("A4:G4").format = {
  fill: colors.forest,
  font: { name: font, size: 10, bold: true, color: colors.white },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: colors.white },
};
const checks = [
  ["Atıksız şehir yaşamı için 7 gerçekçi adım", "Blog", "Uygun", "Özgün metin", "5 birincil/kurumsal kaynak", "Tamamlandı", "Onaylandı"],
  ["Eşyaya ikinci tur", "Instagram carousel", "Uygun", "AI görsel + insan tasarımı", "İddiasız davranış çağrısı", "Tamamlandı", "Onaylandı"],
  ["Satın almadan önce elindekine bak", "Instagram görsel", "Uygun", "AI görsel + insan tasarımı", "İddiasız davranış çağrısı", "Tamamlandı", "Onaylandı"],
  ["Mahallede döngü", "LinkedIn gönderisi", "Uygun", "Özgün metin", "Kaynak listesine bağlı", "Tamamlandı", "Onaylandı"],
  ["Mükemmellik değil tekrar", "X kısa seri", "Uygun", "Özgün metin", "Kesin sonuç vaadi yok", "Tamamlandı", "Onaylandı"],
  ["Bugün bir adımla başla", "18 sn dikey video", "Uygun", "AI görsel + özgün kurgu", "Altyazı ve süre kontrolü", "Tamamlandı", "Onaylandı"],
  ["Haftanın mikro görevi", "TTS ses", "Uygun", "Özgün senaryo", "Ses ve metin karşılaştırıldı", "Tamamlandı", "Onaylandı"],
];
control.getRange("A5:G11").values = checks;
control.getRange("A5:G11").format = {
  font: { name: font, size: 10, color: colors.charcoal },
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: colors.line },
};
control.getRange("A5:G11").format.rowHeight = 45;
for (const row of [6, 8, 10]) {
  control.getRange(`A${row}:G${row}`).format.fill = colors.mist;
}

control.mergeCells("A13:G13");
control.getRange("A13").values = [["DOĞRULAMA KAYNAKLARI"]];
control.getRange("A13:G13").format = {
  fill: colors.sage,
  font: { name: font, size: 11, bold: true, color: colors.charcoal },
  verticalAlignment: "center",
};
control.getRange("A14:G14").values = [["Kurum", "Konu", "Bağlantı", "Erişim", "Kullanım", "Not", "Durum"]];
control.getRange("A14:G14").format = {
  fill: colors.forest,
  font: { name: font, size: 10, bold: true, color: colors.white },
  horizontalAlignment: "center",
  wrapText: true,
};
const sources = [
  ["Sıfır Atık Türkiye", "Sıfır atık yaklaşımı", "https://www.sifiratik.gov.tr/sifir-atik/sifir-atik-nedir", new Date(2026, 9, 16), "Arka plan doğrulama", "Resmî kaynak", "Doğrulandı"],
  ["WWF-Türkiye", "Sahil Sahiplen programı", "https://www.wwf.org.tr/?15760%2Fsahilsahiplenprogramsonuclar2023-2024=", new Date(2026, 9, 16), "Bağlam ve örnek", "Kurumsal kaynak", "Doğrulandı"],
  ["Fazla", "Gıda fazlası çözümleri", "https://fazla.com/gida/", new Date(2026, 9, 16), "Benzer oluşum analizi", "Kurumsal kaynak", "Doğrulandı"],
  ["Too Good To Go", "Gıda israfı hareketi", "https://www.toogoodtogo.com/en-us/about-us", new Date(2026, 9, 16), "Benzer oluşum analizi", "Kurumsal kaynak", "Doğrulandı"],
  ["UNEP", "Zero Waste 101", "https://www.unep.org/interactives/zero-waste-101/index.html", new Date(2026, 9, 16), "Küresel çerçeve", "Birleşmiş Milletler", "Doğrulandı"],
];
control.getRange("A15:G19").values = sources;
control.getRange("A15:G19").format = {
  font: { name: font, size: 9, color: colors.charcoal },
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "all", style: "thin", color: colors.line },
};
control.getRange("D15:D19").setNumberFormat("dd/mm/yyyy");
control.getRange("A15:G19").format.rowHeight = 55;
for (const row of [16, 18]) {
  control.getRange(`A${row}:G${row}`).format.fill = colors.mist;
}
const controlWidths = [25, 25, 54, 16, 25, 22, 16];
controlWidths.forEach((width, index) => {
  control.getRangeByIndexes(0, index, 19, 1).format.columnWidth = width;
});

calendar.getRange("A1:J14").format.font.name = font;
control.getRange("A1:G19").format.font.name = font;

workbook.recalculate();

const calendarPreview = await workbook.render({
  sheetName: "7 Günlük Takvim",
  range: "A1:J14",
  scale: 1.35,
  format: "png",
});
await fs.writeFile(
  path.join(renderDir, "7-gunluk-takvim.png"),
  new Uint8Array(await calendarPreview.arrayBuffer()),
);

const controlPreview = await workbook.render({
  sheetName: "Kontrol ve Kaynaklar",
  range: "A1:G19",
  scale: 1.15,
  format: "png",
});
await fs.writeFile(
  path.join(renderDir, "kontrol-ve-kaynaklar.png"),
  new Uint8Array(await controlPreview.arrayBuffer()),
);

const inspection = await workbook.inspect({
  kind: "formula,region",
  sheetId: "7 Günlük Takvim",
  range: "A1:J14",
  maxChars: 5000,
  tableMaxRows: 16,
  tableMaxCols: 10,
});
const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 50 },
  maxChars: 2000,
});

const output = await SpreadsheetFile.exportXlsx(workbook);
const outputPath = path.join(outputDir, "SifirIz-7-Gunluk-Icerik-Takvimi.xlsx");
await output.save(outputPath);

console.log(JSON.stringify({
  outputPath,
  calendarPreview: path.join(renderDir, "7-gunluk-takvim.png"),
  controlPreview: path.join(renderDir, "kontrol-ve-kaynaklar.png"),
  inspection: inspection.ndjson,
  formulaErrors: formulaErrors.ndjson,
}, null, 2));
