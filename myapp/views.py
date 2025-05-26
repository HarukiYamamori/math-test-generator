# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import google.generativeai as genai
from dotenv import load_dotenv

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from myapp.utils.deepl_util import translate
from myapp.utils.openai_util import MathTestGenerator

load_dotenv()

# Generative AIモデルの設定
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEYが設定されていません。")

# APIキーの設定
genai.configure(api_key=GOOGLE_API_KEY)

# Generative AIモデルの設定
model_name = "gemini-2.5-flash-preview-05-20"
generation_config = {"response_mime_type": "application/json"}
generator = MathTestGenerator(model_name, generation_config)


class MathTestGeneratorAPIView(APIView):
    def post(self, request):
        prompt = request.data.get('prompt')

        if not prompt:
            return Response({"error": "プロンプトは必須です。"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # ユーティリティクラスを使用して問題を生成
            json_data = generator.generate_tests(translate(prompt, "EN-US"))
            return Response(json_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except RuntimeError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
