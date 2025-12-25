import os
import sys

# 1. THIẾT LẬP JAVA 17 (Cực kỳ quan trọng cho Spark trên Colab)
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ["PATH"]

import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import gdown

# 2. KHỞI TẠO SPARK
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
        st.error(f"Lỗi khởi động Spark: {e}")
        return None

# 3. TẢI MÔ HÌNH
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
    except Exception as e:
        st.error(f"Lỗi tải model: {e}")
        return None

# 4. GIAO DIỆN CHÍNH
def main():
    st.set_page_config(page_title="Dự Báo Doanh Thu", layout="wide")
    st.title("🛒 Hệ Thống Dự Báo Doanh Thu Thương Mại Điện Tử")
    
    spark = init_spark()
    model_path = download_model()
    
    if spark and model_path:
        try:
            model = PipelineModel.load(model_path)
            st.success("✅ Mô hình Random Forest đã sẵn sàng!")
            
            # Form nhập liệu
            with st.form(key="prediction_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    category = st.selectbox("Loại Sản Phẩm", ["Electronics", "Home & Kitchen", "Clothing", "Books", "Toys"])
                    units_sold = st.number_input("Số Lượng Bán", min_value=1, value=50)
                    discount = st.slider("Mức Giảm Giá (%)", 0.0, 50.0, 10.0)
                
                with col2:
                    ad_spend = st.number_input("Chi Phí Quảng Cáo ($)", value=500.0)
                    reviews = st.slider("Đánh Giá Khách Hàng", 1.0, 5.0, 4.0)
                    shipping = st.number_input("Chi Phí Vận Chuyển ($)", value=5.0)
                
                # Nút Submit (BẮT BUỘC PHẢI THỤT LỀ Ở ĐÂY)
                submitted = st.form_submit_button("🔮 Dự Báo Doanh Thu")
                
                if submitted:
                    schema = StructType([
                        StructField("Category", StringType(), True),
                        StructField("Units_Sold", IntegerType(), True),
                        StructField("Discount", DoubleType(), True),
                        StructField("Ad_Spend", DoubleType(), True),
                        StructField("Customer_Reviews", DoubleType(), True),
                        StructField("Shipping_Cost", DoubleType(), True)
                    ])
                    input_data = [(category, int(units_sold), float(discount), float(ad_spend), float(reviews), float(shipping))]
                    df = spark.createDataFrame(input_data, schema)
                    
                    prediction = model.transform(df).collect()[0]["prediction"]
                    
                    st.divider()
                    st.header(f"📊 Kết quả dự báo: ${prediction:,.2f}")

        except Exception as e:
            st.error(f"Lỗi load mô hình: {e}")

if __name__ == "__main__":
    main()
