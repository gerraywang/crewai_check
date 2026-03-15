import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# .envファイルから環境変数を読み込む
load_dotenv()

# Google Cloud 設定の取得
project_id = os.getenv("GCP_PROJECT_ID", "default-project")
dataset_id = os.getenv("BILLING_DATASET_ID", "billing_export")
report_bucket = os.getenv("FINOPS_REPORT_BUCKET", "finops-reports")

# 1. Geminiの設定
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    verbose=True,
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. エージェントの定義
billing_analyst = Agent(
    role='Google Cloud 課金アナリスト',
    goal=f'プロジェクト {project_id} の課金データ（BigQuery: {dataset_id}）を分析し、予算超過や異常なコスト増を特定する',
    backstory=f'あなたは {project_id} のコスト管理に精通したエキスパートです。BigQuery内の課金エクスポートデータを読み解き、予算（Budgets）と実際の使用料の乖離を鋭く指摘します。',
    llm=llm,
    verbose=True
)

cloud_optimizer = Agent(
    role='クラウド最適化アーキテクト',
    goal=f'プロジェクト {project_id} のリソース利用効率を最大化し、コスト削減案を策定する',
    backstory='あなたはインフラ構成の最適化プロフェッショナルです。未使用のディスク、オーバープロビジョニングされたインスタンス、GCSのライフサイクル管理不足などを見つけ出し、具体的な削減額を算出します。',
    llm=llm,
    verbose=True
)

finops_operator = Agent(
    role='FinOps オペレーション担当',
    goal=f'分析結果をレポートとして GCS (gs://{report_bucket}/) に出力し、関係者とのレビュー会議をカレンダーに設定する',
    backstory=f'あなたはFinOpsの運用フローを統括します。レポートをバケット {report_bucket} の日付ディレクトリに保存し、Google Calendar APIを用いて適切なタイミングでミーティングを設定する調整役です。',
    llm=llm,
    verbose=True
)

# 3. タスクの定義
analysis_task = Task(
    description=f'プロジェクト {project_id} の先月のGCP課金データをレビューし、最もコストが増加した上位3つのサービスを特定してください。データセット {dataset_id} 内のアノマリーがないか確認し、日本語でまとめてください。',
    expected_output='コスト分析結果の要約レポート（サービス名、増加率、原因推測を含む）。',
    agent=billing_analyst
)

optimization_task = Task(
    description=f'プロジェクト {project_id} の分析結果を受け、コストを15%削減するための具体的なアクションプランを作成してください。例：インスタンスのスケールダウン、ストレージクラスの変更。',
    expected_output='優先順位付けされたコスト削減アクションプラン。',
    agent=cloud_optimizer
)

operation_task = Task(
    description=f'''
    最終的なFinOpsレポートを作成し、以下のシミュレーションを行ってください：
    1. レポートを GCS (gs://{report_bucket}/20260314/) へアップロードする準備。
    2. 次週の月曜日に「{project_id} コスト最適化レビュー会議」を Google Calendar に登録するスケジュール案の作成。
    結果を Markdown 形式で出力してください。
    ''',
    expected_output='GCSアップロードパスとカレンダー予約情報を含む最終サマリーレポート。',
    agent=finops_operator
)

# 4. クルーの編成と実行
finops_crew = Crew(
    agents=[billing_analyst, cloud_optimizer, finops_operator],
    tasks=[analysis_task, optimization_task, operation_task],
    process=Process.sequential,
    verbose=True
)

def run():
    print(f"### Google Cloud FinOps 自動運用クルーを開始します (Target Project: {project_id}) ###")
    result = finops_crew.kickoff(inputs={'date': '2026-03-14'})
    
    print("\n\n########################")
    print(f"## FinOps 運用レポート ({project_id}):")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    run()
