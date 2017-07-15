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

        # make first violin voice and staff
        first_violin_voice = abjad.Voice(name='First Violin Voice')
        first_violin_staff = abjad.Staff(
            [first_violin_voice],
            name='First Violin Staff',
            )

        # make second violin voice and staff
        second_violin_voice = abjad.Voice(name='Second Violin Voice')
        second_violin_staff = abjad.Staff(
            [second_violin_voice],
            name='Second Violin Staff',
            )

        # make viola voice and staff
        viola_voice = abjad.Voice(name='Viola Voice')
        viola_staff = abjad.Staff([viola_voice], name='Viola Staff')

        # make cello voice and staff
        cello_voice = abjad.Voice(name='Cello Voice')
        cello_staff = abjad.Staff([cello_voice], name='Cello Staff')

        # make bass voice and staff
        bass_voice = abjad.Voice(name='Bass Voice')
        bass_staff = abjad.Staff([bass_voice], name='Bass Staff')

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
