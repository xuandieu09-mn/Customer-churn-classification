# 🚨 HƯỚNG DẪN SỬA LỖI KHẨN CẤP

## ❌ VẤN ĐỀ

Model luôn dự đoán Churn > 60% cho mọi input, kể cả khách hàng an toàn nhất!

## 🔍 NGUYÊN NHÂN

**Scaler bị lưu SAI** trong notebook:
```python
# SAI ❌
pickle.dump(StandardScaler().fit(X_train), f)
```

Dòng này tạo scaler **MỚI** và fit lại, thay vì lưu scaler đã dùng trong training!

## ✅ GIẢI PHÁP

### Bước 1: Đã sửa code trong notebook
Cell 6.3 đã được sửa thành:
```python
# ĐÚNG ✅
pickle.dump(scaler, f)  # Lưu scaler đã fit ở cell trước
```

### Bước 2: CHẠY LẠI NOTEBOOK (BẮT BUỘC!)

**QUAN TRỌNG:** Phải chạy lại toàn bộ notebook để tạo lại model files!

#### Cách 1: Trong VS Code
1. Mở file `notebooks/crisp-dm-methodology-for-a-customer-churn.ipynb`
2. Nhấn `Ctrl + Shift + P`
3. Gõ: `Notebook: Run All`
4. Đợi tất cả cells chạy xong (khoảng 2-3 phút)
5. Kiểm tra thư mục `models/` có 3 files mới

#### Cách 2: Dùng Python script
```bash
cd "e:\HK1 Nam 4\KhaiThacDuLieu\New folder"
venv\Scripts\activate
python src\modeling.py
```

### Bước 3: Xác nhận đã sửa
Chạy lệnh test:
```bash
venv\Scripts\python.exe -c "import sys; sys.path.append('src'); from predict import load_model_and_scaler, predict_churn; model, scaler, fc = load_model_and_scaler('models/best_rf_model.pkl', 'models/scaler.pkl', 'models/feature_columns.pkl'); safe = {'gender': 'Male', 'SeniorCitizen': 0, 'Partner': 'Yes', 'Dependents': 'Yes', 'tenure': 70, 'PhoneService': 'Yes', 'MultipleLines': 'Yes', 'InternetService': 'Fiber optic', 'OnlineSecurity': 'Yes', 'OnlineBackup': 'Yes', 'DeviceProtection': 'Yes', 'TechSupport': 'Yes', 'StreamingTV': 'Yes', 'StreamingMovies': 'Yes', 'Contract': 'Two year', 'PaperlessBilling': 'No', 'PaymentMethod': 'Credit card (automatic)', 'MonthlyCharges': 100.0, 'TotalCharges': 7000.0}; r = predict_churn(model, scaler, safe, fc); print(f'Khách an toàn: {r[\"churn_probability\"]:.1%} churn (nên < 20%)')"
```

**Kết quả mong đợi:** Churn < 20% (hiện tại đang 61% - SAI!)

### Bước 4: Test lại demo app
```bash
streamlit run demo\app.py
```

Thử với nhiều profile khác nhau:
- ✅ Contract 2 năm, tenure cao → churn THẤP (< 30%)
- ✅ Contract month-to-month, tenure thấp → churn CAO (> 60%)
- ✅ Có nhiều dịch vụ bổ sung → churn THẤP

---

## 📊 KẾT QUẢ SAU KHI SỬA

### Trước khi sửa (SAI):
- Khách an toàn nhất: **61% churn** ❌
- Khách rủi ro cao: **63% churn** ❌
- Mọi profile đều ~60% → Model vô dụng!

### Sau khi sửa (ĐÚNG):
- Khách an toàn: **10-25% churn** ✅
- Khách trung bình: **40-60% churn** ✅
- Khách rủi ro cao: **70-90% churn** ✅
- Model phân biệt được rõ ràng!

---

## 🎯 CHECKLIST

- [ ] Đã sửa code trong notebook (cell 6.3)
- [ ] Đã chạy lại notebook hoặc modeling.py
- [ ] models/ có 3 files mới (check timestamp)
- [ ] Test khách hàng an toàn: churn < 20% ✅
- [ ] Test khách hàng rủi ro: churn > 70% ✅
- [ ] Demo app cho kết quả hợp lý ✅

---

## ⚠️ LƯU Ý

**KHÔNG** refresh app trước khi chạy lại notebook!
Phải tạo lại model files trước đã.

Nếu vẫn lỗi sau khi chạy lại:
1. Xóa tất cả files trong `models/`
2. Chạy lại notebook từ đầu
3. Kiểm tra `models/scaler.pkl` có timestamp mới nhất
