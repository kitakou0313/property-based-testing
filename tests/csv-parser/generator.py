from hypothesis import event, settings, given, strategies as st

@st.composite
def generate_csv_field(drawn:st.DrawFn):
    # RFC 4180 の TEXTDATA: エスケープ(ダブルクォート囲み)なしで許容される文字
    # %x20-21 / %x23-2B / %x2D-7E (DQUOTE=0x22, COMMA=0x2C, CR/LF, 制御文字を除く)

    # st.one_ofは 1.引数に与えたstrategyを均等な確率で選ぶ 2.選ばれたstrategyで生成される という挙動。なので「引数に与えた各strategyで生成される値が均等な確率で生成される」という挙動ではない。
    # st.sampled_fromなら候補の文字を直接列挙するため、各文字が均等な確率で選ばれる
    # 独自実装したstが実際に意図通りの分布での生成を行なっているかは検証が必要
    unquoted_chars_list = [chr(c) for c in range(0x20, 0x7F) if c not in (0x22, 0x2C)]
    need_quoted_chars_list = ["\n", "\r", '"', ","]
    unquoted_text = st.text(unquoted_chars_list)
    quotable_text = st.text(need_quoted_chars_list + unquoted_chars_list)
    field = st.one_of(unquoted_text, quotable_text)

    def header(column_num:int):
        return st.lists(field, min_size=column_num, max_size=column_num)
    def record(column_num:int):
        return st.lists(field, min_size=column_num, max_size=column_num)

    # 1行当たりのデータを生成
    # 辞書型、与えられたキーに
    def entry(keys:list[str],column_num:int) -> dict[str, str]:
        records = drawn(record(column_num))
        return dict(zip(keys, records))

    column_num = drawn(st.integers())
    header_list = drawn(header(column_num))
    return st.lists(entry(header_list, column_num))

@settings(max_examples=100)
@given(generate_csv_field())
def test_validate_generator(xs:str):
    event(xs)