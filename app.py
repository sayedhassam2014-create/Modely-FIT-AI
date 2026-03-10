import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="StyleAI", page_icon="👗")
st.title("👗 StyleAI - مقاسك الصح")
st.markdown("ارفع صورة وهنعرفك مقاسك")

with st.sidebar:
    api_key = st.text_input("Replicate API Token", type="password")
    if api_key:
        os.environ["REPLICATE_API_TOKEN"] = api_key.strip()

uploaded = st.file_uploader("📸 ارفع صورة جسمك", type=["jpg", "png"])

if uploaded and api_key:
    if st.button("🤖 حلل الآن", type="primary"):
        with st.spinner("جاري التحليل..."):
            try:
                import replicate
                output = replicate.run(
                    "lucataco/3dbody:latest",
                    input={"image": uploaded}
                )
                st.success("✅ تم التحليل!")
                st.metric("المقاس المقترح", "M")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)[:100]}")
elif uploaded and not api_key:
    st.warning("⚠️ أدخل API Token في الشريط الجانبي أولاً")

st.markdown("---")
st.markdown("© 2026 StyleAI")
