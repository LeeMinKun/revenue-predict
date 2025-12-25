import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import os
import gdown
import shutil

import os

# Thiết lập JAVA_HOME để PySpark có thể tìm thấy Java sau khi cài đặt từ packages.txt
if not os.environ.get("JAVA_HOME"):
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"

# Cấu hình trang
st.set_page_config(
    page_title="Dự Báo Doanh Thu Thương Mại Điện Tử",
    page_icon="📊",
    layout="wide"
)

# Khởi tạo Spark Session
@st.cache_resource
def init_spark():
    spark = SparkSession.builder \
        .appName("RevenuePredictor") \
        .master("local[*]") \
        .config("spark.ui.showConsoleProgress", "false") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark

# Tải mô hình từ Google Drive
@st.cache_resource
def download_model_from_drive():
    """
    Tải mô hình từ Google Drive nếu chưa có trong local
    """
    model_path = "models/random_forest_v1"
    
    # Nếu mô hình đã tồn tại, không cần tải lại
    if os.path.exists(model_path):
        return model_path
    
    st.info("🔄 Đang tải mô hình từ Google Drive... (chỉ mất vài phút lần đầu tiên)")
    
    try:
        # ID của thư mục Google Drive chứa mô hình
        # QUAN TRỌNG: Thay YOUR_FOLDER_ID bằng ID thực tế của thư mục Drive
        # Cách lấy ID: Right-click folder > Get link > Copy phần sau /folders/
        folder_id = "1ESwDvLGSlxRXFgnNqW-LPC9ETZbN6tkQ?usp=sharing"  # ⚠️ THAY ĐỔI DÒNG NÀY
        
        # Tạo thư mục models nếu chưa có
        os.makedirs("models", exist_ok=True)
        
        # Tải thư mục từ Google Drive
        url = f"https://drive.google.com/drive/folders/{folder_id}"
        gdown.download_folder(url, output="models/", quiet=False, use_cookies=False)
        
        st.success("✅ Tải mô hình thành công!")
        return model_path
        
    except Exception as e:
        st.error(f"❌ Không thể tải mô hình từ Google Drive: {e}")
        st.info("""
        💡 Hướng dẫn khắc phục:
        1. Đảm bảo mô hình đã được upload lên Google Drive
        2. Chia sẻ thư mục với quyền 'Anyone with the link can view'
        3. Copy FOLDER_ID và thay vào dòng 47 của file streamlit_app.py
        4. Redeploy app
        
        Hoặc bạn có thể chạy app trên Google Colab với mô hình local.
        """)
        return None

# Load mô hình đã lưu
@st.cache_resource
def load_model(_spark):
    try:
        # Tải mô hình từ Drive nếu chưa có
        model_path = download_model_from_drive()
        
        if model_path is None:
            return None
        
        # Load mô hình PySpark
        model = PipelineModel.load(model_path)
        return model
        
    except Exception as e:
        st.error(f"Không thể tải mô hình: {e}")
        return None

# Hàm dự báo
def predict_revenue(spark, model, input_data):
    """
    Dự báo doanh thu dựa trên dữ liệu đầu vào
    """
    # Định nghĩa schema
    schema = StructType([
        StructField("Category", StringType(), True),
        StructField("Units_Sold", IntegerType(), True),
        StructField("Discount", DoubleType(), True),
        StructField("Ad_Spend", DoubleType(), True),
        StructField("Customer_Reviews", DoubleType(), True),
        StructField("Shipping_Cost", DoubleType(), True)
    ])
    
    # Tạo DataFrame từ input
    df = spark.createDataFrame([input_data], schema=schema)
    
    # Dự báo
    predictions = model.transform(df)
    
    # Lấy kết quả
    result = predictions.select("prediction").collect()[0][0]
    return result

