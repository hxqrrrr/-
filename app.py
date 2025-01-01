import streamlit as st
import requests
import json

st.set_page_config(
    page_title="情感分析系统",
    page_icon="🎭",
    layout="centered"
)

st.title("✨ 情感分析系统")
st.write("这是一个基于AI的情感分析系统，可以分析文本中的情感倾向、强度和类型。")

# 输入文本框
text_input = st.text_area(
    "请输入要分析的文本：",
    height=150,
    placeholder="在这里输入文本..."
)

# 分析按钮
if st.button("开始分析", type="primary"):
    if text_input:
        # 显示加载动画
        with st.spinner("正在分析中..."):
            try:
                # 发送请求到FastAPI后端
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={"text": text_input}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 直接使用返回的结果
                    analysis_result = result["result"]
                    
                    # 使用列布局展示结果
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info(f"**情感极性**：{analysis_result['polarity']}")
                        st.info(f"**情感强度**：{analysis_result['intensity']}/10")
                    
                    with col2:
                        st.info(f"**情感类型**：{analysis_result['emotion_type']}")
                    
                    # 显示详细分析
                    st.success("**详细分析**：" + analysis_result['analysis'])
                else:
                    st.error(f"分析失败：{response.text}")
            except Exception as e:
                st.error(f"发生错误：{str(e)}")
    else:
        st.warning("请先输入要分析的文本！")

# 添加页脚
st.markdown("---")
st.markdown("Made with ❤️ by hxq") 