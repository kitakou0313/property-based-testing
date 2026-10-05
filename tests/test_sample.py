from collections import Counter

from hypothesis import given, strategies as st

from sample import my_sort, reverse


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