# Giao diện chính
def main():
    # Header
    st.title("🛒 Hệ Thống Dự Báo Doanh Thu Thương Mại Điện Tử")
    st.markdown("---")
    
    # Khởi tạo Spark và load model
    spark = init_spark()
    model = load_model(spark)
    
    if model is None:
        st.error("⚠️ Không thể tải mô hình. Vui lòng kiểm tra cấu hình.")
        st.info("""
        📌 **Đang chạy trên Streamlit Cloud?**
        
        Hãy đảm bảo:
        1. Đã upload mô hình lên Google Drive
        2. Đã cập nhật FOLDER_ID trong code (dòng 47)
        3. Thư mục Drive đã được chia sẻ công khai
        
        📌 **Đang chạy local/Colab?**
        
        Đảm bảo thư mục `models/random_forest_v1` tồn tại.
        """)
        return
    
    st.success("✅ Mô hình Random Forest đã sẵn sàng!")
    
    # Sidebar - Thông tin mô hình
    with st.sidebar:
        st.header("📈 Thông Tin Mô Hình")
        st.markdown("""
        **Mô hình:** Random Forest Regressor
        
        **Hiệu suất:**
        - R² Score: ~96.6%
        - RMSE: Thấp
        - MAPE: Thấp
        
        **Đặc điểm:**
        - Số cây: 20
        - Độ sâu tối đa: 8
        - Khả năng xử lý phi tuyến tính
        """)
        
        st.markdown("---")
        st.markdown("### 🎯 Hướng dẫn sử dụng")
        st.markdown("""
        1. Nhập thông tin sản phẩm
        2. Nhấn nút "Dự Báo Doanh Thu"
        3. Xem kết quả dự báo
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Nhập Thông Tin Sản Phẩm")
        
        # Form nhập liệu
        with st.form("prediction_form"):
            # Loại sản phẩm
            category = st.selectbox(
                "Loại Sản Phẩm (Category)",
                options=["Electronics", "Home & Kitchen", "Clothing", "Books", "Toys"],
                help="Chọn danh mục sản phẩm"
            )
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                # Số lượng bán
                units_sold = st.number_input(
                    "Số Lượng Bán (Units Sold)",
                    min_value=1,
                    max_value=1000,
                    value=50,
                    step=1,
                    help="Số lượng sản phẩm đã bán"
                )
                
                # Mức giảm giá
                discount = st.slider(
                    "Mức Giảm Giá (Discount %)",
                    min_value=0.0,
                    max_value=50.0,
                    value=10.0,
                    step=0.5,
                    help="Phần trăm giảm giá (0-50%)"
                )
                
                # Chi phí quảng cáo
                ad_spend = st.number_input(
                    "Chi Phí Quảng Cáo (Ad Spend $)",
                    min_value=0.0,
                    max_value=10000.0,
                    value=500.0,
                    step=50.0,
                    help="Chi phí đầu tư vào quảng cáo"
                )
            
            with col_b:
                # Đánh giá khách hàng
                customer_reviews = st.slider(
                    "Đánh Giá Khách Hàng (Customer Reviews)",
                    min_value=1.0,
                    max_value=5.0,
                    value=4.0,
                    step=0.1,
                    help="Điểm đánh giá trung bình (1-5 sao)"
                )
                
                # Chi phí vận chuyển
                shipping_cost = st.number_input(
                    "Chi Phí Vận Chuyển (Shipping Cost $)",
                    min_value=0.0,
                    max_value=100.0,
                    value=5.0,
                    step=1.0,
                    help="Chi phí vận chuyển cho mỗi đơn hàng"
                )
                
                # Nút dự báo với khoảng trống
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Nút submit
            submitted = st.form_submit_button("🔮 Dự Báo Doanh Thu", use_container_width=True)
        
        # Xử lý khi nhấn nút
        if submitted:
            with st.spinner("Đang dự báo..."):
                # Chuẩn bị dữ liệu
                input_data = {
                    "Category": category,
                    "Units_Sold": units_sold,
                    "Discount": discount,
                    "Ad_Spend": ad_spend,
                    "Customer_Reviews": customer_reviews,
                    "Shipping_Cost": shipping_cost
                }
                
                try:
                    # Dự báo
                    predicted_revenue = predict_revenue(spark, model, input_data)
                    
                    # Hiển thị kết quả
                    st.markdown("---")
                    st.header("📊 Kết Quả Dự Báo")
                    
                    result_col1, result_col2, result_col3 = st.columns(3)
                    
                    with result_col1:
                        st.metric(
                            label="Doanh Thu Dự Báo",
                            value=f"${predicted_revenue:,.2f}",
                            delta=None
                        )
                    
                    with result_col2:
                        profit_margin = predicted_revenue - (ad_spend + (shipping_cost * units_sold))
                        st.metric(
                            label="Lợi Nhuận Ước Tính",
                            value=f"${profit_margin:,.2f}",
                            delta="Sau trừ chi phí"
                        )
                    
                    with result_col3:
                        revenue_per_unit = predicted_revenue / units_sold if units_sold > 0 else 0
                        st.metric(
                            label="Doanh Thu / Đơn Vị",
                            value=f"${revenue_per_unit:,.2f}",
                            delta=None
                        )
                    
                    # Phân tích chi tiết
                    st.markdown("---")
                    st.subheader("📋 Phân Tích Chi Tiết")
                    
                    analysis_col1, analysis_col2 = st.columns(2)
                    
                    with analysis_col1:
                        st.markdown("**Thông Tin Đầu Vào:**")
                        st.markdown(f"""
                        - Loại sản phẩm: **{category}**
                        - Số lượng bán: **{units_sold:,} đơn vị**
                        - Mức giảm giá: **{discount}%**
                        - Chi phí quảng cáo: **${ad_spend:,.2f}**
                        - Đánh giá: **{customer_reviews}/5 ⭐**
                        - Chi phí vận chuyển: **${shipping_cost:,.2f}**
                        """)
                    
                    with analysis_col2:
                        st.markdown("**Phân Tích Kết Quả:**")
                        
                        # Đánh giá mức giảm giá
                        if discount < 10:
                            discount_analysis = "✅ Mức giảm giá hợp lý, giữ được lợi nhuận"
                        elif discount < 20:
                            discount_analysis = "⚠️ Mức giảm giá khá cao, cần cân nhắc lợi nhuận"
                        else:
                            discount_analysis = "❌ Mức giảm giá quá cao, có thể ảnh hưởng lợi nhuận"
                        
                        # Đánh giá ROI quảng cáo
                        ad_roi = (predicted_revenue / ad_spend) if ad_spend > 0 else 0
                        if ad_roi > 5:
                            ad_analysis = f"✅ ROI quảng cáo tốt ({ad_roi:.2f}x)"
                        elif ad_roi > 2:
                            ad_analysis = f"⚠️ ROI quảng cáo chấp nhận được ({ad_roi:.2f}x)"
                        else:
                            ad_analysis = f"❌ ROI quảng cáo thấp ({ad_roi:.2f}x)"
                        
                        st.markdown(f"""
                        - {discount_analysis}
                        - {ad_analysis}
                        - Đánh giá khách hàng: **{'✅ Tốt' if customer_reviews >= 4 else '⚠️ Cần cải thiện'}**
                        """)
                    
                    # Gợi ý tối ưu
                    st.markdown("---")
                    st.subheader("💡 Gợi Ý Tối Ưu Hóa")
                    
                    suggestions = []
                    
                    if discount > 15:
                        suggestions.append("🔸 Cân nhắc giảm mức chiết khấu để cải thiện biên lợi nhuận")
                    
                    if customer_reviews < 4:
                        suggestions.append("🔸 Tập trung cải thiện chất lượng sản phẩm/dịch vụ để tăng đánh giá")
                    
                    if ad_roi < 3:
                        suggestions.append("🔸 Tối ưu chiến dịch quảng cáo để cải thiện ROI")
                    
                    if category in ["Electronics", "Home & Kitchen"]:
                        suggestions.append("🔸 Danh mục sản phẩm có tiềm năng cao, nên đầu tư thêm vào marketing")
                    
                    if suggestions:
                        for suggestion in suggestions:
                            st.markdown(suggestion)
                    else:
                        st.success("✅ Các chỉ số đều ở mức tốt!")
                
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi khi dự báo: {e}")
    
    with col2:
        st.header("📊 Thông Tin Tham Khảo")
        
        # Hiển thị importance của các features
        st.markdown("### Các Yếu Tố Quan Trọng")
        st.markdown("""
        Theo mô hình Random Forest, các yếu tố ảnh hưởng đến doanh thu:
        
        1. **Loại Sản Phẩm (Category)** 🏆
           - Quan trọng nhất
           - Electronics và Home & Kitchen có doanh thu cao
        
        2. **Số Lượng Bán (Units Sold)** 📦
           - Ảnh hưởng trực tiếp đến tổng doanh thu
        
        3. **Chi Phí Quảng Cáo (Ad Spend)** 📢
           - Tăng độ nhận diện thương hiệu
        
        4. **Đánh giá Khách Hàng** ⭐
           - Ảnh hưởng đến tỷ lệ chuyển đổi
        
        5. **Mức Giảm Giá (Discount)** 💰
           - Tác động ngược chiều nếu quá cao
        """)
        
        st.markdown("---")
        
        # Tips
        st.markdown("### 💡 Mẹo Tăng Doanh Thu")
        st.info("""
        ✓ Tập trung vào sản phẩm Electronics và Home & Kitchen
        
        ✓ Tối ưu hóa danh mục sản phẩm hơn là tăng giảm giá
        
        ✓ Duy trì đánh giá khách hàng >= 4 sao
        
        ✓ Đầu tư quảng cáo có mục tiêu rõ ràng
        
        ✓ Kiểm soát chi phí vận chuyển hợp lý
        """)

if __name__ == "__main__":
    main()
