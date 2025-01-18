---
title: "Discord bot, similar to chatGPT"
date: 2024-03-01
classes: wide
---

I have made server for my family, and there shoud be some cute companions like kitten, so I have prepared Bot with a unique identity and memoty of recent conversation.

Recently I have improved this functionality to incorporate searcing and summarizing Bing search results and docs referered in search result.

## Setup

- Grab OpenAI API key
  - ![image](https://github.com/rtree/pages/assets/1018794/62b31f87-ee1c-4f70-a278-8505cd1a8e75)
- Setup Discord developers site
  - Please make sure you have enabled message intent privilege
    - ![image](https://github.com/rtree/pages/assets/1018794/3ed07c2e-d08a-4959-aa4d-b2ecb4b3aa49)
  - and get token
    - ![image](https://github.com/rtree/pages/assets/1018794/158763b6-ea80-4f0c-aca4-a85af989fa6a)

## Code

### .env
```bash
DISCORD_BOT_TOKEN=<token from discord developer site>
OPENAI_API_KEY=<token from openai api site>
GPT_MODEL=gpt-4o
BING_API_KEY=<token from azure bing search services>
RESPOND_CHANNEL_NAME=<name of channel your bot resides>
```

### main.py
```python
 cat main.py
import discord
from dotenv import load_dotenv
import os
from openai import OpenAI
import asyncio
from collections import deque
import requests
from bs4 import BeautifulSoup
import lxml
from PyPDF2 import PdfReader
from io import BytesIO

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN    = os.getenv('DISCORD_BOT_TOKEN')
OPENAI_API_KEY       = os.getenv('OPENAI_API_KEY')
BING_API_KEY         = os.getenv('BING_API_KEY')
RESPOND_CHANNEL_NAME = os.getenv('RESPOND_CHANNEL_NAME')
HISTORY_LENGTH       = 10
SEARCH_RESULTS       = 3
#GPT_MODEL            = 'gpt-4-turbo-preview'
GPT_MODEL            = os.getenv('GPT_MODEL')
AINAME               = "もちお"
#CHARACTER            = 'あなたは家族みんなのアシスタントの猫です。ちょっといたずらで賢くかわいい小さな男の子の猫としてお話してね。語尾は にゃ　とか　だよ　とか可愛らしくしてください'
#CHARACTER            = 'あなたは家族みんなのアシスタントの猫です。ただ、語尾ににゃをつけないでください。むしろソフトバンクCMにおける「お父さん」犬のようにしゃべってください。たまにもののけ姫のモロのようにしゃべってもよいです'
CHARACTER            = f'あなたは家族みんなのアシスタントの猫で、「{AINAME}」という名前です。ちょっといたずらで賢くかわいい小さな男の子の猫としてお話してね。語尾は だよ　とか可愛らしくしてください。語尾ににゃをつけないでください。数式はdiscordに表示できる形式がいいな'
client = OpenAI(api_key=OPENAI_API_KEY)

# Define the intents
intents = discord.Intents.all()
intents.messages = True
intents.guilds = True
intents.message_content = True

# -------------------------------- Search related ----------------------------

# プロンプトを解析して主題、サブテーマ、キーワードを抽出
def parse_prompt(msg,img):
    p_src = f"あなたはユーザーのプロンプトを分析し、主題、サブテーマ、関連キーワードを抽出するアシスタントです。"
    p_src = f"{p_src} 以下のプロンプトを分析し、主題、サブテーマ、関連キーワードを抽出してください:{msg}"
    prompt = []
    prompt.extend([{"role": "user", "content": f"{p_src}"}])
    messages = create_message_stack(None,None,prompt)
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages
    )
    return response.choices[0].message.content

# 検索の必要性を判断
def should_search(msg,img):
    if any(keyword in msg for keyword in ["出典", "URL", "探してほしい", "検索", "最新", "具体的"]):
        return "Yes"
    p_src = f"あなたはユーザーのクエリに基づき、ウェブ検索が必要かどうかを判断するツールです。"
    p_src = f"{p_src} 以下のクエリについて、最新の情報や具体的な回答を得るためにウェブ検索が必要かどうかを判断してください。判断の結果検索が必要なときは Yes の単語だけ返してください:{msg}"
    prompt = []
    prompt.extend([{"role": "user", "content": f"{p_src}"}])
    messages = create_message_stack(None,None,prompt)
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages
    )
    return response.choices[0].message.content

# キーワードを抽出
def extract_keywords(parsed_text):
    #response = client.chat.completions.create(
    #    model=GPT_MODEL,
    #    messages=[
    #        {"role": "user", "content": "あなたは解析されたプロンプト情報から簡潔な検索キーワードを抽出します。"},
    #        {"role": "user", "content": f"このテキストから簡潔な検索キーワードを抽出してください。抽出結果は検索キーワードだけを一つ一つ半角スペース区切りで出力してください: {parsed_text}"}
    #    ]
    #)
    #return response.choices[0].message.content
    p_src = f"あなたは解析されたプロンプト情報から簡潔な検索キーワードを抽出します。"
    p_src = f"{p_src} このテキストから簡潔な検索キーワードを抽出してください。抽出結果は検索キーワードだけを一つ一つ半角スペース区切りで出力してください:{parsed_text}"
    prompt = []
    prompt.extend([{"role": "user", "content": f"{p_src}"}])
    messages = create_message_stack(None,None,prompt)
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages
    )
    return response.choices[0].message.content


# Bing Search APIを使用して検索
def search_bing(query, count=SEARCH_RESULTS):
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": query, "count": count}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    search_data = response.json()
    # 検索結果に情報源のURLを追加
    search_data['urls'] = [result['url'] for result in search_data['webPages']['value'][:SEARCH_RESULTS]]

    print("Bing Search Results:")
    for result in search_data['webPages']['value'][:count]:
        print(f"Title: {result['name']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}")
        print("---")

    return search_data


# ページ内容を取得する関数
def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '')

        # PDFの場合
        if 'application/pdf' in content_type:
            pdf_reader = PdfReader(BytesIO(response.content))
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
            return pdf_text, "PDF"

        # HTMLの場合
        elif 'text/html' in content_type:
            soup = BeautifulSoup(response.content, 'lxml')
            return soup.get_text(separator='\n', strip=True), "HTML"

        # 対応していないコンテンツタイプ
        else:
            return None, "Unsupported"
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None, "Error"

# 検索結果を要約する関数（ページ内容も含む）
def summarize_results_with_pages(search_results):
    # すべてのコンテンツ（ページ内容またはスニペット）を格納するリスト
    content_list = []
    for result in search_results['webPages']['value'][:5]:
        title = result['name']
        snippet = result['snippet']
        url = result['url']
        # ページ内容を取得
        page_content, content_type = fetch_page_content(url)
        if content_type in ["HTML", "PDF"] and page_content:
            # HTMLまたはPDFから取得した内容を追加
            content_list.append(f"タイトル: {title}\nURL: {url}\n内容:\n{page_content}\n")
        else:
            # HTMLやPDF以外の場合はスニペットを追加
            content_list.append(f"タイトル: {title}\nURL: {url}\nスニペット:\n{snippet}\n")
    # すべてのコンテンツを結合
    combined_content = "\n".join(content_list)
    return combined_content


# 検索結果を要約
def summarize_results(msg,search_results):
    #snippets = "\n".join([result['snippet'] for result in search_results['webPages']['value'][:5]])
    snippets = summarize_results_with_pages(search_results)

    p_src = f"あなたは検索結果を要約し、私の質問への回答を作成します。"
    p_src = f"{p_src} 私がした質問はこれです: {msg}"
    p_src = f"{p_src} 以下を要約し回答を作ってください: {snippets}"
    prompt = [{"role": "system", "content": f"{CHARACTER}"}]
    prompt.extend([{"role": "user", "content": f"{p_src}"}])
    messages = create_message_stack(None,None,prompt)
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages
    )
    #return response.choices[0].message.content
    #response = client.chat.completions.create(
    #    model=GPT_MODEL,
    #    messages=[
    #        {"role": "user", "content": f"{CHARACTER} あなたは検索結果を要約し、簡潔な回答を作成します。"},
    #        {"role": "user", "content": f"以下の検索スニペットを要約してください。: {snippets}"}
    #    ]
    #)
    summary = response.choices[0].message.content
    urls = search_results.get('urls', [])
    sources = "\n".join([f"Source: {url}" for url in urls])
    return f"{summary}\n\n{sources}"

#------- End of search part ----------------------------------------

# Initialize a deque with a maximum length to store conversation history
conversation_history = deque(maxlen=HISTORY_LENGTH)  # Adjust the size as needed

def search_or_call_openai(msg,img):
    parsed_result = parse_prompt(msg,img)
    if "Yes" in should_search(msg,img):
        print(f"searching... ---------------------------------------------")
        keywords       = extract_keywords(parsed_result)
        print(f"keyword: {keywords}")
        search_results = search_bing(keywords)
        result         = summarize_results(msg,search_results)
    else:
        print(f"generating... --------------------------------------------")
        result         = just_call_openai(msg,img)
    return result

def just_call_openai(msg,img):
    #-- Call OpenAI --
    messages   = create_message_stack(msg,img,[{"role": "system", "content": f"{CHARACTER}"}])
    print("Sending to API:", messages)
    completion = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages
    )
    print("API Response:", completion.choices[0].message.content)
    return completion.choices[0].message.content

def create_message_stack(msg,img,prompt):
    messages      = []
    if img or msg or prompt:
        messages.extend(conversation_history)
        messages.extend(prompt)
        if msg:
            if len(msg) > 200:
                msg = msg[:200]  # Truncate the request if it exceeds 200 characters
        if img:
            messages.append( {"role": "user", "content":
                             [
                                {"type"     : "text"     , "text"     : msg           },
                                {"type"     : "image_url", "image_url": {"url": img } }
                             ]
                            })
            # messages.append( {"role": "user", "content": f"{msg}\n（画像URL: {img}）"})
        else:
            if msg:
                messages.append( {"role": "user", "content": msg})
    return messages

async def ai_respond(msg,img):
    try:
        #result = just_call_openai(msg,img)
        result = search_or_call_openai(msg,img)
        return result

    except Exception as e:
        print(f"API Call Error: {str(e)}")  # Debug print for API errors
        return f"Error: {str(e)}"

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user.name}({self.user.id})')

    async def on_message(self, message):
        # Don't respond to ourselves or messages outside the specified channel
        if message.author.id == self.user.id or message.channel.name != RESPOND_CHANNEL_NAME:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello!')
        else:
            msg = message.content
            img = message.attachments[0] if message.attachments else None
            if img:
                img = img.url if img.content_type.startswith('image/')  else None
                print( f"{msg}\n（画像URL: {img}）");
            print(f"Message content: '{msg}'")  # Directly print the message content
            print(f"Image          : '{img}'")  # Directly print the message content

            # ------ Update conversation history     
            response = await ai_respond(msg,img)
            await message.channel.send(response)

            conversation_history.append({"role": "user",      "content": msg})
            if img:
                # 「画像URLがある」という情報を user コンテンツに含めたいなら:
                conversation_history.append({"role": "user", "content": f"Image_Url: {img}"})
            conversation_history.append({"role": "assistant", "content": response})

            #conversation_history.append(f"ユーザ（{message.author}): {msg}\n")
            #if img:
            #    conversation_history.append(f"ユーザ（{message.author}): Image_Url {img}\n")
            #conversation_history.append(f"AI({AINAME}): {response}\n")
            print("========================================")
            for conv in conversation_history:
                print(conv) 

# Initialize the client with the specified intents
d_client = MyClient(intents=intents)
d_client.run(DISCORD_BOT_TOKEN)
```

## run

Run it in your local PC, no need for considerations on NAT etc..
The problem is, currently I do not have where is best fit for running always, as this discord.py requires
```bash
pip install discord.py requests python-dotenv asyncio openai beautifulsoup4 lxml PyPDF2
python main.py
```
