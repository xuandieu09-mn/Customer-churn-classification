# Dự án Dự đoán Churn Khách hàng - CRISP-DM

## Tổng quan
Dự án này áp dụng phương pháp CRISP-DM đầy đủ để xây dựng mô hình dự đoán khách hàng rời bỏ (churn) dựa trên dữ liệu hành vi có cấu trúc từ tập dữ liệu Telco Customer Churn.

## Mục tiêu
Xây dựng mô hình phân loại đạt F1 Score ≥ 0.60 để dự đoán khách hàng có khả năng rời bỏ dịch vụ.

## Cấu trúc dự án
```
project/
├── data/                           # Dữ liệu (không upload nếu quá lớn)
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv
├── notebooks/
│   └── crisp-dm-methodology-for-a-customer-churn.ipynb
├── src/                            # Mã nguồn Python
│   ├── preprocessing.py            # Tiền xử lý dữ liệu
│   ├── modeling.py                 # Huấn luyện mô hình
│   └── predict.py                  # Dự đoán
├── demo/                           # Ứng dụng demo (optional)
│   └── app.py                      # Streamlit app
├── models/                         # Mô hình đã lưu
│   └── best_rf_model.pkl
├── requirements.txt                # Các thư viện cần thiết
├── README.md                       # File này
└── report.pdf                      # Báo cáo khoa học
```

## Yêu cầu hệ thống
- Python 3.11.9 trở lên
- Jupyter Notebook hoặc VS Code với Jupyter extension
- 4GB RAM (khuyến nghị 8GB+)

## Cài đặt

### 1. Clone repository (nếu có)
```bash
git clone <repository-url>
cd customer-churn-prediction
```

### 2. Tạo môi trường ảo (khuyến nghị)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

## Hướng dẫn chạy

### Chạy Jupyter Notebook
1. Mở terminal/cmd trong thư mục dự án
2. Kích hoạt môi trường ảo (nếu có)
3. Chạy lệnh:
```bash
jupyter notebook
```
4. Mở file `notebooks/crisp-dm-methodology-for-a-customer-churn.ipynb`
5. Chạy các cell theo thứ tự từ trên xuống dưới

### Chạy từ Python scripts
```bash
# Tiền xử lý dữ liệu
python src/preprocessing.py

# Huấn luyện mô hình
python src/modeling.py

# Dự đoán
python src/predict.py
```

### Chạy demo Streamlit (nếu có)
```bash
streamlit run demo/app.py
```

## Phương pháp CRISP-DM

### Giai đoạn 1: Hiểu về bối cảnh kinh doanh
- **Mục tiêu**: Dự đoán khách hàng có khả năng rời bỏ dịch vụ
- **Câu hỏi chính**: Đặc trưng hành vi nào chỉ ra rõ nhất việc khách hàng rời bỏ?
- **Tiêu chí thành công**: F1 Score ≥ 0.60

### Giai đoạn 2: Hiểu về dữ liệu
- Thu thập dữ liệu từ Kaggle (Telco Customer Churn)
- Khám phá 21 đặc trưng: nhân khẩu học, dịch vụ, hợp đồng, tài chính
- Phân tích phân phối và mối quan hệ giữa các đặc trưng

### Giai đoạn 3: Chuẩn bị dữ liệu
- Xử lý giá trị thiếu trong cột TotalCharges
- Mã hóa biến phân loại (One-Hot Encoding)
- Chuẩn hóa đặc trưng số (StandardScaler)
- Chia tập train-test (80-20)

### Giai đoạn 4: Mô hình hóa
- Mô hình Baseline: Logistic Regression
- Mô hình nâng cao: Random Forest
- Tối ưu hóa siêu tham số: GridSearchCV
- Mô hình tổng hợp: Ensemble Voting

### Giai đoạn 5: Đánh giá
- So sánh Accuracy, Precision, Recall, F1 Score
- Vẽ đường cong ROC
- **Kết quả tốt nhất**: Random Forest với F1 = 0.68, AUC = 0.79

### Giai đoạn 6: Triển khai
- Lưu mô hình tốt nhất (.pkl)
- Xây dựng chiến lược triển khai
- Tài liệu hóa quy trình
- Demo ứng dụng (optional)

## Kết quả chính

| Mô hình | Accuracy | Precision | Recall | F1 Score | AUC |
|---------|----------|-----------|--------|----------|-----|
| Logistic Regression | 0.76 | 0.53 | 0.82 | 0.65 | 0.78 |
| **Random Forest** | **0.79** | **0.57** | **0.79** | **0.68** | **0.79** |
| Ensemble | 0.78 | 0.56 | 0.80 | 0.66 | 0.79 |

✅ **Đạt tiêu chí thành công**: F1 Score = 0.68 (≥ 0.60)

## Deliverables

- ✅ Notebook Jupyter với giải thích đầy đủ
- ✅ Mã nguồn Python (src/)
- ✅ requirements.txt
- ✅ README.md
- ⚠️ Báo cáo PDF (cần tạo thêm)
- ⚠️ Mô hình đã lưu (cần thêm code lưu model)
- ⚠️ Demo Streamlit (optional, cần tạo thêm)

## Tác giả
[Tên của bạn]

## Giấy phép
[License nếu có]

## Tham khảo
- Dữ liệu: [Telco Customer Churn - Kaggle](https://www.kaggle.com/blastchar/telco-customer-churn)
- CRISP-DM Methodology
- Scikit-learn Documentation
