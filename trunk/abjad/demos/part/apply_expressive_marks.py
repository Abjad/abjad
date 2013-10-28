# -*- encoding: utf-8 -*-
from abjad import *


def apply_expressive_marks(score):

    voice = score['First Violin Voice']
    markup = markuptools.Markup(
        r'\left-column { div. \line { con sord. } }', Up)
    markup.attach(voice[6][1])
    markup = markuptools.Markup('sim.', Up)
    markup.attach(voice[8][0])
    markup = markuptools.Markup('uniti', Up)
    markup.attach(voice[58][3])
    markup = markuptools.Markup('div.', Up)
    markup.attach(voice[59][0])
    markup = markuptools.Markup('uniti', Up)
    markup.attach(voice[63][3])

    voice = score['Second Violin Voice']
    markup = markuptools.Markup('div.', Up)
    markup.attach(voice[7][0])
    markup = markuptools.Markup('uniti', Up)
    markup.attach(voice[66][1])
    markup = markuptools.Markup('div.', Up)
    markup.attach(voice[67][0])
    markup = markuptools.Markup('uniti', Up)
    markup.attach(voice[74][0])

    voice = score['Viola Voice']
    markup = markuptools.Markup('sole', Up)
    markup.attach(voice[8][0])

    voice = score['Cello Voice']
    markup = markuptools.Markup('div.', Up)
    markup.attach(voice[10][0])
    markup = markuptools.Markup('uniti', Up)
    markup.attach(voice[74][0])
    markup = markuptools.Markup('uniti', Up)
    markup.attach(voice[84][1])
    markup = markuptools.Markup(r'\italic { espr. }', Down)
    markup.attach(voice[86][0])
    markup = markuptools.Markup(r'\italic { molto espr. }', Down)
    markup.attach(voice[88][1])

    voice = score['Bass Voice']
    markup = markuptools.Markup('div.', Up)
    markup.attach(voice[14][0])
    markup = markuptools.Markup(r'\italic { espr. }', Down)
    markup.attach(voice[86][0])
    mutate(voice[88][:]).split([Duration(1, 1), Duration(1, 2)])
    markup = markuptools.Markup(r'\italic { molto espr. }', Down)
    markup.attach(voice[88][1])
    markup = markuptools.Markup('uniti', Up)
    markup.attach(voice[99][1])

    strings_staff_group = score['Strings Staff Group']
    for voice in iterationtools.iterate_voices_in_expr(strings_staff_group):
        markup = markuptools.Markup(r'\italic { (non dim.) }', Down)
        markup.attach(voice[102][0])
