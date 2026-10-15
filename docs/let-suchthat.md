# ErlangのLET / SUCHTHATに相当するHypothesisの書き方

PropErの`?LET` / `?SUCHTHAT`はGeneratorを組み合わせるためのマクロ。
Hypothesisには同名のマクロはないが、strategyのメソッドと`@st.composite`で同じことができる。

## 対応表

| PropEr (Erlang) | Hypothesis | 用途 |
| --- | --- | --- |
| `?LET(X, Gen, f(X))` | `strategy.map(f)` | 生成値を変換するだけ |
| `?LET(X, Gen, Gen2(X))` | `strategy.flatmap(f)` / `@st.composite` | 生成値に依存して次のGeneratorを決める |
| `?SUCHTHAT(X, Gen, Pred)` | `strategy.filter(pred)` | 条件を満たす値だけに絞る |
| `?SUCHTHAT`（テスト内で使う場合） | `hypothesis.assume(cond)` | 条件を満たさないケースをテスト本体で捨てる |

## LET

### 単純な変換: `.map`
- 生成した値に関数を適用するだけなら`.map`を使う
- Generatorの形（型）は変わるが、依存する別のGeneratorは出てこない

```erlang
sorted_list() -> ?LET(L, list(integer()), lists:sort(L)).
```

```python
sorted_list = st.lists(st.integers()).map(sorted)
```

### 生成値に依存する値の生成: `@st.composite` / `.flatmap`
- 生成した値を使って、次のGeneratorを組み立てたい場合に使う
- 例: 「リストの要素数に応じて、indexの範囲を決める」
    - `tests/test_3/test_3.py`の「key_numberの最大値をtuples_listの要素数-1にしたい」はこのケース

```erlang
list_and_index() ->
    ?LET(L, non_empty(list(integer())),
         {L, choose(0, length(L) - 1)}).
```

```python
# composite版（推奨）
@st.composite
def list_and_index(draw):
    xs = draw(st.lists(st.integers(), min_size=1))
    i = draw(st.integers(0, len(xs) - 1))
    return xs, i


@given(list_and_index())
def test_xxx(p):
    xs, i = p
    assert 0 <= i < len(xs)
```

```python
# flatmap版
list_and_index = st.lists(st.integers(), min_size=1).flatmap(
    lambda xs: st.tuples(st.just(xs), st.integers(0, len(xs) - 1))
)

@given(list_and_index)
def test_xxx(p):
    ...
```

- `@st.composite`は`draw`を順に呼ぶだけで書ける
    - `?LET`をネストする代わりになる
    - 依存が2段以上になる場合はcompositeの方が読みやすい
- `@st.composite`で定義したものは**関数呼び出し**（`list_and_index()`）してstrategyにする
    - `.flatmap`の結果はそのままstrategyなので`()`は不要

## SUCHTHAT

### `.filter`
- Generatorが生成した値のうち、条件を満たすものだけを使う

```erlang
even() -> ?SUCHTHAT(N, integer(), N rem 2 =:= 0).
```

```python
even = st.integers().filter(lambda n: n % 2 == 0)
```

### `assume`
- テスト関数の中で、条件を満たさない入力を捨てる
- `.filter`と違い、Generatorの定義ではなくテストごとに条件を変えたい場合に使う

```python
from hypothesis import assume

@given(st.integers())
def test_xxx(n):
    assume(n % 2 == 0)
    ...
```

## 注意点

### filterは「生成して捨てる」方式
- PropErの`?SUCHTHAT`と同様に、条件を満たすまで生成し直す仕組み
- 条件を満たす確率が低いと、Hypothesisが`FailedHealthCheck`（`filter_too_much`）で落とす
    - 以下の例は実際にこのエラーになる

```python
# 条件を満たす確率が極端に低い
st.integers(0, 10**9).filter(lambda n: n % 100000 == 7)

# 生成してからソート済みか確認している
st.lists(st.integers(), min_size=10, unique=True).filter(lambda xs: xs == sorted(xs))
```

- 制約は、filterで後から絞るのではなく**生成側に組み込む**
    - 変換で満たす（`.map`）
    - 依存を使って範囲を決める（`@st.composite`）

```python
# ソート済みのリスト: filterの代わりにmapで変換する
st.lists(st.integers(), min_size=10).map(sorted)

# a <= b のペア: bの下限にaを使う
@st.composite
def ordered_pair(draw):
    a = draw(st.integers())
    b = draw(st.integers(min_value=a))
    return a, b
```

### shrinkingは自動で効く
- `map` / `flatmap` / `composite`のどれでも、失敗した入力は自動で縮小される
- PropErの`?LETSHRINK`のような、縮小方法の手動指定は不要

### 値の生成を実行中に決めたい場合: `st.data()`
- テスト関数の途中で`data.draw(...)`を呼べる
- 生成が前の処理結果に依存するケースで使う

```python
@given(st.data())
def test_xxx(data):
    xs = data.draw(st.lists(st.integers(), min_size=1))
    i = data.draw(st.integers(0, len(xs) - 1))
    ...
```
