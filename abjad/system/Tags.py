import typing
from abjad.utilities.String import String
from .AbjadValueObject import AbjadValueObject


class Tags(AbjadValueObject):
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
        'SHOW_TO_JOIN_BROKEN_SPANNERS'

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _known_tags: tuple = (

        ### BROKEN SPANNERS ###

        'HIDE_TO_JOIN_BROKEN_SPANNERS',
        'SHOW_TO_JOIN_BROKEN_SPANNERS',
        'RIGHT_BROKEN_BEAM', # used in figure-maker

        ### CLEFS ###

        'DEFAULT_CLEF',
        'DEFAULT_CLEF_COLOR',
        'DEFAULT_CLEF_COLOR_CANCELLATION',
        'DEFAULT_CLEF_REDRAW_COLOR',

        'EXPLICIT_CLEF',
        'EXPLICIT_CLEF_COLOR',
        'EXPLICIT_CLEF_COLOR_CANCELLATION',
        'EXPLICIT_CLEF_REDRAW_COLOR',

        'REAPPLIED_CLEF',
        'REAPPLIED_CLEF_COLOR',
        'REAPPLIED_CLEF_COLOR_CANCELLATION',
        'REAPPLIED_CLEF_REDRAW_COLOR',

        'REDUNDANT_CLEF',
        'REDUNDANT_CLEF_COLOR',
        'REDUNDANT_CLEF_COLOR_CANCELLATION',
        'REDUNDANT_CLEF_REDRAW_COLOR',

        ### DOCUMENT COMMANDS ###

        'BREAK',
        'EMPTY_START_BAR',
        'EOL_FERMATA',
        'FERMATA_MEASURE',
        'SHIFTED_CLEF',
        'SPACING',
        'SPACING_OVERRIDE',
        'TWO_VOICE',

        ### DOCUMENT MARKUP ###

        'CLOCK_TIME_MARKUP',
        'FIGURE_NAME_MARKUP',
        'LOCAL_MEASURE_NUMBER_MARKUP',
        'MEASURE_INDEX_MARKUP',
        'MEASURE_NUMBER_MARKUP',
        'SPACING_MARKUP',
        'SPACING_OVERRIDE_MARKUP',
        'STAGE_NUMBER_MARKUP',

        ### DOCUMENT TYPES ###

        'BUILD',
        'FIRST_SEGMENT_DEFAULT',
        'PARTS',
        'SCORE',
        'SEGMENT',

        ### DYNAMICS ###

        'EXPLICIT_DYNAMIC',
        'EXPLICIT_DYNAMIC_COLOR',
        'EXPLICIT_DYNAMIC_COLOR_CANCELLATION',
        'EXPLICIT_DYNAMIC_REDRAW_COLOR',

        'REAPPLIED_DYNAMIC',
        'REAPPLIED_DYNAMIC_COLOR',
        'REAPPLIED_DYNAMIC_COLOR_CANCELLATION',
        'REAPPLIED_DYNAMIC_REDRAW_COLOR',

        'REDUNDANT_DYNAMIC',
        'REDUNDANT_DYNAMIC_COLOR',
        'REDUNDANT_DYNAMIC_COLOR_CANCELLATION',
        'REDUNDANT_DYNAMIC_REDRAW_COLOR',

        ### FIGURES ###

        'FORESHADOW',
        'INCOMPLETE',
        'RECOLLECTION',

        ### INSTRUMENTS ###

        'DEFAULT_INSTRUMENT',
        'DEFAULT_INSTRUMENT_ALERT',
        'DEFAULT_INSTRUMENT_COLOR',
        'REDRAWN_DEFAULT_INSTRUMENT',
        'REDRAWN_DEFAULT_INSTRUMENT_COLOR',

        'EXPLICIT_INSTRUMENT',
        'EXPLICIT_INSTRUMENT_ALERT',
        'EXPLICIT_INSTRUMENT_COLOR',
        'REDRAWN_EXPLICIT_INSTRUMENT',
        'REDRAWN_EXPLICIT_INSTRUMENT_COLOR',

        'REAPPLIED_INSTRUMENT',
        'REAPPLIED_INSTRUMENT_ALERT',
        'REAPPLIED_INSTRUMENT_COLOR',
        'REDRAWN_REAPPLIED_INSTRUMENT',
        'REDRAWN_REAPPLIED_INSTRUMENT_COLOR',

        'REDUNDANT_INSTRUMENT',
        'REDUNDANT_INSTRUMENT_ALERT',
        'REDUNDANT_INSTRUMENT_COLOR',
        'REDRAWN_REDUNDANT_INSTRUMENT',
        'REDRAWN_REDUNDANT_INSTRUMENT_COLOR',

        ### MARGIN MARKUP ###

        'DEFAULT_MARGIN_MARKUP',
        'DEFAULT_MARGIN_MARKUP_ALERT',
        'DEFAULT_MARGIN_MARKUP_COLOR',
        'REDRAWN_DEFAULT_MARGIN_MARKUP',
        'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR',

        'EXPLICIT_MARGIN_MARKUP',
        'EXPLICIT_MARGIN_MARKUP_ALERT',
        'EXPLICIT_MARGIN_MARKUP_COLOR',
        'REDRAWN_EXPLICIT_MARGIN_MARKUP',
        'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR',

        'REAPPLIED_MARGIN_MARKUP',
        'REAPPLIED_MARGIN_MARKUP_ALERT',
        'REAPPLIED_MARGIN_MARKUP_COLOR',
        'REDRAWN_REAPPLIED_MARGIN_MARKUP',
        'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR',

        'REDUNDANT_MARGIN_MARKUP',
        'REDUNDANT_MARGIN_MARKUP_ALERT',
        'REDUNDANT_MARGIN_MARKUP_COLOR',
        'REDRAWN_REDUNDANT_MARGIN_MARKUP',
        'REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR',

        ### METRONOME MARKS ###

        'EXPLICIT_METRONOME_MARK',
        'EXPLICIT_METRONOME_MARK_WITH_COLOR',

        'REAPPLIED_METRONOME_MARK',
        'REAPPLIED_METRONOME_MARK_WITH_COLOR',

        'REDUNDANT_METRONOME_MARK',
        'REDUNDANT_METRONOME_MARK_WITH_COLOR',

        ### PERSISTENT OVERRIDES ###

        'EXPLICIT_PERSISTENT_OVERRIDE',

        'REAPPLIED_PERSISTENT_OVERRIDE',

        'REDUNDANT_PERSISTENT_OVERRIDE',

        ### PITCH HANDLING ###

        'ALLOW_OCTAVE',
        'ALLOW_OUT_OF_RANGE',
        'ALLOW_REPEAT_PITCH',
        'DO_NOT_TRANSPOSE',
        'NOT_YET_PITCHED',
        'NOT_YET_REGISTERED',
        'STAFF_POSITION',

        ### SPACING SECTION ###

        'EXPLICIT_SPACING_SECTION',
        'EXPLICIT_SPACING_SECTION_COLOR',

        'REAPPLIED_SPACING_SECTION',
        'REAPPLIED_SPACING_SECTION_COLOR',

        'REDUNDANT_SPACING_SECTION',
        'REDUNDANT_SPACING_SECTION_COLOR',

        ### STAFF LINES ###

        'EXPLICIT_STAFF_LINES',
        'EXPLICIT_STAFF_LINES_COLOR',

        'REAPPLIED_STAFF_LINES',
        'REAPPLIED_STAFF_LINES_COLOR',

        'REDUNDANT_STAFF_LINES',
        'REDUNDANT_STAFF_LINES_COLOR',

        ### TIME SIGNATURES ###

        'EXPLICIT_TIME_SIGNATURE',
        'EXPLICIT_TIME_SIGNATURE_COLOR',

        'REAPPLIED_TIME_SIGNATURE',
        'REAPPLIED_TIME_SIGNATURE_COLOR',

        'REDUNDANT_TIME_SIGNATURE',
        'REDUNDANT_TIME_SIGNATURE_COLOR',

        ### ZZZ: OTHER ###

        'LEFT_BROKEN_REPEAT_TIE_TO',
        'PITCH',
        'REMOVE_ALL_EMPTY_STAVES',
        'REPEAT_TIE',
        'RHYTHM',
        'RIGHT_BROKEN_TIE_FROM',
        'SOUNDS_DURING_SEGMENT',
        'TEMPORARY_CONTAINER',
        'TIE_FROM',
        'TIE_TO',

    )

    ### SPECIAL METHODS ###

    def __getattr__(self, tag: str) -> str:
        """
        Gets ``tag``.

        Raises attribute error when ``tag`` is unknown.
        """
        if tag not in self._known_tags:
            raise AttributeError('unknown tag {!r}.'.format(tag))
        return tag

    ### PUBLIC METHODS ###

    def clef_color_tags(self, path=None) -> typing.List[str]:
        """
        Gets clef color tags.

        ..  container:: example

            >>> for tag in abjad.tags.clef_color_tags():
            ...     tag
            ...
            'DEFAULT_CLEF_COLOR'
            'DEFAULT_CLEF_REDRAW_COLOR'
            'EXPLICIT_CLEF_COLOR'
            'EXPLICIT_CLEF_REDRAW_COLOR'
            'REAPPLIED_CLEF_COLOR'
            'REAPPLIED_CLEF_REDRAW_COLOR'
            'REDUNDANT_CLEF_COLOR'
            'REDUNDANT_CLEF_REDRAW_COLOR'

        ..  container:: example

            Segment:

            >>> path = abjad.Path('etude', 'segments', '_')
            >>> for tag in abjad.tags.clef_color_tags(path=path):
            ...     tag
            ...
            'DEFAULT_CLEF_COLOR'
            'DEFAULT_CLEF_REDRAW_COLOR'
            'EXPLICIT_CLEF_COLOR'
            'EXPLICIT_CLEF_REDRAW_COLOR'
            'REAPPLIED_CLEF_COLOR'
            'REAPPLIED_CLEF_REDRAW_COLOR'
            'REDUNDANT_CLEF_COLOR'
            'REDUNDANT_CLEF_REDRAW_COLOR'

        ..  container:: example

            Build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> for tag in abjad.tags.clef_color_tags(path=path):
            ...     tag
            ...
            'DEFAULT_CLEF_COLOR'
            'DEFAULT_CLEF_REDRAW_COLOR'
            'EXPLICIT_CLEF_COLOR'
            'EXPLICIT_CLEF_REDRAW_COLOR'
            'REAPPLIED_CLEF_COLOR'
            'REAPPLIED_CLEF_REDRAW_COLOR'
            'REDUNDANT_CLEF_COLOR'
            'REDUNDANT_CLEF_REDRAW_COLOR'
            'REAPPLIED_CLEF'

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
        if path and not path.is_segment():
            tags.append(self.REAPPLIED_CLEF)
        return tags

    def documentation_removal_tags(self):
        """
        Gets documentation removal tags.

        ..  container:: example

            >>> for tag in abjad.tags.documentation_removal_tags():
            ...     tag
            ...
            'CLOCK_TIME_MARKUP'
            'FIGURE_NAME_MARKUP'
            'LOCAL_MEASURE_NUMBER_MARKUP'
            'MEASURE_INDEX_MARKUP'
            'MEASURE_NUMBER_MARKUP'
            'SPACING_MARKUP'
            'STAGE_NUMBER_MARKUP'

        """
        return [
            self.CLOCK_TIME_MARKUP,
            self.FIGURE_NAME_MARKUP,
            self.LOCAL_MEASURE_NUMBER_MARKUP,
            self.MEASURE_INDEX_MARKUP,
            self.MEASURE_NUMBER_MARKUP,
            self.SPACING_MARKUP,
            self.STAGE_NUMBER_MARKUP,
            ]

    def dynamic_color_tags(self, path=None) -> typing.List[str]:
        """
        Gets dynamic color tags.

        ..  container:: example

            >>> for tag in abjad.tags.dynamic_color_tags():
            ...     tag
            ...
            'EXPLICIT_DYNAMIC_COLOR'
            'EXPLICIT_DYNAMIC_REDRAW_COLOR'
            'REAPPLIED_DYNAMIC'
            'REAPPLIED_DYNAMIC_COLOR'
            'REAPPLIED_DYNAMIC_REDRAW_COLOR'
            'REDUNDANT_DYNAMIC_COLOR'
            'REDUNDANT_DYNAMIC_REDRAW_COLOR'

        Ignores ``path``.
        """
        return [
            self.EXPLICIT_DYNAMIC_COLOR,
            self.EXPLICIT_DYNAMIC_REDRAW_COLOR,
            self.REAPPLIED_DYNAMIC,
            self.REAPPLIED_DYNAMIC_COLOR,
            self.REAPPLIED_DYNAMIC_REDRAW_COLOR,
            self.REDUNDANT_DYNAMIC_COLOR,
            self.REDUNDANT_DYNAMIC_REDRAW_COLOR,
            ]

    def instrument_color_tags(self, path=None) -> typing.List[str]:
        """
        Gets instrument color tags.

        ..  container:: example

            >>> for tag in abjad.tags.instrument_color_tags():
            ...     tag
            ...
            'DEFAULT_INSTRUMENT_ALERT'
            'DEFAULT_INSTRUMENT_COLOR'
            'REDRAWN_DEFAULT_INSTRUMENT_COLOR'
            'EXPLICIT_INSTRUMENT_ALERT'
            'EXPLICIT_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_ALERT'
            'REDRAWN_EXPLICIT_INSTRUMENT_COLOR'
            'REDRAWN_REAPPLIED_INSTRUMENT_COLOR'
            'REDUNDANT_INSTRUMENT_ALERT'
            'REDUNDANT_INSTRUMENT_COLOR'
            'REDRAWN_REDUNDANT_INSTRUMENT_COLOR'

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

    def layout_removal_tags(self):
        """
        Gets layout removal tags.

        ..  container:: example

            >>> for tag in abjad.tags.layout_removal_tags():
            ...     tag
            ...
            'EMPTY_START_BAR'
            'EXPLICIT_TIME_SIGNATURE_COLOR'
            'LOCAL_MEASURE_NUMBER_MARKUP'
            'MEASURE_INDEX_MARKUP'
            'MEASURE_NUMBER_MARKUP'
            'REDUNDANT_TIME_SIGNATURE_COLOR'
            'STAGE_NUMBER_MARKUP'

        """
        return [
            self.EMPTY_START_BAR,
            self.EXPLICIT_TIME_SIGNATURE_COLOR,
            self.LOCAL_MEASURE_NUMBER_MARKUP,
            self.MEASURE_INDEX_MARKUP,
            self.MEASURE_NUMBER_MARKUP,
            self.REDUNDANT_TIME_SIGNATURE_COLOR,
            self.STAGE_NUMBER_MARKUP,
            ]

    def margin_markup_color_tags(self, path=None) -> typing.List[str]:
        """
        Gets margin markup color tags.

        ..  container:: example

            >>> for tag in abjad.tags.margin_markup_color_tags():
            ...     tag
            ...
            'DEFAULT_MARGIN_MARKUP_ALERT'
            'DEFAULT_MARGIN_MARKUP_COLOR'
            'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_MARGIN_MARKUP_ALERT'
            'EXPLICIT_MARGIN_MARKUP_COLOR'
            'REAPPLIED_MARGIN_MARKUP_ALERT'
            'REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDUNDANT_MARGIN_MARKUP_ALERT'
            'REDUNDANT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR'

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

    def metronome_mark_color_expression_tags(self, path=None) -> typing.List[str]:
        """
        Gets metronome mark color expression tags.

        ..  container:: example

            >>> for tag in abjad.tags.metronome_mark_color_expression_tags():
            ...     tag
            ...
            'EXPLICIT_METRONOME_MARK_WITH_COLOR'
            'REAPPLIED_METRONOME_MARK_WITH_COLOR'
            'REDUNDANT_METRONOME_MARK_WITH_COLOR'

        """
        return [
            self.EXPLICIT_METRONOME_MARK_WITH_COLOR,
            self.REAPPLIED_METRONOME_MARK_WITH_COLOR,
            self.REDUNDANT_METRONOME_MARK_WITH_COLOR,
            ]

    def metronome_mark_color_suppression_tags(self, path=None) -> typing.List[str]:
        """
        Gets metronome mark color suppression tags.

        ..  container:: example

            >>> for tag in abjad.tags.metronome_mark_color_suppression_tags():
            ...     tag
            ...
            'EXPLICIT_METRONOME_MARK'
            'REDUNDANT_METRONOME_MARK'

        Ignores ``path``.
        """
        return [
            self.EXPLICIT_METRONOME_MARK,
            self.REDUNDANT_METRONOME_MARK,
            ]

    def music_annotation_tags(self) -> typing.List[str]:
        """
        Gets music annotation tags.

        ..  container:: example

            >>> for tag in abjad.tags.music_annotation_tags():
            ...     tag
            ...
            'CLOCK_TIME_MARKUP'
            'FIGURE_NAME_MARKUP'
            'MEASURE_NUMBER_MARKUP'
            'SPACING_MARKUP'
            'SPACING_OVERRIDE_MARKUP'
            'STAGE_NUMBER_MARKUP'

        """
        return [
            self.CLOCK_TIME_MARKUP,
            self.FIGURE_NAME_MARKUP,
            self.MEASURE_NUMBER_MARKUP,
            self.SPACING_MARKUP,
            self.SPACING_OVERRIDE_MARKUP,
            self.STAGE_NUMBER_MARKUP,
            ]

    def persistent_indicator_color_expression_tags(
        self,
        path=None,
        ) -> typing.List[str]:
        """
        Gets persistent indicator color expression tags.

        ..  container:: example

            >>> tags = abjad.tags.persistent_indicator_color_expression_tags()
            >>> for tag in tags:
            ...     tag
            ...
            'DEFAULT_CLEF_COLOR'
            'DEFAULT_CLEF_REDRAW_COLOR'
            'EXPLICIT_CLEF_COLOR'
            'EXPLICIT_CLEF_REDRAW_COLOR'
            'REAPPLIED_CLEF_COLOR'
            'REAPPLIED_CLEF_REDRAW_COLOR'
            'REDUNDANT_CLEF_COLOR'
            'REDUNDANT_CLEF_REDRAW_COLOR'
            'EXPLICIT_DYNAMIC_COLOR'
            'EXPLICIT_DYNAMIC_REDRAW_COLOR'
            'REAPPLIED_DYNAMIC'
            'REAPPLIED_DYNAMIC_COLOR'
            'REAPPLIED_DYNAMIC_REDRAW_COLOR'
            'REDUNDANT_DYNAMIC_COLOR'
            'REDUNDANT_DYNAMIC_REDRAW_COLOR'
            'DEFAULT_INSTRUMENT_ALERT'
            'DEFAULT_INSTRUMENT_COLOR'
            'REDRAWN_DEFAULT_INSTRUMENT_COLOR'
            'EXPLICIT_INSTRUMENT_ALERT'
            'EXPLICIT_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_ALERT'
            'REDRAWN_EXPLICIT_INSTRUMENT_COLOR'
            'REDRAWN_REAPPLIED_INSTRUMENT_COLOR'
            'REDUNDANT_INSTRUMENT_ALERT'
            'REDUNDANT_INSTRUMENT_COLOR'
            'REDRAWN_REDUNDANT_INSTRUMENT_COLOR'
            'DEFAULT_MARGIN_MARKUP_ALERT'
            'DEFAULT_MARGIN_MARKUP_COLOR'
            'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_MARGIN_MARKUP_ALERT'
            'EXPLICIT_MARGIN_MARKUP_COLOR'
            'REAPPLIED_MARGIN_MARKUP_ALERT'
            'REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDUNDANT_MARGIN_MARKUP_ALERT'
            'REDUNDANT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_METRONOME_MARK_WITH_COLOR'
            'REAPPLIED_METRONOME_MARK_WITH_COLOR'
            'REDUNDANT_METRONOME_MARK_WITH_COLOR'
            'EXPLICIT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES_COLOR'
            'REDUNDANT_STAFF_LINES_COLOR'
            'EXPLICIT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE_COLOR'
            'REDUNDANT_TIME_SIGNATURE_COLOR'

        ..  container:: example

            Segment:

            >>> path = abjad.Path('etude', 'segments', '_')
            >>> tags = abjad.tags.persistent_indicator_color_expression_tags(path)
            >>> for tag in tags:
            ...     tag
            ...
            'DEFAULT_CLEF_COLOR'
            'DEFAULT_CLEF_REDRAW_COLOR'
            'EXPLICIT_CLEF_COLOR'
            'EXPLICIT_CLEF_REDRAW_COLOR'
            'REAPPLIED_CLEF_COLOR'
            'REAPPLIED_CLEF_REDRAW_COLOR'
            'REDUNDANT_CLEF_COLOR'
            'REDUNDANT_CLEF_REDRAW_COLOR'
            'EXPLICIT_DYNAMIC_COLOR'
            'EXPLICIT_DYNAMIC_REDRAW_COLOR'
            'REAPPLIED_DYNAMIC'
            'REAPPLIED_DYNAMIC_COLOR'
            'REAPPLIED_DYNAMIC_REDRAW_COLOR'
            'REDUNDANT_DYNAMIC_COLOR'
            'REDUNDANT_DYNAMIC_REDRAW_COLOR'
            'DEFAULT_INSTRUMENT_ALERT'
            'DEFAULT_INSTRUMENT_COLOR'
            'REDRAWN_DEFAULT_INSTRUMENT_COLOR'
            'EXPLICIT_INSTRUMENT_ALERT'
            'EXPLICIT_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_ALERT'
            'REDRAWN_EXPLICIT_INSTRUMENT_COLOR'
            'REDRAWN_REAPPLIED_INSTRUMENT_COLOR'
            'REDUNDANT_INSTRUMENT_ALERT'
            'REDUNDANT_INSTRUMENT_COLOR'
            'REDRAWN_REDUNDANT_INSTRUMENT_COLOR'
            'DEFAULT_MARGIN_MARKUP_ALERT'
            'DEFAULT_MARGIN_MARKUP_COLOR'
            'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_MARGIN_MARKUP_ALERT'
            'EXPLICIT_MARGIN_MARKUP_COLOR'
            'REAPPLIED_MARGIN_MARKUP_ALERT'
            'REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDUNDANT_MARGIN_MARKUP_ALERT'
            'REDUNDANT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_METRONOME_MARK_WITH_COLOR'
            'REAPPLIED_METRONOME_MARK_WITH_COLOR'
            'REDUNDANT_METRONOME_MARK_WITH_COLOR'
            'EXPLICIT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES_COLOR'
            'REDUNDANT_STAFF_LINES_COLOR'
            'EXPLICIT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE_COLOR'
            'REDUNDANT_TIME_SIGNATURE_COLOR'

        ..  container:: example

            Build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> tags = abjad.tags.persistent_indicator_color_expression_tags(path)
            >>> for tag in tags:
            ...     tag
            ...
            'DEFAULT_CLEF_COLOR'
            'DEFAULT_CLEF_REDRAW_COLOR'
            'EXPLICIT_CLEF_COLOR'
            'EXPLICIT_CLEF_REDRAW_COLOR'
            'REAPPLIED_CLEF_COLOR'
            'REAPPLIED_CLEF_REDRAW_COLOR'
            'REDUNDANT_CLEF_COLOR'
            'REDUNDANT_CLEF_REDRAW_COLOR'
            'REAPPLIED_CLEF'
            'EXPLICIT_DYNAMIC_COLOR'
            'EXPLICIT_DYNAMIC_REDRAW_COLOR'
            'REAPPLIED_DYNAMIC'
            'REAPPLIED_DYNAMIC_COLOR'
            'REAPPLIED_DYNAMIC_REDRAW_COLOR'
            'REDUNDANT_DYNAMIC_COLOR'
            'REDUNDANT_DYNAMIC_REDRAW_COLOR'
            'DEFAULT_INSTRUMENT_ALERT'
            'DEFAULT_INSTRUMENT_COLOR'
            'REDRAWN_DEFAULT_INSTRUMENT_COLOR'
            'EXPLICIT_INSTRUMENT_ALERT'
            'EXPLICIT_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_COLOR'
            'REAPPLIED_INSTRUMENT_ALERT'
            'REDRAWN_EXPLICIT_INSTRUMENT_COLOR'
            'REDRAWN_REAPPLIED_INSTRUMENT_COLOR'
            'REDUNDANT_INSTRUMENT_ALERT'
            'REDUNDANT_INSTRUMENT_COLOR'
            'REDRAWN_REDUNDANT_INSTRUMENT_COLOR'
            'DEFAULT_MARGIN_MARKUP_ALERT'
            'DEFAULT_MARGIN_MARKUP_COLOR'
            'REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_MARGIN_MARKUP_ALERT'
            'EXPLICIT_MARGIN_MARKUP_COLOR'
            'REAPPLIED_MARGIN_MARKUP_ALERT'
            'REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR'
            'REDUNDANT_MARGIN_MARKUP_ALERT'
            'REDUNDANT_MARGIN_MARKUP_COLOR'
            'REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR'
            'EXPLICIT_METRONOME_MARK_WITH_COLOR'
            'REAPPLIED_METRONOME_MARK_WITH_COLOR'
            'REDUNDANT_METRONOME_MARK_WITH_COLOR'
            'EXPLICIT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES_COLOR'
            'REDUNDANT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES'
            'EXPLICIT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE_COLOR'
            'REDUNDANT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE'

        """
        tags: typing.List[str] = []
        tags.extend(self.clef_color_tags(path))
        tags.extend(self.dynamic_color_tags(path))
        tags.extend(self.instrument_color_tags(path))
        tags.extend(self.margin_markup_color_tags(path))
        tags.extend(self.metronome_mark_color_expression_tags(path))
        tags.extend(self.staff_lines_color_tags(path))
        tags.extend(self.time_signature_color_tags(path))
        return tags

    def persistent_indicator_color_suppression_tags(
        self,
        path=None,
        ) -> typing.List[str]:
        """
        Gets persistent indicator color suppression tags.

        ..  container:: example

            >>> tags = abjad.tags.persistent_indicator_color_suppression_tags()
            >>> for tag in tags:
            ...     tag
            ...
            'EXPLICIT_METRONOME_MARK'
            'REDUNDANT_METRONOME_MARK'

        ..  container:: example

            Segment:

            >>> path = abjad.Path('etude', 'segments', '_')
            >>> tags = abjad.tags.persistent_indicator_color_suppression_tags(path)
            >>> for tag in tags:
            ...     tag
            ...
            'EXPLICIT_METRONOME_MARK'
            'REDUNDANT_METRONOME_MARK'

        ..  container:: example

            Build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> tags = abjad.tags.persistent_indicator_color_suppression_tags(path)
            >>> for tag in tags:
            ...     tag
            ...
            'EXPLICIT_METRONOME_MARK'
            'REDUNDANT_METRONOME_MARK'

        """
        tags: typing.List[str] = []
        tags.extend(self.metronome_mark_color_suppression_tags())
        return tags

    def persistent_indicator_tags(self) -> typing.List[str]:
        """
        Gets persistence tags.

        ..  container:: example

            >>> for string in abjad.tags.persistent_indicator_tags():
            ...     string
            ...
            'DEFAULT_CLEF'
            'EXPLICIT_CLEF'
            'REAPPLIED_CLEF'
            'REDUNDANT_CLEF'
            'EXPLICIT_DYNAMIC'
            'REAPPLIED_DYNAMIC'
            'REDUNDANT_DYNAMIC'
            'DEFAULT_INSTRUMENT'
            'EXPLICIT_INSTRUMENT'
            'REAPPLIED_INSTRUMENT'
            'REDUNDANT_INSTRUMENT'
            'DEFAULT_MARGIN_MARKUP'
            'EXPLICIT_MARGIN_MARKUP'
            'REAPPLIED_MARGIN_MARKUP'
            'REDUNDANT_MARGIN_MARKUP'
            'EXPLICIT_METRONOME_MARK'
            'REAPPLIED_METRONOME_MARK'
            'REDUNDANT_METRONOME_MARK'
            'EXPLICIT_PERSISTENT_OVERRIDE'
            'REAPPLIED_PERSISTENT_OVERRIDE'
            'REDUNDANT_PERSISTENT_OVERRIDE'
            'EXPLICIT_STAFF_LINES'
            'REAPPLIED_STAFF_LINES'
            'REDUNDANT_STAFF_LINES'
            'EXPLICIT_TIME_SIGNATURE'
            'REAPPLIED_TIME_SIGNATURE'
            'REDUNDANT_TIME_SIGNATURE'

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

    def spacing_markup_tags(self) -> typing.List[str]:
        """
        Gets markup spacing tags.

        ..  container:: example

            >>> for tag in abjad.tags.spacing_markup_tags():
            ...     tag
            ...
            'SPACING_MARKUP'
            'SPACING_OVERRIDE_MARKUP'

        """
        return [
            self.SPACING_MARKUP,
            self.SPACING_OVERRIDE_MARKUP,
            ]

    def spacing_tags(self) -> typing.List[str]:
        """
        Gets spacing tags.

        ..  container:: example

            >>> for tag in abjad.tags.spacing_tags():
            ...     tag
            ...
            'SPACING'
            'SPACING_MARKUP'
            'SPACING_OVERRIDE'
            'SPACING_OVERRIDE_MARKUP'

        """
        return [
            self.SPACING,
            self.SPACING_MARKUP,
            self.SPACING_OVERRIDE,
            self.SPACING_OVERRIDE_MARKUP,
            ]

    def staff_lines_color_tags(self, path=None) -> typing.List[str]:
        """
        Gets staff lines color tags.

        ..  container:: example

            >>> for tag in abjad.tags.staff_lines_color_tags():
            ...     tag
            ...
            'EXPLICIT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES_COLOR'
            'REDUNDANT_STAFF_LINES_COLOR'

        ..  container:: example

            Segment:

            >>> path = abjad.Path('etude', 'segments', '_')
            >>> for tag in abjad.tags.staff_lines_color_tags(path):
            ...     tag
            ...
            'EXPLICIT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES_COLOR'
            'REDUNDANT_STAFF_LINES_COLOR'

        ..  container:: example

            Build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> for tag in abjad.tags.staff_lines_color_tags(path):
            ...     tag
            ...
            'EXPLICIT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES_COLOR'
            'REDUNDANT_STAFF_LINES_COLOR'
            'REAPPLIED_STAFF_LINES'

        """
        tags = [
            self.EXPLICIT_STAFF_LINES_COLOR,
            self.REAPPLIED_STAFF_LINES_COLOR,
            self.REDUNDANT_STAFF_LINES_COLOR,
            ]
        if path and not path.is_segment():
            tags.append(self.REAPPLIED_STAFF_LINES)
        return tags

    def time_signature_color_tags(self, path=None) -> typing.List[str]:
        """
        Gets time signature color tags.

        ..  container:: example

            >>> for tag in abjad.tags.time_signature_color_tags():
            ...     tag
            ...
            'EXPLICIT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE_COLOR'
            'REDUNDANT_TIME_SIGNATURE_COLOR'

        ..  container:: example

            Segment:

            >>> path = abjad.Path('etude', 'segments', '_')
            >>> for tag in abjad.tags.time_signature_color_tags():
            ...     tag
            ...
            'EXPLICIT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE_COLOR'
            'REDUNDANT_TIME_SIGNATURE_COLOR'

        ..  container:: example

            Build:

            >>> path = abjad.Path('etude', 'builds', 'letter-score')
            >>> for tag in abjad.tags.time_signature_color_tags():
            ...     tag
            ...
            'EXPLICIT_TIME_SIGNATURE_COLOR'
            'REAPPLIED_TIME_SIGNATURE_COLOR'
            'REDUNDANT_TIME_SIGNATURE_COLOR'

        """
        tags = [
            self.EXPLICIT_TIME_SIGNATURE_COLOR,
            self.REAPPLIED_TIME_SIGNATURE_COLOR,
            self.REDUNDANT_TIME_SIGNATURE_COLOR,
            ]
        if path and not path.is_segment():
            tags.append(self.REAPPLIED_TIME_SIGNATURE)
        return tags
