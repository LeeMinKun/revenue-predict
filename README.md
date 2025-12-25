```markdown
# 🛒 Hệ Thống Dự Báo Doanh Thu Thương Mại Điện Tử

Hệ thống hỗ trợ ra quyết định (DSS) sử dụng Apache Spark và Streamlit để dự báo doanh thu dựa trên các kịch bản chiến lược Marketing và vận hành bán lẻ.

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
Ứng dụng này được phát triển dựa trên đề tài nghiên cứu về ảnh hưởng của các yếu tố quản trị (giảm giá, quảng cáo, khu vực) đến doanh số. Hệ thống sử dụng mô hình **Random Forest Regressor** với khả năng xử lý song song, đạt độ chính xác cao (**R² ≈ 96.6%**).

**Các yếu tố đầu vào:**
- 📦 **Ngành hàng (Category):** Electronics, Clothing, Books, Home Appliances, Toys.
- 📍 **Khu vực (Region):** North America, Europe, Asia, South America, Oceania.
- 🔢 **Số lượng bán (Units Sold):** Sản lượng đơn hàng dự kiến.
- 💰 **Mức giảm giá (Discount):** Tỷ lệ chiết khấu (0.0 - 1.0).
- 📢 **Ngân sách Marketing (Ad Spend):** Chi phí quảng cáo đầu tư.
- 🖱️ **Số lượt Click (Clicks):** Lượt tương tác khách hàng dự tính.

---

## ✨ Tính Năng Chính
### 1. Dự Báo Thời Gian Thực
- Trả kết quả doanh thu ngay khi thay đổi tham số đầu vào.
- Tính toán lợi nhuận ước tính sau khi trừ chi phí Marketing.

### 2. Dashboard Hiệu Suất
- Hiển thị công khai các chỉ số $R^2$ và tham số kỹ thuật (số cây, độ sâu).
- Củng cố tính minh bạch và niềm tin vào kết quả dự báo.

### 3. Phân Tích Feature Importance
- Trực quan hóa mức độ quan trọng của các biến thông qua biểu đồ cột.
- Giúp nhà quản lý nhận diện "biến số động lực" thúc đẩy doanh thu.

---

## 📁 Cấu Trúc Dự Án
```text
revenue-predict/
├── streamlit_app.py        # File chạy chính của ứng dụng Web
├── Nhom1_KPDLL2.ipynb      # Notebook nghiên cứu (Tiền xử lý & Huấn luyện)
├── requirements.txt        # Danh sách thư viện cần cài đặt
├── README.md               # Tài liệu hướng dẫn này
└── models/
    └── random_forest_v1/   # PipelineModel lưu trữ cấu trúc mô hình

```

---

## 🔧 Kiến Trúc Kỹ Thuật

### Pipeline Xử Lý (Spark ML):

1. **StringIndexer & OneHotEncoder:** Xử lý và mã hóa các biến phân loại.
2. **VectorAssembler:** Tập hợp các đặc trưng thành Vector đầu vào.
3. **StandardScaler (Z-score):** Chuẩn hóa dữ liệu về cùng quy mô.
4. **RandomForestRegressor:** Thực hiện thuật toán dự báo cốt lõi.

### Công Nghệ:

* **Ngôn ngữ:** Python 3.11
* **Backend:** Apache Spark (PySpark) 3.x
* **Frontend:** Streamlit Community Cloud
* **Lưu trữ:** GitHub & Google Drive (Model storage)

---

## 📖 Hướng Dẫn Sử Dụng

### 1. Khởi động ứng dụng

Hệ thống đã được triển khai sẵn trên **Streamlit Cloud**. Bạn chỉ cần truy cập vào liên kết ứng dụng được cung cấp trong Repo này.

### 2. Thao tác dự báo

* Nhập các tham số kinh doanh tại các ô tương ứng.
* Nhấn nút **"BẮT ĐẦU DỰ BÁO"**.
* Quan sát kết quả và biểu đồ phân tích trọng số bên dưới.

---

## 📊 Thông Số Mô Hình

* **Số lượng cây (Num Trees):** 20
* **Độ sâu tối đa (Max Depth):** 8
* **Hệ số xác định ():** 96.6%
* **Phương pháp chuẩn hóa:** Z-score Standardization (StandardScaler).

---

## 🐛 Troubleshooting

* **Lỗi khởi động chậm:** Do Apache Spark cần thời gian nạp Java (JVM) trên Cloud (Hiện tượng Cold Start). Vui lòng đợi 2-3 phút cho lần truy cập đầu tiên.
* **Lỗi "Model not found":** Hệ thống sẽ tự động tải mô hình từ Drive. Nếu gặp lỗi, hãy làm mới (Refresh) lại trình duyệt.

---

## 👥 Tác Giả

**Nhóm 1** - Phân tích dữ liệu lớn với Apache Spark.

* Notebook nghiên cứu chi tiết: [Nhom1_KPDLL2.ipynb](https://www.google.com/search?q=./Nhom1_KPDLL2.ipynb)

---

**Dự án được thực hiện nhằm mục đích học tập và nghiên cứu ứng dụng ML trong kinh doanh. 🎉**
