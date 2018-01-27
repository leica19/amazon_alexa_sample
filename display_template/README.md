# ディスプレイテンプレートのサンプル

Echo Show、Echo spotのようなディスプレイを持ったデバイスでのレイアウトの実装方法についてのサンプルです。

![sample image](https://github.com/sparkgene/amazon_alexa_sample/raw/master/display_template/media/body_template2.png)

## 使い方

### S3にバケットを作成

以下の内容でバケットのポリシーを設定して下さい。
`{your bucket name}` は、ご自身で作成したバケット名に置き換えてください。

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadForGetBucketObjets",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::{your bucket name}/*"
        }
    ]
}
```

media ディレクトリに含まれているファイルをすべて作成したバケットにコピーします。
ブラウザからアップロードしたファイルにアクセスできることを確認します。

### Lambda Functionの作成

#### Lambdaの基本情報

- お好きな名前でLambda ファンクションを作成します
- Runtimeは`Python 3.6` 
- Roleが無い場合はLambda用のロールを作成します。

#### ソース
`src/lambda_function.py` の中身をLambdaのソースに貼り付けて保存します。

#### 環境変数の設定

以下のkeyとvalueで環境変数を設定して下さい。

|key|value|
|---|-----|
|MEDIA_BUCKET| 作成したバケット名 |
|BUCKET_DOMAIN|東京リージョンであれば `s3-ap-northeast-1` 。 `us-east-1` の場合は、 `s3`|

### スキルを作成

カスタムスキルを作成します。
ディスプレイテンプレートは英語版でしか利用できないため、スキルの言語は `English (U.S.)` を利用して下さい。

#### スキル情報

- グローバルフィールド
  - レンダリングテンプレート にチェックを付けます。
  - ビデオアプリ にチェックを付けます。
- 対話モデル
  - インテントスキーマ
    - `model/intentSchema.json` の中身をコピー
  - サンプル発話
    - `modle/SampleUtterances.txt` の中身をコピー


### スキルをテスト

テストシミュレータで `open ＜呼出し名＞` と入力して実行すると開始します。
次のテンプレートを見るか聞いてくるので、 `yes` と入力すると次へ進みます。

直接、テンプレートを指定することも可能です。
（テストシミュレータでは actionとvideoの動作確認は出来ません）

- ＜呼出し名＞ body template number 1
- ＜呼出し名＞ body template number 2
- ＜呼出し名＞ body template number 3
- ＜呼出し名＞ body template number 6
- ＜呼出し名＞ list template number 1
- ＜呼出し名＞ list template number 2
- ＜呼出し名＞ video
- ＜呼出し名＞ action sample
