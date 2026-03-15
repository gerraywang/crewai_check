# Google Cloud FinOps 運用マニュアル (Role-Based)

このドキュメントでは、CrewAI FinOps エージェントを活用した週次運用フローと、組織内での役割分担（Role）、および運用上の注意事項を定義します。

## 👥 組織構成と役割 (Roles & Responsibilities)

FinOps を効果的に推進するため、以下の役割を定義します。

### 1. 意思決定・実行ロール (Human Roles)
| 役割 (Role) | 担当内容 |
| :--- | :--- |
| **FinOps Lead (管理者)** | 運用全体の統括、削減目標の策定、各プロジェクト間での優先順位付けと最終意思決定。 |
| **Infrastructure Engineer (SRE)** | エージェントが提案した最適化案（ライトサイジング等）の技術的妥当性の検証と実行。 |
| **Project Owner (サービス責任者)** | ビジネス要件に基づくリソース増減の承認。コスト変動の背景（キャンペーン等）の共有。 |
| **Finance / Billing Admin** | 予算（Budget）の管理、コスト配分の妥当性確認、クレジットや確約利用割引 (CUD) の管理。 |

### 2. 分析・自動化ロール (AI Roles - FinOps AI System)
FinOps AI は以下の 3 つのサブ・エージェントで構成されるマルチエージェントシステムです。

| エージェント名 | 専門領域 (Sub-Role) |
| :--- | :--- |
| **Billing Analyst** | **【計数分析】** BigQuery 課金データの解析。前月比・前週比の変動要因の特定と異常検知。 |
| **Cloud Optimizer** | **【最適化戦略】** GCP 推奨事項に基づいたコスト削減プランの立案。技術的な削減余地の算出。 |
| **FinOps Operator** | **【運用調整】** 分析結果のドキュメント化（Markdown）。GCS 格納準備およびカレンダー予約。 |

---

## 🤖 FinOps AI 内部ワークフロー (Internal Workflow)

FinOps AI は CrewAI のオーケストレーションにより、以下のステップで自律的に業務を遂行します。

1.  **データリサーチ (Research Phase)**: 
    - `Billing Analyst` が指定されたプロジェクトの課金データセットを調査。
    - コスト増の Top 3 サービスとアノマリーを特定。
2.  **戦略立案 (Strategy Phase)**: 
    - 分析結果を `Cloud Optimizer` が受け取り、削減目標（例：15%削減）に向けたアクションを策定。
    - 優先順位（即時・短期・中期）を決定。
3.  **成果物作成 (Reporting Phase)**: 
    - `FinOps Operator` が全ての情報を統合し、人間が読みやすい形式でレポートを作成。
    - 保存先（GCS）と次週の会議日程（Google Calendar）のシミュレーションを実行。

---

## 📅 週次運用フロー (Weekly Operational Workflow)

### 1. 月曜日：自動分析とレポート生成 (AI 実行)
- **担当**: `FinOps AI`
- **内容**: 
    - 前週の課金データをスキャンし、最適化プランを作成。
    - `gs://{report_bucket}/yyyyMMdd/` への保存準備と関係者への通知。

### 2. 火曜日：技術・財務レビュー (エンジニア & 財務)
- **担当**: `Infrastructure Engineer`, `Finance`
- **内容**: 
    - 生成されたレポートの技術的な現実性と財務的な整合性を確認。

### 3. 水曜日：FinOps コストレビュー会議 (関係者全員)
- **担当**: `All Roles`
- **内容**: 
    - エージェントの提案に基づき、プロジェクトオーナーを含めて協議し、実施を決定。

### 4. 木曜日〜金曜日：最適化の実行 (エンジニア)
- **担当**: `Infrastructure Engineer`
- **内容**: 
    - 承認されたリソース変更を実行。

---

## ⚠️ 運用上の注意事項 (Precautions)

### 1. データの遅延 (Data Latency)
課金データは反映までに **24〜48時間** のラグがあります。月曜朝のレポートは「先週土曜日まで」の確定データに基づくものであることを理解してください。

### 2. 人間による確認 (Human-in-the-loop)
**自動削除は絶対に行わず、必ず Infrastructure Engineer の確認を経てから実行してください。** AI は DR 用リソース等を「無駄」と誤認する可能性があります。

### 3. 権限の最小化 (Least Privilege)
エージェントには `roles/billing.viewer`, `roles/bigquery.dataViewer`, `roles/storage.objectCreator` のみの付与を推奨します。

### 4. コンテキストの共有
意図的なコスト増（キャンペーン等）がある場合は、事前に情報を共有しておくことで AI の誤検知を防げます。
