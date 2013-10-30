# -*- encoding: utf-8 -*-
import collections
from abjad.tools import contexttools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.scoretools import attach


class StringOrchestraScoreTemplate(AbjadObject):
    '''String orchestra score template.

    ::

        >>> template = scoretemplatetools.StringOrchestraScoreTemplate(
        ...     violin_count=6,
        ...     viola_count=4,
        ...     cello_count=3,
        ...     contrabass_count=2,
        ...     )
        >>> score = template()

    ::

        >>> score
        Score-"String Orchestra Score"<<4>>

    ..  doctest::
                
        >>> f(score)        
        \context Score = "String Orchestra Score" <<
            \context StaffGroup = "Violin Staff Group" <<
                \context Staff = "Violin 1 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin 1 }
                    \set Staff.shortInstrumentName = \markup { Vln. 1 }
                    \context Voice = "Violin 1 Voice" {
                    }
                }
                \context Staff = "Violin 2 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin 2 }
                    \set Staff.shortInstrumentName = \markup { Vln. 2 }
                    \context Voice = "Violin 2 Voice" {
                    }
                }
                \context Staff = "Violin 3 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin 3 }
                    \set Staff.shortInstrumentName = \markup { Vln. 3 }
                    \context Voice = "Violin 3 Voice" {
                    }
                }
                \context Staff = "Violin 4 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin 4 }
                    \set Staff.shortInstrumentName = \markup { Vln. 4 }
                    \context Voice = "Violin 4 Voice" {
                    }
                }
                \context Staff = "Violin 5 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin 5 }
                    \set Staff.shortInstrumentName = \markup { Vln. 5 }
                    \context Voice = "Violin 5 Voice" {
                    }
                }
                \context Staff = "Violin 6 Voice" {
                    \clef "treble"
                    \set Staff.instrumentName = \markup { Violin 6 }
                    \set Staff.shortInstrumentName = \markup { Vln. 6 }
                    \context Voice = "Violin 6 Voice" {
                    }
                }
            >>
            \context StaffGroup = "Viola Staff Group" <<
                \context Staff = "Viola 1 Voice" {
                    \clef "alto"
                    \set Staff.instrumentName = \markup { Viola 1 }
                    \set Staff.shortInstrumentName = \markup { Vla. 1 }
                    \context Voice = "Viola 1 Voice" {
                    }
                }
                \context Staff = "Viola 2 Voice" {
                    \clef "alto"
                    \set Staff.instrumentName = \markup { Viola 2 }
                    \set Staff.shortInstrumentName = \markup { Vla. 2 }
                    \context Voice = "Viola 2 Voice" {
                    }
                }
                \context Staff = "Viola 3 Voice" {
                    \clef "alto"
                    \set Staff.instrumentName = \markup { Viola 3 }
                    \set Staff.shortInstrumentName = \markup { Vla. 3 }
                    \context Voice = "Viola 3 Voice" {
                    }
                }
                \context Staff = "Viola 4 Voice" {
                    \clef "alto"
                    \set Staff.instrumentName = \markup { Viola 4 }
                    \set Staff.shortInstrumentName = \markup { Vla. 4 }
                    \context Voice = "Viola 4 Voice" {
                    }
                }
            >>
            \context StaffGroup = "Cello Staff Group" <<
                \context Staff = "Cello 1 Voice" {
                    \clef "bass"
                    \set Staff.instrumentName = \markup { Cello 1 }
                    \set Staff.shortInstrumentName = \markup { Vc. 1 }
                    \context Voice = "Cello 1 Voice" {
                    }
                }
                \context Staff = "Cello 2 Voice" {
                    \clef "bass"
                    \set Staff.instrumentName = \markup { Cello 2 }
                    \set Staff.shortInstrumentName = \markup { Vc. 2 }
                    \context Voice = "Cello 2 Voice" {
                    }
                }
                \context Staff = "Cello 3 Voice" {
                    \clef "bass"
                    \set Staff.instrumentName = \markup { Cello 3 }
                    \set Staff.shortInstrumentName = \markup { Vc. 3 }
                    \context Voice = "Cello 3 Voice" {
                    }
                }
            >>
            \context StaffGroup = "Contrabass Staff Group" <<
                \context Staff = "Contrabass 1 Voice" {
                    \clef "bass_8"
                    \set Staff.instrumentName = \markup { Contrabass 1 }
                    \set Staff.shortInstrumentName = \markup { Cb. 1 }
                    \context Voice = "Contrabass 1 Voice" {
                    }
                }
                \context Staff = "Contrabass 2 Voice" {
                    \clef "bass_8"
                    \set Staff.instrumentName = \markup { Contrabass 2 }
                    \set Staff.shortInstrumentName = \markup { Cb. 2 }
                    \context Voice = "Contrabass 2 Voice" {
                    }
                }
            >>
        >>

    Returns score template.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        violin_count=6,
        viola_count=4,
        cello_count=3,
        contrabass_count=2,
        ):
        assert 0 <= violin_count
        assert 0 <= viola_count
        assert 0 <= cello_count
        assert 0 <= contrabass_count
        self._violin_count = int(violin_count)
        self._viola_count = int(viola_count)
        self._cello_count = int(cello_count)
        self._contrabass_count = int(contrabass_count)

    ### SPECIAL METHODS ###

    def __call__(self):

        string_orchestra_score = scoretools.Score(
            name='String Orchestra Score',
            )

        if self.violin_count:
            violin_staff_group = scoretools.StaffGroup(
                name='Violin Staff Group',
                )
            for i in range(1, self.violin_count + 1):
                violin_voice = scoretools.Voice(
                    name='Violin {} Voice'.format(i),
                    )
                violin_staff = scoretools.Staff(
                    [violin_voice], name='Violin {} Voice'.format(i))
                clef = contexttools.ClefMark('treble')
                attach(clef, violin_staff)
                violin = instrumenttools.Violin(
                    instrument_name_markup='Violin {}'.format(i),
                    short_instrument_name_markup='Vln. {}'.format(i),
                    )
                attach(violin, violin_staff)
                violin_staff_group.append(violin_staff)
            string_orchestra_score.append(violin_staff_group)

        if self.viola_count:
            viola_staff_group = scoretools.StaffGroup(
                name='Viola Staff Group',
                )
            for i in range(1, self.viola_count + 1):
                viola_voice = scoretools.Voice(
                    name='Viola {} Voice'.format(i),
                    )
                viola_staff = scoretools.Staff(
                    [viola_voice], name='Viola {} Voice'.format(i))
                clef = contexttools.ClefMark('alto')
                attach(clef, viola_staff)
                viola = instrumenttools.Viola(
                    instrument_name_markup='Viola {}'.format(i),
                    short_instrument_name_markup='Vla. {}'.format(i),
                    )
                attach(viola, viola_staff)
                viola_staff_group.append(viola_staff)
            string_orchestra_score.append(viola_staff_group)

        if self.cello_count:
            cello_staff_group = scoretools.StaffGroup(
                name='Cello Staff Group',
                )
            for i in range(1, self.cello_count + 1):
                cello_voice = scoretools.Voice(
                    name='Cello {} Voice'.format(i),
                    )
                cello_staff = scoretools.Staff(
                    [cello_voice], name='Cello {} Voice'.format(i))
                clef = contexttools.ClefMark('bass')
                attach(clef, cello_staff)
                cello = instrumenttools.Cello(
                    instrument_name_markup='Cello {}'.format(i),
                    short_instrument_name_markup='Vc. {}'.format(i),
                    )
                attach(cello, cello_staff)
                cello_staff_group.append(cello_staff)
            string_orchestra_score.append(cello_staff_group)

        if self.contrabass_count:
            contrabass_staff_group = scoretools.StaffGroup(
                name='Contrabass Staff Group',
                )
            for i in range(1, self.contrabass_count + 1):
                contrabass_voice = scoretools.Voice(
                    name='Contrabass {} Voice'.format(i),
                    )
                contrabass_staff = scoretools.Staff(
                    [contrabass_voice], name='Contrabass {} Voice'.format(i))
                clef = contexttools.ClefMark('bass_8')
                attach(clef, contrabass_staff)
                contrabass = instrumenttools.Contrabass(
                    instrument_name_markup='Contrabass {}'.format(i),
                    short_instrument_name_markup='Cb. {}'.format(i),
                    )
                attach(contrabass, contrabass_staff)
                contrabass_staff_group.append(contrabass_staff)
            string_orchestra_score.append(contrabass_staff_group)

        # return string quartet score
        return string_orchestra_score

    ### PUBLIC PROPERTIES ###

    @property
    def contrabass_count(self):
        return self._contrabass_count

    @property
    def cello_count(self):
        return self._cello_count

    @property
    def viola_count(self):
        return self._viola_count

    @property
    def violin_count(self):
        return self._violin_count
