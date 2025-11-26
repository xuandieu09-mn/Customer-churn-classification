# Hướng dẫn tạo báo cáo PDF

## Cách 1: Xuất từ Jupyter Notebook (Khuyến nghị)

### Bước 1: Cài đặt các công cụ cần thiết
```bash
pip install nbconvert
pip install pandoc
```

**Windows - Cài Pandoc:**
1. Tải từ: https://github.com/jgm/pandoc/releases
2. Chạy file .msi và cài đặt
3. Hoặc dùng Chocolatey: `choco install pandoc`

**Linux:**
```bash
sudo apt-get install pandoc
sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic
```

### Bước 2: Xuất notebook ra PDF
```bash
# Cách 1: Qua HTML
jupyter nbconvert --to html crisp-dm-methodology-for-a-customer-churn.ipynb
# Sau đó mở file HTML và Print to PDF từ trình duyệt

# Cách 2: Trực tiếp ra PDF (cần LaTeX)
jupyter nbconvert --to pdf crisp-dm-methodology-for-a-customer-churn.ipynb

# Cách 3: Qua WebPDF (không cần LaTeX)
jupyter nbconvert --to webpdf crisp-dm-methodology-for-a-customer-churn.ipynb
```

### Bước 3: Kiểm tra file PDF
File sẽ được tạo tại cùng thư mục với notebook.

---

## Cách 2: Sử dụng VS Code (Đơn giản nhất)

### Bước 1: Mở notebook trong VS Code
1. Mở file `crisp-dm-methodology-for-a-customer-churn.ipynb`
2. Nhấn `Ctrl + Shift + P` (hoặc `Cmd + Shift + P` trên Mac)
3. Gõ: `Notebook: Export to...`
4. Chọn `PDF`

### Bước 2: Đợi VS Code xuất file
VS Code sẽ tự động xuất notebook ra PDF.

---

## Cách 3: Qua Google Colab (Nếu gặp lỗi trên local)

### Bước 1: Upload notebook lên Google Colab
1. Truy cập https://colab.research.google.com/
2. File → Upload notebook
3. Chọn file `crisp-dm-methodology-for-a-customer-churn.ipynb`

### Bước 2: Xuất PDF
1. File → Print
2. Chọn "Save as PDF"
3. Lưu file

---

## Cách 4: Tạo báo cáo Word rồi xuất PDF

```bash
# Xuất ra Word
jupyter nbconvert --to markdown crisp-dm-methodology-for-a-customer-churn.ipynb

# Mở file .md bằng Word/Google Docs và xuất PDF
```

---

## Lưu ý quan trọng

### Trước khi xuất PDF:

1. **Chạy lại toàn bộ notebook:**
   - `Kernel` → `Restart & Run All`
   - Đảm bảo tất cả cells chạy thành công

2. **Xóa output dài (nếu cần):**
   - Với cells có output quá dài, hãy clear output
   - Click chuột phải vào cell → `Clear Cell Output`

3. **Kiểm tra hình ảnh:**
   - Đảm bảo tất cả biểu đồ hiển thị đúng
   - Resize hình ảnh nếu quá lớn

4. **Sửa markdown formatting:**
   - Kiểm tra tiêu đề, danh sách
   - Đảm bảo không có code markdown lỗi

### Nếu gặp lỗi LaTeX:

**Lỗi:** `xelatex not found`
- **Giải pháp:** Dùng `--to webpdf` thay vì `--to pdf`

**Lỗi:** `! LaTeX Error: File 'adjustbox.sty' not found`
- **Giải pháp:** 
  ```bash
  # Windows - Cài MiKTeX
  choco install miktex
  
  # Linux
  sudo apt-get install texlive-latex-extra
  ```

**Lỗi:** PDF bị cắt ngang trang
- **Giải pháp:** Thêm config vào đầu notebook:
  ```python
  %%html
  <style>
  .container { width:100% !important; }
  </style>
  ```

---

## Cấu trúc báo cáo PDF nên có:

✅ **Trang bìa:**
- Tên đề tài
- Tên môn học
- Họ tên sinh viên
- MSSV
- Lớp
- Giảng viên

✅ **Mục lục** (tự động tạo nếu dùng LaTeX)

✅ **Nội dung chính:**
- 6 giai đoạn CRISP-DM
- Code + giải thích
- Biểu đồ và bảng kết quả

✅ **Kết luận và khuyến nghị**

✅ **Tài liệu tham khảo**

---

## Tip: Tạo trang bìa riêng

Tạo file `cover.md`:

```markdown
---
title: "Dự án Dự đoán Customer Churn"
subtitle: "Áp dụng phương pháp CRISP-DM"
author: "Họ tên sinh viên - MSSV"
date: "2024"
---

# Thông tin đề tài

**Môn học:** Khai thác dữ liệu

**Giảng viên:** [Tên giảng viên]

**Lớp:** [Tên lớp]

**Sinh viên thực hiện:**
- Họ tên: [Tên bạn]
- MSSV: [MSSV]

**Thời gian:** Học kỳ 1 - Năm 4

---
```

Rồi merge với notebook:
```bash
pandoc cover.md crisp-dm-methodology-for-a-customer-churn.md -o report.pdf
```

---

## Checklist trước khi nộp báo cáo

- [ ] Tất cả cells đã chạy thành công
- [ ] Có đầy đủ 6 giai đoạn CRISP-DM
- [ ] Code có comment tiếng Việt rõ ràng
- [ ] Biểu đồ hiển thị đẹp, có title và label
- [ ] Có trang bìa với thông tin đầy đủ
- [ ] Kết quả metrics đạt yêu cầu (F1 ≥ 0.60)
- [ ] Có phần kết luận và khuyến nghị
- [ ] File PDF dưới 50MB (nén hình nếu cần)
- [ ] Không có lỗi LaTeX/formatting

---

**Chúc bạn thành công! 🎉**
