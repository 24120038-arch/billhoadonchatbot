import streamlit as st
from datetime import datetime

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Trà Sữa - Tính Hóa Đơn",
    page_icon="🧋",
    layout="wide"
)

# =========================
# DỮ LIỆU MENU
# =========================
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 38000,
    "Trà sữa dâu": 35000,
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà chanh": 25000,
}

SIZE_PRICE = {
    "M": 0,
    "L": 5000,
}

TOPPINGS = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Thạch dừa": 5000,
}

# =========================
# SESSION STATE
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None


# =========================
# HÀM FORMAT TIỀN
# =========================
def format_money(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.title("🧋 QUÁN TRÀ SỮA")
st.subheader("Hệ thống tính hóa đơn")

st.divider()

# =========================
# NHẬP THÔNG TIN KHÁCH HÀNG
# =========================
st.markdown("### 👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)

customer_phone = st.text_input(
    "Số điện thoại",
    placeholder="Nhập số điện thoại..."
)

st.divider()

# =========================
# CHỌN MÓN
# =========================
st.markdown("### 🧋 Chọn món")

col1, col2 = st.columns(2)

with col1:
    drink = st.selectbox(
        "Loại trà sữa / đồ uống",
        list(MENU.keys())
    )

    size = st.radio(
        "Size",
        ["M", "L"],
        horizontal=True
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )

with col2:
    sugar = st.selectbox(
        "Mức độ đường",
        [
            "100% đường",
            "70% đường",
            "50% đường",
            "30% đường",
            "0% đường"
        ]
    )

    ice = st.selectbox(
        "Mức độ đá",
        [
            "100% đá",
            "70% đá",
            "50% đá",
            "30% đá",
            "Không đá"
        ]
    )

    topping = st.selectbox(
        "Topping",
        list(TOPPINGS.keys())
    )


# =========================
# TÍNH GIÁ
# =========================
unit_price = MENU[drink] + SIZE_PRICE[size] + TOPPINGS[topping]
total_item = unit_price * quantity

st.info(
    f"Đơn giá: **{format_money(unit_price)}**  |  "
    f"Thành tiền: **{format_money(total_item)}**"
)


# =========================
# THÊM MÓN
# =========================
if st.button("➕ Thêm món vào hóa đơn", use_container_width=True):

    item = {
        "drink": drink,
        "size": size,
        "quantity": quantity,
        "sugar": sugar,
        "ice": ice,
        "topping": topping,
        "unit_price": unit_price,
        "total": total_item
    }

    st.session_state.cart.append(item)

    st.success(
        f"Đã thêm {quantity} x {drink} vào hóa đơn!"
    )


# =========================
# HIỂN THỊ GIỎ HÀNG
# =========================
st.divider()

st.markdown("### 🛒 Chi tiết hóa đơn")

if len(st.session_state.cart) == 0:

    st.warning("Chưa có món nào trong hóa đơn.")

else:

    grand_total = 0

    for i, item in enumerate(st.session_state.cart):

        with st.container(border=True):

            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:
                st.markdown(
                    f"**{i + 1}. {item['drink']}**"
                )

                st.write(
                    f"Size: {item['size']} | "
                    f"Số lượng: {item['quantity']}"
                )

                st.write(
                    f"Đường: {item['sugar']} | "
                    f"Đá: {item['ice']}"
                )

                st.write(
                    f"Topping: {item['topping']}"
                )

            with col2:
                st.write(
                    f"Đơn giá: {format_money(item['unit_price'])}"
                )

                st.markdown(
                    f"**{format_money(item['total'])}**"
                )

            with col3:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_{i}"
                ):
                    st.session_state.cart.pop(i)
                    st.rerun()

        grand_total += item["total"]

    # =========================
    # TỔNG TIỀN
    # =========================
    st.divider()

    st.markdown(
        f"""
        <div style="
            background-color:#f5f5f5;
            padding:20px;
            border-radius:10px;
            text-align:right;
        ">
            <h3>TỔNG THANH TOÁN</h3>
            <h1 style="color:#d63384;">
                {format_money(grand_total)}
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =========================
    # THANH TOÁN
    # =========================
    st.markdown("### 💳 Phương thức thanh toán")

    payment = st.radio(
        "Chọn phương thức thanh toán",
        [
            "💵 Tiền mặt",
            "📱 Chuyển khoản",
            "💳 Thẻ ngân hàng"
        ],
        horizontal=True
    )

    # =========================
    # XUẤT HÓA ĐƠN
    # =========================
    if st.button(
        "🧾 THANH TOÁN & XUẤT HÓA ĐƠN",
        type="primary",
        use_container_width=True
    ):

        if not customer_name.strip():
            st.error("Vui lòng nhập tên khách hàng.")
            st.stop()

        invoice_time = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        invoice_text = ""

        invoice_text += "========================================\n"
        invoice_text += "           QUÁN TRÀ SỮA\n"
        invoice_text += "              HÓA ĐƠN\n"
        invoice_text += "========================================\n"
        invoice_text += f"Khách hàng: {customer_name}\n"

        if customer_phone:
            invoice_text += f"SĐT: {customer_phone}\n"

        invoice_text += f"Thời gian: {invoice_time}\n"
        invoice_text += "----------------------------------------\n"

        for i, item in enumerate(st.session_state.cart):

            invoice_text += (
                f"{i + 1}. {item['drink']}\n"
            )

            invoice_text += (
                f"   Size: {item['size']} | "
                f"SL: {item['quantity']}\n"
            )

            invoice_text += (
                f"   Đường: {item['sugar']}\n"
            )

            invoice_text += (
                f"   Đá: {item['ice']}\n"
            )

            invoice_text += (
                f"   Topping: {item['topping']}\n"
            )

            invoice_text += (
                f"   Đơn giá: "
                f"{format_money(item['unit_price'])}\n"
            )

            invoice_text += (
                f"   Thành tiền: "
                f"{format_money(item['total'])}\n"
            )

            invoice_text += "----------------------------------------\n"

        invoice_text += (
            f"TỔNG TIỀN: {format_money(grand_total)}\n"
        )

        invoice_text += (
            f"Thanh toán: {payment}\n"
        )

        invoice_text += "========================================\n"
        invoice_text += "       CẢM ƠN QUÝ KHÁCH!\n"
        invoice_text += "========================================\n"

        st.session_state.invoice = invoice_text

        st.success("Thanh toán thành công! Hóa đơn đã được tạo.")


# =========================
# HIỂN THỊ HÓA ĐƠN
# =========================
if st.session_state.invoice:

    st.divider()

    st.markdown("### 🧾 Hóa đơn")

    st.code(
        st.session_state.invoice,
        language="text"
    )

    st.download_button(
        label="📥 Tải hóa đơn (.txt)",
        data=st.session_state.invoice,
        file_name="hoa_don_tra_sua.txt",
        mime="text/plain",
        use_container_width=True
    )


# =========================
# XÓA TOÀN BỘ HÓA ĐƠN
# =========================
if len(st.session_state.cart) > 0:

    st.divider()

    if st.button(
        "🗑️ Xóa toàn bộ hóa đơn",
        use_container_width=True
    ):
        st.session_state.cart = []
        st.session_state.invoice = None
        st.rerun()
