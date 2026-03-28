# =====================================================
# IMPORTS
# =====================================================
import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# =====================================================
# STYLE
# =====================================================
st.markdown("""
<style>
body { background-color: #fafafa; }
.stButton>button {
    background-color: black;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="The Coords Studio", layout="centered")

# =====================================================
# HEADER
# =====================================================
st.title("The Coords Studio")
st.markdown("#### Minimal. Elegant. You ✨")
st.divider()

# =====================================================
# DATASET + MODEL
# =====================================================
data = {"height": [], "weight": [], "size": []}

for h in range(150, 186, 2):
    for w in range(45, 91, 3):
        if w < 55: size = "S"
        elif w < 65: size = "M"
        elif w < 75: size = "L"
        else: size = "XL"
        data["height"].append(h)
        data["weight"].append(w)
        data["size"].append(size)

df = pd.DataFrame(data)

le = LabelEncoder()
df["size_encoded"] = le.fit_transform(df["size"])

X = df[["height", "weight"]]
y = df["size_encoded"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# =====================================================
# INPUT SECTION
# =====================================================
st.markdown("### Find Your Perfect Fit")

col1, col2 = st.columns(2)
with col1:
    height = st.number_input("Height (cm)", 140, 200, 165)
with col2:
    weight = st.number_input("Weight (kg)", 40, 120, 60)

# =====================================================
# BUTTON (FIXED POSITION)
# =====================================================
clicked = st.button("✨ Get My Perfect Size")

# =====================================================
# PRODUCT FUNCTION
# =====================================================
def show_product(image, name, price, original_price, rating, reviews, stock, whatsapp_text):

    discount = int(((original_price - price) / original_price) * 100)

    st.image(image, use_container_width=True)

    st.markdown(f"**{name}**")
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    ₹{price}  ~~₹{original_price}~~  
    **{discount}% OFF**
    """)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown(f"⭐ {rating} ({reviews})")

    if stock <= 5:
        st.markdown(f"<span style='color:red;'>Only {stock} left</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='visibility:hidden;'>placeholder</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <a href="https://wa.me/918997632635?text={whatsapp_text}" target="_blank">
            <button style="width:100%;background:black;color:white;padding:10px;border-radius:8px;">
                BUY NOW
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# DEFAULT PRODUCTS (ALWAYS VISIBLE)
# =====================================================
st.subheader("🛍️ Explore Our Collection")

col1, col2, col3 = st.columns(3)

with col1:
    show_product("images/product1.jpg","Floral Coord Set 🌸",1299,1799,"4.5","120",3,"Hi I want Floral Coord Set")

with col2:
    show_product("images/product2.jpg","Casual Chic Set ✨",1399,1899,"4.6","210",2,"Hi I want Casual Chic Set")

with col3:
    show_product("images/product3.jpg","Party Wear Coord 💃",1599,2199,"4.7","300",1,"Hi I want Party Wear Coord")

# =====================================================
# SMART RECOMMENDATION
# =====================================================
if clicked:

    input_data = pd.DataFrame([[height, weight]], columns=["height", "weight"])
    pred = model.predict(input_data)
    size = le.inverse_transform(pred)[0]

    st.divider()

    st.markdown(f"## ✅ Recommended Size: **{size}**")
    st.success("🔥 Perfect fit for you!")

    st.subheader("🎯 Recommended For You")

    col1, col2 = st.columns(2)

    if size == "M":
        with col1:
            show_product("images/product2.jpg","Casual Chic Set ✨",1399,1899,"4.6","210",2,f"Hi I want Casual Chic Set size {size}")
        with col2:
            show_product("images/product3.jpg","Daily Wear Coord 💖",1499,1999,"4.4","180",8,f"Hi I want Daily Wear Coord size {size}")

    elif size == "S":
        with col1:
            show_product("images/product1.jpg","Floral Coord Set 🌸",1299,1799,"4.5","120",3,f"Hi I want Floral Coord Set size {size}")
        with col2:
            show_product("images/product2.jpg","Summer Light Set ☀️",1199,1699,"4.3","95",6,f"Hi I want Summer Set size {size}")

    elif size == "L":
        with col1:
            show_product("images/product3.jpg","Party Wear Coord 💃",1599,2199,"4.7","300",1,f"Hi I want Party Wear Coord size {size}")
        with col2:
            show_product("images/product1.jpg","Elegant Evening Set 🌙",1699,2299,"4.5","150",4,f"Hi I want Evening Set size {size}")

    else:
        with col1:
            show_product("images/product1.jpg","Comfort Fit Coord 🌸",1499,1999,"4.3","110",5,f"Hi I want Comfort Fit size {size}")
        with col2:
            show_product("images/product3.jpg","Loose Fit Party Set 💃",1599,2199,"4.4","140",3,f"Hi I want Loose Fit size {size}")

# =====================================================
# FOOTER
# =====================================================
st.divider()
st.markdown("Made with ❤️ for fashion lovers")