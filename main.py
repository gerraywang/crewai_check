import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# .envファイルから環境変備を読み込む
load_dotenv()

# 1. Geminiの設定
# 注意: GOOGLE_API_KEY が .env または環境変数に設定されている必要があります
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. エージェントの定義
researcher = Agent(
    role='技術リサーチャー',
    goal='{topic} に関する最新の技術動向とベストプラクティスを調査する',
    backstory='あなたは最先端技術の動向を追い続ける専門家です。複雑な情報を整理し、重要なポイントを抽出するのが得意です。',
    llm=llm,
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role='コンテンツストラテジスト',
    goal='リサーチ結果に基づき、技術者に刺さる魅力的なブログ記事を作成する',
    backstory='あなたは難しい技術概念を、誰にでも分かりやすく、かつ説得力のある文章に変換するプロフェッショナルです。',
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# 3. タスクの定義
research_task = Task(
    description='{topic} についての最新情報を3つの主要なポイントでまとめてください。日本語で回答してください。',
    expected_output='3つの主要なポイントを箇条書きにしたリサーチレポート。',
    agent=researcher
)

write_task = Task(
    description='リサーチレポートを元に、初心者にもわかりやすいブログ記事を作成してください。日本語で回答してください。',
    expected_output='Markdown形式のブログ記事。',
    agent=writer
)

# 4. クルーの編成と実行
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True
)

def run():
    print("### クルーの実行を開始します...")
    result = crew.kickoff(inputs={'topic': 'CrewAIとGeminiを組み合わせたマルチエージェントシステムの可能性'})
    
    print("\n\n########################")
    print("## 最終成果物:")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    run()
