from hypothesis import given, strategies as st
from hypothesis.strategies import DrawFn

def trg_function(bought_items_list:list[str], unit_pricies:dict[str, int], special_pricies:dict[str, int]) -> int:
    return 0
# propetyを考える前に事例ベースで考える

## 特価が発生しないケースの事例ベースケース
def test_unit_test_case():
    assert trg_function(["A", "B", "A"], {"A":5, "B":10}, {}) == 20
    assert trg_function(["A", "B", "A"], {"A":5, "B":10, "C":100}, {}) == 20
    assert trg_function(["F", "B", "C"], {"F":5, "B":10, "C":100}, {}) == 115

## 上記をPropertyにする
@st.composite
def generate(draw:DrawFn):
    item_types_list = draw(st.lists(st.text()))
    unit_prices = st.dictionaries(keys=st.text(), values=st.integers()) # ほぼ存在しないitemのpriceになる 要修正
    return item_types_list, unit_prices, {}


@given(generate())
def test_trg_function_with_pbt(bought_items_list:list[str], unit_pricies:dict[str, int], special_pricies:dict[str, int]):
    item_type_and_counts = {}
    for item in bought_items_list:
        if item not in item_type_and_counts:
            item_type_and_counts[item] = 0
        item_type_and_counts[item] += 1

    summary_price = 0
    for item_type in item_type_and_counts:
        summary_price += item_type_and_counts[item_type] * unit_pricies[item_type]

    assert summary_price == trg_function(bought_items_list=bought_items_list, unit_pricies=unit_pricies, special_pricies=special_pricies)