# revProxy

ブラックリストベースのWAF
blacklist.txtに正規表現を追加していけば強くなる

## 使用方法

> apacheか何かで`localhost:80`にウェブサーバを起動しておくこと

```txt
py revProxy.py
```

`localhost:5000`にアクセスし、apacheの`index.html`が表示されることを確認

`localhost:5000/<script>` などにアクセスすると`WAffle`のページが表示される
