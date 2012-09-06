import collections
from abjad.tools import contexttools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools import stafftools
from abjad.tools import voicetools
from abjad.tools.scoretemplatetools.ScoreTemplate import ScoreTemplate


class TwoStaffPianoScoreTemplate(ScoreTemplate):
    '''.. versionadded:: 2.8

    Two-staff piano score template::

        >>> template = scoretemplatetools.TwoStaffPianoScoreTemplate()
        >>> score = template()

    ::

        >>> score
        Score-"Two-Staff Piano Score"<<1>>

    ::

        >>> f(score)
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

    Return score template.
    '''

    ### CLASS ATTRIBUTES ###

    context_name_abbreviations = collections.OrderedDict({
        'rh': 'RH Voice',
        'lh': 'LH Voice'
        })

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self):

        # make RH voice and staff
        rh_voice = voicetools.Voice(name='RH Voice')
        rh_staff = stafftools.Staff([rh_voice], name='RH Staff')
        contexttools.ClefMark('treble')(rh_staff)

        # make LH voice and staff
        lh_voice = voicetools.Voice(name='LH Voice')
        lh_staff = stafftools.Staff([lh_voice], name='LH Staff')
        contexttools.ClefMark('bass')(lh_staff)

        # make piano staff
        piano_staff = scoretools.PianoStaff([rh_staff, lh_staff], name='Piano Staff')
        instrumenttools.Piano()(piano_staff)

        # make two-staf piano score
        two_staff_piano_score = scoretools.Score([piano_staff], name='Two-Staff Piano Score')

        # return two-staff piano score
        return two_staff_piano_score
