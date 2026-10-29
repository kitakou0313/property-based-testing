from hypothesis import given, strategies as st, event
from hypothesis.strategies import DrawFn
import random

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
### 以下は特価がない時のテスト
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

### 以下は特価がある時のテスト
#### 方針
##### 特価が適用されない買い方をしているリスト + 特価のみが適用される買い方のみをしているリスト の二つを生成し、購入品のリストと合計をマージする
@st.composite
def generator_item_list_with_special_price(draw:DrawFn):
    item_and_price_dict = draw(st.dictionaries(
        keys=st.text(), values=st.integers(), min_size=1
    ))
    items_list_with_special_price = draw(st.sets(st.sampled_from([key for key in item_and_price_dict.keys()]), min_size=1))
    items_with_special_price_and_count_dict:dict[str, tuple[int, int]] = {
        key:draw(
            st.tuples(st.integers(), st.integers())
        ) for key in items_list_with_special_price
    }

    # 特価が適用される買い方のみするケース
    ## 特価が適用される買い方の整数倍（0~）を全物品分買う
    price_from_only_special_price = 0
    bought_item_list_from_only_special_price:list[str] = []
    for item_with_special_price in items_with_special_price_and_count_dict:
        bought_count_of_items = draw(st.integers(min_value=0)) * items_with_special_price_and_count_dict[item_with_special_price][1]
        price_from_only_special_price += items_with_special_price_and_count_dict[item_with_special_price][0] * bought_count_of_items
        bought_item_list_from_only_special_price += [item_with_special_price] * bought_count_of_items

    # 特価が適用されない買い方のみするケース
    price_from_only_without_special_price = 0
    bought_item_list_from_only_without_special_price:list[str] = []
    for item in item_and_price_dict.keys():
        bought_count_of_items = draw(st.integers(min_value=0, max_value=items_with_special_price_and_count_dict[item][1] - 1))
        price_from_only_without_special_price += items_with_special_price_and_count_dict[item][0] * bought_count_of_items
        bought_item_list_from_only_without_special_price += [item] * bought_count_of_items

    # 二つのケースの購入リスト、金額をマージして返す
    return random.shuffle(bought_item_list_from_only_special_price + bought_item_list_from_only_without_special_price), item_and_price_dict, items_with_special_price_and_count_dict, price_from_only_special_price + price_from_only_without_special_price