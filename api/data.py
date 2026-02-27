import vercel
import json
import requests

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

@vercel.http
def api_writing(req):
    data = json.loads(req.body) if req.body else {}
    t = data.get('topic', '')
    wtype = data.get('type', 'article')
    
    prompts = {
        'article': f'写一篇关于"{t}"的文章，800-1500字',
        'ad': f'写一段关于"{t}"的广告文案',
        'social': f'写一条关于"{t}"的社交媒体推文',
        'email': f'写一封关于"{t}"的商业邮件',
        'product': f'写一个关于"{t}"的产品描述'
    }
    prompt = prompts.get(wtype, prompts['article'])
    return json({'result': chat(prompt, '你是一个专业文案')})

@vercel.http
def api_image(req):
    data = json.loads(req.body) if req.body else {}
    prompt = f'把以下描述优化成英文AI绘图提示词：{data.get("description", "")}'
    return json({'result': chat(prompt, '你是AI绘画专家')})

@vercel.http
def api_video(req):
    data = json.loads(req.body) if req.body else {}
    prompt = f'写一个关于"{data.get("topic", "")}"的视频脚本'
    return json({'result': chat(prompt, '你是视频编导')})

@vercel.http
def api_data(req):
    data = json.loads(req.body) if req.body else {}
    prompt = f'分析数据：{data.get("data", "")}，问题：{data.get("question", "")}'
    return json({'result': chat(prompt, '你是数据分析师')})

@vercel.http
def api_trading(req):
    data = json.loads(req.body) if req.body else {}
    prompt = f'分析{data.get("market", "")}市场{data.get("symbol", "")}，给交易建议'
    return json({'result': chat(prompt, '你是金融分析师')})
