# analysis

Streamlitを使って可視化をします。  

## test_data.py

[HTTP DATASET CSIC 2010](https://www.isi.csic.es/dataset/)のTestデータ(6,107件)に対して性能テストを行ったあとの結果（False Positive一覧・False Negative一覧）を確認できます。  
[evaluation.csv](https://drive.google.com/file/d/1PENhBPGiEq_S1qD-JJSLWblR9hBFxknA/view?usp=sharing)を`WAffle/model/evaluation`にダウンロードすることで確認ができます。

`$ streamlit run test_data.py`  

## analysis.py

WAFを介した通信は、csvファイルとして`WAffle/analysis`に保存されています。  

`$ streamlit run analysis.py`  
