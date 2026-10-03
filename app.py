import streamlit as st
st.image("logo.jpg")
import pandas as pd


# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm_Nguyễn Hoàng Anh Duy",
    page_icon="💰",
    layout="centered"
)


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM_Nguyễn Hoàng Anh Duy")
st.write(
    "Nhập thông tin khoản tiền gửi để tính tiền lãi và tổng số tiền nhận được."
)

st.divider()


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=100_000,
        value=100_000_000,
        step=1_000_000,
        format="%d"
    )

with col2:
    ky_han = st.selectbox(
        "Kỳ hạn",
        options=[1, 3, 6, 9, 12, 18, 24, 36],
        format_func=lambda x: f"{x} tháng"
    )

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)


# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    # Lãi suất dạng thập phân
    lai_suat_decimal = lai_suat / 100

    # Tổng lãi theo công thức lãi đơn
    tong_lai = tien_gui * lai_suat_decimal * ky_han / 12

    # Tổng tiền gốc + lãi
    tong_tien = tien_gui + tong_lai

    # =========================
    # TRƯỜNG HỢP CUỐI KỲ
    # =========================
    if hinh_thuc == "Cuối kỳ":

        lai_dinh_ky = tong_lai

        so_ky = 1

        bang_du_lieu = pd.DataFrame({
            "Kỳ nhận lãi": ["Cuối kỳ"],
            "Tiền lãi": [format_money(lai_dinh_ky)]
        })

    # =========================
    # TRƯỜNG HỢP HÀNG THÁNG
    # =========================
    elif hinh_thuc == "Hàng tháng":

        lai_dinh_ky = tien_gui * lai_suat_decimal / 12

        so_ky = ky_han

        bang_du_lieu = pd.DataFrame({
            "Kỳ nhận lãi": [
                f"Tháng {i}" for i in range(1, ky_han + 1)
            ],
            "Tiền lãi": [
                format_money(lai_dinh_ky)
                for _ in range(ky_han)
            ]
        })

    # =========================
    # TRƯỜNG HỢP HÀNG QUÝ
    # =========================
    else:

        lai_dinh_ky = tien_gui * lai_suat_decimal / 4

        so_ky = ky_han // 3

        bang_dulieu_lai = [
            format_money(lai_dinh_ky)
            for _ in range(so_ky)
        ]

        bang_du_lieu = pd.DataFrame({
            "Kỳ nhận lãi": [
                f"Quý {i}" for i in range(1, so_ky + 1)
            ],
            "Tiền lãi": bang_dulieu_lai
        })


    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.divider()
    st.subheader("📊 Kết quả tính toán")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_lai)
        )

    st.metric(
        "💰 Tổng tiền nhận được (Gốc + Lãi)",
        format_money(tong_tien)
    )


    # =========================
    # THÔNG TIN TỔNG QUAN
    # =========================
    st.divider()

    st.subheader("📌 Thông tin khoản gửi")

    thong_tin = pd.DataFrame({
        "Thông tin": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Hình thức nhận lãi"
        ],
        "Giá trị": [
            format_money(tien_gui),
            f"{ky_han} tháng",
            f"{lai_suat:.2f}%/năm",
            hinh_thuc
        ]
    })

    st.table(thong_tin)


    # =========================
    # BẢNG CHI TIẾT
    # =========================
    st.subheader("📅 Chi tiết tiền lãi")

    st.dataframe(
        bang_du_lieu,
        use_container_width=True,
        hide_index=True
    )


    # =========================
    # GHI CHÚ
    # =========================
    st.info(
        "💡 Kết quả được tính theo phương pháp lãi đơn trên tiền gốc "
        "và lãi suất năm. Kết quả thực tế có thể khác tùy theo quy định "
        "của từng ngân hàng, số ngày thực tế và chính sách sản phẩm tiền gửi."
    )
