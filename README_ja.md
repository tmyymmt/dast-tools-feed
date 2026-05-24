# DAST ツールフィード

DAST（動的脆弱性スキャン）ツールのリリース情報フィード。

GitHub Actions により毎週自動更新されます。任意のRSSリーダーで購読できます。

🌐 **公開サイト**: https://tmyymmt.github.io/dast-tools-feed/

## DASTとは？

DAST（Dynamic Application Security Testing：動的アプリケーションセキュリティテスト）とは、ソースコードにアクセスせずに、実際に動作しているアプリケーションにリクエストを送信してレスポンスを観察することで脆弱性を検出するセキュリティテスト手法です。DASTツールは、XSS・SQLインジェクション・認証の欠陥・設定ミスなどの脆弱性を実際の攻撃と同様の手法で検出します。

## 対象ツール

| ツール | 種別 | ライセンス |
|--------|------|----------|
| [OWASP ZAP](https://www.zaproxy.org) | OSS | Apache-2.0 |
| [Nuclei](https://nuclei.projectdiscovery.io) | OSS | MIT |
| [sqlmap](https://sqlmap.org) | OSS | GPL-2.0 |
| [Nikto](https://cirt.net/Nikto2) | OSS | GPL-2.0 |
| [Wapiti](https://wapiti-scanner.github.io) | OSS | GPL-2.0 |
| [Burp Suite](https://portswigger.net/burp) | 商用 | Proprietary |

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

## ローカル開発

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# フィード・ページ生成
FEED_BASE_URL="https://tmyymmt.github.io/dast-tools-feed/feeds" python -m scripts.main

# テスト実行
pytest tests/
```

## ライセンス

MIT License
