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

# Cấu hình Java 17
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

st.set_page_config(page_title="Hệ thống Dự báo Doanh thu", layout="wide")

@st.cache_resource
def init_spark():
    # Thêm thông báo trạng thái lên UI
    status = st.empty()
    status.info("⏳ Đang khởi tạo máy chủ tính toán Spark (JVM)...")
    try:
        spark = SparkSession.builder \
            .appName("DSS") \
            .master("local[1]") \
            .config("spark.driver.memory", "400m") \
            .config("spark.executor.memory", "400m") \
            .config("spark.sql.shuffle.partitions", "1") \
            .getOrCreate()
        status.empty()
        return spark
    except Exception as e:
        st.error(f"Lỗi khởi tạo Spark: {e}")
        return None

@st.cache_resource
def load_model_optimized():
    model_path = "models/random_forest_v1"
    status = st.empty()
    
    if not os.path.exists(model_path):
        status.info("⏳ Đang kết nối Drive và tải mô hình...")
        file_id = "1vOwtKC0wc8CoUONJ6Z45wGLnfOkpQBpY"
        gdown.download(id=file_id, output="model.zip", quiet=False)
        
        status.info("⏳ Đang giải nén gói mô hình...")
        with zipfile.ZipFile("model.zip", 'r') as zip_ref:
            zip_ref.extractall("models/temp")
        
        for root, dirs, files in os.walk("models/temp"):
            if "metadata" in dirs:
                if os.path.exists(model_path): shutil.rmtree(model_path)
                shutil.move(root, model_path)
                break
        shutil.rmtree("models/temp")
        if os.path.exists("model.zip"): os.remove("model.zip")
    
    status.info("⏳ Đang nạp mô hình vào Spark (bước này có thể mất 1-2 phút)...")
    model = PipelineModel.load(model_path)
    status.empty()
    return model

def main():
    st.title("🛒 Hệ Thống Hỗ Trợ Ra Quyết Định Doanh Thu")
    
    # Khởi tạo các thành phần nặng
    spark = init_spark()
    if spark:
        try:
            model = load_model_optimized()
            st.sidebar.success("✅ Hệ thống đã sẵn sàng!")
            
            # --- DASHBOARD SIDEBAR ---
            st.sidebar.header("📊 Thông số mô hình")
            st.sidebar.write("- **R² Score:** 96.6%")
            st.sidebar.write("- **Thuật toán:** Random Forest")

            # --- GIAO DIỆN NHẬP LIỆU ---
            col1, col2 = st.columns(2)
            with col1:
                cat = st.selectbox("Ngành hàng", ["Electronics", "Clothing", "Books", "Home Appliances", "Toys"])
                reg = st.selectbox("Khu vực", ["North America", "Europe", "Asia", "South America", "Oceania"])
                units = st.number_input("Số lượng bán", min_value=1, value=150)
            with col2:
                disc = st.slider("Mức giảm giá", 0.0, 1.0, 0.15)
                ads = st.number_input("Ngân sách Marketing ($)", value=200.0)
                clicks = st.number_input("Số lượt Clicks", value=50)

            if st.button("🔮 THỰC HIỆN DỰ BÁO", use_container_width=True):
                schema = StructType([
                    StructField("Category", StringType(), True),
                    StructField("Region", StringType(), True),
                    StructField("Units_Sold", IntegerType(), True),
                    StructField("Discount_Applied", DoubleType(), True),
                    StructField("Ad_Spend", DoubleType(), True),
                    StructField("Clicks", DoubleType(), True)
                ])
                data = [(cat, reg, int(units), float(disc), float(ads), float(clicks))]
                df = spark.createDataFrame(data, schema)
                
                prediction = model.transform(df).collect()[0]["prediction"]
                
                st.divider()
                r_col, c_col = st.columns([1, 1.5])
                with r_col:
                    st.metric("Doanh thu dự báo", f"${prediction:,.2f}")
                    st.metric("Lợi nhuận dự tính", f"${prediction - ads:,.2f}")
                
                with c_col:
                    # Vẽ biểu đồ mức độ ảnh hưởng (Feature Importance)
                    importances = [0.35, 0.25, 0.15, 0.12, 0.08, 0.05] # Dữ liệu từ notebook
                    labels = ["Units Sold", "Category", "Ad Spend", "Clicks", "Discount", "Region"]
                    fig, ax = plt.subplots()
                    sns.barplot(x=importances, y=labels, palette="viridis", ax=ax)
                    st.pyplot(fig)

        except Exception as e:
            st.error(f"Lỗi nạp hệ thống: {e}")

if __name__ == "__main__":
    main()
