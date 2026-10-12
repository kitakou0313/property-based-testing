from collections import Counter

from hypothesis import event, given, strategies as st

from sample import my_sort, reverse, search_maximum_item, invalid_search_maximum_item

"""
st -> テスト処理を行う関数への入力となる値を生成するgenerator
@given -> テスト処理を行う関数への入力
xs -> generatorが生成した値が入る引数
@given(st.lists(st.integers()))
def test_reverse_twice_is_identity(xs):
    assert reverse(reverse(xs)) == xs


@given(st.lists(st.integers()))
def test_sort_is_ordered(xs):
    result = my_sort(xs)
    assert all(a <= b for a, b in zip(result, result[1:]))


@given(st.lists(st.integers()))
def test_sort_is_permutation(xs):
    assert Counter(my_sort(xs)) == Counter(xs)


@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    assert my_sort(my_sort(xs)) == my_sort(xs)
"""

# @given(st.lists(st.integers()))
# def test_invalid_maximum(xs):
#     maximum_item_in_xs = max(xs)

#     assert maximum_item_in_xs == invalid_search_maximum_item(xs)

# @given(st.lists(st.integers()))
# def test_valid_maximum(xs):
#     maximum_item_in_xs = max(xs)

#     assert maximum_item_in_xs == search_maximum_item(xs)

# test_valid_maximum に統計情報(event)を追加したもの
# pytest --hypothesis-show-statistics で分布を確認できる
# 空リストでは max() が ValueError になるため min_size=1 を指定する
@given(st.lists(st.integers(), min_size=1))
def test_search_maximum_item_with_statistics(xs):
    max_item_in_list = max(xs)

    if len(xs) == 1:
        event("length: 1")
    elif len(xs) <= 10:
        event("length: 20 ~ 10")
    else:
        event("length: 11 ~ ")

    assert search_maximum_item(xs=xs) == max_item_in_list