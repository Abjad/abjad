import abjad


def test_lilypondparsertools_LilyPondParser__indicators__Markup_01():

    target = abjad.Staff([abjad.Note(0, 1)])
    markup = abjad.Markup('hello!', abjad.Up)
    abjad.attach(markup, target[0])

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff {
            c'1 ^ \markup { hello! }
        }
        '''
        )

    string = r'''\new Staff { c'1 ^ "hello!" }'''

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target, 'lilypond') == format(result, 'lilypond') and \
        target is not result
    assert 1 == len(abjad.inspect(result[0]).get_markup())


def test_lilypondparsertools_LilyPondParser__indicators__Markup_02():

    target = abjad.Staff([abjad.Note(0, (1, 4))])
    markup = abjad.Markup(['X', 'Y', 'Z', 'a b c'], abjad.Down)
    abjad.attach(markup, target[0])

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff {
            c'4
                _ \markup {
                    X
                    Y
                    Z
                    "a b c"
                    }
        }
        '''
        )

    string = r'''\new Staff { c' _ \markup { X Y Z "a b c" } }'''

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target, 'lilypond') == format(result, 'lilypond') and \
        target is not result
    assert 1 == len(abjad.inspect(result[0]).get_markup())


def test_lilypondparsertools_LilyPondParser__indicators__Markup_03():
    r'''Articulations following markup block are (re)lexed correctly after
    returning to the "notes" lexical state after popping the "markup lexical state.
    '''

    target = abjad.Staff([abjad.Note(0, (1, 4)), abjad.Note(2, (1, 4))])
    markup = abjad.Markup('hello', abjad.Up)
    abjad.attach(markup, target[0])
    articulation = abjad.Articulation('.')
    abjad.attach(articulation, target[0])

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff {
            c'4 -\staccato ^ \markup { hello }
            d'4
        }
        '''
        )

    string = r'''\new Staff { c' ^ \markup { hello } -. d' }'''

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target, 'lilypond') == format(result, 'lilypond') and \
        target is not result
    assert 1 == len(abjad.inspect(result[0]).get_markup())


def test_lilypondparsertools_LilyPondParser__indicators__Markup_04():

    command1 = abjad.MarkupCommand('bold', ['A', 'B', 'C'])
    command2 = abjad.MarkupCommand('italic', '123')
    markup = abjad.Markup((command1, command2))

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(markup, 'lilypond'))

    assert isinstance(result, abjad.Markup)
    assert format(result, 'lilypond') == format(markup, 'lilypond')


def test_lilypondparsertools_LilyPondParser__indicators__Markup_05():

    command = r'\markup { \char ##x03EE }'
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(command)
    assert format(result, 'lilypond') == abjad.String.normalize(
        r'''
        \markup {
            \char
                #1006
            }
        ''',
        )
