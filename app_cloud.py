import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置页面
st.set_page_config(
    page_title="情感分析系统",
    page_icon="🎭",
    layout="centered"
)

# 标题和说明
st.title("✨ 情感分析系统")
st.write("这是一个基于AI的情感分析系统，可以分析文本中的情感倾向、强度和类型。")

# 从环境变量或Streamlit Secrets获取API密钥
api_key = os.getenv('DEEPSEEK_API_KEY') or st.secrets["DEEPSEEK_API_KEY"]

def analyze_sentiment(text: str) -> dict:
    """调用Deepseek API进行情感分析"""
    api_url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""请分析以下文本的情感，并给出以下信息：
    1. 情感极性（积极、消极或中性）
    2. 情感强度（1-10分）
    3. 主要情感类型（如：快乐、悲伤、愤怒、恐惧等）
    4. 简短分析（不超过100字）
    
    文本：{text}
    
    请以JSON格式返回结果，包含以下字段：
    polarity, intensity, emotion_type, analysis"""

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个专业的情感分析助手。请只返回JSON格式的结果，不要包含其他文本。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"API调用失败: {response.text}")

        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"]
        
        # 清理内容中的markdown标记和多余空白
        content = content.replace("```json", "").replace("```", "").strip()
        
        # 解析JSON内容
        result = json.loads(content)
        return result

    except Exception as e:
        raise Exception(f"处理请求时发生错误: {str(e)}")

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
                # 直接调用API进行分析
                analysis_result = analyze_sentiment(text_input)
                
                # 使用列布局展示结果
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"**情感极性**：{analysis_result['polarity']}")
                    st.info(f"**情感强度**：{analysis_result['intensity']}/10")
                
                with col2:
                    st.info(f"**情感类型**：{analysis_result['emotion_type']}")
                
                # 显示详细分析
                st.success("**详细分析**：" + analysis_result['analysis'])
                
            except Exception as e:
                st.error(f"发生错误：{str(e)}")
    else:
        st.warning("请先输入要分析的文本！")

# 添加页脚
st.markdown("---")
st.markdown("Made with ❤️ by hxqrrr") 