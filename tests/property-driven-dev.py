from hypothesis import given, strategies as st, event
from hypothesis.strategies import DrawFn

def trg_function(bought_items_list:list[str], unit_pricies:dict[str, int], special_pricies:dict[str, int]) -> int:
    summary_price = 0

    for bought_item in bought_items_list:
        summary_price += unit_pricies[bought_item]

    return summary_price

# propetyを考える前に事例ベースで考える

## 特価が発生しないケースの事例ベースケース
def test_unit_test_case():
    assert trg_function(["A", "B", "A"], {"A":5, "B":10}, {}) == 20
    assert trg_function(["A", "B", "A"], {"A":5, "B":10, "C":100}, {}) == 20
    assert trg_function(["F", "B", "C"], {"F":5, "B":10, "C":100}, {}) == 115

## 上記をPropertyにする
## ポジティブテスト（エッジケースを考慮せず、正しい挙動を検討するためのテスト）
@st.composite
def generate(draw:DrawFn):
    unit_prices = draw(st.dictionaries(keys=st.text(), values=st.integers(), min_size=1))
    bought_items_list = draw(st.lists(st.sampled_from([key for key in unit_prices.keys()])))

    expected_total_price = 0
    for bought_item in bought_items_list:
        expected_total_price += unit_prices[bought_item]

    return bought_items_list, unit_prices, {}, expected_total_price 


@given(generate())
def test_trg_function_with_pbt(custom_generator:tuple[list[str], dict[str, int], dict[str, int], int]):
    bought_items_list, unit_pricies, special_pricies, expected_price = custom_generator
    event("item count", len(bought_items_list))
    event("avg unit prices", sum([price for price in unit_pricies.values()]) // len(unit_pricies))
    assert expected_price == trg_function(bought_items_list=bought_items_list, unit_pricies=unit_pricies, special_pricies=special_pricies)