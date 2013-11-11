# -*- encoding: utf-8 -*-
import collections
from abjad.tools import marktools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools import attach


class TwoStaffPianoScoreTemplate(AbjadObject):
    '''Two-staff piano score template.

    ::

        >>> template = scoretemplatetools.TwoStaffPianoScoreTemplate()
        >>> score = template()

    ::

        >>> score
        Score-"Two-Staff Piano Score"<<1>>

    ..  doctest::

        >>> print format(score)
        \context Score = "Two-Staff Piano Score" <<
            \context PianoStaff = "Piano Staff" <<
                \set PianoStaff.instrumentName = \markup { Piano }
                \set PianoStaff.shortInstrumentName = \markup { Pf. }
                \context Staff = "RH Staff" {
                    \clef "treble"
                    \context Voice = "RH Voice" {
                    }
                }
                \context Staff = "LH Staff" {
                    \clef "bass"
                    \context Voice = "LH Voice" {
                    }
                }
            >>
        >>

    Returns score template.
    '''

    ### CLASS VARIABLES ###

    context_name_abbreviations = collections.OrderedDict({
        'rh': 'RH Voice',
        'lh': 'LH Voice',
        })

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self):

        # make RH voice and staff
        rh_voice = scoretools.Voice(name='RH Voice')
        rh_staff = scoretools.Staff(
            [rh_voice], 
            name='RH Staff',
            )
        clef = marktools.Clef('treble')
        attach(clef, rh_staff)

        # make LH voice and staff
        lh_voice = scoretools.Voice(name='LH Voice')
        lh_staff = scoretools.Staff(
            [lh_voice], 
            name='LH Staff',
            )
        clef = marktools.Clef('bass')
        attach(clef, lh_staff)

        # make piano staff
        piano_staff = scoretools.PianoStaff(
            [rh_staff, lh_staff], 
            name='Piano Staff',
            )
        piano = instrumenttools.Piano()
        attach(piano, piano_staff)

        # make two-staf piano score
        two_staff_piano_score = scoretools.Score(
            [piano_staff], 
            name='Two-Staff Piano Score',
            )

        # return two-staff piano score
        return two_staff_piano_score
