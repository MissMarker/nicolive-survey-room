# 収益化設定メモ

このサイトは、楽天アフィリエイトを現在有効にし、AmazonアソシエイトとGoogle AdSenseは準備用の空設定だけを置いています。まだIDやタグを持っていないサービスは、本番広告として表示しません。

## 現在の状態

- 楽天アフィリエイト: 有効
- Amazonアソシエイト: 無効
- Google AdSense: 無効
- ホーム、ランキング、作品詳細、記事下部にスポンサーリンク枠を表示
- 作品詳細の広告は固定のアニメ関連広告として表示

## 設定場所

`index.html` の下部に `MONETIZE_CONFIG` があります。テンプレートから再生成する場合は、`src/index.template.html` と `data/affiliate_config.json` を使います。

```js
const MONETIZE_CONFIG = {
  rakuten: {
    enabled: true
  },
  amazon: {
    enabled: false,
    associateTag: ""
  },
  adsense: {
    enabled: false,
    clientId: "",
    slots: {}
  }
};
```

楽天の固定広告HTMLは、`data/affiliate_config.json` の `rakutenHtml` に入れます。楽天側が発行したURLは変更しないでください。

## Amazonアソシエイトを使う場合

1. Amazonアソシエイトに申し込みます。
2. 審査に通り、正式なアソシエイトタグを取得します。
3. `MONETIZE_CONFIG.amazon.associateTag` に取得したタグを入れます。
4. 作品名検索リンクを作る場合は、必ず正式なタグを使います。
5. 架空のタグや未確認のURLは作らないでください。
6. 利用開始後、`affiliate-disclosure.html` に必要な表示を追記します。

作品詳細で作品名検索リンクを追加する場合は、現在の固定広告とは別枠にし、広告であることが分かるようにPRまたはスポンサーリンクと表示します。

## Google AdSenseを使う場合

1. Google AdSenseに申し込みます。
2. 審査に通り、正式なクライアントIDと広告スロットIDを取得します。
3. `MONETIZE_CONFIG.adsense.enabled` を `true` にします。
4. `clientId` と `slots` に正式な値を入れます。
5. 取得前の仮IDや架空コードは入れないでください。

GitHub Pagesでは静的HTMLとして配信するため、広告コードを入れる前に、表示崩れや読み込みエラーがないか必ず確認してください。

## 文言の注意

現在の楽天広告は固定商品リンクです。開いている作品に連動しているとは限らないため、「この作品の関連商品」「関連商品を探す」「作品名の関連商品です」のような文言は使いません。

公開ページでは、次のような中立的な表示にします。

- スポンサーリンク
- アニメ関連商品の広告リンクです。
- 広告について

## データとの分離

広告設定を変更しても、アンケート結果の数値、作品名、話数、ランキングは変更しません。広告の有無によってデータを補正しないでください。
