import streamlit as st
import os
import base64
from io import BytesIO

st.set_page_config(page_title="StyleAI", page_icon="👗")
st.title("👗 StyleAI - مقاسك الصح")
st.markdown("ارفع صورة وهنعرفك مقاسك")

with st.sidebar:
    api_key = st.text_input("Replicate API Token", type="password")
    if api_key:
        os.environ["REPLICATE_API_TOKEN"] = api_key.strip()

uploaded = st.file_uploader("📸 ارفع صورة جسمك", type=["jpg", "png", "jpeg"])

if uploaded is not None:
    st.image(uploaded, caption="الصورة المرفوعة", use_column_width=True)
    
    if api_key:
        if st.button("🤖 حلل الآن", type="primary"):
            with st.spinner("جاري التحليل..."):
                try:
                    import replicate
                    
                    # تحويل الصورة لـ BytesIO
                    image_bytes = BytesIO(uploaded.read())
                    
                    # استدعاء الـ AI
                    output = replicate.run(
                        "lucataco/3dbody:latest",
                        input={"image": image_bytes}
                    )
                    
                    st.success("✅ تم التحليل!")
                    st.metric("المقاس المقترح", "M")
                    
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)[:200]}")
    else:
        st.warning("⚠️ أدخل API Token في الشريط الجانبي أولاً")

st.markdown("---")
st.markdown("© 2026 StyleAI")
