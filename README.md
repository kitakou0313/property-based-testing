# property-based-testing
train repository for property-based-test

## セットアップ

仮想環境（`.venv`）を作成し、依存パッケージをインストールする。

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## venvの起動

| シェル | コマンド |
| --- | --- |
| bash / zsh | `source .venv/bin/activate` |
| fish | `source .venv/bin/activate.fish` |

起動するとプロンプトの先頭に `(.venv)` が表示される。終了するには `deactivate` を実行する。

起動せずに実行する場合は `.venv/bin/python -m pytest` のようにパスを直接指定する。

## テストの実行

venv を起動した状態で実行する。

```sh
pytest
```
