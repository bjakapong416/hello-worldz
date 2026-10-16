# หมวด 6 · Secrets และ Variables

**จบหมวดนี้:** เปลี่ยนหัวข้อเว็บจากหน้า Settings ได้โดยไม่แก้โค้ด และส่งรหัสลับให้ Python อ่านได้อย่างปลอดภัย · เวลา 20 นาที · ต้องทำ[หมวด 4](04-cd.md)ก่อน

**กฎที่ต้องจำ: ห้ามเขียนรหัสผ่านหรือ token ลงในโค้ด** repo เป็น Public ทุกคนอ่านได้ รวมถึงประวัติ commit ทั้งหมด ลบทีหลังก็ยังอยู่ใน git ถ้าเผลอ commit ไปแล้วให้เปลี่ยนรหัสนั้นทันที

## 6.1 Secret กับ Variable ต่างกันอย่างไร

| | Variable | Secret |
| --- | --- | --- |
| ใช้เก็บ | ค่าตั้งค่าที่ไม่ลับ เช่น ชื่อเว็บ, URL | รหัสผ่าน, API key, token |
| เรียกใน ci.yml | `${{ vars.ชื่อ }}` | `${{ secrets.ชื่อ }}` |
| ดูค่าย้อนหลังใน Settings | ได้ | ไม่ได้ (แก้ได้อย่างเดียว) |
| แสดงใน log | แสดงตามปกติ | ถูกปิดเป็น `***` อัตโนมัติ |
| PR จาก fork ของคนอื่น | อ่านได้ | อ่านไม่ได้ (ป้องกันการขโมย) |

## 6.2 สร้างค่าบน GitHub

1. repo → **Settings** → **Secrets and variables** → **Actions**
2. แท็บ **Variables** → **New repository variable** → Name `SITE_TITLE`, Value `ผลคะแนนกลางภาค 2/2569` → **Add variable**
3. แท็บ **Secrets** → **New repository secret** → Name `DEMO_API_KEY`, Secret `abc123-test-key` → **Add secret**

ชื่อใช้ได้เฉพาะ A–Z, 0–9 และ `_` ห้ามขึ้นต้นด้วย `GITHUB_`

## 6.3 ส่งค่าเข้า Python ด้วย env

GitHub ส่งค่าให้โปรแกรมผ่าน **environment variable** และ Python อ่านด้วย `os.environ` แก้ job `deploy` ใน ci.yml เฉพาะ step Build site และเพิ่ม step ใหม่ 1 step

```yaml
      - name: Build site
        env:
          SITE_TITLE: ${{ vars.SITE_TITLE }}
        run: python build_site.py

      - name: Check secret
        env:
          API_KEY: ${{ secrets.DEMO_API_KEY }}
        run: |
          echo "secret value: $API_KEY"
          python -c "import os; print('API_KEY length:', len(os.environ['API_KEY']))"
```

ฝั่ง Python ไม่ต้องแก้เลย เพราะ `build_site.py` มีบรรทัดนี้อยู่แล้วตั้งแต่[หมวด 2](02-pytest.md)

```python
title = os.environ.get("SITE_TITLE") or "ผลคะแนนวิชา CI/CD"
```

| ส่วน | ความหมาย |
| --- | --- |
| `env: SITE_TITLE: ${{ vars.SITE_TITLE }}` | สร้าง environment variable ชื่อ `SITE_TITLE` ให้ step นี้ ค่ามาจาก Variable ที่สร้างใน 6.2 |
| `os.environ.get("SITE_TITLE")` | Python อ่านค่านั้น ถ้าไม่มีได้ `None` |
| `or "..."` | ถ้าไม่มีหรือเป็นค่าว่าง ใช้ค่าเริ่มต้น (ถ้าลืมสร้าง Variable GitHub จะส่งค่าว่างมา ไม่ใช่ error) |
| `os.environ['API_KEY']` | อ่านแบบบังคับต้องมี ถ้าไม่มีจะ `KeyError` ทันที เหมาะกับค่าที่ขาดไม่ได้ เช่น token |
| `len(...)` | พิมพ์แค่ความยาว เพื่อเช็กว่าได้ค่าจริงโดยไม่เปิดเผยค่า |

## 6.4 ดูผล

1. Push → เปิด log ของ job `deploy` → step **Check secret** จะเห็น `secret value: ***` และ `API_KEY length: 15` — GitHub ปิดค่าให้เองแม้เราสั่ง echo
2. เปิดเว็บ หัวข้อเปลี่ยนเป็น "ผลคะแนนกลางภาค 2/2569"
3. แก้ค่า `SITE_TITLE` ใน Settings → แท็บ Actions → เลือก workflow CI/CD → **Run workflow** เว็บเปลี่ยนหัวข้อโดยไม่ต้อง commit อะไรเลย

การปิด `***` ไม่ใช่กำแพงที่สมบูรณ์ ถ้าแปลงค่าก่อนพิมพ์ (เช่น กลับด้านหน้าหลัง) ค่าจริงจะหลุดใน log ได้ งานจริงห้าม echo หรือ print secret ตัวอย่างนี้ทำเพื่อให้เห็นการปิดค่าเท่านั้น เสร็จแล้วควรลบ step Check secret ออก

## 6.5 ลองบนเครื่องตัวเอง

ตั้ง environment variable ชั่วคราวแล้วรัน เหมือนที่ GitHub ทำให้

```powershell
# Windows (PowerShell)
$env:SITE_TITLE = "ทดสอบบนเครื่อง"
python build_site.py
```

```bash
# macOS / Linux
SITE_TITLE="ทดสอบบนเครื่อง" python3 build_site.py
```

เปิด `_site/index.html` จะเห็นหัวข้อใหม่ test `test_main_builds_site` ในหมวด 2 ทดสอบเรื่องนี้ไว้แล้วด้วย `monkeypatch.setenv`

## สรุปหมวด 6

- [ ] เปลี่ยนหัวข้อเว็บจาก Variable ได้
- [ ] เห็น Secret ถูกปิดเป็น `***` ใน log
- [ ] ลบ step Check secret ออกหลังทดลอง
