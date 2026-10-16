# หมวด 1 · เตรียมโปรเจกต์ Python

**จบหมวดนี้:** มี repo `hello-python` บน GitHub ที่ clone ลงเครื่องแล้ว พร้อม virtual environment และไฟล์ตั้งค่าครบ · เวลา 20 นาที

## ขั้นที่ 1 — สร้าง repo และ clone

1. เข้า github.com → ปุ่ม **+** → **New repository**
2. ตั้งชื่อ `hello-python` เลือก **Public** และติ๊ก **Add a README file** แล้วกด **Create repository**
3. Clone ลงเครื่องแล้วเปิดใน VS Code

```bash
git clone https://github.com/<username>/hello-python.git
cd hello-python
code .
```

4. ตรวจชื่อ branch ต้องเป็น `main` (repo ที่สร้างบน GitHub จะเป็น `main` อยู่แล้ว)

```bash
git branch        # ต้องเห็น  * main
```

ถ้าเห็น `master` ให้รัน `git branch -M main` เพราะ workflow ในคู่มือนี้ฟังเฉพาะ `main` ถ้าชื่อไม่ตรง แท็บ Actions จะว่างเปล่าโดยไม่มี error

## ขั้นที่ 2 — สร้างโครงสร้างโฟลเดอร์

สร้างไฟล์และโฟลเดอร์ตามนี้ ไฟล์ที่มีเครื่องหมาย ← จะเขียนในหมวดที่บอกไว้ ตอนนี้สร้างเฉพาะ 4 ไฟล์ตั้งค่าในขั้นที่ 3

```
hello-python/
├── .github/workflows/ci.yml   ← หมวด 3 และ 4
├── data/
│   └── scores.csv             ← ขั้นที่ 3
├── tests/
│   ├── test_grades.py         ← หมวด 2
│   └── test_build_site.py     ← หมวด 2
├── grades.py                  ← หมวด 2
├── build_site.py              ← หมวด 2
├── requirements-dev.txt       ← ขั้นที่ 3
├── pyproject.toml             ← ขั้นที่ 3
├── .gitignore                 ← ขั้นที่ 3
└── README.md                  (GitHub สร้างให้แล้ว)
```

## ขั้นที่ 3 — ไฟล์ตั้งค่า 4 ไฟล์

**`requirements-dev.txt`** — รายชื่อ library ที่ใช้ ระบุเวอร์ชันตายตัวด้วย `==` เพื่อให้เครื่องเรากับ GitHub ใช้เวอร์ชันเดียวกันเป๊ะ

```
pytest==8.4.2
pytest-cov==7.0.0
ruff==0.14.0
```

| library | ใช้ทำอะไร |
| --- | --- |
| `pytest` | ตัวรัน test |
| `pytest-cov` | วัดว่า test ครอบคลุมโค้ดกี่เปอร์เซ็นต์ (coverage) |
| `ruff` | ตรวจความผิดพลาดทั่วไป เช่น import แต่ไม่ใช้ ตัวแปรไม่ได้ประกาศ (lint) |

**`pyproject.toml`** — บอก pytest ว่า test อยู่ในโฟลเดอร์ `tests` และให้ import `grades` จากโฟลเดอร์หลักได้ ถ้าไม่มีบรรทัด `pythonpath` จะเจอ `ModuleNotFoundError: No module named 'grades'`

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

**`.gitignore`** — ไฟล์ที่ไม่ต้อง commit (สร้างใหม่ได้เสมอ)

```
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
.coverage
_site/
```

**`data/scores.csv`** — ข้อมูลที่จะขึ้นเว็บ (บรรทัดแรกคือชื่อคอลัมน์) บันทึกเป็น UTF-8

```csv
name,score
สมชาย,85
สมหญิง,72
มานี,64
ปิติ,48
```

## ขั้นที่ 4 — สร้าง virtual environment

Virtual environment (venv) คือ Python แยกเฉพาะโปรเจกต์ ติดตั้ง library แล้วไม่ปนกับโปรเจกต์อื่น เปิด terminal ใน VS Code (เมนู **Terminal → New Terminal**) แล้วรัน

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

เมื่อ activate แล้ว หน้าบรรทัด terminal จะมี `(.venv)` ตรวจด้วย `pytest --version` ต้องขึ้น `pytest 8.4.2` ทุกครั้งที่เปิด terminal ใหม่ต้อง activate ใหม่ (VS Code ทำให้เองถ้าเลือก interpreter เป็น `.venv`)

ถ้า Windows ขึ้น `running scripts is disabled on this system` ให้รัน `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` ครั้งเดียว แล้ว activate ใหม่

## สรุปหมวด 1

- [ ] repo `hello-python` อยู่บน branch `main`
- [ ] มี `requirements-dev.txt`, `pyproject.toml`, `.gitignore`, `data/scores.csv`
- [ ] activate venv แล้ว `pytest --version` ทำงาน

ยังไม่ต้อง commit ไปต่อ[หมวด 2](02-pytest.md) เขียนโค้ดและ test ก่อน
