# 課題 - 果物管理システム

## ・実行手順について
以下に、実行手順について記載します。また1から順に実施してください  
1. 以下のコマンドを実行し、マイグレーションファイル作成  
```python manage.py makemigrations```
2. 以下のコマンドを実行し、マイグレーション実行  
```python3 manage.py migrate fruit_app```
3. 以下のコマンドを実行し、superuserの作成  
```python manage.py createsuperuser```  
またメールアドレスは未登録でも問題ありません

1から3を完了した上で、ログイン画面からログインを行い、  
果物管理システムアプリの操作を行ってください

## ・工夫したポイントについて  
以下に、工夫したポイントについて記載します。  
工夫したポイントは3つあります。
1. 販売統計情報画面の各月別、日別のデータをformat_typeで判断させさせて、データを生成しました。
   販売統計情報画面の出力するデータをモジュール化しました。
2. さらに機能を追加することを考慮して、各ページをアプリ層に分割して作成しました。
3. point3
   

