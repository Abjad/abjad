# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import mutate


def apply_expressive_marks(score):
    r'''Applies expressive marks to score.
    '''

    voice = score['First Violin Voice']
    markup = markuptools.Markup(
        r'\left-column { div. \line { con sord. } }', Up)
    attach(markup, voice[6][1])
    markup = markuptools.Markup('sim.', Up)
    attach(markup, voice[8][0])
    markup = markuptools.Markup('uniti', Up)
    attach(markup, voice[58][3])
    markup = markuptools.Markup('div.', Up)
    attach(markup, voice[59][0])
    markup = markuptools.Markup('uniti', Up)
    attach(markup, voice[63][3])

    voice = score['Second Violin Voice']
    markup = markuptools.Markup('div.', Up)
    attach(markup, voice[7][0])
    markup = markuptools.Markup('uniti', Up)
    attach(markup, voice[66][1])
    markup = markuptools.Markup('div.', Up)
    attach(markup, voice[67][0])
    markup = markuptools.Markup('uniti', Up)
    attach(markup, voice[74][0])

    voice = score['Viola Voice']
    markup = markuptools.Markup('sole', Up)
    attach(markup, voice[8][0])

    voice = score['Cello Voice']
    markup = markuptools.Markup('div.', Up)
    attach(markup, voice[10][0])
    markup = markuptools.Markup('uniti', Up)
    attach(markup, voice[74][0])
    markup = markuptools.Markup('uniti', Up)
    attach(markup, voice[84][1])
    markup = markuptools.Markup(r'\italic { espr. }', Down)
    attach(markup, voice[86][0])
    markup = markuptools.Markup(r'\italic { molto espr. }', Down)
    attach(markup, voice[88][1])

    voice = score['Bass Voice']
    markup = markuptools.Markup('div.', Up)
    attach(markup, voice[14][0])
    markup = markuptools.Markup(r'\italic { espr. }', Down)
    attach(markup, voice[86][0])
    mutate(voice[88][:]).split(
        [durationtools.Duration(1, 1), durationtools.Duration(1, 2)]
        )
    markup = markuptools.Markup(r'\italic { molto espr. }', Down)
    attach(markup, voice[88][1])
    markup = markuptools.Markup('uniti', Up)
    attach(markup, voice[99][1])

    strings_staff_group = score['Strings Staff Group']
    for voice in iterate(strings_staff_group).by_class(scoretools.Voice):
        markup = markuptools.Markup(r'\italic { (non dim.) }', Down)
        attach(markup, voice[102][0])