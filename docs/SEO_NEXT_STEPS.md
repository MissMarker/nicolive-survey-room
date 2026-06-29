# Search Console 次の作業

GitHub Pagesで公開したあと、Google検索に反映されやすくするための確認手順です。反映には数日から数週間かかることがあります。

## sitemap.xml を送信する

1. Google Search Consoleを開きます。
2. 対象プロパティを選びます。
3. 左側メニューの「サイトマップ」を開きます。
4. `https://missmarker.github.io/nicolive-survey-room/sitemap.xml` を入力します。
5. 送信します。

## トップページをURL検査する

1. Search Console上部のURL検査欄にトップページのURLを入れます。
2. `https://missmarker.github.io/nicolive-survey-room/` を検査します。
3. 登録されていない場合は、インデックス登録をリクエストします。

## 重要な記事ページをURL検査する

次のような記事から数本を選び、URL検査を行います。

- `articles/how-to-use.html`
- `articles/how-to-read-survey.html`
- `articles/best-rated-anime-guide.html`
- `articles/data-notes.html`

全部を一度に急いで申請しなくても大丈夫です。まずはトップページと主要な記事を確認します。

## site:検索で確認する

Google検索で次のように検索します。

```
site:missmarker.github.io/nicolive-survey-room
```

検索結果にトップページや記事が出てくれば、Googleに認識され始めています。出ない場合でも、公開直後は時間がかかることがあります。

## 反映を待つ

Search Consoleで送信しても、検索結果にすぐ表示されるとは限りません。数日から数週間かかる場合があります。サイトマップ、内部リンク、記事ページが正しく開ける状態を保って待ちます。
