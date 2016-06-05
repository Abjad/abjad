# -*- coding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import indicatortools
from abjad.tools import instrumenttools
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach


class PartCantusScoreTemplate(abctools.AbjadObject):
    r'''Pärt Cantus score template.
    '''

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Calls score template.

        Returns LilyPond file.
        '''

        # make bell voice and staff
        bell_voice = scoretools.Voice(name='Bell Voice')
        bell_staff = scoretools.Staff([bell_voice], name='Bell Staff')
        clef = indicatortools.Clef('treble')
        attach(clef, bell_staff)
        bells = instrumenttools.Instrument(
            instrument_name='Campana in La',
            short_instrument_name='Camp.',
            pitch_range='[C4, C6]',
            )
        attach(bells, bell_staff)
        tempo = indicatortools.Tempo((1, 4), (112, 120))
        attach(tempo, bell_staff)
        time_signature = indicatortools.TimeSignature((6, 4))
        attach(time_signature, bell_staff)

        # make first violin voice and staff
        first_violin_voice = scoretools.Voice(name='First Violin Voice')
        first_violin_staff = scoretools.Staff(
            [first_violin_voice],
            name='First Violin Staff',
            )
        clef = indicatortools.Clef('treble')
        attach(clef, first_violin_staff)
        violin = instrumenttools.Violin(
            instrument_name_markup=markuptools.Markup('Violin I'),
            short_instrument_name_markup=markuptools.Markup('Vl. I'),
            )
        attach(violin, first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = scoretools.Voice(name='Second Violin Voice')
        second_violin_staff = scoretools.Staff(
            [second_violin_voice],
            name='Second Violin Staff',
            )
        clef = indicatortools.Clef('treble')
        attach(clef, second_violin_staff)
        violin = instrumenttools.Violin(
            instrument_name_markup=markuptools.Markup('Violin II'),
            short_instrument_name_markup=markuptools.Markup('Vl. II'),
            )
        attach(violin, second_violin_staff)

        # make viola voice and staff
        viola_voice = scoretools.Voice(name='Viola Voice')
        viola_staff = scoretools.Staff([viola_voice], name='Viola Staff')
        clef = indicatortools.Clef('alto')
        attach(clef, viola_staff)
        viola = instrumenttools.Viola()
        attach(viola, viola_staff)

        # make cello voice and staff
        cello_voice = scoretools.Voice(name='Cello Voice')
        cello_staff = scoretools.Staff([cello_voice], name='Cello Staff')
        clef = indicatortools.Clef('bass')
        attach(clef, cello_staff)
        cello = instrumenttools.Cello()
        attach(cello, cello_staff)

        # make bass voice and staff
        bass_voice = scoretools.Voice(name='Bass Voice')
        bass_staff = scoretools.Staff([bass_voice], name='Bass Staff')
        clef = indicatortools.Clef('bass')
        attach(clef, bass_staff)
        contrabass = instrumenttools.Contrabass(
            short_instrument_name_markup=markuptools.Markup('Cb.'),
            )
        attach(contrabass, bass_staff)

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