from collections import Counter

from hypothesis import given, strategies as st

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

@given(st.lists(st.integers()))
def test_invalid_maximum(xs):
    maximum_item_in_xs = max(xs)

    assert maximum_item_in_xs == invalid_search_maximum_item(xs)

@given(st.lists(st.integers()))
def test_valid_maximum(xs):
    maximum_item_in_xs = max(xs)

    assert maximum_item_in_xs == search_maximum_item(xs)