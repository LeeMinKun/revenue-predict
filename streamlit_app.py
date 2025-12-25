import os
import sys

# Thiết lập Java 17 cho Streamlit Cloud
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import gdown

# Cấu hình giao diện
st.set_page_config(page_title="Dự Báo Doanh Thu Thương Mại Điện Tử", layout="wide")

@st.cache_resource
def init_spark():
    try:
        spark = SparkSession.builder \
            .appName("RevenuePredictor") \
            .master("local[1]") \
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
    st.info("Mô hình sử dụng: Random Forest (R² ~ 96.6%)")
    
    spark = init_spark()
    model_path = download_model()
    
    if not spark or not model_path:
        st.warning("Đang khởi tạo hệ thống...")
        return

    try:
        model = PipelineModel.load(model_path)
        st.success("✅ Hệ thống đã sẵn sàng!")
        
        # Bố trí các ô nhập liệu
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Loại Sản Phẩm (Category)", ["Electronics", "Home & Kitchen", "Clothing", "Books", "Toys"])
            region = st.selectbox("Khu Vực (Region)", ["North", "South", "East", "West"])
            units_sold = st.number_input("Số Lượng Bán (Units Sold)", min_value=1, value=100)
            discount_val = st.slider("Mức Giảm Giá (Discount %)", 0.0, 1.0, 0.1) # Thường là từ 0 đến 1 trong dữ liệu mẫu

        with col2:
            ad_spend = st.number_input("Chi Phí Quảng Cáo ($)", min_value=0.0, value=200.0)
            clicks = st.number_input("Số Lượt Click (Clicks)", min_value=0, value=50) # THÊM BIẾN BỊ THIẾU
            # Hai biến dưới đây có thể không dùng trong model nhưng dùng để tính lợi nhuận
            reviews = st.slider("Đánh Giá (Reviews - tham khảo)", 1.0, 5.0, 4.0)
            shipping = st.number_input("Phí Vận Chuyển ($)", value=5.0)

        if st.button("🔮 Bắt Đầu Dự Báo", use_container_width=True):
            # SCHEMA CHUẨN: Phải chứa các cột mà mô hình mong đợi
            # Dựa trên notebook: Units_Sold, Discount_Applied, Ad_Spend, Clicks, Category, Region
            schema = StructType([
                StructField("Category", StringType(), True),
                StructField("Region", StringType(), True),
                StructField("Units_Sold", IntegerType(), True),
                StructField("Discount_Applied", DoubleType(), True), # Tên cột trong mô hình là Discount_Applied
                StructField("Ad_Spend", DoubleType(), True),
                StructField("Clicks", DoubleType(), True), # Cột Clicks
                # Thêm các cột phụ để tránh lỗi schema nếu mô hình có tham chiếu
                StructField("Customer_Reviews", DoubleType(), True),
                StructField("Shipping_Cost", DoubleType(), True)
            ])
            
            input_data = [(
                str(category), 
                str(region), 
                int(units_sold), 
                float(discount_val), 
                float(ad_spend), 
                float(clicks),
                float(reviews),
                float(shipping)
            )]
            
            df = spark.createDataFrame(input_data, schema)
            
            # Thực hiện transform (dự báo)
            prediction_df = model.transform(df)
            result = prediction_df.collect()[0]["prediction"]
            
            st.divider()
            st.balloons()
            st.header(f"📊 Doanh Thu Dự Báo: ${result:,.2f}")
            
            # Tính toán lợi nhuận
            profit = result - (ad_spend + (shipping * units_sold))
            st.subheader(f"💰 Lợi Nhuận Ước Tính: ${profit:,.2f}")

    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    main()
