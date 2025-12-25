# 🛒 Ứng Dụng Dự Báo Doanh Thu Thương Mại Điện Tử

Ứng dụng web dự báo doanh thu sử dụng mô hình Random Forest và Streamlit, chạy trên Google Colab.

## 📋 Mục Lục
- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Yêu cầu](#yêu-cầu)
- [Cài đặt](#cài-đặt)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Kỹ thuật](#kỹ-thuật)
- [Troubleshooting](#troubleshooting)

## 🎯 Giới Thiệu

Ứng dụng này được xây dựng dựa trên nghiên cứu phân tích ảnh hưởng của chiến lược giảm giá đến doanh số trong thương mại điện tử. Sử dụng mô hình **Random Forest Regressor** với độ chính xác cao (R² ≈ 96.6%), ứng dụng giúp dự báo doanh thu dựa trên các yếu tố:

- 📦 Loại sản phẩm (Category)
- 🔢 Số lượng bán (Units Sold)
- 💰 Mức giảm giá (Discount %)
- 📢 Chi phí quảng cáo (Ad Spend)
- ⭐ Đánh giá khách hàng (Customer Reviews)
- 🚚 Chi phí vận chuyển (Shipping Cost)

## ✨ Tính Năng

### 1. Dự Báo Doanh Thu
- Dự báo chính xác dựa trên mô hình Random Forest
- Tính toán lợi nhuận ước tính
- Hiển thị doanh thu trên mỗi đơn vị

### 2. Phân Tích Chi Tiết
- Phân tích mức giảm giá
- Đánh giá ROI quảng cáo
- Đánh giá chất lượng sản phẩm

### 3. Gợi Ý Tối Ưu
- Đề xuất cải thiện chiến lược giá
- Gợi ý tối ưu chi phí quảng cáo
- Khuyến nghị về danh mục sản phẩm

### 4. Giao Diện Thân Thiện
- Design hiện đại, dễ sử dụng
- Responsive layout
- Real-time prediction
- Visual feedback

## 📦 Yêu Cầu

### Phần mềm:
- Python 3.7+
- Google Colab (khuyến nghị)
- Trình duyệt web hiện đại

### Thư viện Python:
```
streamlit
pyspark
pandas
numpy
```

## 🚀 Cài Đặt

### Phương pháp 1: Sử dụng Google Colab (Khuyến nghị)

1. **Upload các file lên Google Colab:**
   - `Streamlit_App_Colab.ipynb`
   - `Nhom1_KPDLL2.ipynb` (notebook gốc)

2. **Chạy notebook gốc để tạo mô hình:**
   ```python
   # Mở và chạy Nhom1_KPDLL2.ipynb
   # Đảm bảo chạy đến cell cuối để lưu mô hình
   ```

3. **Mở và chạy Streamlit_App_Colab.ipynb:**
   - Chạy lần lượt các cell
   - Đợi URL công khai được tạo
   - Truy cập URL để sử dụng ứng dụng

### Phương pháp 2: Chạy local

```bash
# Clone repository hoặc tải file
git clone <repository-url>

# Di chuyển vào thư mục
cd streamlit-revenue-predictor

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run app.py
```

## 📖 Hướng Dẫn Sử Dụng

### Bước 1: Khởi động ứng dụng

**Trên Google Colab:**
1. Mở `Streamlit_App_Colab.ipynb`
2. Chạy cell "Bước 4: Chạy ứng dụng Streamlit"
3. Đợi URL được tạo (dạng: `https://xxxxx.loca.lt`)
4. Click vào URL hoặc copy-paste vào trình duyệt

**Trên local:**
```bash
streamlit run app.py
```

### Bước 2: Nhập thông tin

1. **Chọn loại sản phẩm:**
   - Electronics (Điện tử)
   - Home & Kitchen (Gia dụng)
   - Clothing (Thời trang)
   - Books (Sách)
   - Toys (Đồ chơi)

2. **Nhập các thông số:**
   - Số lượng bán: 1-1000 đơn vị
   - Mức giảm giá: 0-50%
   - Chi phí quảng cáo: $0-$10,000
   - Đánh giá khách hàng: 1-5 sao
   - Chi phí vận chuyển: $0-$100

### Bước 3: Xem kết quả

Sau khi nhấn "🔮 Dự Báo Doanh Thu", bạn sẽ thấy:

1. **Metrics chính:**
   - Doanh thu dự báo
   - Lợi nhuận ước tính
   - Doanh thu/đơn vị

2. **Phân tích chi tiết:**
   - Thông tin đầu vào
   - Đánh giá các chỉ số
   - ROI quảng cáo

3. **Gợi ý tối ưu:**
   - Cải thiện chiến lược giá
   - Tối ưu quảng cáo
   - Đầu tư danh mục sản phẩm

## 📁 Cấu Trúc Dự Án

```
streamlit-revenue-predictor/
│
├── app.py                          # File chính của ứng dụng Streamlit
├── Streamlit_App_Colab.ipynb      # Notebook để chạy trên Colab
├── Nhom1_KPDLL2.ipynb             # Notebook gốc (training model)
├── README.md                       # File này
├── requirements.txt                # Danh sách thư viện
│
└── models/
    └── random_forest_v1/          # Mô hình đã lưu
        ├── metadata/
        └── stages/
```

## 🔧 Kỹ Thuật

### Mô Hình Machine Learning

**Random Forest Regressor:**
- Số cây: 20
- Độ sâu tối đa: 8
- Seed: 42
- Features: 6 biến đầu vào

**Hiệu suất:**
- R² Score: ~96.6%
- RMSE: Thấp
- MAPE: Thấp

### Pipeline xử lý:
1. StringIndexer (Category)
2. OneHotEncoder
3. VectorAssembler
4. StandardScaler
5. RandomForestRegressor

### Công nghệ sử dụng:

- **Frontend:** Streamlit
- **Backend:** PySpark MLlib
- **ML Framework:** Apache Spark
- **Deployment:** Google Colab + LocalTunnel

## 🐛 Troubleshooting

### Lỗi: "Không thể tải mô hình"

**Nguyên nhân:** Mô hình chưa được tạo hoặc đường dẫn sai

**Giải pháp:**
```python
# Kiểm tra xem mô hình có tồn tại không
import os
os.path.exists("models/random_forest_v1")

# Nếu False, chạy lại notebook gốc để tạo mô hình
```

### Lỗi: LocalTunnel không hoạt động

**Giải pháp 1 - Sử dụng ngrok:**
```python
!pip install pyngrok
from pyngrok import ngrok

# Chạy streamlit trong background
import subprocess
import threading

def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py", "--server.port", "8501"])

thread = threading.Thread(target=run_streamlit)
thread.start()

# Tạo public URL
public_url = ngrok.connect(8501)
print(f"Public URL: {public_url}")
```

**Giải pháp 2 - Sử dụng Colab URL:**
```python
# Cài đặt pyngrok
!pip install pyngrok
from pyngrok import ngrok

# Set auth token (lấy từ ngrok.com)
ngrok.set_auth_token("YOUR_AUTH_TOKEN")

# Tạo tunnel
public_url = ngrok.connect(8501)
print(public_url)
```

### Lỗi: Streamlit chạy chậm

**Giải pháp:**
1. Restart runtime trong Colab
2. Xóa cache:
   ```python
   # Trong Colab
   !rm -rf ~/.streamlit/cache
   ```
3. Giảm số lượng features trong form

### Lỗi: Spark không khởi động

**Giải pháp:**
```python
# Cài đặt lại PySpark
!pip uninstall -y pyspark
!pip install pyspark

# Hoặc set JAVA_HOME
import os
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-11-openjdk-amd64'
```

### Lỗi: Memory overflow

**Giải pháp:**
```python
# Tăng memory cho Spark
spark = SparkSession.builder \
    .appName("RevenuePredictor") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .getOrCreate()
```

## 💡 Tips & Best Practices

### Để có kết quả dự báo tốt nhất:

1. **Chọn danh mục phù hợp:**
   - Electronics và Home & Kitchen có ROI cao nhất
   - Clothing phù hợp cho chiến dịch giảm giá

2. **Tối ưu mức giảm giá:**
   - Giữ ở mức 10-15% cho lợi nhuận tốt
   - Tránh giảm giá trên 20%

3. **Quản lý chi phí quảng cáo:**
   - Mục tiêu ROI >= 3x
   - Đầu tư nhiều hơn vào danh mục có margin cao

4. **Duy trì chất lượng:**
   - Đánh giá >= 4 sao
   - Phản hồi nhanh với khách hàng

## 📊 Insights từ Mô Hình

### Top 5 yếu tố quan trọng:

1. **Category (Loại sản phẩm)** - 40%
   - Quyết định chính đến quy mô doanh thu
   - Electronics > Home & Kitchen > Others

2. **Units_Sold (Số lượng)** - 25%
   - Tỷ lệ thuận với doanh thu

3. **Ad_Spend (Chi phí QC)** - 15%
   - Quan trọng cho nhận diện thương hiệu

4. **Customer_Reviews (Đánh giá)** - 12%
   - Ảnh hưởng đến conversion rate

5. **Discount (Giảm giá)** - 8%
   - Tác động ngược chiều nếu quá cao

## 🤝 Đóng Góp

Nếu bạn muốn đóng góp cho dự án:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

Dự án này được phát triển cho mục đích học tập và nghiên cứu.

## 👥 Tác Giả

Nhóm 1 - Phân tích dữ liệu lớn với Apache Spark

## 📧 Liên Hệ

Nếu có câu hỏi hoặc gặp vấn đề, vui lòng:
- Tạo issue trên GitHub
- Email: [your-email@example.com]

## 🙏 Acknowledgments

- Apache Spark team
- Streamlit team
- Google Colab platform

---

**Chúc bạn thành công với ứng dụng dự báo doanh thu! 🎉**
