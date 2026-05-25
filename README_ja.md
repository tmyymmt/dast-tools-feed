# DAST ツールフィード

DAST（動的脆弱性スキャン）ツールのリリース情報フィード。

GitHub Actions により毎週自動更新されます。任意のRSSリーダーで購読できます。

🌐 **公開サイト**: https://tmyymmt.github.io/dast-tools-feed/

## 対象ツールの種類

本リポジトリが扱うのは、**DAST（Dynamic Application Security Testing）ツール**、すなわち**実行中のアプリケーションに対して動的に脆弱性検査を行うツール**です。

具体的には、稼働中のWebアプリケーションやAPIに対してリクエストを送信し、そのレスポンスや挙動を観測することで、XSS・SQLインジェクション・認証不備・設定ミスなどの脆弱性を検出するツールを対象とします。

以下のカテゴリのツールは対象外です：

- **SCA（Software Composition Analysis）**：SBOMや依存関係解析をもとに既知脆弱性を検出するツール
  （関連: https://github.com/tmyymmt/sca-tools-feed/）
- **SAST（Static Application Security Testing）**：ソースコードを静的解析して脆弱性を検出するツール
  （関連: https://github.com/tmyymmt/sast-tools-feed/）

## 動作原理

- 以下のいずれかの方法でフィードファイルを更新し、HTML ページ（Markdown ソースから生成）をレンダリングする
  - GitHub Actions で週次（毎週土曜 JST 07:00）で実行
  - Issue を作成し、Copilot で PR を作成、レビューを完了し、main にマージ

## フィード URL

### 全ツール統合

| フォーマット | URL |
|------------|-----|
| RSS 2.0 | `https://tmyymmt.github.io/dast-tools-feed/feeds/all.rss` |
| Atom 1.0 | `https://tmyymmt.github.io/dast-tools-feed/feeds/all.atom` |
| JSON Feed 1.1 | `https://tmyymmt.github.io/dast-tools-feed/feeds/all.json` |

### ツール別フィード

`{tool_id}` を `zap`、`nuclei`、`sqlmap`、`nikto`、`wapiti`、`burpsuite` に置き換えてください。

| フォーマット | URL |
|------------|-----|
| RSS 2.0 | `https://tmyymmt.github.io/dast-tools-feed/feeds/{tool_id}.rss` |
| Atom 1.0 | `https://tmyymmt.github.io/dast-tools-feed/feeds/{tool_id}.atom` |
| JSON Feed 1.1 | `https://tmyymmt.github.io/dast-tools-feed/feeds/{tool_id}.json` |

## ページ

- **比較ページ**: [英語](https://tmyymmt.github.io/dast-tools-feed/comparison.html) / [日本語](https://tmyymmt.github.io/dast-tools-feed/comparison_ja.html)
- **ツール別まとめ**: `https://tmyymmt.github.io/dast-tools-feed/{tool_id}.html`

## リリースカテゴリ

リリースはカテゴリで分類され、フィルタリングに使用できます。

| カテゴリ | 説明 |
|---------|------|
| `feature` | 機能追加・変更 |
| `bugfix` | バグ修正 |
| `security` | セキュリティ修正・Hotfix |
| `pricing` | 料金変更 |
| `announcement` | 告知・イベント・受賞 |
| `other` | その他 |

## リポジトリ構成

```
.
├── scripts/            # Python スクリプト
│   ├── main.py         # エントリーポイント
│   ├── models.py       # データモデル
│   ├── categorize.py   # リリース分類
│   ├── storage.py      # JSON ストレージ
│   ├── feed_generator.py   # RSS/Atom/JSON Feed 生成
│   ├── markdown_generator.py  # HTML ページ生成
│   └── collectors/     # ツール種別ごとのデータ収集
│       ├── github.py   # GitHub Releases API コレクター
│       └── burpsuite.py  # Burp Suite HTML スクレイパー
├── tools/
│   └── tools.yml       # ツール設定ファイル
├── data/               # 収集済みリリースデータ（JSON）
├── public/             # 生成された出力（gitignore 済み、GitHub Pages にデプロイ）
├── tests/              # テストスイート
└── docs/               # 仕様書
```

## ルール

- ドキュメントは日本語と英語の両方を作成する
  - 英語は `*.md` 、日本語は `*_ja.md` とする
- 機能改修時に全仕様書も更新する
- AI向けのルールは .github/copilot-instructions.md に記載する

## セットアップ

### 前提条件

- Python 3.11 以上

### インストール

```bash
# 仮想環境の作成と有効化
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 依存ライブラリのインストール
pip install -r requirements.txt

# 開発用ライブラリのインストール（テスト実行時のみ）
pip install -r requirements-dev.txt
```

## ローカル実行

### 環境変数の設定

GitHub API を使用するため、`GITHUB_TOKEN` が必要です。

```bash
export GITHUB_TOKEN=your_github_token
```

### 実行

```bash
python -m scripts.main
```

`public/` 配下の HTML ファイルと `public/feeds/` 配下のフィードファイルが更新されます。

## GitHub Actions

### 自動実行（週次）

`.github/workflows/update-feeds.yml` により、毎週土曜日 JST 07:00（UTC 金曜 22:00）に自動実行されます。

### 手動実行

GitHub リポジトリの **Actions** タブ → **Update Feeds** → **Run workflow** から手動実行できます。

### 必要な設定

- **Secrets**: `GITHUB_TOKEN` は GitHub Actions により自動的に提供されるため、追加設定は不要です。
- **Permissions**: `contents: write`（データコミット用）、`pages: write`（GitHub Pages デプロイ用）が設定済みです。
- **GitHub Pages**: リポジトリの Settings → Pages から、Source を `GitHub Actions` に設定してください。

## ライセンス

MIT License
