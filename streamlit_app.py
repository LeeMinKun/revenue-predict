import os
import sys

# 1. THIẾT LẬP JAVA CHO STREAMLIT CLOUD (Hệ điều hành Debian)
# Dòng này phải nằm trên cùng, trước khi import pyspark
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"

import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import gdown

# Cấu hình trang
st.set_page_config(page_title="Dự Báo Doanh Thu Thương Mại Điện Tử", layout="wide")

@st.cache_resource
def init_spark():
    try:
        # Khởi tạo Spark tối ưu cho Cloud
        spark = SparkSession.builder \
            .appName("RevenuePredictor") \
            .master("local[1]") \
            .config("spark.driver.memory", "2g") \
            .config("spark.ui.showConsoleProgress", "false") \
            .getOrCreate()
        return spark
    except Exception as e:
        st.error(f"Lỗi khởi động Spark: {e}")
        return None

@st.cache_resource
def download_model_from_drive():
    model_path = "models/random_forest_v1"
    if os.path.exists(model_path):
        return model_path
    
    # ID thư mục sạch (không kèm đuôi ?usp=sharing)
    folder_id = "1ESwDvLGSlxRXFgnNqW-LPC9ETZbN6tkQ"
    os.makedirs("models", exist_ok=True)
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    
    try:
        # Tải mô hình từ Drive
        gdown.download_folder(url, output="models/", quiet=False, use_cookies=False)
        return model_path
    except Exception as e:
        st.error(f"Lỗi tải mô hình từ Drive: {e}")
        return None

def main():
    st.title("🛒 Hệ Thống Dự Báo Doanh Thu")
    st.markdown("---")
    
    spark = init_spark()
    model_path = download_model_from_drive()
    
    if spark and model_path:
        try:
            model = PipelineModel.load(model_path)
            st.success("✅ Mô hình Random Forest đã sẵn sàng!")
            
            # Giao diện nhập liệu
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("Loại Sản Phẩm", ["Electronics", "Home & Kitchen", "Clothing", "Books", "Toys"])
                region = st.selectbox("Khu Vực (Region)", ["North", "South", "East", "West"])
                units_sold = st.number_input("Số Lượng Bán", min_value=1, value=50)
                discount = st.slider("Mức Giảm Giá (%)", 0.0, 50.0, 10.0)
            
            with col2:
                ad_spend = st.number_input("Chi Phí Quảng Cáo ($)", min_value=0.0, value=500.0)
                reviews = st.slider("Đánh Giá Khách Hàng", 1.0, 5.0, 4.0)
                shipping = st.number_input("Chi Phí Vận Chuyển ($)", min_value=0.0, value=5.0)

            if st.button("🔮 Dự Báo Doanh Thu", use_container_width=True):
                # Định nghĩa Schema đầy đủ 7 cột như trong notebook huấn luyện
                schema = StructType([
                    StructField("Category", StringType(), True),
                    StructField("Region", StringType(), True),
                    StructField("Units_Sold", IntegerType(), True),
                    StructField("Discount", DoubleType(), True),
                    StructField("Ad_Spend", DoubleType(), True),
                    StructField("Customer_Reviews", DoubleType(), True),
                    StructField("Shipping_Cost", DoubleType(), True)
                ])
                
                input_data = [(category, region, int(units_sold), float(discount), 
                               float(ad_spend), float(reviews), float(shipping))]
                df = spark.createDataFrame(input_data, schema)
                
                # Dự báo doanh thu
                prediction = model.transform(df).collect()[0]["prediction"]
                
                st.divider()
                st.balloons()
                st.header(f"📊 Kết quả dự báo: ${prediction:,.2f}")
                
                # Phân tích nhanh lợi nhuận
                profit = prediction - (ad_spend + (shipping * units_sold))
                st.subheader(f"💰 Lợi nhuận ước tính: ${profit:,.2f}")

        except Exception as e:
            st.error(f"Lỗi load mô hình: {e}")

if __name__ == "__main__":
    main()
