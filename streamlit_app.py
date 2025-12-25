# ... (Giữ nguyên các phần khai báo Spark và Model) ...

def main():
    st.title("🛒 Hệ Thống Dự Báo Doanh Thu")
    
    spark = init_spark()
    model_path = download_and_prepare_model()
    
    if spark and model_path:
        try:
            model = PipelineModel.load(model_path)
            st.success("✅ Mô hình đã sẵn sàng!")
            
            col1, col2 = st.columns(2)
            with col1:
                # CẬP NHẬT: Danh sách Ngành hàng chính xác từ Notebook
                category = st.selectbox("Loại Sản Phẩm", 
                    ["Electronics", "Clothing", "Books", "Home Appliances", "Toys"])
                
                # CẬP NHẬT: Danh sách Khu vực chính xác từ Notebook
                region = st.selectbox("Khu Vực (Region)", 
                    ["North America", "Europe", "Asia", "South America", "Oceania"])
                
                units = st.number_input("Số Lượng Bán", min_value=1, value=100)
                is_discount = st.radio("Có áp dụng giảm giá không?", ["Có", "Không"])

            with col2:
                discount_slider = st.slider("Mức Giảm Giá (0.01 - 1.0)", 0.01, 1.0, 0.1)
                discount_applied = discount_slider if is_discount == "Có" else 0.0
                
                ads = st.number_input("Chi Phí Quảng Cáo ($)", value=200.0)
                clicks = st.number_input("Số Lượt Click (Clicks)", value=50)
                
            if st.button("🔮 Dự Báo Doanh Thu", use_container_width=True):
                schema = StructType([
                    StructField("Category", StringType(), True),
                    StructField("Region", StringType(), True),
                    StructField("Units_Sold", IntegerType(), True),
                    StructField("Discount_Applied", DoubleType(), True),
                    StructField("Ad_Spend", DoubleType(), True),
                    StructField("Clicks", DoubleType(), True)
                ])
                
                data = [(str(category), str(region), int(units), float(discount_applied), float(ads), float(clicks))]
                df = spark.createDataFrame(data, schema)
                
                # Thực hiện dự báo
                pred_df = model.transform(df)
                result = pred_df.collect()[0]["prediction"]
                
                st.divider()
                st.balloons()
                st.header(f"📊 Kết Quả Dự Báo: ${result:,.2f}")
                
        except Exception as e:
            st.error(f"Lỗi thực thi: {e}")

if __name__ == "__main__":
    main()
