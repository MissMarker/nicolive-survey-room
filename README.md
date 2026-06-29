# ニコ生アニメアンケート資料室

ニコニコ生放送のアニメ番組アンケート結果を、年別・クール別・作品別に探せるようにした非公式の静的サイトです。

## ファイル構成

- `index.html` — 公開ページ本体。ヘッダー画像、スタイル、検索用スクリプト、29,463件のデータを含む単一HTMLです。
- `data/survey_data.csv` — `index.html` に埋め込む元データCSVです。
- `data/inbox/recent_rows_template.csv` — 追加データ入力用のひな形です。
- `data/affiliate_config.json` — 楽天アフィリエイトリンクの設定ファイルです。
- `tools/validate_data.py` — データ検証用スクリプトです。
- `tools/merge_recent.py` — 追加データを既存CSVに統合するスクリプトです。
- `tools/build_site.py` — CSVとテンプレートから `index.html` を再生成するスクリプトです。
- `src/index.template.html` — 公開ページのテンプレートです。
- `.github/workflows/update-data.yml` — GitHub Actions用の更新ワークフローです。
- `privacy.html` — プライバシーポリシー。
- `affiliate-disclosure.html` — 広告・アフィリエイト表記。
- `admin.html` — 運営用メモ。
- `docs/UPDATE_GUIDE.md` — 更新手順。
- `docs/PUBLISH_CHECKLIST.md` — 公開前チェックリスト。
- `docs/REMAINING_TASKS.md` — 運用に向けた残作業。
- `docs/QA_REPORT_FINAL.md` — 最終確認結果。

## 公開前の重要注意

このパッケージは公開運用の土台です。一般公開・収益化する前に、データ利用許諾、出典表示、連絡先、プライバシーポリシー、広告表記を確認してください。

外部CSVのURLはコードに直書きせず、GitHub Secrets の `UPSTREAM_CSV_URL` を使ってください。データの欠損値は推測で補完せず、確認できた事実だけを反映してください。
