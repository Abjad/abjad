import typing

from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Tag import Tag


class Tags(object):
    """
    Tags.

    ..  container:: example

        Abjad-level singleton:

        >>> abjad.tags
        Tags()

    ..  container:: example

        Class is also available:

        >>> abjad.Tags()
        Tags()

    ..  container:: example

        >>> abjad.tags.SHOW_TO_JOIN_BROKEN_SPANNERS
        Tag('SHOW_TO_JOIN_BROKEN_SPANNERS')

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _known_tags: tuple = (
        ### BAR EXTENT ###
        "EXPLICIT_BAR_EXTENT",
        "REAPPLIED_BAR_EXTENT",
        "REDUNDANT_BAR_EXTENT",
        ### CLEF ###
        "DEFAULT_CLEF",
        "DEFAULT_CLEF_COLOR",
        "DEFAULT_CLEF_COLOR_CANCELLATION",
        "DEFAULT_CLEF_REDRAW_COLOR",
        "EXPLICIT_CLEF",
        "EXPLICIT_CLEF_COLOR",
        "EXPLICIT_CLEF_COLOR_CANCELLATION",
        "EXPLICIT_CLEF_REDRAW_COLOR",
        "REAPPLIED_CLEF",
        "REAPPLIED_CLEF_COLOR",
        "REAPPLIED_CLEF_COLOR_CANCELLATION",
        "REAPPLIED_CLEF_REDRAW_COLOR",
        "REDUNDANT_CLEF",
        "REDUNDANT_CLEF_COLOR",
        "REDUNDANT_CLEF_COLOR_CANCELLATION",
        "REDUNDANT_CLEF_REDRAW_COLOR",
        ### COMMANDS, IMPORTANT ###
        "ONE_VOICE_COMMAND",
        ### DOCUMENT ANNOTATIONS ###
        "BREAK",
        "CLOCK_TIME",
        "EMPTY_START_BAR",
        "FERMATA_MEASURE",
        "FIGURE_NAME",
        "HIDDEN",
        "HIDE_IN_PARTS",
        "INVISIBLE_MUSIC_COLORING",
        "INVISIBLE_MUSIC_COMMAND",
        "LOCAL_MEASURE_NUMBER",
        "MEASURE_NUMBER",
        "MULTIMEASURE_REST",
        "NOT_MOL",
        "NOTE",
        "ONLY_MOL",
        "PHANTOM",
        "REST_VOICE",
        "SHIFTED_CLEF",
        "SHOW_IN_PARTS",
        "SKIP",
        "SPACING",
        "SPACING_OVERRIDE",
        "SPACING_COMMAND",
        "SPACING_OVERRIDE_COMMAND",
        "STAGE_NUMBER",
        ### DOCUMENT TYPES ###
        "BUILD",
        "FIRST_SEGMENT_DEFAULT",
        "PARTS",
        "SCORE",
        "SEGMENT",
        ### DYNAMIC ###
        "EXPLICIT_DYNAMIC",
        "EXPLICIT_DYNAMIC_COLOR",
        "REAPPLIED_DYNAMIC",
        "REAPPLIED_DYNAMIC_COLOR",
        "REDUNDANT_DYNAMIC",
        "REDUNDANT_DYNAMIC_COLOR",
        ### FIGURES ###
        "FORESHADOW",
        "INCOMPLETE",
        "RECOLLECTION",
        ### INSTRUMENT ###
        "DEFAULT_INSTRUMENT",
        "DEFAULT_INSTRUMENT_ALERT",
        "DEFAULT_INSTRUMENT_COLOR",
        "REDRAWN_DEFAULT_INSTRUMENT",
        "REDRAWN_DEFAULT_INSTRUMENT_COLOR",
        "EXPLICIT_INSTRUMENT",
        "EXPLICIT_INSTRUMENT_ALERT",
        "EXPLICIT_INSTRUMENT_COLOR",
        "REDRAWN_EXPLICIT_INSTRUMENT",
        "REDRAWN_EXPLICIT_INSTRUMENT_COLOR",
        "REAPPLIED_INSTRUMENT",
        "REAPPLIED_INSTRUMENT_ALERT",
        "REAPPLIED_INSTRUMENT_COLOR",
        "REDRAWN_REAPPLIED_INSTRUMENT",
        "REDRAWN_REAPPLIED_INSTRUMENT_COLOR",
        "REDUNDANT_INSTRUMENT",
        "REDUNDANT_INSTRUMENT_ALERT",
        "REDUNDANT_INSTRUMENT_COLOR",
        "REDRAWN_REDUNDANT_INSTRUMENT",
        "REDRAWN_REDUNDANT_INSTRUMENT_COLOR",
        ### MARGIN MARKUP ###
        "DEFAULT_MARGIN_MARKUP",
        "DEFAULT_MARGIN_MARKUP_ALERT",
        "DEFAULT_MARGIN_MARKUP_COLOR",
        "REDRAWN_DEFAULT_MARGIN_MARKUP",
        "REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR",
        "EXPLICIT_MARGIN_MARKUP",
        "EXPLICIT_MARGIN_MARKUP_ALERT",
        "EXPLICIT_MARGIN_MARKUP_COLOR",
        "REDRAWN_EXPLICIT_MARGIN_MARKUP",
        "REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR",
        "REAPPLIED_MARGIN_MARKUP",
        "REAPPLIED_MARGIN_MARKUP_ALERT",
        "REAPPLIED_MARGIN_MARKUP_COLOR",
        "REDRAWN_REAPPLIED_MARGIN_MARKUP",
        "REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR",
        "REDUNDANT_MARGIN_MARKUP",
        "REDUNDANT_MARGIN_MARKUP_ALERT",
        "REDUNDANT_MARGIN_MARKUP_COLOR",
        "REDRAWN_REDUNDANT_MARGIN_MARKUP",
        "REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR",
        ### METRONOME MARK ###
        "EXPLICIT_METRONOME_MARK",
        "EXPLICIT_METRONOME_MARK_WITH_COLOR",
        "REAPPLIED_METRONOME_MARK",
        "REAPPLIED_METRONOME_MARK_WITH_COLOR",
        "REDUNDANT_METRONOME_MARK",
        "REDUNDANT_METRONOME_MARK_WITH_COLOR",
        ### METRONOME MARK SPANNER ###
        "METRIC_MODULATION_IS_NOT_SCALED",
        "METRIC_MODULATION_IS_SCALED",
        "METRIC_MODULATION_IS_STRIPPED",
        ### PERSISTENT OVERRIDE ###
        "EXPLICIT_PERSISTENT_OVERRIDE",
        "REAPPLIED_PERSISTENT_OVERRIDE",
        "REDUNDANT_PERSISTENT_OVERRIDE",
        ### PITCH COLORINGS ###
        "MOCK_COLORING",
        "NOT_YET_PITCHED_COLORING",
        "NOT_YET_REGISTERED_COLORING",
        "OCTAVE_COLORING",
        "OUT_OF_RANGE_COLORING",
        "REPEAT_PITCH_CLASS_COLORING",
        "TACET_COLORING",
        ### RHYTHM ###
        "DURATION_MULTIPLIER",
        ### SPACING SECTION ###
        "EXPLICIT_SPACING_SECTION",
        "EXPLICIT_SPACING_SECTION_COLOR",
        "REAPPLIED_SPACING_SECTION",
        "REAPPLIED_SPACING_SECTION_COLOR",
        "REDUNDANT_SPACING_SECTION",
        "REDUNDANT_SPACING_SECTION_COLOR",
        ### SPANNERS, BROKEN ###
        "AUTODETECT",
        "HIDE_TO_JOIN_BROKEN_SPANNERS",
        "LEFT_BROKEN",
        "RIGHT_BROKEN",
        "RIGHT_BROKEN_BEAM",  # used in figure-maker
        "RIGHT_BROKEN_SHOW_NEXT",
        "SHOW_TO_JOIN_BROKEN_SPANNERS",
        ### SPANNERS, CUSTOM ###
        "BOW_SPEED_SPANNER",
        "CIRCLE_BOW_SPANNER",
        "CLB_SPANNER",
        "COVERED_SPANNER",
        "DAMP_SPANNER",
        "EOS_STOP_MM_SPANNER",
        "HALF_CLT_SPANNER",
        "MATERIAL_ANNOTATION_SPANNER",
        "METRIC_MODULATION_SPANNER",
        "PITCH_ANNOTATION_SPANNER",
        "PIZZICATO_SPANNER",
        "RHYTHM_ANNOTATION_SPANNER",
        "SCP_SPANNER",
        "SPAZZOLATO_SPANNER",
        "STRING_NUMBER_SPANNER",
        "TASTO_SPANNER",
        "VIBRATO_SPANNER",
        ### SPANNERS, OTHER ###
        "SPANNER_START",
        "SPANNER_STOP",
        ### STAFF LINES ###
        "EXPLICIT_STAFF_LINES",
        "EXPLICIT_STAFF_LINES_COLOR",
        "REAPPLIED_STAFF_LINES",
        "REAPPLIED_STAFF_LINES_COLOR",
        "REDUNDANT_STAFF_LINES",
        "REDUNDANT_STAFF_LINES_COLOR",
        ### TIME SIGNATURE ###
        "EXPLICIT_TIME_SIGNATURE",
        "EXPLICIT_TIME_SIGNATURE_COLOR",
        "REAPPLIED_TIME_SIGNATURE",
        "REAPPLIED_TIME_SIGNATURE_COLOR",
        "REDUNDANT_TIME_SIGNATURE",
        "REDUNDANT_TIME_SIGNATURE_COLOR",
    )

    ### SPECIAL METHODS ###

    def __getattr__(self, name: str) -> Tag:
        """
        Gets tag with ``name``.

        Raises attribute error when ``name`` is unknown.
        """
        if name not in self._known_tags:
            raise AttributeError(f"unknown tag {name!r}.")
        return Tag(name)

    def __repr__(self) -> str:
        """
        Delegates to storage format manager.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def NOT_PARTS(self):
        """
        Not parts.
        """
        return Tag("-PARTS")

    @property
    def NOT_SCORE(self):
        """
        Not score.
        """
        return Tag("-SCORE")

    @property
    def NOT_SEGMENT(self):
        """
        Not segment.
        """
        return Tag("-SEGMENT")

    @property
    def ONLY_PARTS(self):
        """
        Only parts.
        """
        return Tag("+PARTS")

    @property
    def ONLY_SCORE(self):
        """
        Only score.
        """
        return Tag("+SCORE")

    @property
    def ONLY_SEGMENT(self):
        """
        Only segment.
        """
        return Tag("+SEGMENT")

    ### PUBLIC METHODS ###

    def annotation_spanner_tags(self) -> typing.List[Tag]:
        """
        Gets annotation spanner tags.

        ..  container:: example

            >>> for tag in abjad.tags.annotation_spanner_tags():
            ...     tag
            Tag('MATERIAL_ANNOTATION_SPANNER')
            Tag('PITCH_ANNOTATION_SPANNER')
            Tag('RHYTHM_ANNOTATION_SPANNER')

        """
        return [
            self.MATERIAL_ANNOTATION_SPANNER,
            self.PITCH_ANNOTATION_SPANNER,
            self.RHYTHM_ANNOTATION_SPANNER,
        ]

    def clef_color_tags(self, path=None) -> typing.List[Tag]:
        """
        Gets clef color tags.

        ..  container:: example

            >>> for tag in abjad.tags.clef_color_tags():
            ...     tag
            ...
            Tag('DEFAULT_CLEF_COLOR')
            Tag('DEFAULT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_CLEF_COLOR')
            Tag('EXPLICIT_CLEF_REDRAW_COLOR')
            Tag('REAPPLIED_CLEF_COLOR')
            Tag('REAPPLIED_CLEF_REDRAW_COLOR')
            Tag('REDUNDANT_CLEF_COLOR')
            Tag('REDUNDANT_CLEF_REDRAW_COLOR')

        ..  container:: example

            Segment:

            >>> path = abjad.Path('etude', 'segments', '_')
            >>> for tag in abjad.tags.clef_color_tags(path=path):
            ...     tag
            ...
            Tag('DEFAULT_CLEF_COLOR')
            Tag('DEFAULT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_CLEF_COLOR')
            Tag('EXPLICIT_CLEF_REDRAW_COLOR')
            Tag('REAPPLIED_CLEF_COLOR')
            Tag('REAPPLIED_CLEF_REDRAW_COLOR')
            Tag('REDUNDANT_CLEF_COLOR')
            Tag('REDUNDANT_CLEF_REDRAW_COLOR')

        ..  container:: example

            Segments:

            >>> path = abjad.Path('etude', 'segments')
            >>> for tag in abjad.tags.clef_color_tags(path=path):
            ...     tag
            ...
            Tag('DEFAULT_CLEF_COLOR')
            Tag('DEFAULT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_CLEF_COLOR')
            Tag('EXPLICIT_CLEF_REDRAW_COLOR')
            Tag('REAPPLIED_CLEF_COLOR')
            Tag('REAPPLIED_CLEF_REDRAW_COLOR')
            Tag('REDUNDANT_CLEF_COLOR')
            Tag('REDUNDANT_CLEF_REDRAW_COLOR')

        ..  container:: example

            Build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> for tag in abjad.tags.clef_color_tags(path=path):
            ...     tag
            ...
            Tag('DEFAULT_CLEF_COLOR')
            Tag('DEFAULT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_CLEF_COLOR')
            Tag('EXPLICIT_CLEF_REDRAW_COLOR')
            Tag('REAPPLIED_CLEF_COLOR')
            Tag('REAPPLIED_CLEF_REDRAW_COLOR')
            Tag('REDUNDANT_CLEF_COLOR')
            Tag('REDUNDANT_CLEF_REDRAW_COLOR')
            Tag('REAPPLIED_CLEF')

        """
        tags = [
            self.DEFAULT_CLEF_COLOR,
            self.DEFAULT_CLEF_REDRAW_COLOR,
            self.EXPLICIT_CLEF_COLOR,
            self.EXPLICIT_CLEF_REDRAW_COLOR,
            self.REAPPLIED_CLEF_COLOR,
            self.REAPPLIED_CLEF_REDRAW_COLOR,
            self.REDUNDANT_CLEF_COLOR,
            self.REDUNDANT_CLEF_REDRAW_COLOR,
        ]
        if path and not path.is_segment() and not path.is_segments():
            tags.append(self.REAPPLIED_CLEF)
        return tags

    def documentation_removal_tags(self) -> typing.List[Tag]:
        """
        Gets documentation removal tags.

        ..  container:: example

            >>> for tag in abjad.tags.documentation_removal_tags():
            ...     tag
            ...
            Tag('CLOCK_TIME')
            Tag('FIGURE_NAME')
            Tag('LOCAL_MEASURE_NUMBER')
            Tag('MEASURE_NUMBER')
            Tag('SPACING')
            Tag('STAGE_NUMBER')

        """
        return [
            self.CLOCK_TIME,
            self.FIGURE_NAME,
            self.LOCAL_MEASURE_NUMBER,
            self.MEASURE_NUMBER,
            self.SPACING,
            self.STAGE_NUMBER,
        ]

    def dynamic_color_tags(self, path=None) -> typing.List[Tag]:
        """
        Gets dynamic color tags.

        ..  container:: example

            >>> for tag in abjad.tags.dynamic_color_tags():
            ...     tag
            ...
            Tag('EXPLICIT_DYNAMIC_COLOR')
            Tag('REAPPLIED_DYNAMIC')
            Tag('REAPPLIED_DYNAMIC_COLOR')
            Tag('REDUNDANT_DYNAMIC_COLOR')

        Ignores ``path``.
        """
        return [
            self.EXPLICIT_DYNAMIC_COLOR,
            self.REAPPLIED_DYNAMIC,
            self.REAPPLIED_DYNAMIC_COLOR,
            self.REDUNDANT_DYNAMIC_COLOR,
        ]

    def instrument_color_tags(self, path=None) -> typing.List[Tag]:
        """
        Gets instrument color tags.

        ..  container:: example

            >>> for tag in abjad.tags.instrument_color_tags():
            ...     tag
            ...
            Tag('DEFAULT_INSTRUMENT_ALERT')
            Tag('DEFAULT_INSTRUMENT_COLOR')
            Tag('REDRAWN_DEFAULT_INSTRUMENT_COLOR')
            Tag('EXPLICIT_INSTRUMENT_ALERT')
            Tag('EXPLICIT_INSTRUMENT_COLOR')
            Tag('REAPPLIED_INSTRUMENT_COLOR')
            Tag('REAPPLIED_INSTRUMENT_ALERT')
            Tag('REDRAWN_EXPLICIT_INSTRUMENT_COLOR')
            Tag('REDRAWN_REAPPLIED_INSTRUMENT_COLOR')
            Tag('REDUNDANT_INSTRUMENT_ALERT')
            Tag('REDUNDANT_INSTRUMENT_COLOR')
            Tag('REDRAWN_REDUNDANT_INSTRUMENT_COLOR')

        Ignores ``path``.
        """
        return [
            self.DEFAULT_INSTRUMENT_ALERT,
            self.DEFAULT_INSTRUMENT_COLOR,
            self.REDRAWN_DEFAULT_INSTRUMENT_COLOR,
            self.EXPLICIT_INSTRUMENT_ALERT,
            self.EXPLICIT_INSTRUMENT_COLOR,
            self.REAPPLIED_INSTRUMENT_COLOR,
            self.REAPPLIED_INSTRUMENT_ALERT,
            self.REDRAWN_EXPLICIT_INSTRUMENT_COLOR,
            self.REDRAWN_REAPPLIED_INSTRUMENT_COLOR,
            self.REDUNDANT_INSTRUMENT_ALERT,
            self.REDUNDANT_INSTRUMENT_COLOR,
            self.REDRAWN_REDUNDANT_INSTRUMENT_COLOR,
        ]

    def layout_removal_tags(self) -> typing.List[Tag]:
        """
        Gets layout removal tags.

        ..  container:: example

            >>> for tag in abjad.tags.layout_removal_tags():
            ...     tag
            ...
            Tag('EMPTY_START_BAR')
            Tag('EXPLICIT_TIME_SIGNATURE_COLOR')
            Tag('LOCAL_MEASURE_NUMBER')
            Tag('MEASURE_NUMBER')
            Tag('REDUNDANT_TIME_SIGNATURE_COLOR')
            Tag('STAGE_NUMBER')

        """
        return [
            self.EMPTY_START_BAR,
            self.EXPLICIT_TIME_SIGNATURE_COLOR,
            self.LOCAL_MEASURE_NUMBER,
            self.MEASURE_NUMBER,
            self.REDUNDANT_TIME_SIGNATURE_COLOR,
            self.STAGE_NUMBER,
        ]

    def margin_markup_color_tags(self, path=None) -> typing.List[Tag]:
        """
        Gets margin markup color tags.

        ..  container:: example

            >>> for tag in abjad.tags.margin_markup_color_tags():
            ...     tag
            ...
            Tag('DEFAULT_MARGIN_MARKUP_ALERT')
            Tag('DEFAULT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR')
            Tag('EXPLICIT_MARGIN_MARKUP_ALERT')
            Tag('EXPLICIT_MARGIN_MARKUP_COLOR')
            Tag('REAPPLIED_MARGIN_MARKUP_ALERT')
            Tag('REAPPLIED_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR')
            Tag('REDUNDANT_MARGIN_MARKUP_ALERT')
            Tag('REDUNDANT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR')

        Ignores ``path``.
        """
        return [
            self.DEFAULT_MARGIN_MARKUP_ALERT,
            self.DEFAULT_MARGIN_MARKUP_COLOR,
            self.REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR,
            self.EXPLICIT_MARGIN_MARKUP_ALERT,
            self.EXPLICIT_MARGIN_MARKUP_COLOR,
            self.REAPPLIED_MARGIN_MARKUP_ALERT,
            self.REAPPLIED_MARGIN_MARKUP_COLOR,
            self.REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR,
            self.REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR,
            self.REDUNDANT_MARGIN_MARKUP_ALERT,
            self.REDUNDANT_MARGIN_MARKUP_COLOR,
            self.REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR,
        ]

    def metronome_mark_color_expression_tags(self, path=None) -> typing.List[Tag]:
        """
        Gets metronome mark color expression tags.

        ..  container:: example

            >>> for tag in abjad.tags.metronome_mark_color_expression_tags():
            ...     tag
            ...
            Tag('EXPLICIT_METRONOME_MARK_WITH_COLOR')
            Tag('REAPPLIED_METRONOME_MARK_WITH_COLOR')
            Tag('REDUNDANT_METRONOME_MARK_WITH_COLOR')

        """
        return [
            self.EXPLICIT_METRONOME_MARK_WITH_COLOR,
            self.REAPPLIED_METRONOME_MARK_WITH_COLOR,
            self.REDUNDANT_METRONOME_MARK_WITH_COLOR,
        ]

    def metronome_mark_color_suppression_tags(self, path=None) -> typing.List[Tag]:
        """
        Gets metronome mark color suppression tags.

        ..  container:: example

            >>> for tag in abjad.tags.metronome_mark_color_suppression_tags():
            ...     tag
            ...
            Tag('EXPLICIT_METRONOME_MARK')
            Tag('REDUNDANT_METRONOME_MARK')

        Ignores ``path``.
        """
        return [self.EXPLICIT_METRONOME_MARK, self.REDUNDANT_METRONOME_MARK]

    def music_annotation_tags(self) -> typing.List[Tag]:
        """
        Gets music annotation tags.

        ..  container:: example

            >>> for tag in abjad.tags.music_annotation_tags():
            ...     tag
            Tag('CLOCK_TIME')
            Tag('FIGURE_NAME')
            Tag('INVISIBLE_MUSIC_COLORING')
            Tag('LOCAL_MEASURE_NUMBER')
            Tag('MATERIAL_ANNOTATION_SPANNER')
            Tag('MOCK_COLORING')
            Tag('NOT_YET_PITCHED_COLORING')
            Tag('OCTAVE_COLORING')
            Tag('PITCH_ANNOTATION_SPANNER')
            Tag('REPEAT_PITCH_CLASS_COLORING')
            Tag('RHYTHM_ANNOTATION_SPANNER')
            Tag('SPACING')
            Tag('SPACING_OVERRIDE')
            Tag('STAGE_NUMBER')
            Tag('TACET_COLORING')

        """
        return [
            self.CLOCK_TIME,
            self.FIGURE_NAME,
            self.INVISIBLE_MUSIC_COLORING,
            self.LOCAL_MEASURE_NUMBER,
            self.MATERIAL_ANNOTATION_SPANNER,
            self.MOCK_COLORING,
            self.NOT_YET_PITCHED_COLORING,
            self.OCTAVE_COLORING,
            self.PITCH_ANNOTATION_SPANNER,
            self.REPEAT_PITCH_CLASS_COLORING,
            self.RHYTHM_ANNOTATION_SPANNER,
            self.SPACING,
            self.SPACING_OVERRIDE,
            self.STAGE_NUMBER,
            self.TACET_COLORING,
        ]

    def persistent_indicator_color_expression_tags(self, path=None) -> typing.List[Tag]:
        """
        Gets persistent indicator color expression tags.

        ..  container:: example

            >>> tags = abjad.tags.persistent_indicator_color_expression_tags()
            >>> for tag in tags:
            ...     tag
            ...
            Tag('DEFAULT_CLEF_COLOR')
            Tag('DEFAULT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_CLEF_COLOR')
            Tag('EXPLICIT_CLEF_REDRAW_COLOR')
            Tag('REAPPLIED_CLEF_COLOR')
            Tag('REAPPLIED_CLEF_REDRAW_COLOR')
            Tag('REDUNDANT_CLEF_COLOR')
            Tag('REDUNDANT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_DYNAMIC_COLOR')
            Tag('REAPPLIED_DYNAMIC')
            Tag('REAPPLIED_DYNAMIC_COLOR')
            Tag('REDUNDANT_DYNAMIC_COLOR')
            Tag('DEFAULT_INSTRUMENT_ALERT')
            Tag('DEFAULT_INSTRUMENT_COLOR')
            Tag('REDRAWN_DEFAULT_INSTRUMENT_COLOR')
            Tag('EXPLICIT_INSTRUMENT_ALERT')
            Tag('EXPLICIT_INSTRUMENT_COLOR')
            Tag('REAPPLIED_INSTRUMENT_COLOR')
            Tag('REAPPLIED_INSTRUMENT_ALERT')
            Tag('REDRAWN_EXPLICIT_INSTRUMENT_COLOR')
            Tag('REDRAWN_REAPPLIED_INSTRUMENT_COLOR')
            Tag('REDUNDANT_INSTRUMENT_ALERT')
            Tag('REDUNDANT_INSTRUMENT_COLOR')
            Tag('REDRAWN_REDUNDANT_INSTRUMENT_COLOR')
            Tag('DEFAULT_MARGIN_MARKUP_ALERT')
            Tag('DEFAULT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR')
            Tag('EXPLICIT_MARGIN_MARKUP_ALERT')
            Tag('EXPLICIT_MARGIN_MARKUP_COLOR')
            Tag('REAPPLIED_MARGIN_MARKUP_ALERT')
            Tag('REAPPLIED_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR')
            Tag('REDUNDANT_MARGIN_MARKUP_ALERT')
            Tag('REDUNDANT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR')
            Tag('EXPLICIT_METRONOME_MARK_WITH_COLOR')
            Tag('REAPPLIED_METRONOME_MARK_WITH_COLOR')
            Tag('REDUNDANT_METRONOME_MARK_WITH_COLOR')
            Tag('EXPLICIT_STAFF_LINES_COLOR')
            Tag('REAPPLIED_STAFF_LINES_COLOR')
            Tag('REDUNDANT_STAFF_LINES_COLOR')
            Tag('EXPLICIT_TIME_SIGNATURE_COLOR')
            Tag('REAPPLIED_TIME_SIGNATURE_COLOR')
            Tag('REDUNDANT_TIME_SIGNATURE_COLOR')

        ..  container:: example

            Segment:

            >>> path = abjad.Path('etude', 'segments', '_')
            >>> tags = abjad.tags.persistent_indicator_color_expression_tags(path)
            >>> for tag in tags:
            ...     tag
            ...
            Tag('DEFAULT_CLEF_COLOR')
            Tag('DEFAULT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_CLEF_COLOR')
            Tag('EXPLICIT_CLEF_REDRAW_COLOR')
            Tag('REAPPLIED_CLEF_COLOR')
            Tag('REAPPLIED_CLEF_REDRAW_COLOR')
            Tag('REDUNDANT_CLEF_COLOR')
            Tag('REDUNDANT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_DYNAMIC_COLOR')
            Tag('REAPPLIED_DYNAMIC')
            Tag('REAPPLIED_DYNAMIC_COLOR')
            Tag('REDUNDANT_DYNAMIC_COLOR')
            Tag('DEFAULT_INSTRUMENT_ALERT')
            Tag('DEFAULT_INSTRUMENT_COLOR')
            Tag('REDRAWN_DEFAULT_INSTRUMENT_COLOR')
            Tag('EXPLICIT_INSTRUMENT_ALERT')
            Tag('EXPLICIT_INSTRUMENT_COLOR')
            Tag('REAPPLIED_INSTRUMENT_COLOR')
            Tag('REAPPLIED_INSTRUMENT_ALERT')
            Tag('REDRAWN_EXPLICIT_INSTRUMENT_COLOR')
            Tag('REDRAWN_REAPPLIED_INSTRUMENT_COLOR')
            Tag('REDUNDANT_INSTRUMENT_ALERT')
            Tag('REDUNDANT_INSTRUMENT_COLOR')
            Tag('REDRAWN_REDUNDANT_INSTRUMENT_COLOR')
            Tag('DEFAULT_MARGIN_MARKUP_ALERT')
            Tag('DEFAULT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR')
            Tag('EXPLICIT_MARGIN_MARKUP_ALERT')
            Tag('EXPLICIT_MARGIN_MARKUP_COLOR')
            Tag('REAPPLIED_MARGIN_MARKUP_ALERT')
            Tag('REAPPLIED_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR')
            Tag('REDUNDANT_MARGIN_MARKUP_ALERT')
            Tag('REDUNDANT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR')
            Tag('EXPLICIT_METRONOME_MARK_WITH_COLOR')
            Tag('REAPPLIED_METRONOME_MARK_WITH_COLOR')
            Tag('REDUNDANT_METRONOME_MARK_WITH_COLOR')
            Tag('EXPLICIT_STAFF_LINES_COLOR')
            Tag('REAPPLIED_STAFF_LINES_COLOR')
            Tag('REDUNDANT_STAFF_LINES_COLOR')
            Tag('EXPLICIT_TIME_SIGNATURE_COLOR')
            Tag('REAPPLIED_TIME_SIGNATURE_COLOR')
            Tag('REDUNDANT_TIME_SIGNATURE_COLOR')

        ..  container:: example

            Segments:

            >>> path = abjad.Path('etude', 'segments')
            >>> tags = abjad.tags.persistent_indicator_color_expression_tags(path)
            >>> for tag in tags:
            ...     tag
            ...
            Tag('DEFAULT_CLEF_COLOR')
            Tag('DEFAULT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_CLEF_COLOR')
            Tag('EXPLICIT_CLEF_REDRAW_COLOR')
            Tag('REAPPLIED_CLEF_COLOR')
            Tag('REAPPLIED_CLEF_REDRAW_COLOR')
            Tag('REDUNDANT_CLEF_COLOR')
            Tag('REDUNDANT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_DYNAMIC_COLOR')
            Tag('REAPPLIED_DYNAMIC')
            Tag('REAPPLIED_DYNAMIC_COLOR')
            Tag('REDUNDANT_DYNAMIC_COLOR')
            Tag('DEFAULT_INSTRUMENT_ALERT')
            Tag('DEFAULT_INSTRUMENT_COLOR')
            Tag('REDRAWN_DEFAULT_INSTRUMENT_COLOR')
            Tag('EXPLICIT_INSTRUMENT_ALERT')
            Tag('EXPLICIT_INSTRUMENT_COLOR')
            Tag('REAPPLIED_INSTRUMENT_COLOR')
            Tag('REAPPLIED_INSTRUMENT_ALERT')
            Tag('REDRAWN_EXPLICIT_INSTRUMENT_COLOR')
            Tag('REDRAWN_REAPPLIED_INSTRUMENT_COLOR')
            Tag('REDUNDANT_INSTRUMENT_ALERT')
            Tag('REDUNDANT_INSTRUMENT_COLOR')
            Tag('REDRAWN_REDUNDANT_INSTRUMENT_COLOR')
            Tag('DEFAULT_MARGIN_MARKUP_ALERT')
            Tag('DEFAULT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR')
            Tag('EXPLICIT_MARGIN_MARKUP_ALERT')
            Tag('EXPLICIT_MARGIN_MARKUP_COLOR')
            Tag('REAPPLIED_MARGIN_MARKUP_ALERT')
            Tag('REAPPLIED_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR')
            Tag('REDUNDANT_MARGIN_MARKUP_ALERT')
            Tag('REDUNDANT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR')
            Tag('EXPLICIT_METRONOME_MARK_WITH_COLOR')
            Tag('REAPPLIED_METRONOME_MARK_WITH_COLOR')
            Tag('REDUNDANT_METRONOME_MARK_WITH_COLOR')
            Tag('EXPLICIT_STAFF_LINES_COLOR')
            Tag('REAPPLIED_STAFF_LINES_COLOR')
            Tag('REDUNDANT_STAFF_LINES_COLOR')
            Tag('REAPPLIED_STAFF_LINES')
            Tag('EXPLICIT_TIME_SIGNATURE_COLOR')
            Tag('REAPPLIED_TIME_SIGNATURE_COLOR')
            Tag('REDUNDANT_TIME_SIGNATURE_COLOR')
            Tag('REAPPLIED_TIME_SIGNATURE')

        ..  container:: example

            Build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> tags = abjad.tags.persistent_indicator_color_expression_tags(path)
            >>> for tag in tags:
            ...     tag
            ...
            Tag('DEFAULT_CLEF_COLOR')
            Tag('DEFAULT_CLEF_REDRAW_COLOR')
            Tag('EXPLICIT_CLEF_COLOR')
            Tag('EXPLICIT_CLEF_REDRAW_COLOR')
            Tag('REAPPLIED_CLEF_COLOR')
            Tag('REAPPLIED_CLEF_REDRAW_COLOR')
            Tag('REDUNDANT_CLEF_COLOR')
            Tag('REDUNDANT_CLEF_REDRAW_COLOR')
            Tag('REAPPLIED_CLEF')
            Tag('EXPLICIT_DYNAMIC_COLOR')
            Tag('REAPPLIED_DYNAMIC')
            Tag('REAPPLIED_DYNAMIC_COLOR')
            Tag('REDUNDANT_DYNAMIC_COLOR')
            Tag('DEFAULT_INSTRUMENT_ALERT')
            Tag('DEFAULT_INSTRUMENT_COLOR')
            Tag('REDRAWN_DEFAULT_INSTRUMENT_COLOR')
            Tag('EXPLICIT_INSTRUMENT_ALERT')
            Tag('EXPLICIT_INSTRUMENT_COLOR')
            Tag('REAPPLIED_INSTRUMENT_COLOR')
            Tag('REAPPLIED_INSTRUMENT_ALERT')
            Tag('REDRAWN_EXPLICIT_INSTRUMENT_COLOR')
            Tag('REDRAWN_REAPPLIED_INSTRUMENT_COLOR')
            Tag('REDUNDANT_INSTRUMENT_ALERT')
            Tag('REDUNDANT_INSTRUMENT_COLOR')
            Tag('REDRAWN_REDUNDANT_INSTRUMENT_COLOR')
            Tag('DEFAULT_MARGIN_MARKUP_ALERT')
            Tag('DEFAULT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR')
            Tag('EXPLICIT_MARGIN_MARKUP_ALERT')
            Tag('EXPLICIT_MARGIN_MARKUP_COLOR')
            Tag('REAPPLIED_MARGIN_MARKUP_ALERT')
            Tag('REAPPLIED_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR')
            Tag('REDUNDANT_MARGIN_MARKUP_ALERT')
            Tag('REDUNDANT_MARGIN_MARKUP_COLOR')
            Tag('REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR')
            Tag('EXPLICIT_METRONOME_MARK_WITH_COLOR')
            Tag('REAPPLIED_METRONOME_MARK_WITH_COLOR')
            Tag('REDUNDANT_METRONOME_MARK_WITH_COLOR')
            Tag('EXPLICIT_STAFF_LINES_COLOR')
            Tag('REAPPLIED_STAFF_LINES_COLOR')
            Tag('REDUNDANT_STAFF_LINES_COLOR')
            Tag('REAPPLIED_STAFF_LINES')
            Tag('EXPLICIT_TIME_SIGNATURE_COLOR')
            Tag('REAPPLIED_TIME_SIGNATURE_COLOR')
            Tag('REDUNDANT_TIME_SIGNATURE_COLOR')
            Tag('REAPPLIED_TIME_SIGNATURE')

        """
        tags: typing.List[Tag] = []
        tags.extend(self.clef_color_tags(path))
        tags.extend(self.dynamic_color_tags(path))
        tags.extend(self.instrument_color_tags(path))
        tags.extend(self.margin_markup_color_tags(path))
        tags.extend(self.metronome_mark_color_expression_tags(path))
        tags.extend(self.staff_lines_color_tags(path))
        tags.extend(self.time_signature_color_tags(path))
        return tags

    def persistent_indicator_color_suppression_tags(
        self, path=None
    ) -> typing.List[Tag]:
        """
        Gets persistent indicator color suppression tags.

        ..  container:: example

            >>> tags = abjad.tags.persistent_indicator_color_suppression_tags()
            >>> for tag in tags:
            ...     tag
            ...
            Tag('EXPLICIT_METRONOME_MARK')
            Tag('REDUNDANT_METRONOME_MARK')

        ..  container:: example

            Segment:

            >>> path = abjad.Path('etude', 'segments', '_')
            >>> tags = abjad.tags.persistent_indicator_color_suppression_tags(path)
            >>> for tag in tags:
            ...     tag
            ...
            Tag('EXPLICIT_METRONOME_MARK')
            Tag('REDUNDANT_METRONOME_MARK')

        ..  container:: example

            Build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> tags = abjad.tags.persistent_indicator_color_suppression_tags(path)
            >>> for tag in tags:
            ...     tag
            ...
            Tag('EXPLICIT_METRONOME_MARK')
            Tag('REDUNDANT_METRONOME_MARK')

        """
        tags: typing.List[Tag] = []
        tags.extend(self.metronome_mark_color_suppression_tags())
        return tags

    def persistent_indicator_tags(self) -> typing.List[Tag]:
        """
        Gets persistence tags.

        ..  container:: example

            >>> for tag in abjad.tags.persistent_indicator_tags():
            ...     tag
            ...
            Tag('DEFAULT_CLEF')
            Tag('EXPLICIT_CLEF')
            Tag('REAPPLIED_CLEF')
            Tag('REDUNDANT_CLEF')
            Tag('EXPLICIT_DYNAMIC')
            Tag('REAPPLIED_DYNAMIC')
            Tag('REDUNDANT_DYNAMIC')
            Tag('DEFAULT_INSTRUMENT')
            Tag('EXPLICIT_INSTRUMENT')
            Tag('REAPPLIED_INSTRUMENT')
            Tag('REDUNDANT_INSTRUMENT')
            Tag('DEFAULT_MARGIN_MARKUP')
            Tag('EXPLICIT_MARGIN_MARKUP')
            Tag('REAPPLIED_MARGIN_MARKUP')
            Tag('REDUNDANT_MARGIN_MARKUP')
            Tag('EXPLICIT_METRONOME_MARK')
            Tag('REAPPLIED_METRONOME_MARK')
            Tag('REDUNDANT_METRONOME_MARK')
            Tag('EXPLICIT_PERSISTENT_OVERRIDE')
            Tag('REAPPLIED_PERSISTENT_OVERRIDE')
            Tag('REDUNDANT_PERSISTENT_OVERRIDE')
            Tag('EXPLICIT_STAFF_LINES')
            Tag('REAPPLIED_STAFF_LINES')
            Tag('REDUNDANT_STAFF_LINES')
            Tag('EXPLICIT_TIME_SIGNATURE')
            Tag('REAPPLIED_TIME_SIGNATURE')
            Tag('REDUNDANT_TIME_SIGNATURE')

        """
        return [
            self.DEFAULT_CLEF,
            self.EXPLICIT_CLEF,
            self.REAPPLIED_CLEF,
            self.REDUNDANT_CLEF,
            #
            self.EXPLICIT_DYNAMIC,
            self.REAPPLIED_DYNAMIC,
            self.REDUNDANT_DYNAMIC,
            #
            self.DEFAULT_INSTRUMENT,
            self.EXPLICIT_INSTRUMENT,
            self.REAPPLIED_INSTRUMENT,
            self.REDUNDANT_INSTRUMENT,
            #
            self.DEFAULT_MARGIN_MARKUP,
            self.EXPLICIT_MARGIN_MARKUP,
            self.REAPPLIED_MARGIN_MARKUP,
            self.REDUNDANT_MARGIN_MARKUP,
            #
            self.EXPLICIT_METRONOME_MARK,
            self.REAPPLIED_METRONOME_MARK,
            self.REDUNDANT_METRONOME_MARK,
            #
            self.EXPLICIT_PERSISTENT_OVERRIDE,
            self.REAPPLIED_PERSISTENT_OVERRIDE,
            self.REDUNDANT_PERSISTENT_OVERRIDE,
            #
            self.EXPLICIT_STAFF_LINES,
            self.REAPPLIED_STAFF_LINES,
            self.REDUNDANT_STAFF_LINES,
            #
            self.EXPLICIT_TIME_SIGNATURE,
            self.REAPPLIED_TIME_SIGNATURE,
            self.REDUNDANT_TIME_SIGNATURE,
            #
        ]

    def spacing_markup_tags(self) -> typing.List[Tag]:
        """
        Gets markup spacing tags.

        ..  container:: example

            >>> for tag in abjad.tags.spacing_markup_tags():
            ...     tag
            ...
            Tag('SPACING')
            Tag('SPACING_OVERRIDE')

        """
        return [self.SPACING, self.SPACING_OVERRIDE]

    def spacing_tags(self) -> typing.List[Tag]:
        """
        Gets spacing tags.

        ..  container:: example

            >>> for tag in abjad.tags.spacing_tags():
            ...     tag
            ...
            Tag('SPACING_COMMAND')
            Tag('SPACING')
            Tag('SPACING_OVERRIDE_COMMAND')
            Tag('SPACING_OVERRIDE')

        """
        return [
            self.SPACING_COMMAND,
            self.SPACING,
            self.SPACING_OVERRIDE_COMMAND,
            self.SPACING_OVERRIDE,
        ]

    def staff_lines_color_tags(self, path=None) -> typing.List[Tag]:
        """
        Gets staff lines color tags.

        ..  container:: example

            >>> for tag in abjad.tags.staff_lines_color_tags():
            ...     tag
            ...
            Tag('EXPLICIT_STAFF_LINES_COLOR')
            Tag('REAPPLIED_STAFF_LINES_COLOR')
            Tag('REDUNDANT_STAFF_LINES_COLOR')

        ..  container:: example

            Segment:

            >>> path = abjad.Path('etude', 'segments', '_')
            >>> for tag in abjad.tags.staff_lines_color_tags(path):
            ...     tag
            ...
            Tag('EXPLICIT_STAFF_LINES_COLOR')
            Tag('REAPPLIED_STAFF_LINES_COLOR')
            Tag('REDUNDANT_STAFF_LINES_COLOR')

        ..  container:: example

            Build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> for tag in abjad.tags.staff_lines_color_tags(path):
            ...     tag
            ...
            Tag('EXPLICIT_STAFF_LINES_COLOR')
            Tag('REAPPLIED_STAFF_LINES_COLOR')
            Tag('REDUNDANT_STAFF_LINES_COLOR')
            Tag('REAPPLIED_STAFF_LINES')

        """
        tags = [
            self.EXPLICIT_STAFF_LINES_COLOR,
            self.REAPPLIED_STAFF_LINES_COLOR,
            self.REDUNDANT_STAFF_LINES_COLOR,
        ]
        if path and not path.is_segment():
            tags.append(self.REAPPLIED_STAFF_LINES)
        return tags

    def time_signature_color_tags(self, path=None) -> typing.List[Tag]:
        """
        Gets time signature color tags.

        ..  container:: example

            >>> for tag in abjad.tags.time_signature_color_tags():
            ...     tag
            ...
            Tag('EXPLICIT_TIME_SIGNATURE_COLOR')
            Tag('REAPPLIED_TIME_SIGNATURE_COLOR')
            Tag('REDUNDANT_TIME_SIGNATURE_COLOR')

        ..  container:: example

            Segment:

            >>> path = abjad.Path('etude', 'segments', '_')
            >>> for tag in abjad.tags.time_signature_color_tags():
            ...     tag
            ...
            Tag('EXPLICIT_TIME_SIGNATURE_COLOR')
            Tag('REAPPLIED_TIME_SIGNATURE_COLOR')
            Tag('REDUNDANT_TIME_SIGNATURE_COLOR')

        ..  container:: example

            Build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> for tag in abjad.tags.time_signature_color_tags():
            ...     tag
            ...
            Tag('EXPLICIT_TIME_SIGNATURE_COLOR')
            Tag('REAPPLIED_TIME_SIGNATURE_COLOR')
            Tag('REDUNDANT_TIME_SIGNATURE_COLOR')

        """
        tags = [
            self.EXPLICIT_TIME_SIGNATURE_COLOR,
            self.REAPPLIED_TIME_SIGNATURE_COLOR,
            self.REDUNDANT_TIME_SIGNATURE_COLOR,
        ]
        if path and not path.is_segment():
            tags.append(self.REAPPLIED_TIME_SIGNATURE)
        return tags
