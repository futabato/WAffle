# revProxy

正規表現によるパターンマッチングとCharacter-level CNNで防御するWAF。  
`denylist.txt`に正規表現を追加していけばより強くなる。  

## 使用方法

事前に`/WAffle/vuln`のウェブサーバを起動しておく必要がある。  

```txt
$ python3 revProxy.py
```

`WAffle/revProxy/`配下で上記のコマンドを実行する。
`localhost:5000`にアクセスし、`index`が表示されることを確認する。

`localhost:5000/<script>alert(1)</script>` などにアクセスすると`WAffle`のページが表示される。  

## dashboard

```txt
$ python3 dashboard.py
```

`localhost:5001`でログを監視できる。  
