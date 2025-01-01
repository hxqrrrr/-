from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
import json
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

app = FastAPI()

class TextInput(BaseModel):
    text: str

class DeepSeekAPI:
    def __init__(self):
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
            "Content-Type": "application/json"
        }

    def analyze_sentiment(self, text: str) -> dict:
        try:
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

            logger.debug("=== 请求信息 ===")
            logger.debug(f"API URL: {self.api_url}")
            logger.debug(f"Headers: {self.headers}")
            logger.debug(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,  # 使用 json 参数而不是 data
                timeout=30
            )

            logger.debug("=== 响应信息 ===")
            logger.debug(f"Status Code: {response.status_code}")
            logger.debug(f"Response Headers: {response.headers}")
            logger.debug(f"Raw Response: {response.text}")

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"API调用失败: {response.text}"
                )

            response_json = response.json()
            logger.debug(f"解析后的响应: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
            
            content = response_json["choices"][0]["message"]["content"]
            logger.debug(f"提取的content: {content}")
            
            # 清理内容中的markdown标记和多余空白
            content = content.replace("```json", "").replace("```", "").strip()
            logger.debug(f"清理后的content: {content}")
            
            # 解析JSON内容
            result = json.loads(content)
            logger.debug(f"最终结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            return {"status": "success", "result": result}

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {str(e)}")
            logger.error(f"尝试解析的内容: {content}")
            raise HTTPException(
                status_code=500,
                detail=f"JSON解析错误: {str(e)}\n原始响应: {content}"
            )
        except Exception as e:
            logger.error(f"发生错误: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"处理请求时发生错误: {str(e)}"
            )

deepseek_api = DeepSeekAPI()

@app.post("/analyze")
def analyze_text(input_data: TextInput):
    logger.info(f"收到分析请求，文本内容: {input_data.text}")
    return deepseek_api.analyze_sentiment(input_data.text)

@app.get("/")
def read_root():
    return {"status": "active", "message": "情感分析API服务正在运行"} 