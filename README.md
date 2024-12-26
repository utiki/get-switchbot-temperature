## Step 1
以下の手順でTOKENを生成
https://blog.switchbot.jp/announcement/api-v1-1/

## Step 2
.envファイルを作成

それぞれの項目を入力
```shell:.env
TOKEN=
CLIENT_SECRET=
HOUSE_THERMOMETER_ID=
OUTSIDE_THERMOMETER_ID=
DATABASE_URL=

POSTGRES_USER=user
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```

## Step3
dockerの起動
```shell
docker-compose up --build
```
