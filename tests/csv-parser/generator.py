from hypothesis import event, settings, given, strategies as st

@st.composite
def generate_csv(drawn:st.DrawFn):
    # RFC 4180 の TEXTDATA: エスケープ(ダブルクォート囲み)なしで許容される文字
    # %x20-21 / %x23-2B / %x2D-7E (DQUOTE=0x22, COMMA=0x2C, CR/LF, 制御文字を除く)

    # st.one_ofは 1.引数に与えたstrategyを均等な確率で選ぶ 2.選ばれたstrategyで生成される という挙動。なので「引数に与えた各strategyで生成される値が均等な確率で生成される」という挙動ではない。
    # st.sampled_fromなら候補の文字を直接列挙するため、各文字が均等な確率で選ばれる
    # 独自実装したstが実際に意図通りの分布での生成を行なっているかは検証が必要
    textdata_char_st = [chr(c) for c in range(0x20, 0x7F) if c not in (0x22, 0x2C)]
    
    unquoted_char = st.text(textdata_char_st, max_size=1, min_size=1)
    quotable_char = st.text(st.sampled_from(["\n", "\r", '"', ","] + textdata_char_st))

    return drawn(quotable_char)

@settings(max_examples=10000)
@given(st.lists(generate_csv()))
def test_validate_generator(char:str):
    event(char)