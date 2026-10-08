from collections import Counter

import pytest
from hypothesis import given, strategies as st

from sample import key_sort_int_tuple

"""
問2
key_sort関数のpropetry based test
"""
# key_numberの最大値をtuples_listの要素数-1にしたい
# そもそもgeneratorにどこまで制約を入れていいのかを考える必要がある（要素数固定でいいのか、tupleの値がすべて比較可能なことは前提としていいのか）
@given(tuples_list=st.lists(st.tuples(st.integers(), st.integers())), key_number=st.integers())
def test_key_sort(tuples_list:list[tuple], key_number:int):
    if key_number < 0 or len(tuples_list) <= key_number:

        with pytest.raises(ValueError):
            key_sort_int_tuple(tuples_list, key_number)
        return

    sorted_tuples_list = key_sort_int_tuple(tuples_list, key_number)

    for i in range(len(sorted_tuples_list) - 1):
        assert sorted_tuples_list[i][key_number] <= sorted_tuples_list[i+1][key_number]
