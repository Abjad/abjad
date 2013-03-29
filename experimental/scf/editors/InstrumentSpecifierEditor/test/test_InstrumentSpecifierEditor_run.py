import scf


def test_InstrumentSpecifierEditor_run_01():
    '''In score.
    '''

    editor = scf.editors.InstrumentSpecifierEditor()
    editor.session.current_score_package_short_name = 'betoerung'
    editor.run(user_input='name foo instrument horn done')

    r'''
    specifiers.InstrumentSpecifier(
        instrument=instrumenttools.FrenchHorn(
            instrument_name='horn',
            instrument_name_markup=markuptools.Markup((
                'Horn',
                )),
            short_instrument_name='hn.',
            short_instrument_name_markup=markuptools.Markup((
                'Hn.',
                ))
            ),
        name='foo'
        )
    '''

    assert editor.target.format == "specifiers.InstrumentSpecifier(\n\tinstrument=instrumenttools.FrenchHorn(\n\t\tinstrument_name='horn',\n\t\tinstrument_name_markup=markuptools.Markup((\n\t\t\t'Horn',\n\t\t\t)),\n\t\tshort_instrument_name='hn.',\n\t\tshort_instrument_name_markup=markuptools.Markup((\n\t\t\t'Hn.',\n\t\t\t))\n\t\t),\n\tname='foo'\n\t)"


def test_InstrumentSpecifierEditor_run_02():
    '''In studio.
    '''

    editor = scf.editors.InstrumentSpecifierEditor()
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
