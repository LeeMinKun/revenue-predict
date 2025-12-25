# 🛒 HỆ THỐNG DỰ BÁO DOANH SỐ

## 📋 Mục Lục
- [Giới thiệu](#-giới-thiệu)
- [Tính năng chính](#-tính-năng-chính)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Kiến trúc kỹ thuật](#-kiến-trúc-kỹ-thuật)
- [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
- [Thông số mô hình](#-thông-số-mô-hình)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Giới Thiệu

Ứng dụng này được phát triển dựa trên đề tài nghiên cứu **"Phân tích ảnh hưởng của chiến lược giảm giá đến doanh số trong thương mại điện tử bằng Apache Spark"**. Hệ thống sử dụng mô hình **Random Forest Regressor** với khả năng xử lý phi tuyến tính và song song, đạt độ chính xác cao (**R² ≈ 96.6%**).

### Kết quả nghiên cứu chính:

- **Loại sản phẩm (Category)** là yếu tố quan trọng nhất quyết định doanh thu (40% tầm quan trọng)
- Electronics và Home & Kitchen là 2 danh mục có tiềm năng doanh thu cao nhất
- Mức giảm giá có tác động ngược chiều nếu quá cao (>20%), không nên lạm dụng
- Tối ưu hóa danh mục sản phẩm hiệu quả hơn việc tăng mức giảm giá

### Các yếu tố đầu vào:

- 📦 **Loại sản phẩm (Category):** Electronics, Home & Kitchen, Clothing, Books, Toys
- 🔢 **Số lượng bán (Units Sold):** Sản lượng đơn hàng dự kiến (1-1000 đơn vị)
- 💰 **Mức giảm giá (Discount):** Tỷ lệ chiết khấu (0%-50%)
- 📢 **Chi phí quảng cáo (Ad Spend):** Ngân sách Marketing đầu tư ($0-$10,000)
- ⭐ **Đánh giá khách hàng (Customer Reviews):** Điểm đánh giá trung bình (1-5 sao)
- 🚚 **Chi phí vận chuyển (Shipping Cost):** Chi phí giao hàng ($0-$100)

---

## ✨ Tính Năng Chính

### 1. Dự Báo Thời Gian Thực
- Trả kết quả doanh thu ngay lập tức khi thay đổi tham số đầu vào
- Tính toán lợi nhuận ước tính sau khi trừ chi phí Marketing và vận chuyển
- Hiển thị doanh thu trên mỗi đơn vị bán

### 2. Phân Tích Chi Tiết
- Đánh giá mức độ hợp lý của chiết khấu
- Tính toán ROI (Return on Investment) của chiến dịch quảng cáo
- Đánh giá chất lượng sản phẩm dựa trên Customer Reviews

### 3. Gợi Ý Tối Ưu Hóa
- Đề xuất cải thiện chiến lược giá
- Gợi ý tối ưu chi phí quảng cáo
- Khuyến nghị về danh mục sản phẩm có tiềm năng cao

### 4. Dashboard Hiệu Suất
- Hiển thị công khai các chỉ số R² và tham số kỹ thuật (số cây, độ sâu)
- Trực quan hóa Feature Importance - mức độ quan trọng của từng biến
- Củng cố tính minh bạch và niềm tin vào kết quả dự báo

---

## 📁 Cấu Trúc Dự Án

```text
revenue-predictor-app/
├── streamlit_app.py        # File chạy chính của ứng dụng Web
├── Nhom1_KPDLL2.ipynb      # Notebook nghiên cứu (Tiền xử lý & Huấn luyện)
├── requirements.txt        # Danh sách thư viện cần cài đặt
├── README.md               # Tài liệu hướng dẫn này
├── DEPLOY_GUIDE.md         # Hướng dẫn deploy lên Streamlit Cloud
├── QUICK_START.md          # Hướng dẫn nhanh 3 cách sử dụng
└── models/
    └── random_forest_v1/   # PipelineModel lưu trữ cấu trúc mô hình (trên Google Drive)
```

---

## 🔧 Kiến Trúc Kỹ Thuật

### Pipeline Xử Lý (Spark ML):

1. **StringIndexer:** Chuyển đổi biến phân loại (Category) thành số
2. **OneHotEncoder:** Mã hóa one-hot cho Category
3. **VectorAssembler:** Tập hợp các đặc trưng thành Vector đầu vào
4. **StandardScaler (Z-score):** Chuẩn hóa dữ liệu về cùng quy mô
5. **RandomForestRegressor:** Thực hiện thuật toán dự báo cốt lõi

### So sánh với Linear Regression:

| Mô hình | R² Score | RMSE | Ưu điểm |
|---------|----------|------|---------|
| Linear Regression | 86.4% | Cao | Đơn giản, dễ giải thích |
| **Random Forest** | **96.6%** | **Thấp hơn 50%** | **Xử lý phi tuyến, chống overfitting** |

### Công Nghệ:

- **Ngôn ngữ:** Python 3.8+
- **Backend:** Apache Spark (PySpark) 3.4+
- **Frontend:** Streamlit 1.28+
- **ML Framework:** Spark MLlib
- **Deployment:** Streamlit Community Cloud
- **Model Storage:** Google Drive (với gdown)

---

## 📖 Hướng Dẫn Sử Dụng

### Phương án 1: Truy cập trực tiếp (Khuyến nghị)

Hệ thống đã được triển khai sẵn trên **Streamlit Cloud**. Bạn chỉ cần truy cập vào liên kết:

🔗 **[https://your-app-url.streamlit.app](https://your-app-url.streamlit.app)**

### Phương án 2: Chạy trên Google Colab

1. Upload file `Streamlit_App_Colab.ipynb` lên Google Colab
2. Chạy lần lượt các cell trong notebook
3. Lấy URL công khai và truy cập

📖 **Xem chi tiết:** [QUICK_START.md](./QUICK_START.md)

### Phương án 3: Chạy local

```bash
# Clone repository
git clone https://github.com/your-username/revenue-predictor-app.git
cd revenue-predictor-app

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run streamlit_app.py
```

**Lưu ý:** Phải có thư mục `models/random_forest_v1/` trong cùng folder

---

## 🎮 Thao Tác Dự Báo

### Bước 1: Nhập thông tin sản phẩm

1. **Chọn loại sản phẩm** từ dropdown:
   - Electronics (Điện tử) - ROI cao nhất
   - Home & Kitchen (Gia dụng) - Tiềm năng lớn
   - Clothing (Thời trang)
   - Books (Sách)
   - Toys (Đồ chơi)

2. **Nhập các thông số kinh doanh:**
   - Số lượng bán dự kiến
   - Mức giảm giá (%): Khuyến nghị 10-15%
   - Chi phí quảng cáo: Mục tiêu ROI >= 3x
   - Đánh giá khách hàng: Nên >= 4 sao
   - Chi phí vận chuyển

### Bước 2: Xem kết quả

Nhấn nút **"🔮 DỰ BÁO DOANH THU"** để nhận:

- **Metrics chính:**
  - 💰 Doanh thu dự báo
  - 📊 Lợi nhuận ước tính
  - 📈 Doanh thu/đơn vị

- **Phân tích chi tiết:**
  - Đánh giá mức giảm giá
  - ROI quảng cáo
  - Đánh giá chất lượng

- **Gợi ý tối ưu:**
  - Cải thiện chiến lược
  - Tối ưu chi phí
  - Đầu tư danh mục

---

## 📊 Thông Số Mô Hình

### Cấu hình Random Forest:

- **Số lượng cây (numTrees):** 20
- **Độ sâu tối đa (maxDepth):** 8
- **Seed:** 42 (reproducibility)
- **Features:** 6 biến đầu vào

### Hiệu suất (10-Fold Cross Validation):

- **R² Score:** 96.6% (±0.5%)
- **RMSE:** Giảm 50% so với Linear Regression
- **MAE:** Thấp
- **MAPE:** Thấp

### Feature Importance (Theo thứ tự):

1. **Category (Loại sản phẩm)** - 40% ⭐⭐⭐⭐⭐
2. **Units_Sold (Số lượng)** - 25% ⭐⭐⭐⭐
3. **Ad_Spend (Chi phí QC)** - 15% ⭐⭐⭐
4. **Customer_Reviews (Đánh giá)** - 12% ⭐⭐
5. **Discount (Giảm giá)** - 8% ⭐

### Phương pháp chuẩn hóa:

- **StandardScaler:** Z-score Standardization
- **Formula:** z = (x - μ) / σ
- **Áp dụng cho:** Tất cả biến số sau khi encoding

---

## 💡 Insights Từ Nghiên Cứu

### Phát hiện chính:

1. **"Loại sản phẩm" quan trọng hơn "Mức giảm giá"**
   - Random Forest phát hiện: Category quyết định 40% doanh thu
   - Linear Regression đã bỏ sót insight này do giả định tuyến tính

2. **Tác động ngược chiều của giảm giá quá cao**
   - Giảm giá > 20% có thể làm giảm lợi nhuận
   - Không nên lạm dụng chiến lược giảm giá sâu

3. **Danh mục có ROI cao nhất:**
   - Electronics: Margin cao, đầu tư marketing hiệu quả
   - Home & Kitchen: Tiềm năng lớn, nên mở rộng

4. **Đánh giá khách hàng quan trọng:**
   - Review >= 4 sao tăng conversion rate đáng kể
   - Nên đầu tư vào chất lượng sản phẩm/dịch vụ

### Khuyến nghị chiến lược:

✅ **Nên làm:**
- Tập trung vào Electronics và Home & Kitchen
- Duy trì giảm giá ở mức 10-15%
- Đầu tư marketing có mục tiêu (ROI >= 3x)
- Cải thiện đánh giá khách hàng lên >= 4 sao

❌ **Không nên:**
- Giảm giá quá sâu (> 20%)
- Đầu tư marketing mù quáng
- Bỏ qua chất lượng sản phẩm

---

## 🐛 Troubleshooting

### Lỗi khởi động chậm

**Nguyên nhân:** Apache Spark cần thời gian nạp Java (JVM) trên Cloud (Cold Start)

**Giải pháp:** 
- Đợi 2-3 phút cho lần truy cập đầu tiên
- Các lần sau sẽ nhanh hơn

### Lỗi "Model not found"

**Nguyên nhân:** 
- Mô hình chưa được tải từ Google Drive
- FOLDER_ID trong code chưa đúng

**Giải pháp:**
1. Kiểm tra thông báo "🔄 Đang tải mô hình từ Google Drive..."
2. Nếu lỗi, kiểm tra FOLDER_ID trong `streamlit_app.py` (dòng 47)
3. Đảm bảo thư mục Drive đã được chia sẻ công khai
4. Refresh lại trình duyệt

### Lỗi "Out of Memory"

**Nguyên nhân:** Streamlit Cloud free tier giới hạn 1GB RAM

**Giải pháp:**
- Tối ưu mô hình (giảm số cây xuống 15, độ sâu xuống 6)
- Hoặc upgrade lên Streamlit Cloud Pro ($20/tháng)

### App bị "sleep"

**Nguyên nhân:** Không được truy cập trong 7 ngày (free tier)

**Giải pháp:**
- Click "Yes, wake it up!" khi được hỏi
- App sẽ khởi động lại trong 10-20 giây
- Hoặc upgrade để app chạy 24/7

### Tải mô hình từ Drive quá chậm

**Giải pháp:**
1. Nén mô hình thành file .zip
2. Upload .zip lên Drive
3. Sửa code để tải và giải nén file .zip

---

## 📚 Tài Liệu Bổ Sung

- 📖 [QUICK_START.md](./QUICK_START.md) - So sánh 3 cách sử dụng
- 🚀 [DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md) - Hướng dẫn chi tiết deploy
- 📓 [Nhom1_KPDLL2.ipynb](./Nhom1_KPDLL2.ipynb) - Notebook nghiên cứu đầy đủ

---

## 👥 Tác Giả

**Nhóm 1** - Phân tích dữ liệu lớn với Apache Spark
---

## 📧 Liên Hệ

Nếu có câu hỏi hoặc gặp vấn đề:
- 📧 Email: cuongmvpdz1@gmail.com

---
## 🙏 Acknowledgments

- **Apache Spark** - Framework xử lý dữ liệu lớn
- **Streamlit** - Framework tạo web app nhanh chóng
- **Google Colab** - Môi trường phát triển miễn phí
- **Streamlit Community Cloud** - Nền tảng hosting miễn phí

---


**Dự án được thực hiện nhằm mục đích học tập và nghiên cứu ứng dụng ML trong kinh doanh. 🎉**

**⭐ Nếu thấy hữu ích, hãy cho repo một star nhé!**
