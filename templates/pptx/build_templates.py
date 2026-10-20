"""Build editable Concept / Process / Comparison PowerPoint templates.

Usage:
    python templates/pptx/build_templates.py

Output:
    templates/pptx/technical-slide-templates.pptx
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

OUTPUT_PATH = Path(__file__).resolve().parent / "technical-slide-templates.pptx"
SLIDE_W = 13.333
SLIDE_H = 7.5
FONT_NAME = "Malgun Gothic"
CHARACTER_SPACING_PT = -1.0  # PowerPoint: Character Spacing > Condensed > 1.0 pt

COLORS = {
    "navy": "12233F", "deep": "1B3558", "blue": "3168C8",
    "teal": "26A6A1", "amber": "E49A4D", "ink": "1B2940",
    "muted": "64748B", "canvas": "F6F8FC", "white": "FFFFFF",
    "border": "DDE4EF", "pale_blue": "EAF1FF",
    "pale_teal": "E3F6F3", "pale_amber": "FFF3E4",
    "red": "F6C7BF", "green": "B7E9D1", "channel_blue": "B9CFF5",
}


def rgb(token: str) -> RGBColor:
    """Resolve one hex token to a PPTX color."""
    return RGBColor.from_string(COLORS.get(token, token))


def rectangle(slide, x, y, w, h, *, fill="white", stroke="border",
              rounded=True, line_width=1):
    """Add an editable rounded rectangle in inch units."""
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    sh = slide.shapes.add_shape(
        kind, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb(fill)
    sh.line.color.rgb = rgb(stroke)
    sh.line.width = Pt(line_width)
    if rounded:
        sh.adjustments[0] = 0.12
    return sh


def textbox(slide, content, x, y, w, h, *, size=18, bold=False,
            color="ink", align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.MIDDLE,
            margin=0.0):
    """Add editable text with global condensed character spacing (-1 pt)."""
    shape = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(0.015)
    tf.margin_bottom = Inches(0.015)
    tf.vertical_anchor = valign
    for i, line in enumerate(str(content).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        p.line_spacing = 1.18
        run = p.add_run()
        run.text = line
        run.font.name = FONT_NAME
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = rgb(color)
        # OOXML spc uses hundredths of a point (1 pt = 100 units).
        # python-pptx does not expose this through the run.font API.
        run._r.get_or_add_rPr().set(
            "spc", str(round(CHARACTER_SPACING_PT * 100))
        )
    return shape


def horizontal_line(slide, y):
    """Create footer separator."""
    sh = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.69), Inches(y), Inches(11.94), Inches(0.013)
    )
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb("border")
    sh.line.fill.background()


def base_slide(pres, title, subtitle, slide_type, slide_number):
    """Create 16:9 canvas with consistent header and footer."""
    slide = pres.slides.add_slide(pres.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = rgb("canvas")
    textbox(slide, f"{slide_type.upper()} / {slide_number:02d}",
            0.69, 0.48, 6.0, 0.28, size=11.5, color="blue", bold=True)
    textbox(slide, title, 0.69, 0.88, 12.0, 0.65,
            size=32, color="navy", bold=True)
    textbox(slide, subtitle, 0.69, 1.66, 12.0, 0.40,
            size=17, color="muted")
    horizontal_line(slide, 6.92)
    textbox(slide, f"Design Template Library · {slide_type}",
            0.69, 7.04, 8.0, 0.21, size=10.5, color="muted")
    textbox(slide, f"{slide_number:02d} / 03", 11.62, 7.04, 1.0, 0.21,
            size=10.5, color="muted", align=PP_ALIGN.RIGHT)
    return slide


def concept_slide(pres):
    """Concept: one idea, short explanations and a concrete RGB visual."""
    slide = base_slide(
        pres, "이미지는 숫자로 표현된다",
        "컴퓨터는 픽셀 값을 입력으로 받아 이미지의 특징을 계산한다.",
        "Concept", 1,
    )
    rectangle(slide, 0.69, 2.41, 6.00, 3.80)
    textbox(slide, "이미지 데이터를 이해하는 방법", 1.04, 2.73, 5.35, 0.48,
            size=21, bold=True, color="navy")
    lines = [
        "컬러 이미지는 R, G, B 채널로 표현",
        "각 채널은 픽셀 값이 모인 2차원 배열",
        "CNN은 배열에서 공간적 패턴을 학습",
    ]
    for i, line in enumerate(lines):
        cy = 3.64 + 0.70 * i
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(1.06), Inches(cy),
            Inches(0.12), Inches(0.12)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = rgb("blue")
        circle.line.fill.background()
        textbox(slide, line, 1.40, cy - 0.17, 4.99, 0.48, size=17.5)
    rectangle(slide, 6.98, 2.41, 5.65, 3.80,
              fill="pale_blue", stroke="CFDDFA")
    textbox(slide, "RGB CHANNELS → TENSOR", 7.34, 2.79, 4.7, 0.28,
            size=11.5, color="blue", bold=True)
    sizes = [("R", "red"), ("G", "green"), ("B", "channel_blue")]
    for j, (label, color) in enumerate(sizes):
        mx = 7.52 + j * 1.48
        for row in range(3):
            for col in range(3):
                rectangle(
                    slide, mx + col * 0.31, 3.39 + row * 0.31,
                    0.28, 0.28, fill=color, stroke="white", rounded=False,
                )
        textbox(slide, label, mx + 0.31, 4.42, 0.40, 0.28,
                size=14.5, bold=True, color="deep", align=PP_ALIGN.CENTER)
        if j < 2:
            textbox(slide, "+", mx + 1.11, 3.70, 0.29, 0.36,
                    size=18, bold=True, color="muted", align=PP_ALIGN.CENTER)
    rectangle(slide, 7.40, 4.95, 4.75, 0.58)
    textbox(slide, "64 × 64 × 3  (H × W × C)", 7.54, 5.07, 4.47, 0.30,
            size=18.6, bold=True, color="navy", align=PP_ALIGN.CENTER)
    textbox(slide, "이미지 크기 64×64는 예시이며, 텐서 축 순서는 프레임워크에 따라 다를 수 있음",
            7.42, 5.66, 4.79, 0.39, size=11.4, color="muted")


def process_slide(pres):
    """Process: input -> feature extraction -> task -> output."""
    slide = base_slide(
        pres, "CNN의 기본 데이터 흐름",
        "이미지에서 특징을 추출한 뒤 목적에 맞는 예측 결과를 만든다.",
        "Process", 2,
    )
    cards = [
        ("INPUT", "입력 이미지", "RGB 픽셀 데이터", "white", "border"),
        ("FEATURE", "CNN", "계층적으로\n특징 추출", "pale_blue", "blue"),
        ("TASK", "Task Head", "분류 등\n목적별 처리", "white", "border"),
        ("OUTPUT", "예측 결과", "클래스 점수 등", "pale_teal", "teal"),
    ]
    width = 2.57
    for i, (step, title, sub, fill, stroke) in enumerate(cards):
        x = 0.69 + 3.12 * i
        rectangle(slide, x, 2.91, width, 2.64, fill=fill, stroke=stroke,
                  line_width=1.5 if i in (1, 3) else 1)
        textbox(slide, step, x + 0.18, 3.19, width - 0.36, 0.23,
                size=10.5, bold=True, color="blue", align=PP_ALIGN.CENTER)
        textbox(slide, title, x + 0.15, 3.69, width - 0.30, 0.41,
                size=18.8, bold=True, color="navy", align=PP_ALIGN.CENTER)
        textbox(slide, sub, x + 0.20, 4.33, width - 0.40, 0.62,
                size=15.1, color="muted", align=PP_ALIGN.CENTER)
        if i < 3:
            textbox(slide, "→", x + 2.64, 3.91, 0.42, 0.47,
                    size=27, bold=True, color="blue", align=PP_ALIGN.CENTER)
    rectangle(slide, 0.78, 5.87, 0.04, 0.42,
              fill="teal", stroke="teal", rounded=False)
    textbox(slide,
            "핵심: Feature extractor와 Task head의 역할을 분리해 이해한다.",
            1.02, 5.88, 11.15, 0.38, size=16.5, color="deep")


def comparison_slide(pres):
    """Comparison: rule-based approach versus machine learning."""
    slide = base_slide(
        pres, "규칙 기반과 머신러닝의 차이",
        "판단 기준을 누가, 어떻게 만드는지가 핵심적인 차이다.",
        "Comparison", 3,
    )
    cards = [
        (0.69, "RULE-BASED", "사람이 규칙을 정의",
         "예측·판단 조건과 규칙을\n개발자가 직접 작성한다.",
         "예: 1 + 1 = 2", "명확하고 단순한 조건에 적합",
         "pale_amber", "945616"),
        (6.79, "MACHINE LEARNING", "데이터에서 규칙을 학습",
         "정의된 학습 목표와 데이터로\n모델 파라미터를 추정한다.",
         "예: 이미지 속 사과 분류", "복잡한 시각 패턴에 유리할 수 있음",
         "pale_blue", "blue"),
    ]
    for x, badge, title, desc, example, foot, badge_fill, badge_color in cards:
        rectangle(slide, x, 2.42, 5.83, 3.79)
        rectangle(slide, x + 0.29, 2.70, 2.40, 0.40,
                  fill=badge_fill, stroke=badge_fill)
        textbox(slide, badge, x + 0.40, 2.78, 2.22, 0.23,
                size=10.9, bold=True, color=badge_color)
        textbox(slide, title, x + 0.31, 3.30, 5.25, 0.50,
                size=22.2, bold=True, color="navy")
        textbox(slide, desc, x + 0.31, 4.03, 5.24, 0.68,
                size=16.4, color="muted")
        rectangle(slide, x + 0.31, 5.02, 5.20, 0.62,
                  fill="canvas", stroke="canvas")
        textbox(slide, example, x + 0.48, 5.13, 4.88, 0.35,
                size=18.4, bold=True, color="deep")
        textbox(slide, foot, x + 0.32, 5.78, 5.18, 0.25,
                size=12.9, color="muted")


def main() -> None:
    """Generate a reusable 3-slide PPTX source deck."""
    pres = Presentation()
    pres.slide_width = Inches(SLIDE_W)
    pres.slide_height = Inches(SLIDE_H)
    concept_slide(pres)
    process_slide(pres)
    comparison_slide(pres)
    pres.save(OUTPUT_PATH)
    print(f"Created {OUTPUT_PATH} ({len(pres.slides)} slides)")


if __name__ == "__main__":
    main()
