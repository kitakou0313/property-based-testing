from hypothesis import event, given, strategies as st
from hypothesis.strategies import DrawFn
from sample import key_sort_int_tuple

import pytest
"""
テストケースの変換(LET相当)
st.map関数を使う
"""

"""
テストケースのfiltering(SUCHTHAT相当)
st.filter関数を使う
"""

"""
生成した値を用いて別のGeneratorを生成したい場合
st.compositeを使ってgeneratorを作る
"""
@st.composite
def generate_tuples_list_and_range_error_key(draw:DrawFn):
    xs = draw(
        st.lists(st.tuples(st.integers(), st.integers(), st.integers()))
    )
    outrange_key_number = draw(st.integers(min_value=len(xs)))

    return xs, outrange_key_number

@given(generate_tuples_list_and_range_error_key())
def test_key_sort_with_outrange_key_number(custom_generator):
    trg_tuple_list, key = custom_generator
    with pytest.raises(ValueError):
        key_sort_int_tuple(tuples=trg_tuple_list, n=key)