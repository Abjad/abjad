from abjad import *


def test_leaftools_replace_leaves_in_expr_with_named_parallel_voices_01():
    c = p(r'{ c8 \times 2/3 { c8 c c } \times 4/5 { c16 c c c c } c8 }')
    result = leaftools.replace_leaves_in_expr_with_named_parallel_voices(c.leaves[2:7], 'upper', 'lower')
    assert c.lilypond_format == '{\n\tc8\n\t\\times 2/3 {\n\t\tc8\n\t\t<<\n\t\t\t\\context Voice = "upper" {\n\t\t\t\tc8\n\t\t\t\tc8\n\t\t\t}\n\t\t\t\\context Voice = "lower" {\n\t\t\t\tc8\n\t\t\t\tc8\n\t\t\t}\n\t\t>>\n\t}\n\t\\times 4/5 {\n\t\t<<\n\t\t\t\\context Voice = "upper" {\n\t\t\t\tc16\n\t\t\t\tc16\n\t\t\t\tc16\n\t\t\t}\n\t\t\t\\context Voice = "lower" {\n\t\t\t\tc16\n\t\t\t\tc16\n\t\t\t\tc16\n\t\t\t}\n\t\t>>\n\t\tc16\n\t\tc16\n\t}\n\tc8\n}'
