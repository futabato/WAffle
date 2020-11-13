# revProxy

ブラックリストベースのWAF
blacklist.txtに正規表現を追加していけば強くなる

## 使用方法

> `/WAffle/vuln`のウェブサーバを起動しておくこと

```txt
python3 revProxy.py
```

`WAffle/revProxy/`配下で上のコマンドを実行する。
`localhost:5000`にアクセスし、`index`が表示されることを確認する

`localhost:5000/<script>` などにアクセスすると`WAffle`のページが表示される

## dashboard

```txt
python3 dashboard.py
```

`localhost:5001`でログが監視できる
