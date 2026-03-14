# CrewAI & Gemini マルチエージェントシステム

このプロジェクトは、**CrewAI** と **Google Gemini** モデルを組み合わせた、技術リサーチおよびコンテンツ作成を自動化するマルチエージェントシステムのデモです。

## 🚀 はじめかた

### 1. 前準備
- [Google AI Studio](https://aistudio.google.com/) で API キーを取得してください。
- Docker と Docker Compose がインストールされていることを確認してください。

### 2. 環境変数の設定
`.env.example` をコピーして `.env` を作成し、取得した API キーを設定します。

```bash
cp .env.example .env
```

`.env` 内の `GOOGLE_API_KEY` を編集します：
```text
GOOGLE_API_KEY=あなたのAPIキー
```

### 3. Docker で実行
ビルドと実行は以下のコマンド一つで行えます：

```bash
docker compose up --build
```

## 🧠 プロジェクト構成
- `main.py`: CrewAI のエージェント、タスク、クルーの定義。
- `Dockerfile`: アプリケーションのコンテナ定義。
- `docker-compose.yml`: 環境変数とボリューム設定。
- `requirements.txt`: 依存ライブラリ（CrewAI, LangChain, Google GenAI）。

## 🤖 エージェント紹介
- **技術リサーチャー**: 特定のトピックに関する最新技術動向を調査し、ポイントをまとめます。
- **コンテンツストラテジスト**: リサーチ結果を元に、初心者にも分かりやすい Markdown 形式のブログ記事を作成します。

## ⚠️ 注意事項
このプロジェクトは、実行時の日付設定（2026年など）に合わせ、最適な Gemini モデル（`gemini-flash-latest`）を使用するように構成されています。
