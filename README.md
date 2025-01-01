# 情感分析系统

这是一个基于 FastAPI 和 Streamlit 的情感分析系统，使用 Deepseek 进行文本情感分析。

## 功能特点

- 分析文本的情感极性（积极、消极或中性）
- 评估情感强度（1-10分）
- 识别主要情感类型
- 提供详细的情感分析说明

## 安装步骤

1. 克隆项目并安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
- 复制 `.env.example` 文件为 `.env`
- 在 `.env` 文件中填入你的 Deepseek API 密钥：
```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

## 启动服务

1. 启动 FastAPI 后端服务：
```bash
uvicorn api:app --reload
```

2. 在新的终端窗口中启动 Streamlit 前端：
```bash
streamlit run app.py
```

## 使用方法

1. 打开浏览器访问 http://localhost:8501
2. 在文本框中输入要分析的文本
3. 点击"开始分析"按钮
4. 查看分析结果

## API 文档

启动后端服务后，可以访问 http://localhost:8000/docs 查看完整的 API 文档。

## 注意事项

- 确保已安装所有依赖包
- 必须配置有效的 Deepseek API 密钥
- 后端和前端服务需要同时运行