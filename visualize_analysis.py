"""
Script trực quan hóa Feature Importance và phân tích Churn
Chạy: python visualize_analysis.py
"""

import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Thiết lập style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load model và feature columns
print("📂 Đang tải mô hình...")
model = pickle.load(open('models/best_rf_model.pkl', 'rb'))
feature_cols = pickle.load(open('models/feature_columns.pkl', 'rb'))

# Load data
print("📂 Đang tải dữ liệu...")
df = pd.read_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Tính % Churn
churn_pct = df['Churn'].value_counts(normalize=True) * 100

print("\n" + "="*70)
print("📊 PHÂN TÍCH DỮ LIỆU KHÁCH HÀNG CHURN")
print("="*70)

# 1. Thống kê Churn
print("\n1️⃣  TỶ LỆ CHURN:")
print(f"   - Tổng khách hàng: {len(df):,}")
print(f"   - Churn (Yes): {df['Churn'].value_counts()['Yes']:,} ({churn_pct['Yes']:.2f}%)")
print(f"   - No Churn (No): {df['Churn'].value_counts()['No']:,} ({churn_pct['No']:.2f}%)")

# 2. Feature Importance
feat_imp = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n2️⃣  TOP 10 ĐẶC TRƯNG QUAN TRỌNG NHẤT:")
for i, row in feat_imp.head(10).iterrows():
    print(f"   {feat_imp.index.get_loc(i)+1:2d}. {row['feature']:40s} {row['importance']*100:6.2f}%")

# 3. Phân loại features
numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
numeric_imp = feat_imp[feat_imp['feature'].isin(numeric_features)]['importance'].sum()
categorical_imp = feat_imp[~feat_imp['feature'].isin(numeric_features)]['importance'].sum()

print("\n3️⃣  PHÂN LOẠI THEO LOẠI BIẾN:")
print(f"   - Biến số (3 biến): {numeric_imp*100:.2f}%")
print(f"   - Biến phân loại (27 biến): {categorical_imp*100:.2f}%")

# 4. Top features by category
print("\n4️⃣  TOP 5 BIẾN SỐ:")
for i, row in feat_imp[feat_imp['feature'].isin(numeric_features)].iterrows():
    print(f"   - {row['feature']:20s} {row['importance']*100:6.2f}%")

print("\n5️⃣  TOP 5 BIẾN PHÂN LOẠI:")
top_cat = feat_imp[~feat_imp['feature'].isin(numeric_features)].head(5)
for i, row in top_cat.iterrows():
    print(f"   - {row['feature']:40s} {row['importance']*100:6.2f}%")

print("\n" + "="*70)

# ============= VISUALIZATIONS =============

# Figure 1: Churn Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Pie chart
colors = ['#66c2a5', '#fc8d62']
axes[0].pie(df['Churn'].value_counts(), labels=['No Churn', 'Churn'], 
            autopct='%1.1f%%', colors=colors, startangle=90, textprops={'fontsize': 12})
axes[0].set_title('Phân phối Churn trong Dataset', fontsize=14, fontweight='bold')

