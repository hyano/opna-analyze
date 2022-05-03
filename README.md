# opna-analyze

OPNA(YM2608)の挙動を調べるために即席で用意した環境です。
PC-8801mkIISR(以下、PC-88)とRS-232Cケーブルで接続し、簡単なサーバプログラムをPC-88側で動作させ、
ホストからコマンドを送信して、OPNAのレジスタを読み書きすることによって、挙動を調べます。

# 手順

## ホスト側の準備

* pySerialを使えるようにする。以下、例。
  * python -m venv .venv
  * source .venv/bin/activate
  * pip -r requirements.txt
* あちこちにハードコーディングされているシリアルポートのデバイス名を環境に合わせる。
  * ex.) RsOPNA.py

## PC-88側でのサーバプログラムの起動

* ボーレートをPC-88とホストで合わせる。私は19,200bpsを使用した。
* PC-88をシリアルポートからプログラムをロード待ちにする。
  * (PC-88): LOAD "COM:N81"
* ホストからサーバプログラムを転送する。
  * (Host): python ./util/upload.py basic/rsopna.bas
  * (PC-88): 頃合いを見計らって、STOPで停止。
* サーバプログラムを実行する。
  * (PC-88): RUN

## テストプログラムの実行

* python -u mem_rw.py

# 実行結果など

* [ログの例](log/mem_rw.txt)
* [上記からの考察](doc/OPNA.md)
# その他

* 2022/04
  * OPNAのADPCM周りの挙動を調べようと思い立ち、屋根裏からPC-88を引っ張り出してきました。
  * 作業を始めて間も無くしたところで、残念ながらPC-88が起動しなくなってしまいました。
  * PC-88を使っての調査は継続できなくなってしまいましたが、再利用の可能性もあるので、GitHubに保全しておくことにしました。
  * 調査用HWを入手できたら、再開してみようと思っています。
