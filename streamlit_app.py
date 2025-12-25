import os
import sys
import zipfile
import shutil
import gdown
import streamlit as st
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# Cấu hình Java 17 cho Streamlit Cloud
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

st.set_page_config(page_title="Dự Báo Doanh Thu", layout="wide")

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
    # Thư mục đích mà Spark sẽ load
    final_model_path = "models/random_forest_v1"
    zip_path = "model.zip"
    extract_path = "models/temp_extract"
    
    if os.path.exists(final_model_path):
        return final_model_path
    
    file_id = "1vOwtKC0wc8CoUONJ6Z45wGLnfOkpQBpY"
    
    try:
        # 1. Tải file dùng ID (tránh lỗi permission URL)
        gdown.download(id=file_id, output=zip_path, quiet=False)
        
        # 2. Giải nén vào thư mục tạm
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        # 3. KIỂM TRA CẤU TRÚC THƯ MỤC (Xử lý lỗi Path Not Found)
        # Tìm xem thư mục 'metadata' nằm ở đâu
        actual_path = extract_path
        for root, dirs, files in os.walk(extract_path):
            if "metadata" in dirs:
                actual_path = root
                break
        
        # 4. Di chuyển về đúng vị trí chuẩn
        os.makedirs("models", exist_ok=True)
        if os.path.exists(final_model_path):
            shutil.rmtree(final_model_path)
        shutil.move(actual_path, final_model_path)
        
        # Dọn dẹp
        if os.path.exists(zip_path): os.remove(zip_path)
        if os.path.exists(extract_path): shutil.rmtree(extract_path)
            
        return final_model_path
    except Exception as e:
        st.error(f"Lỗi chuẩn bị mô hình: {e}")
        return None

def main():
    st.title("🛒 Hệ Thống Dự Báo Doanh Thu")
    
    spark = init_spark()
    # Sử dụng hàm chuẩn hóa đường dẫn mới
    model_path = download_prepare_model() if 'download_prepare_model' in locals() else download_and_prepare_model()
    
    if spark and model_path:
        try:
            # Spark load PipelineModel từ thư mục có chứa folder 'metadata'
            model = PipelineModel.load(model_path)
            st.success("✅ Mô hình đã nạp thành công!")
            
            # Giao diện nhập liệu
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    category = st.selectbox("Loại Sản Phẩm", ["Electronics", "Home & Kitchen", "Clothing", "Books", "Toys"])
                    region = st.selectbox("Khu Vực", ["North", "South", "East", "West"])
                    units = st.number_input("Số Lượng Bán", min_value=1, value=100)
                    disc_app = st.selectbox("Áp dụng giảm giá?", ["Yes", "No"])
                with col2:
                    disc_val = st.slider("Mức Giảm Giá (0.0-1.0)", 0.0, 1.0, 0.1)
                    ads = st.number_input("Quảng Cáo ($)", value=200.0)
                    clicks = st.number_input("Số Lượt Click", value=50)
                    ship = st.number_input("Phí Vận Chuyển ($)", value=5.0)

            if st.button("🔮 Dự Báo Ngay", use_container_width=True):
                schema = StructType([
                    StructField("Category", StringType(), True),
                    StructField("Region", StringType(), True),
                    StructField("Discount_Applied", StringType(), True),
                    StructField("Units_Sold", IntegerType(), True),
                    StructField("Discount", DoubleType(), True),
                    StructField("Ad_Spend", DoubleType(), True),
                    StructField("Clicks", DoubleType(), True),
                    StructField("Customer_Reviews", DoubleType(), True),
                    StructField("Shipping_Cost", DoubleType(), True)
                ])
                
                # Customer_Reviews mặc định 4.0 vì model yêu cầu 9 cột
                data = [(category, region, disc_app, int(units), float(disc_val), float(ads), float(clicks), 4.0, float(ship))]
                df = spark.createDataFrame(data, schema)
                pred = model.transform(df).collect()[0]["prediction"]
                
                st.divider()
                st.header(f"📊 Dự báo: ${pred:,.2f}")
                
        except Exception as e:
            st.error(f"Lỗi load mô hình: {e}")

if __name__ == "__main__":
    main()
