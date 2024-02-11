# 課題 - 果物管理システム

## バージョンについて
以下に、Pythonのバージョンと各パッケージのバージョン/導入理由について記載します。
#### Pythonのバージョン  
- Python: 3.12.0
#### 各パッケージのバージョン/導入理由 
- Django: 5.0.1
- django-bootstrap5: 23.4  
  → bootstrapでデザインを整えるために導入しました。
- django-pandas: 0.6.6  
  → djangoでqueryset型のデータをデータフレームに変換するために導入しました。  
- numpy: 1.26.3
- pandas: 2.2.0

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

ログイン画面から実行手順3で作成したsuperuserでログインを行い、果物管理システムアプリの操作を行ってください。

## 工夫したポイントについて  
以下に、工夫した6つのポイントについて記載します。
- 販売統計情報のコンテクストのデータ(累計、月別、日別)を取得するクラスを作成し、  
  クラス内で関数を3つ作成しました。
- 販売統計情報画面のデータ(累計、月別、日別)生成する関数をモジュール化しました。  
  ```statistics_info\statistics_module.py```を作成しました。
- 販売統計情報画面の各月別、日別のデータをformat_typeで判断させさせて、データを生成しました。  
  月別の場合、```'monthly'```  (statistics_info\statistics_views.py L30)  
  日別の場合、```'dayly'```  (statistics_info\statistics_views.py L65)  
- 今後、機能を追加することを考慮して、各ページをアプリ層に分割して作成しました。  
  またページ自体を削除する際のデグレード防止も考慮しました。
- 各画面のデザインがぶれないように画面のデザインをbootstrapを用いて整えて、画面に統一性を持たせました。  
- データベースはsqlite3を使用しました。sqlite3はタイムゾーンの設定のオプションがないため、アプリ内で考慮して作成をしました。

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
└── README.md
</pre>
