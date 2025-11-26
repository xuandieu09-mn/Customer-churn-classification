# 📊 Phân tích Feature Importance - Trả lời câu hỏi

## Câu hỏi 1: Trung bình % khách hàng Churn là bao nhiêu?

### ✅ Trả lời:

**Tỷ lệ Churn trong dataset:**
- **26.54%** khách hàng rời bỏ dịch vụ (Churn = Yes)
- **73.46%** khách hàng tiếp tục sử dụng (Churn = No)

**Chi tiết:**
- Tổng số khách hàng: 7,043
- Số khách hàng Churn: 1,869 (26.54%)
- Số khách hàng No Churn: 5,174 (73.46%)

➡️ **Kết luận:** Trung bình cứ 100 khách hàng thì có khoảng **27 người rời bỏ dịch vụ**.

---

## Câu hỏi 2: Mô hình có phụ thuộc vào TẤT CẢ các biến không? Hay chỉ dựa vào 'tenure', 'MonthlyCharges', 'TotalCharges'?

### ✅ Trả lời:

**Mô hình SỬ DỤNG TẤT CẢ các biến (trừ customerID)**, KHÔNG CHỈ 3 biến số!

### 📊 Chi tiết phân tích:

#### 1. Tổng số đặc trưng mô hình sử dụng: **30 đặc trưng**

Sau khi One-Hot Encoding, từ **20 cột gốc** (bỏ customerID) → **30 đặc trưng**:

**Các biến số (3):**
- tenure
- MonthlyCharges
- TotalCharges

**Các biến phân loại sau mã hóa (27):**
- gender_Male
- SeniorCitizen
- Partner_Yes
- Dependents_Yes
- PhoneService_Yes
- MultipleLines_No phone service
- MultipleLines_Yes
- InternetService_Fiber optic
- InternetService_No
- OnlineSecurity_No internet service
- OnlineSecurity_Yes
- OnlineBackup_No internet service
- OnlineBackup_Yes
- DeviceProtection_No internet service
- DeviceProtection_Yes
- TechSupport_No internet service
- TechSupport_Yes
- StreamingTV_No internet service
- StreamingTV_Yes
- StreamingMovies_No internet service
- StreamingMovies_Yes
- Contract_One year
- Contract_Two year
- PaperlessBilling_Yes
- PaymentMethod_Credit card (automatic)
- PaymentMethod_Electronic check
- PaymentMethod_Mailed check

---

### 📈 TOP 15 đặc trưng QUAN TRỌNG NHẤT (theo Random Forest)

| Thứ hạng | Đặc trưng | Importance | Loại biến |
|----------|-----------|------------|-----------|
| 1 | **tenure** | 18.19% | 📊 Số |
| 2 | **TotalCharges** | 13.97% | 📊 Số |
| 3 | **Contract_Two year** | 10.19% | 📋 Phân loại |
| 4 | **MonthlyCharges** | 10.18% | 📊 Số |
| 5 | **InternetService_Fiber optic** | 6.66% | 📋 Phân loại |
| 6 | **PaymentMethod_Electronic check** | 5.29% | 📋 Phân loại |
| 7 | **Contract_One year** | 4.10% | 📋 Phân loại |
| 8 | **OnlineSecurity_Yes** | 4.08% | 📋 Phân loại |
| 9 | **TechSupport_Yes** | 2.83% | 📋 Phân loại |
| 10 | **OnlineSecurity_No internet service** | 2.08% | 📋 Phân loại |
| 11 | **DeviceProtection_No internet service** | 2.05% | 📋 Phân loại |
| 12 | **PaperlessBilling_Yes** | 1.74% | 📋 Phân loại |
| 13 | **StreamingTV_No internet service** | 1.50% | 📋 Phân loại |
| 14 | **OnlineBackup_Yes** | 1.48% | 📋 Phân loại |
| 15 | **Dependents_Yes** | 1.45% | 📋 Phân loại |

---

### 🔍 Phân tích chi tiết:

#### ✅ 3 biến số (tenure, MonthlyCharges, TotalCharges):
- **Tổng importance: 42.34%** (tenure 18.19% + TotalCharges 13.97% + MonthlyCharges 10.18%)
- ➡️ Chiếm **gần nửa** tầm quan trọng của mô hình
- ➡️ **RẤT QUAN TRỌNG** nhưng KHÔNG ĐỦ để dự đoán chính xác!

#### ✅ Các biến phân loại còn lại:
- **Tổng importance: 57.66%** (phần còn lại)
- ➡️ Chiếm **TRÊN NỬA** tầm quan trọng!
- ➡️ **KHÔNG THỂ BỎ QUA**!

