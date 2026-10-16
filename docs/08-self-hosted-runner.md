# หมวด 8 · Self-hosted runner

**จบหมวดนี้:** pytest รันบนคอมพิวเตอร์ของนิสิตเองแทนเครื่องของ GitHub เห็นงานเข้ามาใน terminal · เวลา 30 นาที · ต้องทำ[หมวด 3](03-ci.md)ก่อน

**ใช้ตอนไหน?** เมื่อต้องการฮาร์ดแวร์พิเศษ (GPU สำหรับงาน AI, บอร์ด IoT), ต้องเข้าถึงเครือข่ายภายในองค์กร (เช่น ฐานข้อมูลของคณะ) หรือ private repo ใช้นาที Actions เกินโควตาฟรี

**คำเตือน:** ใช้ self-hosted runner กับ **private repo เท่านั้น** บน public repo ใครก็ fork แล้วเปิด PR ให้รันคำสั่งอะไรก็ได้บนเครื่องของเรา รวมถึงอ่านไฟล์ส่วนตัว หมวดนี้จึงใช้ repo ใหม่แบบ Private และทำเฉพาะส่วน test (Pages บน private repo ต้องใช้ GitHub Pro)

## 8.1 เตรียม repo

1. สร้าง repo ใหม่ชื่อ `hello-runner` เลือก **Private**
2. Copy `grades.py`, `build_site.py`, `tests/`, `data/`, `requirements-dev.txt`, `pyproject.toml`, `.gitignore` จาก `hello-python` มาใส่ แล้ว push
3. เครื่องที่จะเป็น runner ต้องมี Git และ Python (`git --version`, `python --version`)

## 8.2 ติดตั้ง runner

1. repo `hello-runner` → **Settings** → **Actions** → **Runners** → **New self-hosted runner**
2. เลือก OS (Windows / macOS / Linux) และ Architecture (ส่วนใหญ่ x64, Mac ชิป M เลือก ARM64)
3. GitHub แสดงคำสั่ง 3 ชุด ให้ **copy จากหน้าเว็บไปรันตามลำดับ** (เวอร์ชันและ token เปลี่ยนทุกครั้ง token หมดอายุใน 1 ชั่วโมง)
    - **Download** — สร้างโฟลเดอร์ `actions-runner` แล้วดาวน์โหลดตัว runner
    - **Configure** — คำสั่ง `config` ที่มี `--url` และ `--token` ผูก runner กับ repo
    - **Run** — `./run.cmd` (Windows) หรือ `./run.sh` (macOS/Linux)
4. ตอน configure กด Enter ใช้ค่าเริ่มต้นได้ทั้งหมด label ที่ได้คือ `self-hosted`, ชื่อ OS (`Windows`, `macOS`, `Linux`) และ architecture (`X64`, `ARM64`)
5. เห็น `Listening for Jobs` ใน terminal และหน้า Runners ขึ้น **Idle** สีเขียว = พร้อม **ห้ามปิด terminal นี้**

## 8.3 ci.yml สำหรับ runner บนเครื่องเรา

ต่างจากหมวด 3 สองจุด: `runs-on` ชี้ไปที่เครื่องเรา และสร้าง venv ใน job เพราะเครื่องเราไม่ได้ถูกล้างทุกครั้ง (ไม่ควร `pip install` ลง Python หลักของเครื่อง)

**runner เป็น Windows**

```yaml
name: CI on my machine

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: [self-hosted, windows]
    steps:
      - uses: actions/checkout@v4
      - run: python --version
      - run: python -m venv .venv
      - run: .venv\Scripts\python -m pip install -r requirements-dev.txt
      - run: .venv\Scripts\python -m ruff check .
      - run: .venv\Scripts\python -m pytest
```

**runner เป็น macOS หรือ Linux** — เปลี่ยน label และ path ของ venv

```yaml
    runs-on: [self-hosted, macos]     # หรือ [self-hosted, linux]
    steps:
      - uses: actions/checkout@v4
      - run: python3 --version
      - run: python3 -m venv .venv
      - run: .venv/bin/python -m pip install -r requirements-dev.txt
      - run: .venv/bin/python -m ruff check .
      - run: .venv/bin/python -m pytest
```

| บรรทัด | ความหมาย |
| --- | --- |
| `runs-on: [self-hosted, windows]` | ส่งงานให้ runner ที่มี label **ครบทุกตัว**ในรายการ |
| ไม่มี `setup-python` | ใช้ Python ที่ติดตั้งในเครื่องอยู่แล้ว step `python --version` จะพิมพ์เวอร์ชันของเครื่องเรา |
| `python -m venv .venv` | สร้าง venv ในโฟลเดอร์งาน แยกจาก Python หลัก |
| `.venv\Scripts\python -m ...` | เรียก Python ใน venv ตรง ๆ แทนการ activate เพราะแต่ละ step เป็น shell ใหม่ (activate ใน step หนึ่งไม่ติดไป step ถัดไป) |

## 8.4 ดูผล

1. Push workflow ขึ้นไป
2. terminal ที่รัน runner จะขึ้น `Running job: test` และ `Job test completed with result: Succeeded`
3. โค้ดที่ถูก checkout อยู่ใน `actions-runner/_work/hello-runner/hello-runner/` บนเครื่องเรา เปิดดูได้ รวมถึงโฟลเดอร์ `.venv` ที่ job สร้าง
4. ปิด runner (Ctrl+C) แล้วกด **Run workflow** — job ค้าง Queued รอจน runner กลับมา นี่คือข้อเสีย: เครื่องต้องเปิดอยู่ตลอด

| | GitHub-hosted (`ubuntu-latest`) | Self-hosted |
| --- | --- | --- |
| ค่าใช้จ่าย | ฟรีไม่จำกัดสำหรับ public repo | ไม่เสียนาที Actions แต่เสียค่าเครื่องและค่าไฟ |
| เครื่องสะอาดทุกครั้ง | ใช่ | ไม่ ไฟล์จาก job ก่อนยังอยู่ |
| ดูแลระบบ | GitHub ดูแล | เราอัปเดต OS, Python และตัว runner เอง |
| เข้าถึงเครือข่ายภายใน / GPU | ไม่ได้ | ได้ |

เลิกใช้แล้วถอด runner ออก: Settings → Actions → Runners → คลิกชื่อ runner → **Remove** แล้วรันคำสั่ง `config remove` ที่หน้านั้นแสดง แล้วลบโฟลเดอร์ `actions-runner`

## สรุปหมวด 8

- [ ] runner ขึ้น Idle และรับงานสำเร็จ 1 ครั้ง
- [ ] เห็นไฟล์งานใน `_work` บนเครื่องตัวเอง
- [ ] ถอด runner ออกหลังใช้เสร็จ
