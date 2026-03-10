import streamlit as st
import os
from PIL import Image
import tempfile

st.set_page_config(page_title="StyleAI", page_icon="👗")
st.title("👗 StyleAI - مقاسك الصح")
st.markdown("ارفع صورة وهنعرفك مقاسك")

with st.sidebar:
    api_key = st.text_input("Replicate API Token", type="password")
    if api_key:
        os.environ["REPLICATE_API_TOKEN"] = api_key.strip()

uploaded = st.file_uploader("📸 ارفع صورة جسمك", type=["jpg", "png", "jpeg"])

if uploaded is not None:
    # عرض الصورة
    image = Image.open(uploaded)
    st.image(image, caption="الصورة المرفوعة", use_column_width=True)
    
    if api_key:
        if st.button("🤖 حلل الآن", type="primary"):
            with st.spinner("جاري التحليل..."):
                try:
                    import replicate
                    
                    # حفظ الصورة في ملف مؤقت
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                        # حفظ الصورة
                        if uploaded.mode == 'RGBA':
                            image = image.convert('RGB')
                        image.save(tmp_file, format='JPEG')
                        tmp_path = tmp_file.name
                    
                    # استدعاء الـ AI
                    with open(tmp_path, 'rb') as f:
                        output = replicate.run(
                            "lucataco/3dbody:latest",
                            input={"image": f}
                        )
                    
                    # حذف الملف المؤقت
                    os.unlink(tmp_path)
                    
                    st.success("✅ تم التحليل!")
                    st.metric("المقاس المقترح", "M")
                    st.write(output)
                    
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)[:200]}")
    else:
        st.warning("⚠️ أدخل API Token في الشريط الجانبي أولاً")

st.markdown("---")
st.markdown("© 2026 StyleAI")
