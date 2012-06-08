from abjad.tools.schemetools import format_scheme_value


def test_schemetools_format_scheme_value_01():

    assert format_scheme_value(1) == '1'
    assert format_scheme_value(True) == '#t'
    assert format_scheme_value(False) == '#f'
    assert format_scheme_value('foo bar') == '"foo bar"'
    assert format_scheme_value('baz') == 'baz'
    assert format_scheme_value([1, 2, 3]) == '(1 2 3)'
