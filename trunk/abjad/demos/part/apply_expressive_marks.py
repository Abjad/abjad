from abjad import *


def apply_expressive_marks(score):

    voice = score['First Violin Voice']
    markuptools.Markup(r'\left-column { div. \line { con sord. } }', Up)(voice[6][1])
    markuptools.Markup('sim.', Up)(voice[8][0])
    markuptools.Markup('uniti', Up)(voice[58][3])
    markuptools.Markup('div.', Up)(voice[59][0])
    markuptools.Markup('uniti', Up)(voice[63][3])

    voice = score['Second Violin Voice']
    markuptools.Markup('div.', Up)(voice[7][0])
    markuptools.Markup('uniti', Up)(voice[66][1])
    markuptools.Markup('div.', Up)(voice[67][0])
    markuptools.Markup('uniti', Up)(voice[74][0])

    voice = score['Viola Voice']
    markuptools.Markup('sole', Up)(voice[8][0])

    voice = score['Cello Voice']
    markuptools.Markup('div.', Up)(voice[10][0])
    markuptools.Markup('uniti', Up)(voice[74][0])
    markuptools.Markup('uniti', Up)(voice[84][1])
    markuptools.Markup(r'\italic { espr. }', Down)(voice[86][0])
    markuptools.Markup(r'\italic { molto espr. }', Down)(voice[88][1])

    voice = score['Bass Voice']
    markuptools.Markup('div.', Up)(voice[14][0])
    markuptools.Markup(r'\italic { espr. }', Down)(voice[86][0])
    componenttools.split_components_at_offsets(voice[88][:], [Duration(1, 1), Duration(1, 2)])
    markuptools.Markup(r'\italic { molto espr. }', Down)(voice[88][1])
    markuptools.Markup('uniti', Up)(voice[99][1])

    for voice in iterationtools.iterate_voices_in_expr(score['Strings Staff Group']):
        markuptools.Markup(r'\italic { (non dim.) }', Down)(voice[102][0])




