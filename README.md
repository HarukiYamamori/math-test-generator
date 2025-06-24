# Math Test Generator API

## 概要

このプロジェクトは、Google Gemini API と DeepL API を利用して、ユーザーが指定したプロンプトに基づいて数学の問題、解答、解説を自動生成する Django REST API です。生成されたコンテンツは、指定されたJSON形式で返却され、数式はLaTeX形式、書式はHTMLタグで表現されます。

## 機能

-   **数学問題の自動生成**: ユーザーからのプロンプト（指示）に基づいて、Google Gemini API が数学の問題を生成します。
-   **DeepLによるプロンプト翻訳**: Gemini APIに渡すプロンプトは、DeepL APIを使用して自動的に日本語から英語に翻訳されます。
-   **詳細な解答と解説**: 問題だけでなく、公式の利用、計算過程、思考過程を含む詳細な解答と解説が提供されます。
-   **JSON形式での出力**: 生成された問題、解答、解説は、`problem`、`answer`、`explanation` をキーとするJSONオブジェクトとして出力されます。ルートキーは `questions` です。
-   **LaTeX数式対応**: 数式はJavaScriptの `JSON.parse` で正しく読み込めるように、二重エスケープされたLaTeX形式（例: `\\frac{a}{b}`）で記述されます。
-   **HTMLタグによる書式設定**: 改行（`<br>`）や太字（`<strong>`）などの書式はHTMLタグで表現されます。
-   **CORS対応**: フロントエンドアプリケーションからのAPIアクセスを許可するため、CORS (Cross-Origin Resource Sharing) が設定されています。

## 技術スタック

-   **バックエンド**: Django, Django REST Framework
-   **AI/翻訳 API**: Google Gemini API, DeepL API
-   **言語**: Python

## 環境構築

### 前提条件

-   Python 3.x
-   pip

### セットアップ手順

1.  **リポジトリのクローン**

    ```bash
    git clone https://github.com/your-username/math-test-generator.git
    cd math-test-generator
    ```

2.  **仮想環境の作成と有効化**

    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate   # Windows
    ```

3.  **依存関係のインストール**

    ```bash
    pip install -r requirements.txt
    ```

4.  **環境変数の設定**

    プロジェクトルートに `.env` ファイルを作成し、以下のAPIキーを設定してください。

    ```
    GOOGLE_API_KEY=あなたのGoogle Gemini APIキー
    DEEPL_API_KEY=あなたのDeepL APIキー
    ```

    -   Google Gemini APIキーは [Google Cloud Console](https://console.cloud.google.com/apis/credentials) で取得できます。
    -   DeepL APIキーは [DeepL API Document](https://www.deepl.com/ja/docs-api) で取得できます。

5.  **データベースのマイグレーション**

    ```bash
    python manage.py migrate
    ```

6.  **開発サーバーの起動**

    ```bash
    python manage.py runserver
    ```

    サーバーは通常 `http://127.0.0.1:8000/` で起動します。

## APIエンドポイント

### 数学問題生成API

-   **URL**: `/api/generate-math-test/` (例: `http://127.0.0.1:8000/api/generate-math-test/`)
-   **メソッド**: `POST`
-   **リクエストボディ**:
    -   `prompt` (string, 必須): 生成したい数学問題の内容に関するプロンプト（日本語）。

    ```json
    {
        "prompt": "中学レベルの二次方程式の問題を3問作成してください。"
    }
    ```

-   **レスポンス**:
    成功した場合、生成された問題のJSONデータが返されます。

    ```json
    {
        "questions": [
            {
                "problem": "問題1の内容（HTMLタグとLaTeX数式を含む）",
                "answer": "解答1の内容（HTMLタグとLaTeX数式を含む）",
                "explanation": "解説1の内容（HTMLタグとLaTeX数式を含む）"
            },
            {
                "problem": "問題2の内容",
                "answer": "解答2の内容",
                "explanation": "解説2の内容"
            }
            // ... 他の問題 ...
        ]
    }
    ```

    エラーが発生した場合、以下の形式でエラーメッセージが返されます。

    ```json
    {
        "error": "エラーメッセージ"
    }
    ```

    -   `400 Bad Request`: プロンプトが提供されていない場合。
    -   `500 Internal Server Error`: APIキーの問題、Generative AIのエラー、JSONパースエラーなど、サーバー内部でエラーが発生した場合。