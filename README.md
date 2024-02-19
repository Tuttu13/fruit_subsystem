# 課題 - 果物管理システム

## バージョンについて
以下に、Pythonのバージョンと各パッケージのバージョン/導入理由について記載します。
#### Pythonのバージョン  
- Python: 3.12.0
#### 各パッケージのバージョン/導入理由 
- Django: 5.0.1
- django-bootstrap5: 23.4  
  → bootstrapでデザインを整えるために導入しました。
- jaconv==0.3.4  
  → カタカナとひらがなを変換するために導入しました。

## データベースについて
- データベースは、sqlite3を使用しました。

## 実行手順について
以下に、実行手順について記載します。1～5までの項目を順に沿って実施してください。  
1. 以下のコマンドを実行し、マイグレーションファイルを作成  
```python manage.py makemigrations fruit_app```
2. 以下のコマンドを実行し、マイグレーションを実行  
```python manage.py migrate```
3. 以下のコマンドを実行し、superuserを作成  
```python manage.py createsuperuser```  
　※メールアドレスは未登録でも問題ありません
4. 以下のコマンドを実行し、サーバーを起動  
```python manage.py runserver```
5. 以下のサーバーへアクセス  
```http://127.0.0.1:8000/```

ログイン画面から実行手順3で作成したsuperuserでログインを行い、果物管理システムの操作を行ってください。

## 工夫したポイントについて  
以下に、工夫した7つのポイントについて記載します。
- 販売統計情報のコンテクストのデータ(累計、月別、日別)を取得するクラスを作成しました。  
  クラス内で関数を3つ定義し、画面に出力するデータ(累計、月別、日別)を取得しました。
- 販売統計情報画面のデータ(累計、月別、日別)生成する関数をモジュール化しました。  
  ```statistics_info/statistics_module.py```を作成しました。
- 販売統計情報画面の各月別、日別のデータをdate_typeで判断させて、データを生成しました。  
  月別の場合、```"monthly"```  (statistics_info/statistics_views.py L37)  
  日別の場合、```"daily"```  (statistics_info/statistics_views.py L67)  
- 当月、当日を判断するためにkeyリストを作成し、dict型データからget関数を用いてkeyに該当するvalueを取得する処理にしました。  
  当月の場合、create_monthly_key_list関数 (statistics_info\statistics_views.py L39)  
  当日の場合、create_daily_key_list関数 (statistics_info\statistics_views.py L69)  
  上記で作成したkeyを基にget_latest_fruits_list関数で処理を行いました。 
- 今後、新しくページ・機能を追加することに考慮して、各ページごとにアプリを作成し分割しました。  
  またページ自体を削除する際にデグレード防止も考慮しました。
- 各画面のデザインがぶれないように画面のデザインをbootstrapを用いて整え、画面に統一性を持たせました。  
- データベースはsqlite3を使用しました。sqlite3はタイムゾーンの設定をするオプションがないため、アプリ内で考慮して作成をしました。  
converter_datetime関数で処理を行いました。

## フォルダ構成概要
以下に、フォルダ構成の概要についてツリーにしました。
<pre>
fruit_subsystem
├── account(ログイン機能)
├── fruit_app(果物マスタ管理機能)
├── fruit_sales_manager(プロジェクト設定)
├── sales(販売情報管理機能)
├── statistics_info(販売統計情報機能)
├── templates(各画面html)
├── manage.py
├── README.md
└── requirements.txt
</pre>
