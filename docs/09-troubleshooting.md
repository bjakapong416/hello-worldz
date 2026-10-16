# หมวด 9 · แก้ปัญหาและแบบฝึกหัด

เมื่อ CI แดง ให้เปิด log ของ step ที่เป็นกากบาทแดงเสมอ บรรทัดก่อน `Error: Process completed with exit code 1` มักบอกสาเหตุจริง แล้วลองรันคำสั่งเดียวกันบนเครื่องตัวเอง

## ตารางแก้ปัญหา

| หมวด | อาการ | สาเหตุ | วิธีแก้ |
| --- | --- | --- | --- |
| 1 | `running scripts is disabled` ตอน activate | PowerShell บล็อก script | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| 1 | `python` ไม่พบคำสั่ง | ไม่ได้ติ๊ก Add to PATH / macOS ใช้ `python3` | ติดตั้งใหม่แล้วติ๊ก PATH หรือใช้ `python3` |
| 2 | `ModuleNotFoundError: No module named 'grades'` | ไม่มี `pythonpath = ["."]` ใน `pyproject.toml` | เพิ่มตามหมวด 1 ขั้นที่ 3 |
| 2 | `collected 0 items` | ชื่อไฟล์/ฟังก์ชันไม่ขึ้นต้นด้วย `test_` | ตั้งชื่อ `test_*.py` และ `def test_...` |
| 2 | `UnicodeEncodeError: 'charmap' codec` | print ภาษาไทยบน terminal Windows | print เป็นอังกฤษ หรือตั้ง `$env:PYTHONUTF8 = "1"` |
| 2 | coverage ไม่ถึง 80% | มีบรรทัดที่ไม่มี test เรียก | ดูคอลัมน์ `Missing` แล้วเขียน test เพิ่ม |
| 3 | แท็บ Actions ว่างเปล่า | ชื่อโฟลเดอร์ผิด หรือ branch ไม่ใช่ `main` | ต้องเป็น `.github/workflows/` ตรงตัว ตรวจด้วย `git branch` |
| 3 | `Invalid workflow file` | YAML ย่อหน้าผิด หรือใช้ Tab | ใช้ space 2 ช่อง `uses:` กับ `with:` ต้องตรงคอลัมน์เดียวกัน |
| 3 | test ผ่านบนเครื่อง แต่พังบน GitHub | ลืม commit ไฟล์ หรือลืมใส่ library ใน `requirements-dev.txt` | `git status` ดูไฟล์ที่ยังไม่ commit |
| 3 | Python ผิดเวอร์ชัน (เช่นได้ 3.1) | ไม่ใส่เครื่องหมายคำพูดที่ `python-version` | เขียน `"3.13"` เสมอ |
| 4 | deploy error: `Get Pages site failed` / 404 | ยังไม่ตั้ง Pages Source | Settings → Pages → Source: GitHub Actions แล้วกด **Re-run jobs** |
| 4 | deploy error เรื่อง permission / id-token | ขาด `permissions:` | ต้องมี `pages: write` และ `id-token: write` |
| 4 | เว็บไม่เปลี่ยนหลัง deploy เขียว | Browser cache | `Ctrl+Shift+R` หรือเปิดแท็บไม่ระบุตัวตน |
| 4 | `upload-pages-artifact` หาไฟล์ไม่เจอ | ลืม step `python build_site.py` หรือ `path` ไม่ตรง | ต้อง build ก่อน upload และ `path: _site` |
| 5 | PR ค้าง "Waiting for status to be reported" | ชื่อ check ใน Branch protection ไม่ตรงชื่อ job (มักเกิดหลังใช้ matrix) | แก้ชื่อเป็น `test (3.13)` ฯลฯ |
| 5 | ยัง push ตรงเข้า `main` ได้ | เจ้าของ repo ข้ามกฎได้ | ติ๊ก **Do not allow bypassing the above settings** |
| 5 | `git push` ถูก rejected | บน GitHub มี commit ที่เครื่องเรายังไม่มี (เช่นหลัง merge PR) | `git pull` ก่อน แล้ว push ใหม่ |
| 6 | หัวข้อเว็บไม่เปลี่ยนตาม Variable | สร้างในแท็บ Secrets แทน Variables หรือชื่อไม่ตรง | เทียบชื่อทีละตัว GitHub ไม่แจ้ง error เมื่อหาชื่อไม่เจอ |
| 6 | `KeyError: 'API_KEY'` | ไม่ได้ใส่ `env:` ใน step นั้น | `env:` ต้องอยู่ใน step เดียวกับ `run:` ที่ใช้ค่า |
| 8 | job ค้าง Queued | runner ออฟไลน์ หรือ label ไม่ตรง | เปิด `run` ใหม่ เทียบ label กับ `runs-on` |

