from operator import itemgetter

def reverse(xs: list[int]) -> list[int]:
    return xs[::-1]

def search_maximum_item(xs: list[int]) -> int:
    res = xs[0]

    for item in xs:
        res = item if item > res else res

    return res

def invalid_search_maximum_item(xs: list[int]) -> int:
    res = xs[0]
    return res

def my_sort(xs: list[int]) -> list[int]:
    return sorted(xs)

def key_sort_int_tuple(tuples:list[tuple[int]], n:int) -> list[tuple[int]]:
    if len(tuples) == 0:
        return []
    if n < 0 or len(tuples[0])-1 < n:
        raise ValueError("Index out of range")
    
    return sorted(tuples, key=itemgetter(n))
