# หมวด 2 · เขียน test ด้วย pytest

**จบหมวดนี้:** มีโค้ด 2 ไฟล์กับ test 18 ตัวที่ผ่านบนเครื่อง และอ่านผลเมื่อ test พังเป็น · เวลา 40 นาที · ต้องทำ[หมวด 1](01-setup.md)ก่อน

หลักคิดของ test: ทุก test ทำ 3 อย่าง — **เตรียมข้อมูล → เรียกโค้ด → ตรวจผลด้วย `assert`** ถ้า `assert` ไม่จริง test นั้นพัง และ pytest จะจบด้วย exit code 1 ซึ่งเป็นสิ่งที่ GitHub ใช้ตัดสินว่า CI แดง

## 2.1 โค้ดที่จะทดสอบ: grades.py

```python
def grade(score):
    """แปลงคะแนน 0-100 เป็นเกรด"""
    if not 0 <= score <= 100:
        raise ValueError("คะแนนต้องอยู่ระหว่าง 0-100")
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    if score >= 50:
        return "D"
    return "F"


def average(scores):
    """หาค่าเฉลี่ย ถ้าไม่มีข้อมูลให้ error"""
    if not scores:
        raise ValueError("ต้องมีคะแนนอย่างน้อย 1 ค่า")
    return round(sum(scores) / len(scores), 2)
```

## 2.2 โค้ดที่จะทดสอบ: build_site.py

ไฟล์นี้คือตัวสร้างเว็บ แบ่งเป็น 3 ฟังก์ชันเล็ก ๆ ให้ test ง่าย: อ่านไฟล์ → สร้าง HTML → เขียนไฟล์

```python
import csv
import html
import os
from pathlib import Path

from grades import average, grade

OUTPUT_DIR = Path("_site")


def load_scores(csv_path):
    """อ่านไฟล์ CSV คืนค่าเป็น list ของ (ชื่อ, คะแนน)"""
    with open(csv_path, encoding="utf-8") as f:
        return [(row["name"], int(row["score"])) for row in csv.DictReader(f)]


def render_html(rows, title):
    """สร้างหน้าเว็บ HTML จากข้อมูลคะแนน"""
    table_rows = "\n".join(
        f"<tr><td>{html.escape(name)}</td><td>{score}</td><td>{grade(score)}</td></tr>"
        for name, score in rows
    )
    avg = average([score for _, score in rows])
    return f"""<!DOCTYPE html>
<html lang="th">
<head><meta charset="UTF-8"><title>{html.escape(title)}</title></head>
<body>
<h1>{html.escape(title)}</h1>
<table>
<tr><th>ชื่อ</th><th>คะแนน</th><th>เกรด</th></tr>
{table_rows}
</table>
<p>ค่าเฉลี่ย: {avg}</p>
</body>
</html>
"""


def main():
    title = os.environ.get("SITE_TITLE") or "ผลคะแนนวิชา CI/CD"
    rows = load_scores("data/scores.csv")
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "index.html").write_text(render_html(rows, title), encoding="utf-8")
    print(f"Built {OUTPUT_DIR / 'index.html'} ({len(rows)} students)")


if __name__ == "__main__":
    main()
```

- `html.escape(...)` — กันไม่ให้ชื่อที่มี `<` `>` กลายเป็นโค้ด HTML จริง (ป้องกันการโจมตีแบบ XSS)
- `os.environ.get("SITE_TITLE") or ...` — อ่านหัวข้อเว็บจาก environment variable ถ้าไม่มีหรือเป็นค่าว่างใช้ค่าเริ่มต้น ใช้ `or` แทนการส่งค่าเริ่มต้นเข้า `get()` เพราะ GitHub ส่งค่าว่างมาเมื่อยังไม่ได้ตั้ง Variable (จะใช้ใน[หมวด 6](06-secrets.md))
- `print` เป็นภาษาอังกฤษโดยตั้งใจ เพราะ terminal บน Windows บางเครื่องพิมพ์ภาษาไทยไม่ได้ และจะขึ้น `UnicodeEncodeError` (บนเว็บยังเป็นภาษาไทยปกติ)

ลองรันดู: `python build_site.py` จะได้ไฟล์ `_site/index.html` เปิดด้วย browser ได้เลย

## 2.3 test ของ grades.py — tests/test_grades.py

```python
import pytest

from grades import average, grade


@pytest.mark.parametrize(
    "score, expected",
    [(100, "A"), (80, "A"), (79, "B"), (70, "B"), (60, "C"), (50, "D"), (49, "F"), (0, "F")],
)
def test_grade(score, expected):
    assert grade(score) == expected


@pytest.mark.parametrize("score", [-1, 101])
def test_grade_out_of_range(score):
    with pytest.raises(ValueError):
        grade(score)


def test_average():
    assert average([80, 70, 60]) == 70


def test_average_rounds_to_2_digits():
    assert average([1, 2, 2]) == pytest.approx(1.67)


def test_average_empty_list():
    with pytest.raises(ValueError, match="อย่างน้อย 1 ค่า"):
        average([])
```

## 2.4 test ของ build_site.py — tests/test_build_site.py

