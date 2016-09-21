# -*- coding: utf-8 -*-
import collections
from abjad.tools import indicatortools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class StringOrchestraScoreTemplate(AbjadValueObject):
    r'''String orchestra score template.

    ::

        >>> template = templatetools.StringOrchestraScoreTemplate()
        >>> score = template()
        >>> print(format(score))
        \context Score = "Score" <<
            \tag #'(Violin1 Violin2 Violin3 Violin4 Violin5 Violin6 Viola1 Viola2 Viola3 Viola4 Cello1 Cello2 Cello3 Contrabass1 Contrabass2)
            \context TimeSignatureContext = "TimeSignatureContext" {
            }
            \context StaffGroup = "Outer Staff Group" <<
                \context ViolinStaffGroup = "Violin Staff Group" <<
                    \tag #'Violin1
                    \context StringPerformerStaffGroup = "Violin 1 Staff Group" <<
                        \context BowingStaff = "Violin 1 Bowing Staff" <<
                            \context BowingVoice = "Violin 1 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Violin 1 Fingering Staff" <<
                            \clef "treble"
                            \context FingeringVoice = "Violin 1 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Violin2
                    \context StringPerformerStaffGroup = "Violin 2 Staff Group" <<
                        \context BowingStaff = "Violin 2 Bowing Staff" <<
                            \context BowingVoice = "Violin 2 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Violin 2 Fingering Staff" <<
                            \clef "treble"
                            \context FingeringVoice = "Violin 2 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Violin3
                    \context StringPerformerStaffGroup = "Violin 3 Staff Group" <<
                        \context BowingStaff = "Violin 3 Bowing Staff" <<
                            \context BowingVoice = "Violin 3 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Violin 3 Fingering Staff" <<
                            \clef "treble"
                            \context FingeringVoice = "Violin 3 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Violin4
                    \context StringPerformerStaffGroup = "Violin 4 Staff Group" <<
                        \context BowingStaff = "Violin 4 Bowing Staff" <<
                            \context BowingVoice = "Violin 4 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Violin 4 Fingering Staff" <<
                            \clef "treble"
                            \context FingeringVoice = "Violin 4 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Violin5
                    \context StringPerformerStaffGroup = "Violin 5 Staff Group" <<
                        \context BowingStaff = "Violin 5 Bowing Staff" <<
                            \context BowingVoice = "Violin 5 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Violin 5 Fingering Staff" <<
                            \clef "treble"
                            \context FingeringVoice = "Violin 5 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Violin6
                    \context StringPerformerStaffGroup = "Violin 6 Staff Group" <<
                        \context BowingStaff = "Violin 6 Bowing Staff" <<
                            \context BowingVoice = "Violin 6 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Violin 6 Fingering Staff" <<
                            \clef "treble"
                            \context FingeringVoice = "Violin 6 Fingering Voice" {
                            }
                        >>
                    >>
                >>
                \context ViolaStaffGroup = "Viola Staff Group" <<
                    \tag #'Viola1
                    \context StringPerformerStaffGroup = "Viola 1 Staff Group" <<
                        \context BowingStaff = "Viola 1 Bowing Staff" <<
                            \context BowingVoice = "Viola 1 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Viola 1 Fingering Staff" <<
                            \clef "alto"
                            \context FingeringVoice = "Viola 1 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Viola2
                    \context StringPerformerStaffGroup = "Viola 2 Staff Group" <<
                        \context BowingStaff = "Viola 2 Bowing Staff" <<
                            \context BowingVoice = "Viola 2 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Viola 2 Fingering Staff" <<
                            \clef "alto"
                            \context FingeringVoice = "Viola 2 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Viola3
                    \context StringPerformerStaffGroup = "Viola 3 Staff Group" <<
                        \context BowingStaff = "Viola 3 Bowing Staff" <<
                            \context BowingVoice = "Viola 3 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Viola 3 Fingering Staff" <<
                            \clef "alto"
                            \context FingeringVoice = "Viola 3 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Viola4
                    \context StringPerformerStaffGroup = "Viola 4 Staff Group" <<
                        \context BowingStaff = "Viola 4 Bowing Staff" <<
                            \context BowingVoice = "Viola 4 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Viola 4 Fingering Staff" <<
                            \clef "alto"
                            \context FingeringVoice = "Viola 4 Fingering Voice" {
                            }
                        >>
                    >>
                >>
                \context CelloStaffGroup = "Cello Staff Group" <<
                    \tag #'Cello1
                    \context StringPerformerStaffGroup = "Cello 1 Staff Group" <<
                        \context BowingStaff = "Cello 1 Bowing Staff" <<
                            \context BowingVoice = "Cello 1 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Cello 1 Fingering Staff" <<
                            \clef "bass"
                            \context FingeringVoice = "Cello 1 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Cello2
                    \context StringPerformerStaffGroup = "Cello 2 Staff Group" <<
                        \context BowingStaff = "Cello 2 Bowing Staff" <<
                            \context BowingVoice = "Cello 2 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Cello 2 Fingering Staff" <<
                            \clef "bass"
                            \context FingeringVoice = "Cello 2 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Cello3
                    \context StringPerformerStaffGroup = "Cello 3 Staff Group" <<
                        \context BowingStaff = "Cello 3 Bowing Staff" <<
                            \context BowingVoice = "Cello 3 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Cello 3 Fingering Staff" <<
                            \clef "bass"
                            \context FingeringVoice = "Cello 3 Fingering Voice" {
                            }
                        >>
                    >>
                >>
                \context ContrabassStaffGroup = "Contrabass Staff Group" <<
                    \tag #'Contrabass1
                    \context StringPerformerStaffGroup = "Contrabass 1 Staff Group" <<
                        \context BowingStaff = "Contrabass 1 Bowing Staff" <<
                            \context BowingVoice = "Contrabass 1 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Contrabass 1 Fingering Staff" <<
                            \clef "bass_8"
                            \context FingeringVoice = "Contrabass 1 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Contrabass2
                    \context StringPerformerStaffGroup = "Contrabass 2 Staff Group" <<
                        \context BowingStaff = "Contrabass 2 Bowing Staff" <<
                            \context BowingVoice = "Contrabass 2 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Contrabass 2 Fingering Staff" <<
                            \clef "bass_8"
                            \context FingeringVoice = "Contrabass 2 Fingering Voice" {
                            }
                        >>
                    >>
                >>
            >>
        >>

    As a string quartet:

    ::

        >>> template = templatetools.StringOrchestraScoreTemplate(
        ...     violin_count=2,
        ...     viola_count=1,
        ...     cello_count=1,
        ...     contrabass_count=0,
        ...     )
        >>> score = template()
        >>> print(format(score))
        \context Score = "Score" <<
            \tag #'(Violin1 Violin2 Viola Cello)
            \context TimeSignatureContext = "TimeSignatureContext" {
            }
            \context StaffGroup = "Outer Staff Group" <<
                \context ViolinStaffGroup = "Violin Staff Group" <<
                    \tag #'Violin1
                    \context StringPerformerStaffGroup = "Violin 1 Staff Group" <<
                        \context BowingStaff = "Violin 1 Bowing Staff" <<
                            \context BowingVoice = "Violin 1 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Violin 1 Fingering Staff" <<
                            \clef "treble"
                            \context FingeringVoice = "Violin 1 Fingering Voice" {
                            }
                        >>
                    >>
                    \tag #'Violin2
                    \context StringPerformerStaffGroup = "Violin 2 Staff Group" <<
                        \context BowingStaff = "Violin 2 Bowing Staff" <<
                            \context BowingVoice = "Violin 2 Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Violin 2 Fingering Staff" <<
                            \clef "treble"
                            \context FingeringVoice = "Violin 2 Fingering Voice" {
                            }
                        >>
                    >>
                >>
                \context ViolaStaffGroup = "Viola Staff Group" <<
                    \tag #'Viola
                    \context StringPerformerStaffGroup = "Viola Staff Group" <<
                        \context BowingStaff = "Viola Bowing Staff" <<
                            \context BowingVoice = "Viola Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Viola Fingering Staff" <<
                            \clef "alto"
                            \context FingeringVoice = "Viola Fingering Voice" {
                            }
                        >>
                    >>
                >>
                \context CelloStaffGroup = "Cello Staff Group" <<
                    \tag #'Cello
                    \context StringPerformerStaffGroup = "Cello Staff Group" <<
                        \context BowingStaff = "Cello Bowing Staff" <<
                            \context BowingVoice = "Cello Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Cello Fingering Staff" <<
                            \clef "bass"
                            \context FingeringVoice = "Cello Fingering Voice" {
                            }
                        >>
                    >>
                >>
            >>
        >>

    As a cello solo:

    ::

        >>> template = templatetools.StringOrchestraScoreTemplate(
        ...     violin_count=0,
        ...     viola_count=0,
        ...     cello_count=1,
        ...     contrabass_count=0,
        ...     )
        >>> score = template()
        >>> print(format(score))
        \context Score = "Score" <<
            \tag #'(Cello)
            \context TimeSignatureContext = "TimeSignatureContext" {
            }
            \context StaffGroup = "Outer Staff Group" <<
                \context CelloStaffGroup = "Cello Staff Group" <<
                    \tag #'Cello
                    \context StringPerformerStaffGroup = "Cello Staff Group" <<
                        \context BowingStaff = "Cello Bowing Staff" <<
                            \context BowingVoice = "Cello Bowing Voice" {
                            }
                        >>
                        \context FingeringStaff = "Cello Fingering Staff" <<
                            \clef "bass"
                            \context FingeringVoice = "Cello Fingering Voice" {
                            }
                        >>
                    >>
                >>
            >>
        >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cello_count',
        '_contrabass_count',
        '_split_hands',
        '_use_percussion_clefs',
        '_viola_count',
        '_violin_count',
        '_context_name_abbreviations',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        violin_count=6,
        viola_count=4,
        cello_count=3,
        contrabass_count=2,
        split_hands=True,
        use_percussion_clefs=False,
        ):
        assert 0 <= violin_count
        assert 0 <= viola_count
        assert 0 <= cello_count
        assert 0 <= contrabass_count
        self._violin_count = int(violin_count)
        self._viola_count = int(viola_count)
        self._cello_count = int(cello_count)
        self._contrabass_count = int(contrabass_count)
        self._split_hands = bool(split_hands)
        self._use_percussion_clefs = bool(use_percussion_clefs)
        self._context_name_abbreviations = collections.OrderedDict()

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls string orchestra template.

        Returns score.
        '''

        ### TAGS ###

        tag_names = []

        ### SCORE ###

        staff_group = scoretools.StaffGroup(
            name='Outer Staff Group',
            )

        score = scoretools.Score(
            [staff_group],
            name='Score',
            )

        ### VIOLINS ###

        if self.violin_count:
            clef_name = 'treble'
            if self.use_percussion_clefs:
                clef_name = 'percussion'
            instrument = instrumenttools.Violin()
            instrument_count = self.violin_count
            instrument_staff_group, instrument_tag_names = \
                self._make_instrument_staff_group(
                    clef_name=clef_name,
                    count=instrument_count,
                    instrument=instrument,
                    )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### VIOLAS ###

        if self.viola_count:
            clef_name = 'alto'
            if self.use_percussion_clefs:
                clef_name = 'percussion'
            instrument = instrumenttools.Viola()
            instrument_count = self.viola_count
            instrument_staff_group, instrument_tag_names = \
                self._make_instrument_staff_group(
                    clef_name=clef_name,
                    count=instrument_count,
                    instrument=instrument,
                    )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### CELLOS ###

        if self.cello_count:
            clef_name = 'bass'
            if self.use_percussion_clefs:
                clef_name = 'percussion'
            instrument = instrumenttools.Cello()
            instrument_count = self.cello_count
            instrument_staff_group, instrument_tag_names = \
                self._make_instrument_staff_group(
                    clef_name=clef_name,
                    count=instrument_count,
                    instrument=instrument,
                    )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### BASSES ###

        if self.contrabass_count:
            clef_name = 'bass_8'
            if self.use_percussion_clefs:
                clef_name = 'percussion'
            instrument = instrumenttools.Contrabass()
            instrument_count = self.contrabass_count
            instrument_staff_group, instrument_tag_names = \
                self._make_instrument_staff_group(
                    clef_name=clef_name,
                    count=instrument_count,
                    instrument=instrument,
                    )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### TIME SIGNATURE CONTEXT ###

        time_signature_context = scoretools.Context(
            name='TimeSignatureContext',
            context_name='TimeSignatureContext',
            )
        instrument_tags = ' '.join(tag_names)
        tag_string = "tag #'({})".format(instrument_tags)
        tag_command = indicatortools.LilyPondCommand(tag_string, 'before')
        attach(tag_command, time_signature_context)

        score.insert(0, time_signature_context)

        return score

    ### PRIVATE METHODS ###

    def _make_instrument_staff_group(
        self,
        clef_name=None,
        count=None,
        instrument=None,
        ):
        instrument_name = instrument.instrument_name.title()
        instrument_staff_group = scoretools.StaffGroup(
            context_name='{}StaffGroup'.format(instrument_name),
            name='{} Staff Group'.format(instrument_name),
            )
        tag_names = []
        if count == 1:
            performer_staff_group, tag_name = \
                self._make_performer_staff_group(
                    clef_name=clef_name,
                    instrument=instrument,
                    number=None,
                    )
            instrument_staff_group.append(performer_staff_group)
            tag_names.append(tag_name)
        else:
            for i in range(1, count + 1):
                performer_staff_group, tag_name = \
                    self._make_performer_staff_group(
                        clef_name=clef_name,
                        instrument=instrument,
                        number=i,
                        )
                instrument_staff_group.append(performer_staff_group)
                tag_names.append(tag_name)
        return instrument_staff_group, tag_names

    def _make_performer_staff_group(
        self,
        clef_name=None,
        instrument=None,
        number=None,
        ):
        if number is not None:
            name = '{} {}'.format(
                instrument.instrument_name.title(),
                number,
                )
        else:
            name = instrument.instrument_name.title()
        pitch_range = instrument.pitch_range
        staff_group = scoretools.StaffGroup(
            context_name='StringPerformerStaffGroup',
            name='{} Staff Group'.format(name),
            )
        tag_name = name.replace(' ', '')
        tag_string = "tag #'{}".format(tag_name)
        tag_command = indicatortools.LilyPondCommand(
            tag_string,
            'before',
            )
        attach(tag_command, staff_group)
        if self.split_hands:
            lh_voice = scoretools.Voice(
                context_name='FingeringVoice',
                name='{} Fingering Voice'.format(name),
                )
            abbreviation = lh_voice.name.lower().replace(' ', '_')
            self.context_name_abbreviations[abbreviation] = lh_voice.name
            lh_staff = scoretools.Staff(
                [
                    lh_voice
                    ],
                context_name='FingeringStaff',
                name='{} Fingering Staff'.format(name),
                )
            lh_staff.is_simultaneous = True
            attach(pitch_range, lh_staff)
            attach(indicatortools.Clef(clef_name), lh_staff)
            rh_voice = scoretools.Voice(
                context_name='BowingVoice',
                name='{} Bowing Voice'.format(name),
                )
            abbreviation = rh_voice.name.lower().replace(' ', '_')
            self.context_name_abbreviations[abbreviation] = rh_voice.name
            rh_staff = scoretools.Staff(
                [
                    rh_voice
                    ],
                context_name='BowingStaff',
                name='{} Bowing Staff'.format(name),
                )
            rh_staff.is_simultaneous = True
            staff_group.extend([rh_staff, lh_staff])
        else:
            lh_voice = scoretools.Voice(
                context_name='FingeringVoice',
                name='{} Voice'.format(name),
                )
            lh_staff = scoretools.Staff(
                [
                    lh_voice
                    ],
                context_name='FingeringStaff',
                name='{} Staff'.format(name),
                )
            lh_staff.is_simultaneous = True
            attach(pitch_range, lh_staff)
            attach(indicatortools.Clef(clef_name), lh_staff)
            staff_group.append(lh_staff)
        return staff_group, tag_name

    ### PUBLIC PROPERTIES ###

    @property
    def cello_count(self):
        r'''Number of cellos in string orchestra.

        Returns nonnegative integer.
        '''
        return self._cello_count

    @property
    def context_name_abbreviations(self):
        r'''Voice name abbreviations.
        '''
        return self._context_name_abbreviations

    @property
    def contrabass_count(self):
        r'''Number of contrabasses in string orchestra.

        Returns nonnegative integer.
        '''
        return self._contrabass_count

    @property
    def split_hands(self):
        r'''Is true if each performer's hand receives a separate staff.
        '''
        return self._split_hands

    @property
    def use_percussion_clefs(self):
        r'''Is true if each staff should use a percussion clef rather than the
        normal clef for that instrument.
        '''
        return self._use_percussion_clefs

    @property
    def viola_count(self):
        r'''Number of violas in string orcestra.

        Returns nonnegative integer.
        '''
        return self._viola_count

    @property
    def violin_count(self):
        r'''Number of violins in string orchestra.

        Returns nonnegative integer.
        '''
        return self._violin_count
