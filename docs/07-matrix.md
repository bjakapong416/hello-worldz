# หมวด 7 · Matrix: test หลายเวอร์ชันพร้อมกัน

**จบหมวดนี้:** job `test` แตกเป็นหลาย job ที่รันพร้อมกัน หนึ่ง job ต่อหนึ่งเวอร์ชัน Python · เวลา 15 นาที · ต้องทำ[หมวด 3](03-ci.md)ก่อน

**ทำไมต้องทำ?** เครื่องของเพื่อนในทีมหรือเซิร์ฟเวอร์จริงอาจใช้ Python คนละเวอร์ชัน ฟีเจอร์บางตัวมีเฉพาะเวอร์ชันใหม่ (เช่น `match` ต้อง 3.10 ขึ้นไป) Matrix เขียน job ครั้งเดียวแต่รู้ผลทุกเวอร์ชัน

## 7.1 แก้ job test

```yaml
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.12", "3.13", "3.14"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
          cache-dependency-path: requirements-dev.txt
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Lint
        run: ruff check .
      - name: Test
        run: pytest --cov=grades --cov=build_site --cov-report=term-missing --cov-fail-under=80
```

| บรรทัด | ความหมาย |
| --- | --- |
| `matrix: python-version: [...]` | สร้าง job 3 ตัว แต่ละตัวได้ค่าไม่เหมือนกัน ชื่อ `python-version` ตั้งเองได้ แต่ต้องตรงกับตอนเรียกใช้ |
| `${{ matrix.python-version }}` | ดึงค่าของ job นั้นมาใช้ |
| `"3.12"` (มีเครื่องหมายคำพูด) | **ห้ามลืม** — ไม่ใส่ YAML จะอ่านเป็นตัวเลข และ `3.10` กลายเป็น `3.1` ทันที |
| `fail-fast: false` | ค่าเริ่มต้นคือ `true` ซึ่งถ้าเวอร์ชันหนึ่งพังจะยกเลิกตัวอื่น ตั้งเป็น `false` เพื่อให้เห็นผลครบทุกเวอร์ชัน |

job `deploy` ที่มี `needs: test` ไม่ต้องแก้ มันจะรอให้**ทั้ง 3 ตัว**ผ่านก่อนเอง และยัง deploy แค่ครั้งเดียว

## 7.2 ดูผล

1. Push หรือเปิด PR
2. หน้า workflow run จะเห็น `test (3.12)`, `test (3.13)`, `test (3.14)` รันขนานกัน แล้วต่อด้วย `deploy`
3. คลิก step **Set up Python** ในแต่ละ job จะเห็นเวอร์ชันที่ติดตั้งจริง

**ระวัง: ชื่อ check เปลี่ยน** — ถ้าทำ[หมวด 5](05-pull-request.md)ไว้แล้ว ชื่อ check จะไม่ใช่ `test` อีกต่อไป PR จะค้างที่ "Expected — Waiting for status to be reported" ตลอดกาล ให้ไปที่ Settings → Branches → แก้ rule → ลบ `test` ออก แล้วเพิ่ม `test (3.12)`, `test (3.13)`, `test (3.14)` แทน

## 7.3 เพิ่มหลาย OS (ทางเลือก)

```yaml
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.12", "3.14"]
```

Matrix จะจับคู่ทุกแบบ 2 × 2 = 4 job จำนวน job โตเร็วมาก (3 OS × 3 เวอร์ชัน = 9 job) เลือกเฉพาะค่าที่จำเป็นจริง ตัดคู่ที่ไม่ต้องการได้ด้วย `exclude:`

```yaml
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.12", "3.14"]
        exclude:
          - os: windows-latest
            python-version: "3.12"
```

ทำไมควร test บน Windows ด้วย? เพราะ bug บางตัวเกิดเฉพาะ Windows เช่น เปิดไฟล์ภาษาไทยโดยไม่ระบุ `encoding="utf-8"` ซึ่งบน Linux ผ่านแต่บน Windows อ่านเป็นตัวอักษรเพี้ยนหรือ error (โค้ดในคู่มือนี้ระบุ `encoding="utf-8"` ทุกจุดแล้ว) runner Windows ใช้เวลาเริ่มนานกว่า Linux

## สรุปหมวด 7

- [ ] เห็น test รัน 3 เวอร์ชันพร้อมกัน
- [ ] deploy รอให้ทุกเวอร์ชันผ่านก่อน
- [ ] อัปเดตชื่อ check ใน Branch protection แล้ว (ถ้าทำหมวด 5)
