from experimental import *


def test_InstrumentSpecifierEditor_run_01():
    '''In score.
    '''

    editor = scoremanagertools.editors.InstrumentSpecifierEditor()
    editor.session.current_score_package_name = 'example_score_1'
    editor.run(user_input='name foo instrument horn done')

    r'''
    specifiers.InstrumentSpecifier(
        instrument=instrumenttools.FrenchHorn(),
        name='foo'
        )
    '''

    assert editor.target.format == "specifiers.InstrumentSpecifier(\n\tinstrument=instrumenttools.FrenchHorn(),\n\tname='foo'\n\t)"


def test_InstrumentSpecifierEditor_run_02():
    '''Home.
    '''

    editor = scoremanagertools.editors.InstrumentSpecifierEditor()
    editor.run(user_input='name foo instrument untuned ratt done')

    r'''
    specifiers.InstrumentSpecifier(
        instrument=instrumenttools.UntunedPercussion(
            instrument_name='rattle',
            short_instrument_name='rattle'
            ),
        name='foo'
        )
    '''

    assert editor.target.format == "specifiers.InstrumentSpecifier(\n\tinstrument=instrumenttools.UntunedPercussion(\n\t\tinstrument_name='rattle',\n\t\tshort_instrument_name='rattle'\n\t\t),\n\tname='foo'\n\t)"