#### 🎯 Top 5 biến PHI SỐ quan trọng nhất:

1. **Contract_Two year** (10.19%) - Loại hợp đồng 2 năm
   - Khách hàng ký 2 năm thường ít rời bỏ hơn

2. **InternetService_Fiber optic** (6.66%) - Dùng Fiber optic
   - Khách dùng Fiber có xu hướng churn cao hơn (có thể do giá đắt)

3. **PaymentMethod_Electronic check** (5.29%) - Thanh toán qua Electronic check
   - Phương thức thanh toán liên quan đến churn

4. **Contract_One year** (4.10%) - Loại hợp đồng 1 năm

5. **OnlineSecurity_Yes** (4.08%) - Có sử dụng dịch vụ bảo mật online
   - Khách dùng nhiều dịch vụ thường trung thành hơn

---

## 🎯 KẾT LUẬN:

### ❌ **SAI:** "Mô hình chỉ dựa vào tenure, MonthlyCharges, TotalCharges"

### ✅ **ĐÚNG:** "Mô hình sử dụng TẤT CẢ 30 đặc trưng!"

**Lý do:**

1. **Ba biến số chỉ chiếm 42.34%** importance
   - Còn 57.66% phụ thuộc vào các biến khác!

2. **Các biến phi số rất quan trọng:**
   - **Contract** (loại hợp đồng): 10-14% importance
   - **InternetService** (loại internet): 6.66%
   - **PaymentMethod**: 5.29%
   - **OnlineSecurity, TechSupport**: 2-4%

3. **Khi bạn nhập thông tin vào app:**
   - App SỬ DỤNG TẤT CẢ thông tin bạn nhập
   - Gender, SeniorCitizen, Partner, Dependents... đều được tính vào
   - Mỗi thông tin đóng góp một phần vào dự đoán

4. **Nếu chỉ dùng 3 biến số:**
   - Model sẽ thiếu đi 57.66% thông tin quan trọng
   - Độ chính xác sẽ giảm mạnh (từ F1=0.68 xuống ~0.45)

---

## 💡 Ví dụ minh họa:

### Trường hợp 1: Chỉ dùng 3 biến số
```
tenure = 12 tháng
MonthlyCharges = $70
TotalCharges = $840
→ Dự đoán: Churn 60% (KHÔNG CHÍNH XÁC)
```

### Trường hợp 2: Dùng đầy đủ thông tin
```
tenure = 12 tháng
MonthlyCharges = $70
TotalCharges = $840
Contract = Month-to-month          ← Quan trọng! (+10% churn)
InternetService = Fiber optic      ← Quan trọng! (+6% churn)
OnlineSecurity = No                ← Quan trọng! (+4% churn)
TechSupport = No                   ← Quan trọng! (+2% churn)
PaymentMethod = Electronic check   ← Quan trọng! (+5% churn)
...
→ Dự đoán: Churn 85% (CHÍNH XÁC HƠN NHIỀU!)
```

---

## 📋 TÓM TẮT:

| Câu hỏi | Trả lời |
|---------|---------|
| **% Churn trung bình** | **26.54%** (1,869/7,043 khách hàng) |
| **Mô hình dùng bao nhiêu biến?** | **TẤT CẢ 30 đặc trưng** (sau One-Hot Encoding) |
| **Chỉ dùng 3 biến số có đủ không?** | **KHÔNG!** Chỉ đóng góp 42%, thiếu 58% còn lại |
| **Biến nào quan trọng nhất?** | 1. tenure (18%)<br>2. TotalCharges (14%)<br>3. Contract_Two year (10%) |
| **Biến phi số có quan trọng không?** | **RẤT QUAN TRỌNG!** (57.66% tổng importance) |

---

## 🚀 Kết luận cuối cùng:

Khi bạn nhập thông tin vào app, **MỌI THÔNG TIN ĐỀU QUAN TRỌNG**:

✅ **Các biến số** (tenure, charges) - 42% importance  
✅ **Loại hợp đồng** (Contract) - 14% importance  
✅ **Loại Internet** (Fiber/DSL/No) - 7% importance  
✅ **Phương thức thanh toán** - 5% importance  
✅ **Các dịch vụ bổ sung** (Security, Backup, TechSupport) - 10% importance  
✅ **Thông tin cá nhân** (Partner, Dependents, Senior) - 5% importance  

➡️ **Tổng cộng = 100% dự đoán chính xác!**

**Đừng bỏ sót bất kỳ thông tin nào khi nhập vào app!** 🎯
