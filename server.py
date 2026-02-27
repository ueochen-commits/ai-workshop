#!/usr/bin/env python3
"""AI神器工坊后端"""
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = '51d844a1668448a2bd3d29a7e1c1d8da.pU4Sru3IIXy10kiS'
API_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'

def chat(prompt, system='你是一个有用的AI助手'):
    try:
        r = requests.post(API_URL, headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }, json={
            'model': 'glm-4',
            'messages': [
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': prompt}
            ]
        }, timeout=60)
        result = r.json()
        if 'choices' in result:
            return result['choices'][0]['message']['content']
        return f'错误: {result}'
    except Exception as e:
        return f'调用失败: {e}'

@app.route('/api/chat', methods=['POST'])
def api_chat():
    return jsonify({'result': chat(request.json.get('prompt', ''))})

@app.route('/api/writing', methods=['POST'])
def api_writing():
    d = request.json
    t = d.get('topic', '')
    wtype = d.get('type', 'article')
    
    if wtype == 'article':
        prompt = f'写一篇关于"{t}"的文章，800-1500字'
    elif wtype == 'ad':
        prompt = f'写一段关于"{t}"的广告文案'
    elif wtype == 'social':
        prompt = f'写一条关于"{t}"的社交媒体推文'
    elif wtype == 'email':
        prompt = f'写一封关于"{t}"的商业邮件'
    else:
        prompt = f'写一个关于"{t}"的产品描述'
    
    return jsonify({'result': chat(prompt, '你是一个专业文案')})

@app.route('/api/image', methods=['POST'])
def api_image():
    d = request.json
    prompt = f'把以下描述优化成英文AI绘图提示词：{d.get("description", "")}'
    return jsonify({'result': chat(prompt, '你是AI绘画专家')})

@app.route('/api/video', methods=['POST'])
def api_video():
    d = request.json
    prompt = f'写一个关于"{d.get("topic", "")}"的视频脚本'
    return jsonify({'result': chat(prompt, '你是视频编导')})

@app.route('/api/data', methods=['POST'])
def api_data():
    d = request.json
    prompt = f'分析数据：{d.get("data", "")}，问题：{d.get("question", "")}'
    return jsonify({'result': chat(prompt, '你是数据分析师')})

@app.route('/api/trading', methods=['POST'])
def api_trading():
    d = request.json
    prompt = f'分析{d.get("market", "")}市场{d.get("symbol", "")}，给交易建议'
    return jsonify({'result': chat(prompt, '你是金融分析师')})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("AI神器工坊 启动成功!")
    app.run(port=5000)
