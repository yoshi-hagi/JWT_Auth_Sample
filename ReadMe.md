これはJWT認証をFastAPIのみで行うサンプルコードです。  
起動前にmigrate_db.pyを実行し、データベースの生成及びマイグレーションをして下さい。  
SQLite3でのデータベースが作成されます。 
コマンド: py -m migrate_db
ローカルで起動する場合はuvicornで起動して下さい。  
コマンド: py -m uvicorn main:app --reload  
認証に必要なデータ登録はSwaggerUI上で実行して下さい。  
※URL末尾に/docsを付けて移動し、'/auth/create/user'からis_adminをtrueにして管理者を作成して下さい。  
