"""
Ứng dụng Streamlit Demo dự đoán Customer Churn
Chạy: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sys
import os

# Thêm đường dẫn src vào path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from predict import predict_churn, load_model_and_scaler


# Cấu hình trang
st.set_page_config(
    page_title="Dự đoán Customer Churn",
    page_icon="📊",
    layout="wide"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .churn-high {
        background-color: #ffcccc;
        border: 2px solid #ff0000;
        color: #800000;
    }
    .churn-medium {
        background-color: #fff4cc;
        border: 2px solid #ffa500;
        color: #800000;

    }
    .churn-low {
        background-color: #ccffcc;
        border: 2px solid #00cc00;
        color: #006600;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    """Tải mô hình, scaler và feature columns (cache để tăng tốc)"""
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'rf_model.pkl')
    scaler_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'scaler.pkl')
    feature_cols_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'feature_columns.pkl')
    
    try:
        model, scaler, feature_columns = load_model_and_scaler(model_path, scaler_path, feature_cols_path)
        return model, scaler, feature_columns, None
    except Exception as e:
        return None, None, None, str(e)


def main():
    # Header
    st.markdown("<h1 class='main-header'>🔮 Dự đoán Churn Khách hàng</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Tải mô hình
    model, scaler, feature_columns, error = load_models()
    
    if error:
        st.error(f"❌ Lỗi khi tải mô hình: {error}")
        st.info("💡 Vui lòng chạy `python src/modeling.py` trước để tạo mô hình!")
        return
    
    # Sidebar: Thông tin dự án
    with st.sidebar:
        st.header("📚 Thông tin dự án")
        st.write("""
        **Mục tiêu:** Dự đoán khách hàng có khả năng rời bỏ dịch vụ
        
        **Phương pháp:** CRISP-DM
        
        **Mô hình:** Random Forest (Optimized)
        
        **Độ chính xác:** F1 Score = 0.68
        """)
        
        st.markdown("---")
        st.header("🎯 Cách sử dụng")
        st.write("""
        1. Nhập thông tin khách hàng
        2. Nhấn nút "Dự đoán"
        3. Xem kết quả và khuyến nghị
        """)
    
    # Main content: Form nhập liệu
    st.header("📝 Nhập thông tin khách hàng")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Thông tin cá nhân")
        gender = st.selectbox("Giới tính", ["Female", "Male"])
        senior_citizen = st.selectbox("Người cao tuổi", ["No", "Yes"])
        partner = st.selectbox("Có bạn đời", ["No", "Yes"])
        dependents = st.selectbox("Có người phụ thuộc", ["No", "Yes"])
        tenure = st.slider("Thời gian sử dụng (tháng)", 0, 72, 12)
    
    with col2:
        st.subheader("Dịch vụ sử dụng")
        phone_service = st.selectbox("Dịch vụ điện thoại", ["No", "Yes"])
        multiple_lines = st.selectbox("Nhiều đường dây", ["No", "Yes", "No phone service"])
        internet_service = st.selectbox("Dịch vụ Internet", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Bảo mật trực tuyến", ["No", "Yes", "No internet service"])
        online_backup = st.selectbox("Sao lưu trực tuyến", ["No", "Yes", "No internet service"])
        device_protection = st.selectbox("Bảo vệ thiết bị", ["No", "Yes", "No internet service"])
        tech_support = st.selectbox("Hỗ trợ kỹ thuật", ["No", "Yes", "No internet service"])
        streaming_tv = st.selectbox("TV streaming", ["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Phim streaming", ["No", "Yes", "No internet service"])
    
    with col3:
        st.subheader("Thông tin thanh toán")
        contract = st.selectbox("Loại hợp đồng", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Hóa đơn điện tử", ["No", "Yes"])
        payment_method = st.selectbox("Phương thức thanh toán", [
            "Electronic check", 
            "Mailed check", 
            "Bank transfer (automatic)", 
            "Credit card (automatic)"
        ])
        monthly_charges = st.number_input("Phí hàng tháng ($)", 0.0, 200.0, 70.0, 0.5)
        
        # Tính tự động TotalCharges dựa trên tenure và monthly_charges
        total_charges = tenure * monthly_charges
        st.metric(
            label="Tổng phí ($)", 
            value=f"${total_charges:,.2f}",
            help="Tự động tính = Thời gian sử dụng × Phí hàng tháng"
        )
    
    # Nút dự đoán
    st.markdown("---")
    if st.button("🔮 Dự đoán Churn", type="primary", use_container_width=True):
        # Tạo dictionary dữ liệu
        customer_data = {
            'gender': gender,
            'SeniorCitizen': 1 if senior_citizen == "Yes" else 0,
            'Partner': partner,
            'Dependents': dependents,
            'tenure': tenure,
            'PhoneService': phone_service,
            'MultipleLines': multiple_lines,
            'InternetService': internet_service,
            'OnlineSecurity': online_security,
            'OnlineBackup': online_backup,
            'DeviceProtection': device_protection,
            'TechSupport': tech_support,
            'StreamingTV': streaming_tv,
            'StreamingMovies': streaming_movies,
            'Contract': contract,
            'PaperlessBilling': paperless_billing,
            'PaymentMethod': payment_method,
            'MonthlyCharges': monthly_charges,
            'TotalCharges': total_charges
        }
        
        # Dự đoán
        with st.spinner("Đang phân tích..."):
            try:
                result = predict_churn(model, scaler, customer_data, feature_columns)
                
                # Hiển thị kết quả
                st.header("📊 Kết quả dự đoán")
                
                churn_prob = result['churn_probability']
                
                # Xác định mức độ rủi ro
                if churn_prob > 0.7:
                    box_class = "churn-high"
                    icon = "🔴"
                    risk_level = "CAO"
                    recommendation = """
                    **Khuyến nghị:**
                    - ⚠️ Liên hệ ngay với khách hàng
                    - 💰 Đưa ra ưu đãi đặc biệt
                    - 📞 Tăng cường chăm sóc khách hàng
                    - 🎁 Xem xét gói dịch vụ dài hạn với giảm giá
                    """
                elif churn_prob > 0.5:
                    box_class = "churn-medium"
                    icon = "🟡"
                    risk_level = "TRUNG BÌNH"
                    recommendation = """
                    **Khuyến nghị:**
                    - 📧 Gửi email khảo sát sự hài lòng
                    - 💡 Giới thiệu các dịch vụ phù hợp
                    - 📞 Theo dõi định kỳ
                    """
                else:
                    box_class = "churn-low"
                    icon = "🟢"
                    risk_level = "THẤP"
                    recommendation = """
                    **Khuyến nghị:**
                    - ✅ Duy trì chất lượng dịch vụ
                    - 🎯 Tiếp tục chăm sóc bình thường
                    - 💌 Gửi lời cảm ơn và ưu đãi định kỳ
                    """
                
                # Box kết quả
                st.markdown(f"""
                <div class='result-box {box_class}'>
                    <h2>{icon} {result['prediction']}</h2>
                    <h3>Mức độ rủi ro: {risk_level}</h3>
                    <p style='font-size: 1.2rem;'>
                        Xác suất Churn: <strong>{churn_prob:.1%}</strong><br>
                        Xác suất No Churn: <strong>{result['no_churn_probability']:.1%}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Biểu đồ xác suất
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    st.subheader("📈 Xác suất dự đoán")
                    prob_df = pd.DataFrame({
                        'Kết quả': ['No Churn', 'Churn'],
                        'Xác suất': [result['no_churn_probability'], churn_prob]
                    })
                    st.bar_chart(prob_df.set_index('Kết quả'))
                
                with col_chart2:
                    st.subheader("💡 Khuyến nghị hành động")
                    st.markdown(recommendation)
                
            except Exception as e:
                st.error(f"❌ Lỗi khi dự đoán: {str(e)}")


if __name__ == "__main__":
    main()
