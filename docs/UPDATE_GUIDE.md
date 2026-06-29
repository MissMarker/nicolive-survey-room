# 更新手順

この手順は、PC操作に慣れていない人でもデータを更新できるようにしたものです。

## 1. まず確認するもの

- `index.html` が現在公開するページです。
- `data/survey_data.csv` が元データです。
- `data/inbox/recent_rows_template.csv` が追加データ用のひな形です。
- 欠損値は推測で埋めないでください。分からない値は空欄のままにします。

## 2. 手元で1件ずつ追加する場合

1. `data/inbox/recent_rows_template.csv` をコピーします。
2. コピーしたファイル名を `recent_rows.csv` にします。
3. 追加したい行だけを `recent_rows.csv` に入力します。
4. 列の順番は変えないでください。
5. 作品名、数値、日時、lvIDは確認できた内容だけを書きます。

## 3. コマンドで確認する場合

サイトのフォルダを開いて、次の順番で実行します。

```bash
python tools/merge_recent.py --base data/survey_data.csv --recent data/inbox/recent_rows.csv --out data/survey_data.csv
python tools/validate_data.py data/survey_data.csv
python tools/build_site.py --csv data/survey_data.csv --template src/index.template.html --out index.html
```

更新後は `index.html` をブラウザで開き、検索、年別、作品から探す、ランキングを確認します。

## 4. GitHub Actionsで自動更新する場合

1. GitHubのリポジトリを開きます。
2. `Settings` を開きます。
3. `Secrets and variables` の `Actions` を開きます。
4. `New repository secret` を押します。
5. 名前に `UPSTREAM_CSV_URL` を入れます。
6. 値に取得元CSVのURLを入れます。

URLはコードに直接書かず、必ず GitHub Secrets に入れてください。

## 5. 公開前の確認

- データ利用許諾を確認する。
- 出典表示が必要な場合は追加する。
- 連絡先を用意する。
- プライバシーポリシーと広告表記を確認する。
- `admin.html` は検索エンジンに出さない運用のままにする。

## 6. 楽天アフィリエイトリンクを入れる場合

1. 楽天アフィリエイトで広告リンクを作成します。
2. `data/affiliate_config.json` を開きます。
3. `enabled` を `true` にします。
4. `rakutenLinks` に、表示名とURLを追加します。
5. `python tools/build_site.py --csv data/survey_data.csv --template src/index.template.html --out index.html` を実行します。

広告リンクには、公開ページ側で `rel="sponsored nofollow noopener noreferrer"` が付くようにしています。

