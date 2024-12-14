import streamlit as st
import pandas as pd
from scipy.stats import ttest_ind

st.title("T Testi Uygulaması")

# 1. Dosya yükleme
uploaded_file = st.file_uploader("Lütfen bir CSV dosyası yükleyin", type=["csv"])

if uploaded_file is not None:
    # 2. Yüklenen dosyanın içeriğini göster
    data = pd.read_csv(uploaded_file)
    st.write("Yüklenen Veri:")
    st.dataframe(data)

    # 3. Kullanıcıdan güven düzeyi ve sütun seçimi
    confidence_level = st.selectbox("Güven düzeyi:", [90, 95, 99])
    selected_columns = st.multiselect("T testi yapılacak sütunları seçin (iki sütun):", data.columns)

    if len(selected_columns) == 2:
        # 4. Verilerin uygun olup olmadığını kontrol et
        col1, col2 = selected_columns
        if pd.api.types.is_numeric_dtype(data[col1]) and pd.api.types.is_numeric_dtype(data[col2]):
            # T testi
            alpha = 1 - (confidence_level / 100)
            t_stat, p_value = ttest_ind(data[col1], data[col2], equal_var=False)
            
            # Sonuçları göster
            st.write(f"T istatistiği: {t_stat:.4f}")
            st.write(f"P değeri: {p_value:.4f}")
            if p_value < alpha:
                st.success("Sonuç: H0 hipotezi reddedilir.")
            else:
                st.info("Sonuç: H0 hipotezi reddedilemez.")
        else:
            st.error("Seçilen sütunlar sayısal veri türünde olmalıdır!")
    else:
        st.warning("Lütfen iki sütun seçin!")
else:
    st.info("Bir dosya yüklemeden devam edemezsiniz.")