```python
from build_site import load_scores, main, render_html


def test_load_scores(tmp_path):
    csv_file = tmp_path / "scores.csv"
    csv_file.write_text("name,score\nเอ,90\nบี,40\n", encoding="utf-8")
    assert load_scores(csv_file) == [("เอ", 90), ("บี", 40)]


def test_render_html_has_title_and_rows():
    page = render_html([("สมชาย", 85), ("ปิติ", 48)], "ทดสอบ")
    assert "<title>ทดสอบ</title>" in page
    assert "<td>สมชาย</td><td>85</td><td>A</td>" in page
    assert "<td>ปิติ</td><td>48</td><td>F</td>" in page
    assert "ค่าเฉลี่ย: 66.5" in page


def test_render_html_escapes_names():
    page = render_html([("<script>", 50)], "ทดสอบ")
    assert "<script>" not in page
    assert "&lt;script&gt;" in page


def test_real_data_file_is_valid():
    rows = load_scores("data/scores.csv")
    assert len(rows) > 0
    assert all(0 <= score <= 100 for _, score in rows)


def test_main_builds_site(tmp_path, monkeypatch):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "scores.csv").write_text("name,score\nเอ,90\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SITE_TITLE", "หัวข้อจาก Variable")

    main()

    page = (tmp_path / "_site" / "index.html").read_text(encoding="utf-8")
    assert "<h1>หัวข้อจาก Variable</h1>" in page
```

## 2.5 เทคนิค pytest ที่ใช้ในตัวอย่าง

| เทคนิค | ใช้ทำอะไร | ตัวอย่างจากโค้ด |
| --- | --- | --- |
| `assert a == b` | ตรวจว่าผลตรงกัน | `assert average([80, 70, 60]) == 70` |
| `assert x in y` | ตรวจว่ามีข้อความอยู่ในผล | `assert "<title>ทดสอบ</title>" in page` |
| `@pytest.mark.parametrize` | เขียน test ครั้งเดียว รันหลายชุดข้อมูล | `test_grade` รัน 8 ครั้ง |
| `pytest.raises` | ตรวจว่าโค้ด **ต้อง** error | คะแนน -1 กับ 101 |
| `pytest.approx` | เทียบทศนิยมแบบใกล้เคียง | `1.67` (เพราะ `0.1 + 0.2` ไม่เท่ากับ `0.3` พอดี) |
| `tmp_path` | โฟลเดอร์ชั่วคราว ลบทิ้งเองหลัง test | สร้าง CSV ปลอมใน `test_load_scores` |
| `monkeypatch` | เปลี่ยนสภาพแวดล้อมชั่วคราว (โฟลเดอร์, env var) แล้วคืนค่าเดิมเอง | `monkeypatch.setenv("SITE_TITLE", ...)` |

เลือกค่าที่จะ test ให้ครบ 3 กลุ่ม:

- **กรณีปกติ** — เช่น 65 ได้ C
- **ค่าขอบ** — 80 กับ 79, 0 กับ 100 จุดที่เกรดเปลี่ยน bug มักซ่อนอยู่ตรงนี้ (เช่นเขียน `>` แทน `>=`)
- **กรณีผิดปกติ** — คะแนนติดลบ, list ว่าง โค้ดที่ควร error แต่ไม่ error คือ bug

`test_real_data_file_is_valid` พิเศษกว่าตัวอื่น: มันตรวจ**ข้อมูลจริง**ที่จะขึ้นเว็บ ถ้าใครพิมพ์คะแนนผิดใน CSV (เช่น `850` หรือ `แปดสิบ`) CI จะแดงและเว็บจะไม่ถูกอัปเดตด้วยข้อมูลผิด

## 2.6 รันบนเครื่อง

รัน 3 คำสั่งนี้ทุกครั้งก่อน push เพราะใน[หมวด 3](03-ci.md) GitHub จะรันชุดเดียวกันนี้

```bash
ruff check .
pytest
pytest --cov=grades --cov=build_site --cov-report=term-missing --cov-fail-under=80
```

ผลที่ควรเห็นจากคำสั่งสุดท้าย

```
Name            Stmts   Miss  Cover   Missing
---------------------------------------------
build_site.py      21      1    95%   48
grades.py          16      0   100%
---------------------------------------------
TOTAL              37      1    97%
Required test coverage of 80% reached. Total coverage: 97.30%
18 passed
```

| คอลัมน์ | ความหมาย |
| --- | --- |
| `Stmts` | จำนวนบรรทัดคำสั่งในไฟล์ |
| `Miss` | บรรทัดที่ไม่มี test ไหนเรียกใช้ |
| `Missing` | เลขบรรทัดที่ไม่มี test (บรรทัด 48 คือ `main()` ใต้ `if __name__` ซึ่งไม่จำเป็นต้อง test) |
| `--cov-fail-under=80` | ถ้ารวมต่ำกว่า 80% ให้ถือว่าไม่ผ่าน (exit code 1) |

## 2.7 อ่านผลเมื่อ test พัง

ลองทำให้พังเอง: แก้ `if score >= 80:` เป็น `if score > 80:` ใน `grades.py` แล้วรัน `pytest`

```
FAILED tests/test_grades.py::test_grade[80-A] - AssertionError: assert 'B' == 'A'
1 failed, 17 passed
```

อ่านทีละส่วน: ไฟล์ `test_grades.py` → test `test_grade` → ชุดข้อมูล `[80-A]` → ได้ `'B'` แต่คาดหวัง `'A'` รู้ทันทีว่าคะแนน 80 พัง แก้กลับเป็น `>=` ก่อนไปต่อ

## สรุปหมวด 2

- [ ] `ruff check .` ขึ้น `All checks passed!`
- [ ] `pytest` ขึ้น `18 passed`
- [ ] coverage เกิน 80%
- [ ] เคยทำให้ test พังและอ่านผลออก

Commit ได้แล้ว (ยังไม่ต้อง push) — `git add .` → `git commit -m "add grades and tests"` แล้วไป[หมวด 3](03-ci.md)
