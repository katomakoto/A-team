# Aチーム
__メンバー__
- 慶應義塾大学　加藤慎
- 東京大学　　　橋本直樹
- 東京工業大学　宮下和也
- ゲームアシスタント　知能あかり  
<img src="https://res.cloudinary.com/hx3z2s9d0/image/upload/v1577234505/ritsu_1_dash.png" title="知能あかり" width=200>
デザイン：橋本直樹 

# セールスポイントや差別化できる点
- プレイヤーの目線： ゲームのUIをこだわる  
見やすいデザイン，操作に不快感のない便利な機能を作る．またプレイしたくなるようなゲームにする．  
SNSの活用や著作権への配慮など商業的な観点も意識しながら，サブカルチャーを取り入れることで，  
新たな顧客獲得まで見据えたwebページとして提供する．
- 運営側の目線： おしゃれで洗礼されたソースコードにする  
可読性と保守性を意識し，チームでの開発を円滑に進める．  

作成したwebサイト:　 https://hab-with-a-girl.herokuapp.com/ 　<--ここをクリック！  


# 課題の情報
My Mastermind   
https://damp-earth-70561.herokuapp.com/  

Player information  
Name: A  
ID  : 6839fe8a-78ce-4d4c-92af-1962aa3b3cc5  
Name: A2  
ID  : 7ae6a8d9-e168-46c0-9d5b-68ab13e383b0  

# ディレクトリの構成
.  
├── Pipfile  
│(web用)  
├── manage .py  
├── Procfile  
├── requirements .txt  
├── runtime .txt        
├── templates   
│    └── sample .html (webページ)  
├── battlepages  
│    │(html用のjavascriptとcss)   
│    ├── static  
│    │    ├── game_api .js (jsでの対戦)  
│    │  
│    │(djangoでのページの機能追加)  
│    ├── views .py (jsとの通信と対戦用アルゴリズムの操作)  
│     
├── config  
│    ├── local_setting .py (deploy用に追加)  
│     
└── main  
　   ├── \_\_init__ .py  
　   │(__提出用コード__)  
　   ├── battle100A .py  
　   ├── battle100A2 .py  
　   │(対戦アルゴリズムのクラスの作成)  
　   ├── requestsapi .py (apiとの通信機能)  
　   ├── hitandblow .py (対戦時に必要な情報の取得や判定機能, requestsapi継承)  
　   ├── number_guess_simple .py (5桁の数字予測アルゴリズム, hitandblow継承)   
　   │(開発時に使用したtest，コマンド上での対戦や，性能評価に使用したコードなど)  
　   └── tests  
　　  　　 ├──

# 100回対戦するとき(コマンド)
```bash
python main/battle100A.py
```
ROOM IDをinputで聞かれるので，入力した部屋番号から昇順で対戦が100回行われる．
# clone後のインストールの操作(コマンド)
Pythonの設定（3.9.1-6までは確認済み）
```bash
pyenv install 3.9.1
pyenv global 3.9.1
```
仮想環境の構築
```bash
pipenv install
```
# djangoをローカルで動かすとき(コマンド)
```bash
python manage.py runserver
```
停止はctrl+c  

http://127.0.0.1:8000/  

# 開発作業のメモ
- pytestを動かすときのコマンド
```bash
pytest -v --capture=no
```