# Bar chart
churn_counts = df['Churn'].value_counts()
axes[1].bar(['No Churn', 'Churn'], churn_counts.values, color=colors, edgecolor='black')
axes[1].set_ylabel('Số lượng khách hàng', fontsize=12)
axes[1].set_title('Số lượng khách hàng theo Churn', fontsize=14, fontweight='bold')
for i, v in enumerate(churn_counts.values):
    axes[1].text(i, v + 100, f'{v:,}', ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('churn_distribution.png', dpi=300, bbox_inches='tight')
print("\n✅ Đã lưu: churn_distribution.png")

# Figure 2: Top 15 Feature Importance
fig, ax = plt.subplots(figsize=(12, 8))

top15 = feat_imp.head(15).sort_values('importance')
colors_feat = ['#e74c3c' if f in numeric_features else '#3498db' for f in top15['feature']]

ax.barh(range(len(top15)), top15['importance']*100, color=colors_feat, edgecolor='black')
ax.set_yticks(range(len(top15)))
ax.set_yticklabels(top15['feature'], fontsize=10)
ax.set_xlabel('Importance (%)', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Đặc trưng Quan trọng nhất\n(Đỏ = Biến số, Xanh = Biến phân loại)', 
             fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Add values
for i, v in enumerate(top15['importance']*100):
    ax.text(v + 0.3, i, f'{v:.2f}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
print("✅ Đã lưu: feature_importance.png")

# Figure 3: Numeric vs Categorical Importance
fig, ax = plt.subplots(figsize=(8, 6))

categories = ['Biến số\n(3 biến)', 'Biến phân loại\n(27 biến)']
importances = [numeric_imp*100, categorical_imp*100]
colors_pie = ['#e74c3c', '#3498db']

wedges, texts, autotexts = ax.pie(importances, labels=categories, autopct='%1.1f%%',
                                    colors=colors_pie, startangle=90, 
                                    textprops={'fontsize': 12, 'fontweight': 'bold'})
ax.set_title('So sánh Importance: Biến số vs Biến phân loại', 
             fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('numeric_vs_categorical.png', dpi=300, bbox_inches='tight')
print("✅ Đã lưu: numeric_vs_categorical.png")

# Figure 4: Feature Importance by Category
fig, ax = plt.subplots(figsize=(12, 8))

# Group by feature type
feature_groups = {
    'Biến số (3)': feat_imp[feat_imp['feature'].isin(numeric_features)]['importance'].sum(),
    'Contract': feat_imp[feat_imp['feature'].str.contains('Contract')]['importance'].sum(),
    'Internet Service': feat_imp[feat_imp['feature'].str.contains('InternetService')]['importance'].sum(),
    'Payment Method': feat_imp[feat_imp['feature'].str.contains('PaymentMethod')]['importance'].sum(),
    'Online Security': feat_imp[feat_imp['feature'].str.contains('OnlineSecurity')]['importance'].sum(),
    'Tech Support': feat_imp[feat_imp['feature'].str.contains('TechSupport')]['importance'].sum(),
    'Device Protection': feat_imp[feat_imp['feature'].str.contains('DeviceProtection')]['importance'].sum(),
    'Online Backup': feat_imp[feat_imp['feature'].str.contains('OnlineBackup')]['importance'].sum(),
    'Streaming': feat_imp[feat_imp['feature'].str.contains('Streaming')]['importance'].sum(),
    'Khác': 1 - sum(feature_groups.values()) if sum([v for v in feature_groups.values()]) < 1 else 0
}

# Calculate remaining
calculated_sum = sum(feature_groups.values())
feature_groups['Khác'] = max(0, 1 - calculated_sum)

groups_df = pd.DataFrame(list(feature_groups.items()), columns=['Group', 'Importance'])
groups_df = groups_df.sort_values('Importance', ascending=True)

colors_groups = plt.cm.Set3(range(len(groups_df)))
ax.barh(range(len(groups_df)), groups_df['Importance']*100, color=colors_groups, edgecolor='black')
ax.set_yticks(range(len(groups_df)))
ax.set_yticklabels(groups_df['Group'], fontsize=11)
ax.set_xlabel('Importance (%)', fontsize=12, fontweight='bold')
ax.set_title('Importance theo nhóm đặc trưng', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

for i, v in enumerate(groups_df['Importance']*100):
    ax.text(v + 0.5, i, f'{v:.2f}%', va='center', fontsize=10)

plt.tight_layout()
plt.savefig('feature_groups.png', dpi=300, bbox_inches='tight')
print("✅ Đã lưu: feature_groups.png")

print("\n" + "="*70)
print("🎉 HOÀN TẤT! Đã tạo 4 biểu đồ:")
print("   1. churn_distribution.png - Phân phối Churn")
print("   2. feature_importance.png - Top 15 features quan trọng")
print("   3. numeric_vs_categorical.png - So sánh biến số vs phân loại")
print("   4. feature_groups.png - Importance theo nhóm")
print("="*70)

# Show plots
print("\n💡 Mở cửa sổ để xem biểu đồ...")
plt.show()
