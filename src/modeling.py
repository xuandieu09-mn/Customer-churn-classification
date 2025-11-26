"""
Module huấn luyện mô hình cho dự án Customer Churn
Áp dụng theo CRISP-DM Phase 4: Modeling và Phase 5: Evaluation
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, confusion_matrix, 
    classification_report, roc_curve
)
import pickle
import matplotlib.pyplot as plt
import seaborn as sns


def train_logistic_regression(X_train, y_train, max_iter=1000):
    """
    Huấn luyện mô hình Logistic Regression
    
    Args:
        X_train: Dữ liệu huấn luyện
        y_train: Nhãn huấn luyện
        max_iter: Số vòng lặp tối đa
        
    Returns:
        model: Mô hình đã huấn luyện
    """
    print("🔄 Đang huấn luyện Logistic Regression...")
    model = LogisticRegression(max_iter=max_iter, random_state=42)
    model.fit(X_train, y_train)
    print("✅ Hoàn tất huấn luyện Logistic Regression")
    return model


def train_random_forest(X_train, y_train, n_estimators=100):
    """
    Huấn luyện mô hình Random Forest
    
    Args:
        X_train: Dữ liệu huấn luyện
        y_train: Nhãn huấn luyện
        n_estimators: Số cây trong rừng
        
    Returns:
        model: Mô hình đã huấn luyện
    """
    print("🔄 Đang huấn luyện Random Forest...")
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    model.fit(X_train, y_train)
    print("✅ Hoàn tất huấn luyện Random Forest")
    return model


def optimize_random_forest(X_train, y_train):
    """
    Tối ưu hóa siêu tham số cho Random Forest bằng GridSearchCV
    
    Args:
        X_train: Dữ liệu huấn luyện
        y_train: Nhãn huấn luyện
        
    Returns:
        best_model: Mô hình tốt nhất sau tối ưu
    """
    print("🔄 Đang tối ưu hóa Random Forest với GridSearchCV...")
    
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10]
    }
    
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        rf, param_grid, cv=5, 
        scoring='f1', n_jobs=-1, verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"✅ Tham số tốt nhất: {grid_search.best_params_}")
    print(f"✅ F1 Score tốt nhất (CV): {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_


def train_ensemble(X_train, y_train, lr_model, rf_model):
    """
    Tạo mô hình Ensemble Voting từ Logistic Regression và Random Forest
    
    Args:
        X_train: Dữ liệu huấn luyện
        y_train: Nhãn huấn luyện
        lr_model: Mô hình Logistic Regression
        rf_model: Mô hình Random Forest
        
    Returns:
        ensemble_model: Mô hình Ensemble
    """
    print("🔄 Đang tạo Ensemble Voting Classifier...")
    
    ensemble = VotingClassifier(
        estimators=[('lr', lr_model), ('rf', rf_model)],
        voting='soft'
    )
    
    ensemble.fit(X_train, y_train)
    print("✅ Hoàn tất huấn luyện Ensemble")
    
    return ensemble


def evaluate_model(model, X_test, y_test, model_name="Model"):
    """
    Đánh giá mô hình và in ra các metrics
    
    Args:
        model: Mô hình cần đánh giá
        X_test: Dữ liệu kiểm tra
        y_test: Nhãn thực tế
        model_name: Tên mô hình
        
    Returns:
        dict: Dictionary chứa các metrics
    """
    print(f"\n📊 Đánh giá {model_name}:")
    print("="*50)
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'auc': roc_auc_score(y_test, y_proba)
    }
    
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 Score:  {metrics['f1']:.4f}")
    print(f"AUC-ROC:   {metrics['auc']:.4f}")
    
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, 
                                target_names=['No Churn', 'Churn']))
    
    return metrics


def compare_models(models_dict, X_test, y_test):
    """
    So sánh nhiều mô hình
    
    Args:
        models_dict: Dictionary {tên_mô_hình: mô_hình}
        X_test: Dữ liệu kiểm tra
        y_test: Nhãn thực tế
        
    Returns:
        pd.DataFrame: Bảng so sánh metrics
    """
    results = []
    
    for name, model in models_dict.items():
        metrics = evaluate_model(model, X_test, y_test, name)
        metrics['model'] = name
        results.append(metrics)
    
    df_results = pd.DataFrame(results)
    df_results = df_results[['model', 'accuracy', 'precision', 'recall', 'f1', 'auc']]
    
    print("\n" + "="*70)
    print("📊 BẢNG SO SÁNH MÔ HÌNH")
    print("="*70)
    print(df_results.to_string(index=False))
    
    return df_results


def save_model(model, filepath):
    """
    Lưu mô hình vào file .pkl
    
    Args:
        model: Mô hình cần lưu
        filepath: Đường dẫn file output
    """
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    print(f"✅ Đã lưu mô hình tại: {filepath}")


def save_feature_columns(columns, filepath):
    """
    Lưu danh sách tên cột đặc trưng
    
    Args:
        columns: Danh sách tên cột
        filepath: Đường dẫn file output
    """
    with open(filepath, 'wb') as f:
        pickle.dump(columns, f)
    print(f"✅ Đã lưu feature columns tại: {filepath}")


def load_model(filepath):
    """
    Tải mô hình từ file .pkl
    
    Args:
        filepath: Đường dẫn file mô hình
        
    Returns:
        model: Mô hình đã tải
    """
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    print(f"✅ Đã tải mô hình từ: {filepath}")
    return model


if __name__ == "__main__":
    # Import preprocessing
    from preprocessing import preprocess_pipeline
    
    # Tiền xử lý dữ liệu
    filepath = "../WA_Fn-UseC_-Telco-Customer-Churn.csv"
    X_train, X_test, y_train, y_test, scaler = preprocess_pipeline(filepath)
    
    # Huấn luyện các mô hình
    lr_model = train_logistic_regression(X_train, y_train)
    rf_model = train_random_forest(X_train, y_train)
    
    # Tối ưu Random Forest
    best_rf = optimize_random_forest(X_train, y_train)
    
    # Ensemble
    ensemble = train_ensemble(X_train, y_train, lr_model, best_rf)
    
    # So sánh
    models = {
        'Logistic Regression': lr_model,
        'Random Forest': rf_model,
        'Optimized Random Forest': best_rf,
        'Ensemble': ensemble
    }
    
    results_df = compare_models(models, X_test, y_test)
    
    # Lưu mô hình tốt nhất
    save_model(best_rf, "../models/best_rf_model.pkl")
    save_model(scaler, "../models/scaler.pkl")
    save_feature_columns(X_train.columns.tolist(), "../models/feature_columns.pkl")
