# 全仕様書

このディレクトリ以下に本プロジェクトの全仕様を記述する。

## 記述方針

- 仕様は本ファイルを起点として辿れるようにする
- 1ファイルが巨大になり、読みにくくならないように、仕様書は階層的に管理する
- 仕様の記述量が多い場合は、まず抽象度高く簡潔に記載し、詳細は子ファイルを作成しそちらに記載する
- 子ファイルを作成する場合
  - 前提情報のファイルへのリンクを付けること

---

## 1. 対象ツール

### 調査対象

| ツール | 種別 | 情報源 | 取得方法 |
|---|---|---|---|
| OWASP ZAP | OSS | https://github.com/zaproxy/zaproxy | GitHub Releases API |
| Nuclei | OSS | https://github.com/projectdiscovery/nuclei | GitHub Releases API |
| sqlmap | OSS | https://github.com/sqlmapproject/sqlmap | GitHub Releases API |
| Nikto | OSS | https://github.com/sullo/nikto | GitHub Releases API |
| Wapiti | OSS | https://github.com/wapiti-scanner/wapiti | GitHub Releases API |
| Burp Suite | 商用（SaaS/デスクトップ） | https://portswigger.net/burp/releases | HTMLスクレイピング |

### 対象外（参考記述のみ）

以下のカテゴリのツールは調査対象外とする。

- **SCA（Software Composition Analysis）**：コンポーネントやライブラリの既知CVEをスキャンするツール（例：Trivy、Grype）
- **静的コード解析（SAST）**：ソースコードの記述パターンから脆弱性を検出するツール（例：SonarQube、Semgrep）
- **SBOMの生成・管理のみを行うツール**：脆弱性スキャンを行わないもの（例：microsoft/sbom-tool）

---

## 2. フィード仕様

### フォーマット

- RSS 2.0
- Atom 1.0
- JSON Feed 1.1

の3形式すべてに対応する。

### 含める情報項目

- バージョン（タグ名）
- 日時（公開日時）
- URL（リリースページへのリンク）
- サマリ（タイトル・概要）
- 変更内容（CHANGELOG / リリースノート本文）
- リリース種別カテゴリ（後述）

### リリース種別カテゴリ

フィードはリリース種別でカテゴリ分けする。フィルタリングにも使用する。

- `feature`：機能追加・変更
- `pricing`：料金変更
- `security`：セキュリティ修正・Hotfix
- `bugfix`：バグ修正
- `announcement`：告知・登壇・受賞等
- `other`：その他

### 更新頻度

- GitHub Actions で週次実行（毎週土曜 JST 07:00 / UTC 金曜 22:00）
- または Issue 作成 → Copilot によるPR作成 → レビュー → mainマージ

### 公開エンドポイント

- GitHub Pages で公開

---

## 3. データ収集

### 収集方式

| 対象種別 | 方法 |
|---|---|
| GitHub OSS（OWASP ZAP・Nuclei 等） | GitHub Actions + GitHub Releases API（構造化データ取得可） |
| 商用（Burp Suite） | GitHub Actions + HTMLスクレイピング |

### GitHub Releases API

- エンドポイント：`https://api.github.com/repos/{owner}/{repo}/releases`
- 取得可能なフィールド：`tag_name`（バージョン）、`published_at`（日時）、`body`（CHANGELOG相当）、`html_url`
- レート制限：未認証60req/時、トークンあり5000req/時
- **APIを優先し、スクレイピングは最終手段とする**（HTML変更で壊れやすいため）

### 実行方式

- ポーリング（週次定期実行）を基本とする
- イベント駆動（GitHub webhook等）は対象サービスが非対応のため採用しない

---

## 4. データ保存・管理

- 収集データはリポジトリ内ファイルとして保存（JSONの中間形式）
- 各ソースから取得したデータをJSON（中間形式）で統一して保存し、そこからRSS/Atom/JSON Feedを生成する
  - ソース変更時の影響範囲を最小化できる
- 履歴は永久に保持・蓄積する（削除しない）
- 対象ツールはYAML等の設定ファイルで管理し、コード変更なしで追加できる構造にする

---

## 5. 公開・配信

- 対象ユーザー：不特定多数
- 購読方法：RSSリーダー、またはリポジトリのファイルを直接参照
- フィルタリング：リリース種別カテゴリで絞り込み可能

### 公開 URL

https://tmyymmt.github.io/dast-tools-feed/

### 出力ファイル構成（public/）

`public/` はリポジトリには含めない（.gitignore 済み）。GitHub Actions 実行時に生成し、GitHub Pages にデプロイする。

| パス | 内容 |
|---|---|
| `feeds/all.{rss,atom,json}` | 全ツール統合フィード |
| `feeds/{tool_id}.{rss,atom,json}` | ツール別フィード |
| `{tool_id}.html` / `{tool_id}_ja.html` | ツールごとのまとめページ（英語/日本語） |
| `comparison.html` / `comparison_ja.html` | 全ツール比較ページ（概要版テーブル＋詳細版テーブル） |
| `index.html` | トップページ（フィード一覧・比較ページへのリンク） |
| `.nojekyll` | GitHub Pages の Jekyll 処理を無効化 |

HTMLページは `prefers-color-scheme` メディアクエリでブラウザ・OS の設定を検知し、自動的にダークモードを適用する。

`index.html` のツール一覧は概要版テーブルと同じソート順（概要版機能フラグのチェックマーク数降順、同数は `gui: true` 優先、さらに同条件はアルファベット昇順）で並べる。`comparison.html` の各テーブルはテーブルごとに独立したソート順を持つ（そのテーブルの列のチェックマーク数降順、同数は `gui: true` 優先、さらに同条件はアルファベット順）。

### ツール個別ページの構成

ツール個別ページ（`{tool_id}.html` / `{tool_id}_ja.html`）には以下を含む。

- ツール概要（タイトル・説明・種別・ライセンス・ホームページリンク）
- **機能表**：9 項目の機能フラグを ✅/❌ で表示
  - Webアプリケーションスキャン、APIスキャン、認証スキャン、アクティブスキャン、パッシブスキャン、Webクローラー、CI/CD連携、レポート生成、GUI
- 機能一覧の情報源リンク（tools.yml の `features_url`、未設定時は `homepage` にフォールバック）
- リリース履歴（バージョン・日付・説明のリスト）
- リリース履歴見出し直下に情報源 URL リンク（上流のリリースページへのリンク）

### 比較ページの構成

比較ページ（`comparison.html` / `comparison_ja.html`）は 2 つのテーブルで構成する。

- **概要版テーブル**：ツール名（個別ページへのリンクと機能一覧リンクを含む）・最新バージョン・最終更新日・種別・ライセンス・費用および基本機能フラグ（Webスキャン・APIスキャン・認証・アクティブ・パッシブ）。
- **詳細版テーブル**：ツール名（個別ページへのリンクと機能一覧リンクを含む）・全機能フラグ・独自機能列を含む。機能フラグ一覧：
  - Webスキャン、APIスキャン、認証、アクティブ、パッシブ、クローラー、CI/CD、レポート、GUI

各テーブルは独立したソート順を持つ（そのテーブルの列のチェックマーク数降順、同数はGUIあり優先、さらに同条件はアルファベット順）。

---

## 6. 非機能要件

詳細は [spec-nonfunctional_ja.md](spec-nonfunctional_ja.md) を参照。

- GitHub API を優先し、スクレイピングは最終手段とする
- 障害時は部分失敗を許容し、他ツールのフィードは継続して更新する
- アトミック書き込みにより中途半端なファイルを公開しない
