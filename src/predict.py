"""
Module dự đoán cho dự án Customer Churn
Áp dụng theo CRISP-DM Phase 6: Deployment
"""

import pandas as pd
import numpy as np
import pickle


def load_model_and_scaler(model_path, scaler_path, feature_cols_path=None):
    """
    Tải mô hình, scaler và danh sách feature columns
    
    Args:
        model_path: Đường dẫn đến file mô hình .pkl
        scaler_path: Đường dẫn đến file scaler .pkl
        feature_cols_path: Đường dẫn đến file feature_columns.pkl
        
    Returns:
        tuple: (model, scaler, feature_columns)
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    feature_columns = None
    if feature_cols_path:
        try:
            with open(feature_cols_path, 'rb') as f:
                feature_columns = pickle.load(f)
        except FileNotFoundError:
            print("⚠️  Không tìm thấy file feature_columns.pkl")
    
    print("✅ Đã tải mô hình và scaler thành công")
    return model, scaler, feature_columns


def preprocess_input(data, scaler, feature_columns=None):
    """
    Tiền xử lý dữ liệu đầu vào để dự đoán
    
    Args:
        data: DataFrame hoặc dictionary chứa dữ liệu khách hàng
        scaler: Scaler đã fit từ tập huấn luyện
        feature_columns: Danh sách tên cột từ lúc train (để align)
        
    Returns:
        pd.DataFrame: Dữ liệu đã xử lý sẵn sàng cho dự đoán
    """
    if isinstance(data, dict):
        data = pd.DataFrame([data])
    
    # Xử lý TotalCharges
    if 'TotalCharges' in data.columns:
        data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
        data['TotalCharges'].fillna(0, inplace=True)
    
    # Xóa customerID nếu có
    if 'customerID' in data.columns:
        data = data.drop('customerID', axis=1)
    
    # Chuẩn hóa các cột số TRƯỚC KHI One-Hot Encoding (quan trọng!)
    # Scaler được fit với 3 cột: tenure, MonthlyCharges, TotalCharges
    numeric_cols_to_scale = ['tenure', 'MonthlyCharges', 'TotalCharges']
    if all(col in data.columns for col in numeric_cols_to_scale):
        data[numeric_cols_to_scale] = scaler.transform(data[numeric_cols_to_scale])
    
    # One-Hot Encoding SAU KHI đã scale
    data = pd.get_dummies(data, drop_first=True)
    
    # Align columns với training data
    if feature_columns is not None:
        # Thêm các cột thiếu với giá trị 0
        for col in feature_columns:
            if col not in data.columns:
                data[col] = 0
        
        # Giữ lại và sắp xếp theo đúng thứ tự các cột từ training
        data = data[feature_columns]
    
    return data


def predict_churn(model, scaler, customer_data, feature_columns=None):
    """
    Dự đoán khả năng churn cho khách hàng
    
    Args:
        model: Mô hình đã huấn luyện
        scaler: Scaler để chuẩn hóa dữ liệu
        customer_data: Dữ liệu khách hàng (dict hoặc DataFrame)
        feature_columns: Danh sách tên cột từ lúc train
        
    Returns:
        dict: Kết quả dự đoán {prediction, probability}
    """
    # Tiền xử lý
    X = preprocess_input(customer_data, scaler, feature_columns)
    
    # Dự đoán
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    
    result = {
        'prediction': 'Churn' if prediction == 1 else 'No Churn',
        'churn_probability': probability[1],
        'no_churn_probability': probability[0]
    }
    
    return result


def predict_batch(model, scaler, filepath, feature_columns=None):
    """
    Dự đoán hàng loạt từ file CSV
    
    Args:
        model: Mô hình đã huấn luyện
        scaler: Scaler để chuẩn hóa
        filepath: Đường dẫn file CSV chứa dữ liệu khách hàng
        feature_columns: Danh sách tên cột từ lúc train
        
    Returns:
        pd.DataFrame: DataFrame kết quả với cột dự đoán và xác suất
    """
    # Tải dữ liệu
    df = pd.read_csv(filepath)
    
    # Lưu customerID nếu có
    customer_ids = df['customerID'] if 'customerID' in df.columns else None
    
    # Tiền xử lý
    X = preprocess_input(df.copy(), scaler, feature_columns)
    
    # Dự đoán
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]
    
    # Tạo DataFrame kết quả
    results = pd.DataFrame({
        'customerID': customer_ids,
        'prediction': ['Churn' if p == 1 else 'No Churn' for p in predictions],
        'churn_probability': probabilities
    })
    
    return results


def display_prediction(result):
    """
    Hiển thị kết quả dự đoán đẹp mắt
    
    Args:
        result: Dictionary kết quả từ predict_churn()
    """
    print("\n" + "="*50)
    print("🔮 KẾT QUẢ DỰ ĐOÁN CHURN")
    print("="*50)
    print(f"Kết luận: {result['prediction']}")
    print(f"Xác suất Churn: {result['churn_probability']:.2%}")
    print(f"Xác suất No Churn: {result['no_churn_probability']:.2%}")
    print("="*50)
    
    if result['churn_probability'] > 0.7:
        print("⚠️  Cảnh báo: Khả năng rời bỏ CAO - Cần can thiệp ngay!")
    elif result['churn_probability'] > 0.5:
        print("⚡ Cảnh báo: Khả năng rời bỏ TRUNG BÌNH - Theo dõi sát")
    else:
        print("✅ An toàn: Khả năng rời bỏ THẤP")


if __name__ == "__main__":
    # Ví dụ 1: Dự đoán cho 1 khách hàng
    print("📌 Ví dụ 1: Dự đoán cho 1 khách hàng\n")
    
    model, scaler, feature_columns = load_model_and_scaler(
        "../models/best_rf_model.pkl",
        "../models/scaler.pkl",
        "../models/feature_columns.pkl"
    )
    
    # Dữ liệu mẫu của 1 khách hàng
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
    
    result = predict_churn(model, scaler, customer, feature_columns)
    display_prediction(result)
    
    # Ví dụ 2: Dự đoán hàng loạt
    print("\n\n📌 Ví dụ 2: Dự đoán hàng loạt từ file CSV\n")
    
    try:
        batch_results = predict_batch(
            model, scaler, 
            "../WA_Fn-UseC_-Telco-Customer-Churn.csv",
            feature_columns
        )
        
        print(f"✅ Đã dự đoán cho {len(batch_results)} khách hàng")
        print("\n📊 10 kết quả đầu tiên:")
        print(batch_results.head(10))
        
        # Lưu kết quả
        batch_results.to_csv("../predictions.csv", index=False)
        print("\n✅ Đã lưu kết quả vào predictions.csv")
        
    except FileNotFoundError:
        print("⚠️  File dữ liệu không tìm thấy, bỏ qua ví dụ này")
