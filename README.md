# WAffle

a Web Application Firewall using Signature and Character-level CNN

## 概要

正規表現によるパターンマッチングとCharacter-level CNNで防御するWeb Application FirewallをPythonで実装しました。  

[HTTP DATASET CSIC 2010](https://www.isi.csic.es/dataset/)のテストデータ(6,107件)に対して、Accuracy: 86.4, Precision: 75.7, Recall: 99.3という精度が出ています。  

使用したテストデータと、性能テストを行った後のcsvファイル、学習済みモデルはGoogle Driveからダウンロードできます。  
- [test_data.csv](https://drive.google.com/file/d/1tAyz4NLxBurCJPr72Yoa-u6lB9B3jsrc/view?usp=sharing)
- [evaluation.csv](https://drive.google.com/file/d/1PENhBPGiEq_S1qD-JJSLWblR9hBFxknA/view?usp=sharing)
- [model.h5](https://drive.google.com/file/d/1vXMnACj1IAAuXcG-gWbuYEsoB9Kaqxn8/view?usp=sharing)  

### revProxy

`revProxy.py`がWAFの本体となっています。  
`$ python revProxy.py`
簡単なダッシュボードを用意しています。  
`$ python dashboard.py`

### vuln

防御対象となる脆弱なWebアプリケーションをPHPで実装しています。  
バックドアなども含まれるため、cloneしたらフォルダをWindows Defenderから除外するようにする必要があります。  
`$ docker-compose up --build -d`

### model

[Character-level CNN](https://arxiv.org/abs/1509.01626)という手法を使っています。  
[Web Application Firewall using Character-level Convolutional Neural Network](http://iyatomi-lab.info/sites/default/files/user/CSPA2018%20Proceedings_ito.pdf)という論文を参考に、Kerasで実装しました。  

### analysis

WAffleを介した通信内容はcsvファイルとして保存していて、Streamlitによって開くことができるようになっています。  
`$ streamlit run analysis.py`  