## Checklist รวม

- [ ] หมวด 1: โปรเจกต์พร้อม, venv ทำงาน
- [ ] หมวด 2: `pytest` ผ่าน 18 ตัว, coverage เกิน 80%
- [ ] หมวด 3: CI เขียวบน GitHub
- [ ] หมวด 4: เว็บขึ้น และข้อมูลผิดไม่ถูก deploy
- [ ] หมวด 5: PR ที่ test พัง merge ไม่ได้
- [ ] หมวด 6: หัวข้อเว็บมาจาก Variable
- [ ] หมวด 7: test 3 เวอร์ชัน Python
- [ ] หมวด 8: runner บนเครื่องตัวเองรับงานได้

## คำถามทบทวน

1. ถ้าเพิ่มไฟล์ `tests/test_report.py` ใหม่ ต้องแก้ ci.yml ไหม เพราะอะไร
2. GitHub รู้ได้อย่างไรว่า step `pytest` ผ่านหรือไม่ผ่าน
3. บรรทัดไหนใน ci.yml ที่ทำให้เว็บไม่ถูก deploy เมื่อ test พัง
4. ทำไมต้อง test คะแนน 80 และ 79 ทั้งคู่ ทั้งที่ test 65 ก็ผ่านแล้ว
5. ทำไมไม่ commit โฟลเดอร์ `_site` และ `.venv` ขึ้น repo
6. Secret กับ Variable ต่างกันอย่างไร ยกตัวอย่างค่าที่ควรเก็บแบบละ 2 อย่าง
7. Matrix `os: [ubuntu-latest, windows-latest, macos-latest]` กับ `python-version: ["3.12", "3.13"]` ได้กี่ job
8. ทำไมไม่ควรใช้ self-hosted runner กับ public repo

## แบบฝึกหัด (เรียงจากง่ายไปยาก)

1. **เกรดบวก** — แก้ `grade()` ให้มี B+ (75–79) และ C+ (65–69) เขียน test ค่าขอบให้ครบก่อนแก้โค้ด เปิด PR ให้เห็นแดงก่อน แล้วค่อยทำให้เขียว (Test-Driven Development)
2. **สถิติบนเว็บ** — เพิ่มคะแนนสูงสุด ต่ำสุด และ `pass_rate` ลงหน้าเว็บ พร้อม test ใน `test_build_site.py`
3. **ตรวจข้อมูลเข้มขึ้น** — เพิ่ม test ที่ทำให้ CI แดงเมื่อ CSV มีชื่อซ้ำกัน หรือชื่อว่าง
4. **รายงาน coverage เป็นไฟล์** — เพิ่ม `--cov-report=html` แล้วใช้ `actions/upload-artifact@v4` เก็บโฟลเดอร์ `htmlcov` ไว้ดาวน์โหลดจากหน้า workflow run

## เอกสารอ้างอิง

[pytest](https://docs.pytest.org/) · [pytest-cov](https://pytest-cov.readthedocs.io/) · [Ruff](https://docs.astral.sh/ruff/) · [setup-python](https://github.com/actions/setup-python) · [Workflow syntax](https://docs.github.com/actions/reference/workflows-and-actions/workflow-syntax) · [Secrets](https://docs.github.com/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) · [Self-hosted runners](https://docs.github.com/actions/hosting-your-own-runners)
