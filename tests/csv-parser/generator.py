from hypothesis import given, strategies as st

@st.composite
def generate_csv(drawn:st.DrawFn):
    # RFC 4180 の TEXTDATA: エスケープ(ダブルクォート囲み)なしで許容される文字
    # %x20-21 / %x23-2B / %x2D-7E (DQUOTE=0x22, COMMA=0x2C, CR/LF, 制御文字を除く)
    textdata_char_st = st.one_of(
        st.characters(min_codepoint=0x20, max_codepoint=0x21),
        st.characters(min_codepoint=0x23, max_codepoint=0x2B),
        st.characters(min_codepoint=0x2D, max_codepoint=0x7E)
    )
    test_data_st = st.text(textdata_char_st)