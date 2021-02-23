# WAffle

a Web Application Firewall using Signature and Character-level CNN  

## 概要

正規表現によるパターンマッチングとCharacter-level CNNで防御するWeb Application FirewallをPythonで実装しました。  

[HTTP DATASET CSIC 2010](https://www.isi.csic.es/dataset/)をTraining : Validation : Test = 7.5 : 1.5 : 1.0に分割し、学習と検証を行いました。  
Testデータ(6,107件)に対して、Accuracy: 86.4, Precision: 75.7, Recall: 99.3という精度が出ています。  

使用したテストデータと、性能テストを行った後のcsvファイル、学習済みモデルはGoogle Driveからダウンロードできます。  
- [test_data.csv](https://drive.google.com/file/d/1tAyz4NLxBurCJPr72Yoa-u6lB9B3jsrc/view?usp=sharing)
- [evaluation.csv](https://drive.google.com/file/d/1PENhBPGiEq_S1qD-JJSLWblR9hBFxknA/view?usp=sharing)
- [model.h5](https://drive.google.com/file/d/1vXMnACj1IAAuXcG-gWbuYEsoB9Kaqxn8/view?usp=sharing)  

元のデータセットをcsv形式に変換したものはkaggleにて公開されていたので、以下のリンクからダウンロードしました。  
[CSIC 2010 Web Application Attacks | Kaggle](https://www.kaggle.com/ispangler/csic-2010-web-application-attacks)  

### revProxy

`revProxy.py`がWAFの本体となっています。  
`$ python revProxy.py`  
簡単なダッシュボードを用意しています。  
`$ python dashboard.py`

### vuln

防御対象となる脆弱なWebアプリケーションをPHPで実装しています。  
バックドアなども含まれるため、cloneしたらフォルダをWindows Defenderから除外する必要があります。  
`$ docker-compose up --build`

### model

[Character-level CNN](https://arxiv.org/abs/1509.01626)という手法を使っています。  
[Web Application Firewall using Character-level Convolutional Neural Network](http://iyatomi-lab.info/sites/default/files/user/CSPA2018%20Proceedings_ito.pdf)という論文を参考に、Kerasで実装しました。  

### analysis

WAffleを介した通信内容はcsvファイルとして保存していて、Streamlitによって開くことができるようになっています。  
`$ streamlit run analysis.py`  
