# -*- coding: utf-8 -*-
import abjad


class PartCantusScoreTemplate(abjad.abctools.AbjadObject):
    r'''Pärt Cantus score template.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Calls score template.

        Returns LilyPond file.
        '''

        # make bell voice and staff
        bell_voice = abjad.Voice(name='Bell Voice')
        bell_staff = abjad.Staff([bell_voice], name='Bell Staff')
        clef = abjad.Clef('treble')
        abjad.attach(clef, bell_staff)
        bells = abjad.instrumenttools.Instrument(
            instrument_name='Campana in La',
            short_instrument_name='Camp.',
            pitch_range='[C4, C6]',
            )
        abjad.attach(bells, bell_staff)
        mark = abjad.MetronomeMark((1, 4), (112, 120))
        abjad.attach(mark, bell_staff)
        time_signature = abjad.TimeSignature((6, 4))
        abjad.attach(time_signature, bell_staff)

        # make first violin voice and staff
        first_violin_voice = abjad.Voice(name='First Violin Voice')
        first_violin_staff = abjad.Staff(
            [first_violin_voice],
            name='First Violin Staff',
            )
        clef = abjad.Clef('treble')
        abjad.attach(clef, first_violin_staff)
        violin = abjad.instrumenttools.Violin(
            instrument_name_markup=abjad.Markup('Violin I'),
            short_instrument_name_markup=abjad.Markup('Vl. I'),
            )
        abjad.attach(violin, first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = abjad.Voice(name='Second Violin Voice')
        second_violin_staff = abjad.Staff(
            [second_violin_voice],
            name='Second Violin Staff',
            )
        clef = abjad.Clef('treble')
        abjad.attach(clef, second_violin_staff)
        violin = abjad.instrumenttools.Violin(
            instrument_name_markup=abjad.Markup('Violin II'),
            short_instrument_name_markup=abjad.Markup('Vl. II'),
            )
        abjad.attach(violin, second_violin_staff)

        # make viola voice and staff
        viola_voice = abjad.Voice(name='Viola Voice')
        viola_staff = abjad.Staff([viola_voice], name='Viola Staff')
        clef = abjad.Clef('alto')
        abjad.attach(clef, viola_staff)
        viola = abjad.instrumenttools.Viola()
        abjad.attach(viola, viola_staff)

        # make cello voice and staff
        cello_voice = abjad.Voice(name='Cello Voice')
        cello_staff = abjad.Staff([cello_voice], name='Cello Staff')
        clef = abjad.Clef('bass')
        abjad.attach(clef, cello_staff)
        cello = abjad.instrumenttools.Cello()
        abjad.attach(cello, cello_staff)

        # make bass voice and staff
        bass_voice = abjad.Voice(name='Bass Voice')
        bass_staff = abjad.Staff([bass_voice], name='Bass Staff')
        clef = abjad.Clef('bass')
        abjad.attach(clef, bass_staff)
        contrabass = abjad.instrumenttools.Contrabass(
            short_instrument_name_markup=abjad.Markup('Cb.'),
            )
        abjad.attach(contrabass, bass_staff)

        # make strings staff group
        strings_staff_group = abjad.StaffGroup([
            first_violin_staff,
            second_violin_staff,
            viola_staff,
            cello_staff,
            bass_staff,
            ],
            name='Strings Staff Group',
            )

        # make score
        score = abjad.Score([
            bell_staff,
            strings_staff_group,
            ],
            name='Pärt Cantus Score'
            )

        # return Pärt Cantus score
        return score
