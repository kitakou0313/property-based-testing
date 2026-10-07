from collections import Counter

from hypothesis import given, strategies as st

from sample import key_sort

"""
問2
key_sort関数のpropetry based test
"""
# key_numberの最大値をtuples_listの要素数-1にしたい
# そもそもgeneratorにどこまで制約を入れていいのかを考える必要がある（要素数固定でいいのか、tupleの値がすべて比較可能なことは前提としていいのか）
@given(tuples_list=st.lists(st.tuples(st.)), key_number=st.integers(max_value=0))
def test_key_sort(tuples_list, key_number):
    sorted_tuples_list = key_sort(tuples_list, key_number)

    for i in range(len(sorted_tuples_list) - 1):
        assert sorted_tuples_list[i][key_number] < sorted_tuples_list[i+1]
