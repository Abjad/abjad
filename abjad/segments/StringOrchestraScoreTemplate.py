from abjad.utilities.OrderedDict import OrderedDict
from .ScoreTemplate import ScoreTemplate


class StringOrchestraScoreTemplate(ScoreTemplate):
    r"""
    String orchestra score template.

    ..  container:: example

        >>> template = abjad.StringOrchestraScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score])
        \context Score = "Score"
        <<
            \tag #'(Violin1 Violin2 Violin3 Violin4 Violin5 Violin6 Viola1 Viola2 Viola3 Viola4 Cello1 Cello2 Cello3 Contrabass1 Contrabass2)
            \context GlobalContext = "GlobalContext"
            {
            }
            \context StaffGroup = "Outer Staff Group"
            <<
                \context ViolinStaffGroup = "Violin Staff Group"
                <<
                    \tag #'Violin1
                    \context StringPerformerStaffGroup = "Violin 1 Staff Group"
                    <<
                        \context BowingStaff = "Violin 1 Bowing Staff"
                        <<
                            \context BowingVoice = "Violin 1 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin 1 Fingering Staff"
                        <<
                            \context FingeringVoice = "Violin 1 Fingering Voice"
                            {
                                \clef "treble" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin2
                    \context StringPerformerStaffGroup = "Violin 2 Staff Group"
                    <<
                        \context BowingStaff = "Violin 2 Bowing Staff"
                        <<
                            \context BowingVoice = "Violin 2 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin 2 Fingering Staff"
                        <<
                            \context FingeringVoice = "Violin 2 Fingering Voice"
                            {
                                \clef "treble" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin3
                    \context StringPerformerStaffGroup = "Violin 3 Staff Group"
                    <<
                        \context BowingStaff = "Violin 3 Bowing Staff"
                        <<
                            \context BowingVoice = "Violin 3 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin 3 Fingering Staff"
                        <<
                            \context FingeringVoice = "Violin 3 Fingering Voice"
                            {
                                \clef "treble" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin4
                    \context StringPerformerStaffGroup = "Violin 4 Staff Group"
                    <<
                        \context BowingStaff = "Violin 4 Bowing Staff"
                        <<
                            \context BowingVoice = "Violin 4 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin 4 Fingering Staff"
                        <<
                            \context FingeringVoice = "Violin 4 Fingering Voice"
                            {
                                \clef "treble" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin5
                    \context StringPerformerStaffGroup = "Violin 5 Staff Group"
                    <<
                        \context BowingStaff = "Violin 5 Bowing Staff"
                        <<
                            \context BowingVoice = "Violin 5 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin 5 Fingering Staff"
                        <<
                            \context FingeringVoice = "Violin 5 Fingering Voice"
                            {
                                \clef "treble" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin6
                    \context StringPerformerStaffGroup = "Violin 6 Staff Group"
                    <<
                        \context BowingStaff = "Violin 6 Bowing Staff"
                        <<
                            \context BowingVoice = "Violin 6 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin 6 Fingering Staff"
                        <<
                            \context FingeringVoice = "Violin 6 Fingering Voice"
                            {
                                \clef "treble" %! ST3
                                s1
                            }
                        >>
                    >>
                >>
                \context ViolaStaffGroup = "Viola Staff Group"
                <<
                    \tag #'Viola1
                    \context StringPerformerStaffGroup = "Viola 1 Staff Group"
                    <<
                        \context BowingStaff = "Viola 1 Bowing Staff"
                        <<
                            \context BowingVoice = "Viola 1 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Viola 1 Fingering Staff"
                        <<
                            \context FingeringVoice = "Viola 1 Fingering Voice"
                            {
                                \clef "alto" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Viola2
                    \context StringPerformerStaffGroup = "Viola 2 Staff Group"
                    <<
                        \context BowingStaff = "Viola 2 Bowing Staff"
                        <<
                            \context BowingVoice = "Viola 2 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Viola 2 Fingering Staff"
                        <<
                            \context FingeringVoice = "Viola 2 Fingering Voice"
                            {
                                \clef "alto" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Viola3
                    \context StringPerformerStaffGroup = "Viola 3 Staff Group"
                    <<
                        \context BowingStaff = "Viola 3 Bowing Staff"
                        <<
                            \context BowingVoice = "Viola 3 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Viola 3 Fingering Staff"
                        <<
                            \context FingeringVoice = "Viola 3 Fingering Voice"
                            {
                                \clef "alto" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Viola4
                    \context StringPerformerStaffGroup = "Viola 4 Staff Group"
                    <<
                        \context BowingStaff = "Viola 4 Bowing Staff"
                        <<
                            \context BowingVoice = "Viola 4 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Viola 4 Fingering Staff"
                        <<
                            \context FingeringVoice = "Viola 4 Fingering Voice"
                            {
                                \clef "alto" %! ST3
                                s1
                            }
                        >>
                    >>
                >>
                \context CelloStaffGroup = "Cello Staff Group"
                <<
                    \tag #'Cello1
                    \context StringPerformerStaffGroup = "Cello 1 Staff Group"
                    <<
                        \context BowingStaff = "Cello 1 Bowing Staff"
                        <<
                            \context BowingVoice = "Cello 1 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Cello 1 Fingering Staff"
                        <<
                            \context FingeringVoice = "Cello 1 Fingering Voice"
                            {
                                \clef "bass" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Cello2
                    \context StringPerformerStaffGroup = "Cello 2 Staff Group"
                    <<
                        \context BowingStaff = "Cello 2 Bowing Staff"
                        <<
                            \context BowingVoice = "Cello 2 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Cello 2 Fingering Staff"
                        <<
                            \context FingeringVoice = "Cello 2 Fingering Voice"
                            {
                                \clef "bass" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Cello3
                    \context StringPerformerStaffGroup = "Cello 3 Staff Group"
                    <<
                        \context BowingStaff = "Cello 3 Bowing Staff"
                        <<
                            \context BowingVoice = "Cello 3 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Cello 3 Fingering Staff"
                        <<
                            \context FingeringVoice = "Cello 3 Fingering Voice"
                            {
                                \clef "bass" %! ST3
                                s1
                            }
                        >>
                    >>
                >>
                \context ContrabassStaffGroup = "Contrabass Staff Group"
                <<
                    \tag #'Contrabass1
                    \context StringPerformerStaffGroup = "Contrabass 1 Staff Group"
                    <<
                        \context BowingStaff = "Contrabass 1 Bowing Staff"
                        <<
                            \context BowingVoice = "Contrabass 1 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Contrabass 1 Fingering Staff"
                        <<
                            \context FingeringVoice = "Contrabass 1 Fingering Voice"
                            {
                                \clef "bass_8" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Contrabass2
                    \context StringPerformerStaffGroup = "Contrabass 2 Staff Group"
                    <<
                        \context BowingStaff = "Contrabass 2 Bowing Staff"
                        <<
                            \context BowingVoice = "Contrabass 2 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Contrabass 2 Fingering Staff"
                        <<
                            \context FingeringVoice = "Contrabass 2 Fingering Voice"
                            {
                                \clef "bass_8" %! ST3
                                s1
                            }
                        >>
                    >>
                >>
            >>
        >>

    ..  container:: example

        As a string quartet:

        >>> template = abjad.StringOrchestraScoreTemplate(
        ...     violin_count=2,
        ...     viola_count=1,
        ...     cello_count=1,
        ...     contrabass_count=0,
        ...     )
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score])
        \context Score = "Score"
        <<
            \tag #'(Violin1 Violin2 Viola Cello)
            \context GlobalContext = "GlobalContext"
            {
            }
            \context StaffGroup = "Outer Staff Group"
            <<
                \context ViolinStaffGroup = "Violin Staff Group"
                <<
                    \tag #'Violin1
                    \context StringPerformerStaffGroup = "Violin 1 Staff Group"
                    <<
                        \context BowingStaff = "Violin 1 Bowing Staff"
                        <<
                            \context BowingVoice = "Violin 1 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin 1 Fingering Staff"
                        <<
                            \context FingeringVoice = "Violin 1 Fingering Voice"
                            {
                                \clef "treble" %! ST3
                                s1
                            }
                        >>
                    >>
                    \tag #'Violin2
                    \context StringPerformerStaffGroup = "Violin 2 Staff Group"
                    <<
                        \context BowingStaff = "Violin 2 Bowing Staff"
                        <<
                            \context BowingVoice = "Violin 2 Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Violin 2 Fingering Staff"
                        <<
                            \context FingeringVoice = "Violin 2 Fingering Voice"
                            {
                                \clef "treble" %! ST3
                                s1
                            }
                        >>
                    >>
                >>
                \context ViolaStaffGroup = "Viola Staff Group"
                <<
                    \tag #'Viola
                    \context StringPerformerStaffGroup = "Viola Staff Group"
                    <<
                        \context BowingStaff = "Viola Bowing Staff"
                        <<
                            \context BowingVoice = "Viola Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Viola Fingering Staff"
                        <<
                            \context FingeringVoice = "Viola Fingering Voice"
                            {
                                \clef "alto" %! ST3
                                s1
                            }
                        >>
                    >>
                >>
                \context CelloStaffGroup = "Cello Staff Group"
                <<
                    \tag #'Cello
                    \context StringPerformerStaffGroup = "Cello Staff Group"
                    <<
                        \context BowingStaff = "Cello Bowing Staff"
                        <<
                            \context BowingVoice = "Cello Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Cello Fingering Staff"
                        <<
                            \context FingeringVoice = "Cello Fingering Voice"
                            {
                                \clef "bass" %! ST3
                                s1
                            }
                        >>
                    >>
                >>
            >>
        >>

    ..  container:: example

        As a cello solo:

        >>> template = abjad.StringOrchestraScoreTemplate(
        ...     violin_count=0,
        ...     viola_count=0,
        ...     cello_count=1,
        ...     contrabass_count=0,
        ...     )
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score])
        \context Score = "Score"
        <<
            \tag #'(Cello)
            \context GlobalContext = "GlobalContext"
            {
            }
            \context StaffGroup = "Outer Staff Group"
            <<
                \context CelloStaffGroup = "Cello Staff Group"
                <<
                    \tag #'Cello
                    \context StringPerformerStaffGroup = "Cello Staff Group"
                    <<
                        \context BowingStaff = "Cello Bowing Staff"
                        <<
                            \context BowingVoice = "Cello Bowing Voice"
                            {
                                s1
                            }
                        >>
                        \context FingeringStaff = "Cello Fingering Staff"
                        <<
                            \context FingeringVoice = "Cello Fingering Voice"
                            {
                                \clef "bass" %! ST3
                                s1
                            }
                        >>
                    >>
                >>
            >>
        >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cello_count',
        '_contrabass_count',
        '_split_hands',
        '_use_percussion_clefs',
        '_viola_count',
        '_violin_count',
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
        super().__init__()
        self._violin_count = int(violin_count)
        self._viola_count = int(viola_count)
        self._cello_count = int(cello_count)
        self._contrabass_count = int(contrabass_count)
        self._split_hands = bool(split_hands)
        self._use_percussion_clefs = bool(use_percussion_clefs)

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls string orchestra template.

        Returns score.
        """
        import abjad

        ### TAGS ###

        tag_names = []

        ### SCORE ###

        staff_group = abjad.StaffGroup(
            name='Outer Staff Group',
            )

        score = abjad.Score(
            [staff_group],
            name='Score',
            )

        ### VIOLINS ###

        if self.violin_count:
            clef_name = 'treble'
            if self.use_percussion_clefs:
                clef_name = 'percussion'
            instrument = abjad.Violin()
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
            instrument = abjad.Viola()
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
            instrument = abjad.Cello()
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
            instrument = abjad.Contrabass()
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

        global_context = abjad.Context(
            name='GlobalContext',
            lilypond_type='GlobalContext',
            )
        instrument_tags = ' '.join(tag_names)
        tag_string = r"\tag #'({})".format(instrument_tags)
        tag_command = abjad.LilyPondLiteral(tag_string, 'before')
        abjad.attach(tag_command, global_context)
        score.insert(0, global_context)
        return score

    ### PRIVATE METHODS ###

    def _make_instrument_staff_group(
        self,
        clef_name=None,
        count=None,
        instrument=None,
        ):
        import abjad
        name = instrument.name.title()
        instrument_staff_group = abjad.StaffGroup(
            lilypond_type='{}StaffGroup'.format(name),
            name='{} Staff Group'.format(name),
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
        import abjad
        if number is not None:
            name = '{} {}'.format(
                instrument.name.title(),
                number,
                )
        else:
            name = instrument.name.title()
        pitch_range = instrument.pitch_range
        staff_group = abjad.StaffGroup(
            lilypond_type='StringPerformerStaffGroup',
            name='{} Staff Group'.format(name),
            )
        tag_name = name.replace(' ', '')
        tag_string = r"\tag #'{}".format(tag_name)
        tag_command = abjad.LilyPondLiteral(tag_string, 'before')
        abjad.attach(tag_command, staff_group)
        if self.split_hands:
            lh_voice = abjad.Voice(
                [],
                lilypond_type='FingeringVoice',
                name='{} Fingering Voice'.format(name),
                )
            abbreviation = lh_voice.name.lower().replace(' ', '_')
            self.voice_abbreviations[abbreviation] = lh_voice.name
            lh_staff = abjad.Staff(
                [
                    lh_voice
                    ],
                lilypond_type='FingeringStaff',
                name='{} Fingering Staff'.format(name),
                )
            lh_staff.is_simultaneous = True
            abjad.annotate(lh_staff, 'pitch_range', pitch_range)
            abjad.annotate(lh_staff, 'default_clef', abjad.Clef(clef_name))
            rh_voice = abjad.Voice(
                [],
                lilypond_type='BowingVoice',
                name='{} Bowing Voice'.format(name),
                )
            abbreviation = rh_voice.name.lower().replace(' ', '_')
            self.voice_abbreviations[abbreviation] = rh_voice.name
            rh_staff = abjad.Staff(
                [
                    rh_voice
                    ],
                lilypond_type='BowingStaff',
                name='{} Bowing Staff'.format(name),
                )
            rh_staff.is_simultaneous = True
            staff_group.extend([rh_staff, lh_staff])
        else:
            lh_voice = abjad.Voice(
                [],
                lilypond_type='FingeringVoice',
                name='{} Voice'.format(name),
                )
            lh_staff = abjad.Staff(
                [
                    lh_voice
                    ],
                lilypond_type='FingeringStaff',
                name='{} Staff'.format(name),
                )
            lh_staff.is_simultaneous = True
            abjad.annotate(lh_staff, 'pitch_range', pitch_range)
            abjad.annotate(lh_staff, 'default_clef', abjad.Clef(clef_name))
            staff_group.append(lh_staff)
        return staff_group, tag_name

    ### PUBLIC PROPERTIES ###

    @property
    def cello_count(self):
        """
        Number of cellos in string orchestra.

        Returns nonnegative integer.
        """
        return self._cello_count

    @property
    def contrabass_count(self):
        """
        Number of contrabasses in string orchestra.

        Returns nonnegative integer.
        """
        return self._contrabass_count

    @property
    def split_hands(self):
        """
        Is true if each performer's hand receives a separate staff.
        """
        return self._split_hands

    @property
    def use_percussion_clefs(self):
        """
        Is true if each staff should use a percussion clef rather than the
        normal clef for that instrument.
        """
        return self._use_percussion_clefs

    @property
    def viola_count(self):
        """
        Number of violas in string orcestra.

        Returns nonnegative integer.
        """
        return self._viola_count

    @property
    def violin_count(self):
        """
        Number of violins in string orchestra.

        Returns nonnegative integer.
        """
        return self._violin_count
