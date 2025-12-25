import os
import sys

# 1. Cấu hình Java 17
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ["PATH"]

import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import gdown

# Cấu hình trang
st.set_page_config(page_title="Dự Báo Doanh Thu", layout="wide")

@st.cache_resource
def init_spark():
    try:
        spark = SparkSession.builder \
            .appName("RevenuePredictor") \
            .master("local[*]") \
            .config("spark.driver.bindAddress", "127.0.0.1") \
            .getOrCreate()
        return spark
    except Exception as e:
        return None

@st.cache_resource
def download_model():
    model_path = "models/random_forest_v1"
    if os.path.exists(model_path):
        return model_path
    folder_id = "1ESwDvLGSlxRXFgnNqW-LPC9ETZbN6tkQ"
    os.makedirs("models", exist_ok=True)
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    try:
        gdown.download_folder(url, output="models/", quiet=False, use_cookies=False)
        return model_path
    except:
        return None

def main():
    st.title("🛒 Hệ Thống Dự Báo Doanh Thu Thương Mại Điện Tử")
    
    spark = init_spark()
    model_path = download_model()
    
    if not spark or not model_path:
        st.error("Đang khởi tạo hệ thống hoặc tải mô hình...")
        return

    try:
        model = PipelineModel.load(model_path)
        st.success("✅ Mô hình Random Forest đã sẵn sàng!")
        
        st.subheader("📝 Nhập Thông Tin Sản Phẩm")
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Loại Sản Phẩm", ["Electronics", "Home & Kitchen", "Clothing", "Books", "Toys"])
            region = st.selectbox("Khu Vực (Region)", ["North", "South", "East", "West"])
            units_sold = st.number_input("Số Lượng Bán", min_value=1, value=50)
            
        with col2:
            discount = st.slider("Mức Giảm Giá (%)", 0.0, 50.0, 10.0)
            ad_spend = st.number_input("Chi Phí Quảng Cáo ($)", min_value=0.0, value=500.0)
            reviews = st.slider("Đánh Giá Khách Hàng", 1.0, 5.0, 4.0)
            shipping = st.number_input("Chi Phí Vận Chuyển ($)", min_value=0.0, value=5.0)

        # Sử dụng nút bấm bình thường, không dùng Form
        if st.button("🔮 Dự Báo Doanh Thu", use_container_width=True):
            # Tạo Schema dựa trên notebook Nhom1_KPDLL2.ipynb
            schema = StructType([
                StructField("Category", StringType(), True),
                StructField("Region", StringType(), True),
                StructField("Units_Sold", IntegerType(), True),
                StructField("Discount", DoubleType(), True),
                StructField("Ad_Spend", DoubleType(), True),
                StructField("Customer_Reviews", DoubleType(), True),
                StructField("Shipping_Cost", DoubleType(), True)
            ])
            
            input_data = [(str(category), str(region), int(units_sold), float(discount), float(ad_spend), float(reviews), float(shipping))]
            df = spark.createDataFrame(input_data, schema)
            
            # Dự báo
            prediction_df = model.transform(df)
            result = prediction_df.collect()[0]["prediction"]
            
            st.divider()
            st.balloons()
            st.header(f"📊 Doanh thu dự báo: ${result:,.2f}")
            
            # Tính lợi nhuận ước tính
            profit = result - (ad_spend + (shipping * units_sold))
            st.subheader(f"💰 Lợi nhuận ước tính: ${profit:,.2f}")

    except Exception as e:
        st.error(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
