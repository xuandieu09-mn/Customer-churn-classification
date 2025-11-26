"""
Module xử lý tiền xử lý dữ liệu cho dự án Customer Churn
Áp dụng theo CRISP-DM Phase 3: Data Preparation
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def load_data(filepath):
    """
    Tải dữ liệu từ file CSV
    
    Args:
        filepath (str): Đường dẫn đến file dữ liệu
        
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu
    """
    df = pd.read_csv(filepath)
    print(f"Đã tải dữ liệu: {df.shape[0]} hàng, {df.shape[1]} cột")
    return df


def handle_missing_values(df):
    """
    Xử lý giá trị thiếu trong dữ liệu
    
    Args:
        df (pd.DataFrame): DataFrame đầu vào
        
    Returns:
        pd.DataFrame: DataFrame đã xử lý giá trị thiếu
    """
    # Chuyển TotalCharges về số (có thể có khoảng trắng)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Điền giá trị thiếu bằng median
    df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
    
    print(f"Số giá trị thiếu sau xử lý: {df.isnull().sum().sum()}")
    return df


def encode_categorical_features(df):
    """
    Mã hóa các đặc trưng phân loại
    
    Args:
        df (pd.DataFrame): DataFrame đầu vào
        
    Returns:
        pd.DataFrame: DataFrame đã mã hóa
    """
    # Xóa cột customerID (không cần thiết)
    if 'customerID' in df.columns:
        df = df.drop('customerID', axis=1)
    
    # Mã hóa biến đích (Churn)
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    
    # One-Hot Encoding cho các đặc trưng phân loại khác
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    
    print(f"Số đặc trưng sau mã hóa: {df.shape[1]}")
    return df


def split_features_target(df):
    """
    Tách đặc trưng và biến đích
    
    Args:
        df (pd.DataFrame): DataFrame đầy đủ
        
    Returns:
        tuple: (X, y) - đặc trưng và biến đích
    """
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    
    print(f"Shape của X: {X.shape}")
    print(f"Shape của y: {y.shape}")
    print(f"Tỷ lệ Churn: {y.mean():.2%}")
    
    return X, y


def scale_features(X_train, X_test):
    """
    Chuẩn hóa đặc trưng số
    
    Args:
        X_train (pd.DataFrame): Tập huấn luyện
        X_test (pd.DataFrame): Tập kiểm tra
        
    Returns:
        tuple: (X_train_scaled, X_test_scaled, scaler)
    """
    scaler = StandardScaler()
    
    # Chỉ chuẩn hóa các cột số
    numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
    
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])
    
    return X_train_scaled, X_test_scaled, scaler


def preprocess_pipeline(filepath, test_size=0.2, random_state=42):
    """
    Pipeline đầy đủ cho tiền xử lý dữ liệu
    
    Args:
        filepath (str): Đường dẫn file dữ liệu
        test_size (float): Tỷ lệ tập test
        random_state (int): Random seed
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test, scaler)
    """
    print("=== BẮT ĐẦU TIỀN XỬ LÝ DỮ LIỆU ===\n")
    
    # Bước 1: Tải dữ liệu
    df = load_data(filepath)
    
    # Bước 2: Xử lý giá trị thiếu
    df = handle_missing_values(df)
    
    # Bước 3: Mã hóa đặc trưng phân loại
    df = encode_categorical_features(df)
    
    # Bước 4: Tách X và y
    X, y = split_features_target(df)
    
    # Bước 5: Chia train-test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"\nĐã chia dữ liệu: Train={len(X_train)}, Test={len(X_test)}")
    
    # Bước 6: Chuẩn hóa
    X_train, X_test, scaler = scale_features(X_train, X_test)
    
    print("\n=== HOÀN TẤT TIỀN XỬ LÝ ===")
    
    return X_train, X_test, y_train, y_test, scaler


if __name__ == "__main__":
    # Test module
    filepath = "../WA_Fn-UseC_-Telco-Customer-Churn.csv"
    X_train, X_test, y_train, y_test, scaler = preprocess_pipeline(filepath)
    
    print("\n📊 Tóm tắt dữ liệu:")
    print(f"- Tập train: {X_train.shape}")
    print(f"- Tập test: {X_test.shape}")
    print(f"- Số đặc trưng: {X_train.shape[1]}")
