"""
APIクライアントをグローバル変数として管理するモジュール
"""

from google import genai
from openai import OpenAI
import os
from dotenv import load_dotenv
_gemini_client = None
_openai_client = None

def get_gemini_client():
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = genai.Client()
    return _gemini_client

def get_openai_client():
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _openai_client
