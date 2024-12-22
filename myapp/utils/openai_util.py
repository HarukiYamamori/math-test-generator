import json
import google.generativeai as genai


class MathTestGenerator:
    def __init__(self, model_name, generation_config):
        self.model = genai.GenerativeModel(model_name, generation_config=generation_config)

    def generate_tests(self, prompt):
        # プロンプトの生成
        prompt = (
            f'{prompt}'
            '解説は、公式の利用、計算過程、解答に至るまでの思考過程などを含めて記述してください。'
            '解答は、問題文、解答、解説のキーを持つJSONオブジェクトとして出力し、JSONオブジェクトのキーは、'
            '"problem", "answer", "explanation"としてください。また、JSONオブジェクトのルートキーは必ず '
            '"questions" にし、全て日本語で出力してください。'
        )
        try:
            # AIにリクエストを送信
            response = self.model.generate_content(prompt)
            return json.loads(response.text)  # 生成されたJSONを返す
        except json.JSONDecodeError:
            raise ValueError("JSONパースエラーが発生しました。")
        except Exception as e:
            raise RuntimeError(f"問題生成中にエラーが発生しました: {str(e)}")
