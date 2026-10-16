# ตัวอย่างโปรเจกต์ Python CI/CD (เว็บประกาศผลคะแนน)

โค้ดฉบับสมบูรณ์ของคู่มือใน [`docs/`](../../docs/README.md) ทดสอบแล้วบน Python 3.13: ruff ผ่าน, pytest 18 ตัวผ่าน, coverage 97%

| ไฟล์ | หน้าที่ |
| --- | --- |
| `grades.py` | คำนวณเกรดและค่าเฉลี่ย |
| `build_site.py` | อ่าน `data/scores.csv` แล้วสร้าง `_site/index.html` |
| `tests/` | test ทั้งหมด (pytest) |
| `ci.yml` | workflow ฉบับสมบูรณ์ — ย้ายไปไว้ที่ `.github/workflows/ci.yml` ใน repo ของตัวเอง |

## นำไปใช้

1. Copy ทุกไฟล์ในโฟลเดอร์นี้ไปไว้ที่ root ของ repo ใหม่ (เช่น `hello-python`)
2. ย้าย `ci.yml` ไปไว้ที่ `.github/workflows/ci.yml`
3. ตั้ง Settings → Pages → Source เป็น **GitHub Actions**
4. รันบนเครื่องให้ผ่านก่อน push

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
ruff check .
pytest --cov=grades --cov=build_site --cov-report=term-missing --cov-fail-under=80
python build_site.py
```

ไฟล์ `ci.yml` อยู่นอก `.github/workflows/` โดยตั้งใจ เพื่อไม่ให้ไปรันใน repo `hello-worldz` นี้
