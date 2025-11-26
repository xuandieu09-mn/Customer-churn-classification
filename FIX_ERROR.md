# 🔧 Hướng dẫn sửa lỗi và chạy lại

## ✅ Đã sửa lỗi: Feature names mismatch

### Vấn đề
Khi chạy demo app và nhập thông tin khách hàng, gặp lỗi:
```
❌ Lỗi khi dự đoán: The feature names should match those that were passed during fit.
```

### Nguyên nhân
- Khi huấn luyện model, dữ liệu có đầy đủ các cột từ `pd.get_dummies()`
- Khi dự đoán với 1 khách hàng mới, một số cột bị thiếu (vì không có tất cả giá trị categorical)
- Ví dụ: Nếu khách hàng có `Contract='Month-to-month'`, thì `Contract_One year` và `Contract_Two year` sẽ không xuất hiện

### Giải pháp
✅ **Đã sửa** bằng cách:
1. Lưu thêm `feature_columns.pkl` - danh sách tên cột từ lúc huấn luyện
2. Khi dự đoán: align columns để khớp với training data
3. Thêm cột thiếu với giá trị 0
4. Sắp xếp đúng thứ tự cột

---

## 📋 Các bước để chạy lại

### Bước 1: Chạy lại notebook để tạo model mới
```bash
# Mở notebook trong VS Code hoặc Jupyter
# Kernel → Restart & Run All
```

Hoặc chạy trực tiếp từ Python:
```bash
python src/modeling.py
```

Sau khi chạy xong, kiểm tra thư mục `models/` phải có **3 files**:
- ✅ `best_rf_model.pkl` - Mô hình Random Forest
- ✅ `scaler.pkl` - StandardScaler
- ✅ `feature_columns.pkl` - Danh sách tên cột (**MỚI**)

### Bước 2: Chạy lại demo app
```bash
streamlit run demo/app.py
```

### Bước 3: Test dự đoán
1. Nhập thông tin khách hàng vào form
2. Nhấn nút "🔮 Dự đoán Churn"
3. Kiểm tra kết quả hiển thị đúng (không còn lỗi)

---

## 🧪 Test nhanh bằng Python

Tạo file test `test_prediction.py`:

```python
import sys
sys.path.append('src')

from predict import load_model_and_scaler, predict_churn

# Load model
model, scaler, feature_columns = load_model_and_scaler(
    'models/best_rf_model.pkl',
    'models/scaler.pkl',
    'models/feature_columns.pkl'
)

# Test data
customer = {
    'gender': 'Female',
    'SeniorCitizen': 0,
    'Partner': 'Yes',
    'Dependents': 'No',
    'tenure': 12,
    'PhoneService': 'Yes',
    'MultipleLines': 'No',
    'InternetService': 'Fiber optic',
    'OnlineSecurity': 'No',
    'OnlineBackup': 'No',
    'DeviceProtection': 'No',
    'TechSupport': 'No',
    'StreamingTV': 'Yes',
    'StreamingMovies': 'No',
    'Contract': 'Month-to-month',
    'PaperlessBilling': 'Yes',
    'PaymentMethod': 'Electronic check',
    'MonthlyCharges': 70.35,
    'TotalCharges': 844.2
}

# Dự đoán
result = predict_churn(model, scaler, customer, feature_columns)
print(f"\n✅ Kết quả: {result['prediction']}")
print(f"📊 Xác suất Churn: {result['churn_probability']:.2%}")
```

Chạy:
```bash
python test_prediction.py
```

Nếu chạy thành công không lỗi → Đã fix xong! ✅

---

## 🔍 Kiểm tra các file đã được cập nhật

### 1. `src/modeling.py`
- ✅ Thêm function `save_feature_columns()`
- ✅ Lưu `feature_columns.pkl` trong main

### 2. `src/predict.py`
- ✅ Cập nhật `load_model_and_scaler()` để load feature_columns
- ✅ Cập nhật `preprocess_input()` để align columns
- ✅ Cập nhật `predict_churn()` và `predict_batch()` để nhận feature_columns

### 3. `demo/app.py`
- ✅ Load `feature_columns.pkl`
- ✅ Pass feature_columns vào `predict_churn()`

### 4. `crisp-dm-methodology-for-a-customer-churn.ipynb`
- ✅ Cell 6.3 đã cập nhật để lưu `feature_columns.pkl`

---

## ⚠️ Lưu ý quan trọng

### Nếu vẫn gặp lỗi sau khi chạy lại:

**Lỗi 1:** `FileNotFoundError: feature_columns.pkl`
- **Nguyên nhân:** Chưa chạy lại notebook hoặc modeling.py
- **Giải pháp:** Chạy lại notebook từ đầu hoặc `python src/modeling.py`

**Lỗi 2:** `KeyError: 'Contract_One year'`
- **Nguyên nhân:** Vẫn dùng model cũ (không có feature_columns.pkl)
- **Giải pháp:** 
  1. Xóa tất cả file trong `models/`
  2. Chạy lại notebook từ đầu

**Lỗi 3:** Demo app không load được model
- **Nguyên nhân:** Đường dẫn sai hoặc file bị corrupt
- **Giải pháp:** Kiểm tra `models/` có đủ 3 files chưa

### Nếu muốn reset hoàn toàn:

```bash
# Xóa models cũ
del models\*.pkl

# Chạy lại từ đầu
python src/modeling.py

# Hoặc chạy notebook
jupyter notebook crisp-dm-methodology-for-a-customer-churn.ipynb
```

---

## 📊 Cấu trúc code sau khi sửa

```
Training (modeling.py):
1. Load data
2. Preprocess → get X_train với columns = [col1, col2, ..., colN]
3. Train model
4. Save:
   - model.pkl
   - scaler.pkl
   - feature_columns.pkl ← SAVE danh sách [col1, col2, ..., colN]

Prediction (predict.py):
1. Load:
   - model.pkl
   - scaler.pkl
   - feature_columns.pkl ← LOAD danh sách columns
2. Preprocess input data
3. Align columns:
   - Thêm cột thiếu = 0
   - Xóa cột thừa
   - Sắp xếp theo đúng thứ tự
4. Predict ✅
```

---

## ✅ Checklist sau khi sửa

- [ ] Chạy lại notebook/modeling.py thành công
- [ ] Thư mục `models/` có đủ 3 files (.pkl)
- [ ] Chạy `python src/predict.py` không lỗi
- [ ] Demo app chạy được và dự đoán thành công
- [ ] Test với nhiều input khác nhau đều OK

---

**Tóm lại:** Lỗi đã được sửa hoàn toàn. Chỉ cần chạy lại notebook/modeling.py để tạo file `feature_columns.pkl` là xong! 🎉
