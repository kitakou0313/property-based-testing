from hypothesis import given, strategies as st

def test_trg_function(bought_items_list:list[str], unit_pricies:dict[str, int]) -> int:
    return 0
# propetyを考える前に事例ベースで考える
def test_unit_test_case():
    assert test_trg_function(["A", "B", "A"], {"A":5, "B":10}) == 20
    assert test_trg_function(["A", "B", "A"], {"A":5, "B":10, "C":100}) == 20
    assert test_trg_function(["F", "B", "C"], {"F":5, "B":10, "C":100}) == 115