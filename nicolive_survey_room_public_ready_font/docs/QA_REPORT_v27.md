# QA_REPORT_v27

## 修正内容
- ヘッダーの文字まわりの白い枠・境界線・カード背景を削除。
- 画像はヘッダー全面の背景として維持。
- 文字の読みやすさは、ヘッダー全体の薄いグラデーションと控えめな文字影で確保。
- PCでは右側、スマホでは下側に文字が乗る配置を維持。
- `index.html` は画像をHTML内に埋め込んだままなので、プレビューでも画像が出る構成。

## 確認
- `index.html` に `header-card` / `header-figure` / `header-copy` のCSSあり。
- `header-copy` の `border` は 0。
- `header-copy` の `background` は transparent。
- 画像は `data:image/png;base64` として埋め込み済み。
