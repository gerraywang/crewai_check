# CrewAI & Gemini マルチエージェントシステム

このリポジトリには、**CrewAI** と **Google Gemini** を組み合わせたマルチエージェントシステムのデモプロジェクトが含まれています。

## 📁 ディレクトリ構成
- `sample-blog-writer/`: 最初のデモ。技術リサーチからブログ記事作成までを自動化。
- `gcp-finops-agent/`: Google Cloud の FinOps 運用（コスト分析、最適化提案、報告準備）を自動化。

## 🚀 はじめかた

### 1. 前準備
- [Google AI Studio](https://aistudio.google.com/) で API キーを取得してください。
- Docker と Docker Compose がインストールされていることを確認してください。

### 2. 環境変数の設定
ルートディレクトリにある `.env.example` をコピーして `.env` を作成し、各項目を設定してください。

```bash
cp .env.example .env
```

`.env` の内容（例）：
```text
GOOGLE_API_KEY=あなたのGeminiAPIキー
GCP_PROJECT_ID=分析対象のプロジェクトID
BILLING_DATASET_ID=BigQueryの課金データセット名
FINOPS_REPORT_BUCKET=レポート保存先のGCSバケット名
```

### 3. 各エージェントの実行

**Google Cloud FinOps エージェントを実行：**
```bash
docker compose run --rm finops-agent
```

**ブログ記事作成デモを実行：**
```bash
docker compose run --rm blog-writer
```

## 🛠️ 技術スタック
- **Framework**: CrewAI 0.5.0+
- **LLM**: Google Gemini 1.5 シリーズ (`gemini-flash-latest`)
- **SDK**: LangChain, Google GenAI SDK
- **Environment**: Docker, Docker Compose
