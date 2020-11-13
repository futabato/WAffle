# revProxy

ブラックリストベースのWAF
blacklist.txtに正規表現を追加していけば強くなる

## 使用方法

> `/WAffle/vuln`のウェブサーバを起動しておくこと

```txt
python3 revProxy.py
```

`localhost:5000`にアクセスし、`index`が表示されることを確認する

`localhost:5000/<script>` などにアクセスすると`WAffle`のページが表示される
