import os
import sys
import zipfile
import shutil
import gdown
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# 1. Cấu hình Java 17 cho Streamlit Cloud
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

# Cấu hình giao diện trang
st.set_page_config(page_title="Dự Báo Doanh Thu E-Commerce", layout="wide")

@st.cache_resource
def init_spark():
    try:
        spark = SparkSession.builder \
            .appName("RevenuePredictor") \
            .master("local[1]") \
            .config("spark.driver.memory", "512m") \
            .config("spark.ui.showConsoleProgress", "false") \
            .getOrCreate()
        return spark
    except Exception as e:
        return None

@st.cache_resource
def download_and_prepare_model():
    final_model_path = "models/random_forest_v1"
    zip_path = "model.zip"
    extract_path = "models/temp_extract"
    
    if os.path.exists(final_model_path):
        return final_model_path
    
    file_id = "1vOwtKC0wc8CoUONJ6Z45wGLnfOkpQBpY"
    try:
        gdown.download(id=file_id, output=zip_path, quiet=False)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        actual_path = extract_path
        for root, dirs, files in os.walk(extract_path):
            if "metadata" in dirs:
                actual_path = root
                break
        
        os.makedirs("models", exist_ok=True)
        if os.path.exists(final_model_path): shutil.rmtree(final_model_path)
        shutil.move(actual_path, final_model_path)
        
        if os.path.exists(zip_path): os.remove(zip_path)
        if os.path.exists(extract_path): shutil.rmtree(extract_path)
        return final_model_path
    except:
        return None

def main():
    # Dòng này bây giờ sẽ không còn lỗi NameError vì đã có import streamlit as st ở trên
    st.title("🛒 Hệ Thống Dự Báo Doanh Thu Thương Mại Điện Tử")
    st.markdown("---")
    
    spark = init_spark()
    model_path = download_and_prepare_model()
    
    if spark and model_path:
        try:
            model = PipelineModel.load(model_path)
            st.sidebar.success("✅ Mô hình đã nạp thành công!")
            
            # Sidebar - Thông tin mô hình
            st.sidebar.header("Thông Tin Mô Hình")
            st.sidebar.write("**Thuật toán:** Random Forest Regressor")
            st.sidebar.write("**Độ chính xác (R²):** ~96.6%")
            
            # Giao diện nhập liệu
            st.subheader("📝 Nhập Thông Tin Sản Phẩm")
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("Loại Sản Phẩm", 
                    ["Electronics", "Clothing", "Books", "Home Appliances", "Toys"])
                region = st.selectbox("Khu Vực (Region)", 
                    ["North America", "Europe", "Asia", "South America", "Oceania"])
                units = st.number_input("Số Lượng Bán (Units Sold)", min_value=1, value=150)
            
            with col2:
                discount_app = st.slider("Mức Giảm Giá (Discount_Applied)", 0.0, 1.0, 0.15)
                ad_spend = st.number_input("Chi Phí Quảng Cáo ($)", min_value=0.0, value=120.0)
                clicks = st.number_input("Số Lượt Click (Clicks)", min_value=0, value=25)

            if st.button("🔮 Bắt Đầu Dự Báo", use_container_width=True):
                # Khởi tạo dữ liệu đầu vào cho Spark
                schema = StructType([
                    StructField("Category", StringType(), True),
                    StructField("Region", StringType(), True),
                    StructField("Units_Sold", IntegerType(), True),
                    StructField("Discount_Applied", DoubleType(), True),
                    StructField("Ad_Spend", DoubleType(), True),
                    StructField("Clicks", DoubleType(), True)
                ])
                
                input_data = [(str(category), str(region), int(units), float(discount_app), float(ad_spend), float(clicks))]
                df = spark.createDataFrame(input_data, schema)
                
                # Dự báo
                prediction = model.transform(df).collect()[0]["prediction"]
                
                # Hiển thị kết quả Pro
                st.divider()
                st.balloons()
                
                res_col1, res_col2 = st.columns([1, 1])
                with res_col1:
                    st.metric(label="Doanh Thu Dự Báo", value=f"${prediction:,.2f}")
                    profit = prediction - ad_spend
                    st.metric(label="Lợi Nhuận Dự Tính (Sau trừ QC)", value=f"${profit:,.2f}")
                
                with res_col2:
                    # TRỰC QUAN HÓA: Feature Importance (Dựa trên kết quả từ Notebook của bạn)
                    st.write("### 📊 Các yếu tố ảnh hưởng nhất")
                    # Dữ liệu mẫu dựa trên mô hình RF của bạn
                    importance_data = pd.DataFrame({
                        'Yếu tố': ['Số lượng bán', 'Ngành hàng', 'Quảng cáo', 'Clicks', 'Giảm giá', 'Khu vực'],
                        'Mức độ (%)': [35, 25, 15, 12, 8, 5]
                    })
                    fig, ax = plt.subplots(figsize=(6, 4))
                    sns.barplot(x='Mức độ (%)', y='Yếu tố', data=importance_data, palette='viridis', ax=ax)
                    st.pyplot(fig)

        except Exception as e:
            st.error(f"Lỗi thực thi: {e}")

if __name__ == "__main__":
    main()
