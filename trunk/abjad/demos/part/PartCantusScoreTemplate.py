# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools import stafftools
from abjad.tools import voicetools
from abjad.tools import scoretemplatetools
from abjad.tools import abctools


class PartCantusScoreTemplate(abctools.AbjadObject):

    ### SPECIAL METHODS ###

    def __call__(self):

        # make bell voice and staff
        bell_voice = voicetools.Voice(name='Bell Voice')
        bell_staff = stafftools.Staff([bell_voice], name='Bell Staff')
        clef = contexttools.ClefMark('treble')
        clef.attach(bell_staff)
        bells = instrumenttools.Instrument('Campana in La', 'Camp.')
        bells.attach(bell_staff)
        tempo = contexttools.TempoMark((1, 4), (112, 120))
        tempo.attach(bell_staff)
        time_signature = contexttools.TimeSignatureMark((6, 4))
        time_signature.attach(bell_staff)

        # make first violin voice and staff
        first_violin_voice = voicetools.Voice(name='First Violin Voice')
        first_violin_staff = stafftools.Staff(
            [first_violin_voice],
            name='First Violin Staff',
            )
        clef = contexttools.ClefMark('treble')
        clef.attach(first_violin_staff)
        violin = instrumenttools.Violin(
            instrument_name_markup='Violin I',
            short_instrument_name_markup='Vl. I'
            )
        violin.attach(first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = voicetools.Voice(name='Second Violin Voice')
        second_violin_staff = stafftools.Staff(
            [second_violin_voice],
            name='Second Violin Staff',
            )
        clef = contexttools.ClefMark('treble')
        clef.attach(second_violin_staff)
        violin = instrumenttools.Violin(
            instrument_name_markup='Violin II',
            short_instrument_name_markup='Vl. II'
            )
        violin.attach(second_violin_staff)

        # make viola voice and staff
        viola_voice = voicetools.Voice(name='Viola Voice')
        viola_staff = stafftools.Staff([viola_voice], name='Viola Staff')
        clef = contexttools.ClefMark('alto')
        clef.attach(viola_staff)
        viola = instrumenttools.Viola()
        viola.attach(viola_staff)

        # make cello voice and staff
        cello_voice = voicetools.Voice(name='Cello Voice')
        cello_staff = stafftools.Staff([cello_voice], name='Cello Staff')
        clef = contexttools.ClefMark('bass')
        clef.attach(cello_staff)
        cello = instrumenttools.Cello()
        cello.attach(cello_staff)

        # make bass voice and staff
        bass_voice = voicetools.Voice(name='Bass Voice')
        bass_staff = stafftools.Staff([bass_voice], name='Bass Staff')
        clef = contexttools.ClefMark('bass')
        clef.attach(bass_staff)
        contrabass = instrumenttools.Contrabass(
            short_instrument_name_markup='Cb.'
            )
        contrabass.attach(bass_staff)

        # make strings staff group
        strings_staff_group = scoretools.StaffGroup([
            first_violin_staff,
            second_violin_staff,
            viola_staff,
            cello_staff,
            bass_staff,
            ],
            name='Strings Staff Group',
            )

        # make score
        score = scoretools.Score([
            bell_staff,
            strings_staff_group,
            ],
            name='Pärt Cantus Score'
            )

        # return Pärt Cantus score
        return score
