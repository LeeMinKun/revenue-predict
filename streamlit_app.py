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
        
        # Tìm thư mục chứa metadata
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
    st.title("🛒 Hệ Thống Dự Báo Doanh Thu Thương Mại Điện Tử")
    
    spark = init_spark()
    model_path = download_and_prepare_model()
    
    if spark and model_path:
        try:
            model = PipelineModel.load(model_path)
            st.success("✅ Mô hình đã sẵn sàng!")
            
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("Loại Sản Phẩm", ["Electronics", "Home & Kitchen", "Clothing", "Books", "Toys"])
                region = st.selectbox("Khu Vực", ["North", "South", "East", "West"])
                units = st.number_input("Số Lượng Bán", min_value=1, value=100)
                is_discount = st.radio("Có áp dụng giảm giá không?", ["Có", "Không"])

            with col2:
                # Nếu không giảm giá thì mức giảm là 0
                discount_slider = st.slider("Mức Giảm Giá (0.01 - 1.0)", 0.01, 1.0, 0.1)
                discount_applied = discount_slider if is_discount == "Có" else 0.0
                
                ads = st.number_input("Chi Phí Quảng Cáo ($)", value=200.0)
                clicks = st.number_input("Số Lượt Click (Clicks)", value=50)
                st.info(f"Mức giảm giá áp dụng vào mô hình: {discount_applied}")

            if st.button("🔮 Dự Báo Doanh Thu", use_container_width=True):
                # SCHEMA CHUẨN từ Notebook Nhom1_KPDLL2.ipynb
                # input_cols = ["Units_Sold", "Discount_Applied", "Ad_Spend", "Clicks", "Cat_Vec", "Reg_Vec"]
                schema = StructType([
                    StructField("Category", StringType(), True),
                    StructField("Region", StringType(), True),
                    StructField("Units_Sold", IntegerType(), True),
                    StructField("Discount_Applied", DoubleType(), True), # PHẢI LÀ DOUBLE
                    StructField("Ad_Spend", DoubleType(), True),
                    StructField("Clicks", DoubleType(), True)
                ])
                
                data = [(str(category), str(region), int(units), float(discount_applied), float(ads), float(clicks))]
                df = spark.createDataFrame(data, schema)
                
                # Dự báo
                pred_df = model.transform(df)
                result = pred_df.collect()[0]["prediction"]
                
                st.divider()
                st.balloons()
                st.header(f"📊 Kết Quả Dự Báo: ${result:,.2f}")
                
        except Exception as e:
            st.error(f"Lỗi load mô hình: {e}")

if __name__ == "__main__":
    main()
