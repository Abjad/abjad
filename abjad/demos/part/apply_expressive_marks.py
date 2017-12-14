import abjad


def apply_expressive_marks(score):
    r'''Applies expressive marks to score.
    '''

    voice = score['First Violin Voice']
    markup = abjad.Markup(
        r'\left-column { div. \line { con sord. } }', abjad.Up)
    abjad.attach(markup, voice[6][1])
    markup = abjad.Markup('sim.', abjad.Up)
    abjad.attach(markup, voice[8][0])
    markup = abjad.Markup('uniti', abjad.Up)
    abjad.attach(markup, voice[58][3])
    markup = abjad.Markup('div.', abjad.Up)
    abjad.attach(markup, voice[59][0])
    markup = abjad.Markup('uniti', abjad.Up)
    abjad.attach(markup, voice[63][3])

    voice = score['Second Violin Voice']
    markup = abjad.Markup('div.', abjad.Up)
    abjad.attach(markup, voice[7][0])
    markup = abjad.Markup('uniti', abjad.Up)
    abjad.attach(markup, voice[66][1])
    markup = abjad.Markup('div.', abjad.Up)
    abjad.attach(markup, voice[67][0])
    markup = abjad.Markup('uniti', abjad.Up)
    abjad.attach(markup, voice[74][0])

    voice = score['Viola Voice']
    markup = abjad.Markup('sole', abjad.Up)
    abjad.attach(markup, voice[8][0])

    voice = score['Cello Voice']
    markup = abjad.Markup('div.', abjad.Up)
    abjad.attach(markup, voice[10][0])
    markup = abjad.Markup('uniti', abjad.Up)
    abjad.attach(markup, voice[74][0])
    markup = abjad.Markup('uniti', abjad.Up)
    abjad.attach(markup, voice[84][1])
    markup = abjad.Markup(r'\italic { espr. }', abjad.Down)
    abjad.attach(markup, voice[86][0])
    markup = abjad.Markup(r'\italic { molto espr. }', abjad.Down)
    abjad.attach(markup, voice[88][1])

    voice = score['Bass Voice']
    markup = abjad.Markup('div.', abjad.Up)
    abjad.attach(markup, voice[14][0])
    markup = abjad.Markup(r'\italic { espr. }', abjad.Down)
    abjad.attach(markup, voice[86][0])
    abjad.mutate(voice[88][:]).split(
        [abjad.Duration(1, 1), abjad.Duration(1, 2)]
        )
    markup = abjad.Markup(r'\italic { molto espr. }', abjad.Down)
    abjad.attach(markup, voice[88][1])
    markup = abjad.Markup('uniti', abjad.Up)
    abjad.attach(markup, voice[99][1])

    strings_staff_group = score['Strings Staff Group']
    for voice in abjad.iterate(strings_staff_group).components(abjad.Voice):
        markup = abjad.Markup(r'\italic { (non dim.) }', abjad.Down)
        abjad.attach(markup, voice[102][0])
