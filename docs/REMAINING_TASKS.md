# REMAINING_TASKS

自動更新運用に向けた骨組みは追加済みです。

## 追加済み

- `data/survey_data.csv`
- `data/inbox/recent_rows_template.csv`
- `tools/validate_data.py`
- `tools/merge_recent.py`
- `tools/build_site.py`
- `src/index.template.html`
- `.github/workflows/update-data.yml`
- `docs/UPDATE_GUIDE.md`
- `docs/PUBLISH_CHECKLIST.md`

## 残作業

- 外部CSVを使う場合は、GitHub Secrets に `UPSTREAM_CSV_URL` を設定する。
- データ利用許諾、出典表示、連絡先、プライバシーポリシー、広告表記を公開前に確認する。
- 初回のGitHub Actions実行後、作成されたPull Requestの差分を人の目で確認する。
- 更新後は `index.html` の表示、検索、年別、作品から探す、ランキングを確認する。
- 欠損値は推測で補完せず、確認できない値は空欄のまま扱う。
