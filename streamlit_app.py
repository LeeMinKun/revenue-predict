import os
import sys
import zipfile
import shutil

# 1. Cấu hình Java 17 cho Streamlit Cloud
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import gdown

# Cấu hình trang
st.set_page_config(page_title="Dự Báo Doanh Thu", layout="wide")

@st.cache_resource
def init_spark():
    try:
        # Cấu hình tối giản để tiết kiệm RAM trên Cloud
        spark = SparkSession.builder \
            .appName("RevenuePredictor") \
            .master("local[1]") \
            .config("spark.driver.memory", "512m") \
            .config("spark.ui.showConsoleProgress", "false") \
            .getOrCreate()
        return spark
    except Exception as e:
        st.error(f"Lỗi khởi tạo Spark: {e}")
        return None

@st.cache_resource
def download_and_extract_model():
    model_dir = "models/random_forest_v1"
    zip_path = "model.zip"
    
    if os.path.exists(model_dir):
        return model_dir
    
    # ID file ZIP của bạn
    file_id = "1vOwtKC0wc8CoUONJ6Z45wGLnfOkpQBpY"
    
    try:
        # SỬA TẠI ĐÂY: Dùng id= thay vì url=
        with st.spinner("📦 Đang tải gói mô hình từ Google Drive..."):
            # gdown sẽ tự xử lý xác nhận file lớn khi dùng tham số id
            gdown.download(id=file_id, output=zip_path, quiet=False)
        
        if os.path.exists(zip_path):
            with st.spinner("📂 Đang giải nén..."):
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall("models/")
            os.remove(zip_path)
            return model_dir
        else:
            st.error("Không tìm thấy file tải về.")
            return None
    except Exception as e:
        st.error(f"Lỗi tải file: {e}")
        return None

def main():
    st.title("🛒 Hệ Thống Dự Báo Doanh Thu Thương Mại Điện Tử")
    
    spark = init_spark()
    model_path = download_and_extract_model()
    
    if spark and model_path:
        try:
            model = PipelineModel.load(model_path)
            st.success("✅ Hệ thống đã sẵn sàng với mô hình tối ưu!")
            
            # Form nhập liệu
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("Loại Sản Phẩm", ["Electronics", "Home & Kitchen", "Clothing", "Books", "Toys"])
                region = st.selectbox("Khu Vực", ["North", "South", "East", "West"])
                units_sold = st.number_input("Số Lượng Bán", min_value=1, value=100)
                discount_applied = st.selectbox("Áp dụng giảm giá?", ["Yes", "No"])

            with col2:
                discount_val = st.slider("Mức Giảm Giá (0.0 - 1.0)", 0.0, 1.0, 0.1)
                ad_spend = st.number_input("Chi Phí Quảng Cáo ($)", value=200.0)
                clicks = st.number_input("Số Lượt Click", value=50)
                shipping = st.number_input("Phí Vận Chuyển ($)", value=5.0)

            if st.button("🔮 Dự Báo Ngay", use_container_width=True):
                # Định nghĩa Schema đầy đủ để khớp với Pipeline cũ
                schema = StructType([
                    StructField("Category", StringType(), True),
                    StructField("Region", StringType(), True),
                    StructField("Discount_Applied", StringType(), True),
                    StructField("Units_Sold", IntegerType(), True),
                    StructField("Discount", DoubleType(), True),
                    StructField("Ad_Spend", DoubleType(), True),
                    StructField("Clicks", DoubleType(), True),
                    StructField("Customer_Reviews", DoubleType(), True), # Mặc định nếu model cần
                    StructField("Shipping_Cost", DoubleType(), True)
                ])
                
                input_data = [(str(category), str(region), str(discount_applied), int(units_sold), 
                               float(discount_val), float(ad_spend), float(clicks), 4.0, float(shipping))]
                
                df = spark.createDataFrame(input_data, schema)
                prediction = model.transform(df).collect()[0]["prediction"]
                
                st.divider()
                st.balloons()
                st.header(f"📊 Kết quả dự báo: ${prediction:,.2f}")
                
        except Exception as e:
            st.error(f"Lỗi thực thi: {e}")

if __name__ == "__main__":
    main()
