"""
Tags.

..  container:: example

    >>> abjad.tags.SHOW_TO_JOIN_BROKEN_SPANNERS
    Tag('SHOW_TO_JOIN_BROKEN_SPANNERS')

"""
import typing

from .tag import Tag

### BAR EXTENT ###

EXPLICIT_BAR_EXTENT = Tag("EXPLICIT_BAR_EXTENT")
REAPPLIED_BAR_EXTENT = Tag("REAPPLIED_BAR_EXTENT")
REDUNDANT_BAR_EXTENT = Tag("REDUNDANT_BAR_EXTENT")

### CLEF ###

DEFAULT_CLEF = Tag("DEFAULT_CLEF")
DEFAULT_CLEF_COLOR = Tag("DEFAULT_CLEF_COLOR")
DEFAULT_CLEF_COLOR_CANCELLATION = Tag("DEFAULT_CLEF_COLOR_CANCELLATION")
DEFAULT_CLEF_REDRAW_COLOR = Tag("DEFAULT_CLEF_REDRAW_COLOR")
EXPLICIT_CLEF = Tag("EXPLICIT_CLEF")
EXPLICIT_CLEF_COLOR = Tag("EXPLICIT_CLEF_COLOR")
EXPLICIT_CLEF_COLOR_CANCELLATION = Tag("EXPLICIT_CLEF_COLOR_CANCELLATION")
EXPLICIT_CLEF_REDRAW_COLOR = Tag("EXPLICIT_CLEF_REDRAW_COLOR")
REAPPLIED_CLEF = Tag("REAPPLIED_CLEF")
REAPPLIED_CLEF_COLOR = Tag("REAPPLIED_CLEF_COLOR")
REAPPLIED_CLEF_COLOR_CANCELLATION = Tag("REAPPLIED_CLEF_COLOR_CANCELLATION")
REAPPLIED_CLEF_REDRAW_COLOR = Tag("REAPPLIED_CLEF_REDRAW_COLOR")
REDUNDANT_CLEF = Tag("REDUNDANT_CLEF")
REDUNDANT_CLEF_COLOR = Tag("REDUNDANT_CLEF_COLOR")
REDUNDANT_CLEF_COLOR_CANCELLATION = Tag("REDUNDANT_CLEF_COLOR_CANCELLATION")
REDUNDANT_CLEF_REDRAW_COLOR = Tag("REDUNDANT_CLEF_REDRAW_COLOR")

### COMMANDS IMPORTANT ###

ONE_VOICE_COMMAND = Tag("ONE_VOICE_COMMAND")

### DOCUMENT ANNOTATIONS ###

BREAK = Tag("BREAK")
CLOCK_TIME = Tag("CLOCK_TIME")
EMPTY_START_BAR = Tag("EMPTY_START_BAR")
FERMATA_MEASURE = Tag("FERMATA_MEASURE")
FIGURE_NAME = Tag("FIGURE_NAME")
HIDDEN = Tag("HIDDEN")
HIDE_IN_PARTS = Tag("HIDE_IN_PARTS")
INVISIBLE_MUSIC_COLORING = Tag("INVISIBLE_MUSIC_COLORING")
INVISIBLE_MUSIC_COMMAND = Tag("INVISIBLE_MUSIC_COMMAND")
LOCAL_MEASURE_NUMBER = Tag("LOCAL_MEASURE_NUMBER")
MEASURE_NUMBER = Tag("MEASURE_NUMBER")
MULTIMEASURE_REST = Tag("MULTIMEASURE_REST")
NOT_MOL = Tag("NOT_MOL")
NOTE = Tag("NOTE")
ONLY_MOL = Tag("ONLY_MOL")
PHANTOM = Tag("PHANTOM")
REST_VOICE = Tag("REST_VOICE")
SHIFTED_CLEF = Tag("SHIFTED_CLEF")
SHOW_IN_PARTS = Tag("SHOW_IN_PARTS")
SKIP = Tag("SKIP")
SPACING = Tag("SPACING")
SPACING_OVERRIDE = Tag("SPACING_OVERRIDE")
SPACING_COMMAND = Tag("SPACING_COMMAND")
SPACING_OVERRIDE_COMMAND = Tag("SPACING_OVERRIDE_COMMAND")
STAGE_NUMBER = Tag("STAGE_NUMBER")

### DOCUMENT TYPES ###

BUILD = Tag("BUILD")
FIRST_SEGMENT_DEFAULT = Tag("FIRST_SEGMENT_DEFAULT")
PARTS = Tag("PARTS")
SCORE = Tag("SCORE")
SEGMENT = Tag("SEGMENT")

### DYNAMIC ###

EXPLICIT_DYNAMIC = Tag("EXPLICIT_DYNAMIC")
EXPLICIT_DYNAMIC_COLOR = Tag("EXPLICIT_DYNAMIC_COLOR")
REAPPLIED_DYNAMIC = Tag("REAPPLIED_DYNAMIC")
REAPPLIED_DYNAMIC_COLOR = Tag("REAPPLIED_DYNAMIC_COLOR")
REDUNDANT_DYNAMIC = Tag("REDUNDANT_DYNAMIC")
REDUNDANT_DYNAMIC_COLOR = Tag("REDUNDANT_DYNAMIC_COLOR")

### FIGURES ###

FORESHADOW = Tag("FORESHADOW")
INCOMPLETE = Tag("INCOMPLETE")
RECOLLECTION = Tag("RECOLLECTION")

### INSTRUMENT ###

DEFAULT_INSTRUMENT = Tag("DEFAULT_INSTRUMENT")
DEFAULT_INSTRUMENT_ALERT = Tag("DEFAULT_INSTRUMENT_ALERT")
DEFAULT_INSTRUMENT_COLOR = Tag("DEFAULT_INSTRUMENT_COLOR")
REDRAWN_DEFAULT_INSTRUMENT = Tag("REDRAWN_DEFAULT_INSTRUMENT")
REDRAWN_DEFAULT_INSTRUMENT_COLOR = Tag("REDRAWN_DEFAULT_INSTRUMENT_COLOR")
EXPLICIT_INSTRUMENT = Tag("EXPLICIT_INSTRUMENT")
EXPLICIT_INSTRUMENT_ALERT = Tag("EXPLICIT_INSTRUMENT_ALERT")
EXPLICIT_INSTRUMENT_COLOR = Tag("EXPLICIT_INSTRUMENT_COLOR")
REDRAWN_EXPLICIT_INSTRUMENT = Tag("REDRAWN_EXPLICIT_INSTRUMENT")
REDRAWN_EXPLICIT_INSTRUMENT_COLOR = Tag("REDRAWN_EXPLICIT_INSTRUMENT_COLOR")
REAPPLIED_INSTRUMENT = Tag("REAPPLIED_INSTRUMENT")
REAPPLIED_INSTRUMENT_ALERT = Tag("REAPPLIED_INSTRUMENT_ALERT")
REAPPLIED_INSTRUMENT_COLOR = Tag("REAPPLIED_INSTRUMENT_COLOR")
REDRAWN_REAPPLIED_INSTRUMENT = Tag("REDRAWN_REAPPLIED_INSTRUMENT")
REDRAWN_REAPPLIED_INSTRUMENT_COLOR = Tag("REDRAWN_REAPPLIED_INSTRUMENT_COLOR")
REDUNDANT_INSTRUMENT = Tag("REDUNDANT_INSTRUMENT")
REDUNDANT_INSTRUMENT_ALERT = Tag("REDUNDANT_INSTRUMENT_ALERT")
REDUNDANT_INSTRUMENT_COLOR = Tag("REDUNDANT_INSTRUMENT_COLOR")
REDRAWN_REDUNDANT_INSTRUMENT = Tag("REDRAWN_REDUNDANT_INSTRUMENT")
REDRAWN_REDUNDANT_INSTRUMENT_COLOR = Tag("REDRAWN_REDUNDANT_INSTRUMENT_COLOR")

### MARGIN MARKUP ###

DEFAULT_MARGIN_MARKUP = Tag("DEFAULT_MARGIN_MARKUP")
DEFAULT_MARGIN_MARKUP_ALERT = Tag("DEFAULT_MARGIN_MARKUP_ALERT")
DEFAULT_MARGIN_MARKUP_COLOR = Tag("DEFAULT_MARGIN_MARKUP_COLOR")
REDRAWN_DEFAULT_MARGIN_MARKUP = Tag("REDRAWN_DEFAULT_MARGIN_MARKUP")
REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR = Tag("REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR")
EXPLICIT_MARGIN_MARKUP = Tag("EXPLICIT_MARGIN_MARKUP")
EXPLICIT_MARGIN_MARKUP_ALERT = Tag("EXPLICIT_MARGIN_MARKUP_ALERT")
EXPLICIT_MARGIN_MARKUP_COLOR = Tag("EXPLICIT_MARGIN_MARKUP_COLOR")
REDRAWN_EXPLICIT_MARGIN_MARKUP = Tag("REDRAWN_EXPLICIT_MARGIN_MARKUP")
REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR = Tag("REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR")
REAPPLIED_MARGIN_MARKUP = Tag("REAPPLIED_MARGIN_MARKUP")
REAPPLIED_MARGIN_MARKUP_ALERT = Tag("REAPPLIED_MARGIN_MARKUP_ALERT")
REAPPLIED_MARGIN_MARKUP_COLOR = Tag("REAPPLIED_MARGIN_MARKUP_COLOR")
REDRAWN_REAPPLIED_MARGIN_MARKUP = Tag("REDRAWN_REAPPLIED_MARGIN_MARKUP")
REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR = Tag("REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR")
REDUNDANT_MARGIN_MARKUP = Tag("REDUNDANT_MARGIN_MARKUP")
REDUNDANT_MARGIN_MARKUP_ALERT = Tag("REDUNDANT_MARGIN_MARKUP_ALERT")
REDUNDANT_MARGIN_MARKUP_COLOR = Tag("REDUNDANT_MARGIN_MARKUP_COLOR")
REDRAWN_REDUNDANT_MARGIN_MARKUP = Tag("REDRAWN_REDUNDANT_MARGIN_MARKUP")
REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR = Tag("REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR")

### METRONOME MARK ###

EXPLICIT_METRONOME_MARK = Tag("EXPLICIT_METRONOME_MARK")
EXPLICIT_METRONOME_MARK_WITH_COLOR = Tag("EXPLICIT_METRONOME_MARK_WITH_COLOR")
REAPPLIED_METRONOME_MARK = Tag("REAPPLIED_METRONOME_MARK")
REAPPLIED_METRONOME_MARK_WITH_COLOR = Tag("REAPPLIED_METRONOME_MARK_WITH_COLOR")
REDUNDANT_METRONOME_MARK = Tag("REDUNDANT_METRONOME_MARK")
REDUNDANT_METRONOME_MARK_WITH_COLOR = Tag("REDUNDANT_METRONOME_MARK_WITH_COLOR")

### METRONOME MARK SPANNER ###

METRIC_MODULATION_IS_NOT_SCALED = Tag("METRIC_MODULATION_IS_NOT_SCALED")
METRIC_MODULATION_IS_SCALED = Tag("METRIC_MODULATION_IS_SCALED")
METRIC_MODULATION_IS_STRIPPED = Tag("METRIC_MODULATION_IS_STRIPPED")

### PERSISTENT OVERRIDE ###

EXPLICIT_PERSISTENT_OVERRIDE = Tag("EXPLICIT_PERSISTENT_OVERRIDE")
REAPPLIED_PERSISTENT_OVERRIDE = Tag("REAPPLIED_PERSISTENT_OVERRIDE")
REDUNDANT_PERSISTENT_OVERRIDE = Tag("REDUNDANT_PERSISTENT_OVERRIDE")

### PITCH COLORINGS ###

MOCK_COLORING = Tag("MOCK_COLORING")
NOT_YET_PITCHED_COLORING = Tag("NOT_YET_PITCHED_COLORING")
NOT_YET_REGISTERED_COLORING = Tag("NOT_YET_REGISTERED_COLORING")
OCTAVE_COLORING = Tag("OCTAVE_COLORING")
OUT_OF_RANGE_COLORING = Tag("OUT_OF_RANGE_COLORING")
REPEAT_PITCH_CLASS_COLORING = Tag("REPEAT_PITCH_CLASS_COLORING")
TACET_COLORING = Tag("TACET_COLORING")

### RHYTHM ###

DURATION_MULTIPLIER = Tag("DURATION_MULTIPLIER")

### SPACING SECTION ###

EXPLICIT_SPACING_SECTION = Tag("EXPLICIT_SPACING_SECTION")
EXPLICIT_SPACING_SECTION_COLOR = Tag("EXPLICIT_SPACING_SECTION_COLOR")
REAPPLIED_SPACING_SECTION = Tag("REAPPLIED_SPACING_SECTION")
REAPPLIED_SPACING_SECTION_COLOR = Tag("REAPPLIED_SPACING_SECTION_COLOR")
REDUNDANT_SPACING_SECTION = Tag("REDUNDANT_SPACING_SECTION")
REDUNDANT_SPACING_SECTION_COLOR = Tag("REDUNDANT_SPACING_SECTION_COLOR")

### SPANNERS BROKEN ###

AUTODETECT = Tag("AUTODETECT")
HIDE_TO_JOIN_BROKEN_SPANNERS = Tag("HIDE_TO_JOIN_BROKEN_SPANNERS")
LEFT_BROKEN = Tag("LEFT_BROKEN")
RIGHT_BROKEN = Tag("RIGHT_BROKEN")
RIGHT_BROKEN_BEAM = Tag("RIGHT_BROKEN_BEAM")  # used in figure-maker
RIGHT_BROKEN_SHOW_NEXT = Tag("RIGHT_BROKEN_SHOW_NEXT")
SHOW_TO_JOIN_BROKEN_SPANNERS = Tag("SHOW_TO_JOIN_BROKEN_SPANNERS")

### SPANNERS CUSTOM ###

BOW_SPEED_SPANNER = Tag("BOW_SPEED_SPANNER")
CIRCLE_BOW_SPANNER = Tag("CIRCLE_BOW_SPANNER")
CLB_SPANNER = Tag("CLB_SPANNER")
COVERED_SPANNER = Tag("COVERED_SPANNER")
DAMP_SPANNER = Tag("DAMP_SPANNER")
EOS_STOP_MM_SPANNER = Tag("EOS_STOP_MM_SPANNER")
HALF_CLT_SPANNER = Tag("HALF_CLT_SPANNER")
MATERIAL_ANNOTATION_SPANNER = Tag("MATERIAL_ANNOTATION_SPANNER")
METRIC_MODULATION_SPANNER = Tag("METRIC_MODULATION_SPANNER")
PITCH_ANNOTATION_SPANNER = Tag("PITCH_ANNOTATION_SPANNER")
PIZZICATO_SPANNER = Tag("PIZZICATO_SPANNER")
RHYTHM_ANNOTATION_SPANNER = Tag("RHYTHM_ANNOTATION_SPANNER")
SCP_SPANNER = Tag("SCP_SPANNER")
SPAZZOLATO_SPANNER = Tag("SPAZZOLATO_SPANNER")
STRING_NUMBER_SPANNER = Tag("STRING_NUMBER_SPANNER")
TASTO_SPANNER = Tag("TASTO_SPANNER")
VIBRATO_SPANNER = Tag("VIBRATO_SPANNER")

### SPANNERS OTHER ###

SPANNER_START = Tag("SPANNER_START")
SPANNER_STOP = Tag("SPANNER_STOP")

### STAFF LINES ###

EXPLICIT_STAFF_LINES = Tag("EXPLICIT_STAFF_LINES")
EXPLICIT_STAFF_LINES_COLOR = Tag("EXPLICIT_STAFF_LINES_COLOR")
REAPPLIED_STAFF_LINES = Tag("REAPPLIED_STAFF_LINES")
REAPPLIED_STAFF_LINES_COLOR = Tag("REAPPLIED_STAFF_LINES_COLOR")
REDUNDANT_STAFF_LINES = Tag("REDUNDANT_STAFF_LINES")
REDUNDANT_STAFF_LINES_COLOR = Tag("REDUNDANT_STAFF_LINES_COLOR")

### TIME SIGNATURE ###

EXPLICIT_TIME_SIGNATURE = Tag("EXPLICIT_TIME_SIGNATURE")
EXPLICIT_TIME_SIGNATURE_COLOR = Tag("EXPLICIT_TIME_SIGNATURE_COLOR")
REAPPLIED_TIME_SIGNATURE = Tag("REAPPLIED_TIME_SIGNATURE")
REAPPLIED_TIME_SIGNATURE_COLOR = Tag("REAPPLIED_TIME_SIGNATURE_COLOR")
REDUNDANT_TIME_SIGNATURE = Tag("REDUNDANT_TIME_SIGNATURE")
REDUNDANT_TIME_SIGNATURE_COLOR = Tag("REDUNDANT_TIME_SIGNATURE_COLOR")

NOT_PARTS = Tag("-PARTS")

NOT_SCORE = Tag("-SCORE")

NOT_SEGMENT = Tag("-SEGMENT")

ONLY_PARTS = Tag("+PARTS")

ONLY_SCORE = Tag("+SCORE")

ONLY_SEGMENT = Tag("+SEGMENT")


def annotation_spanner_tags() -> typing.List[Tag]:
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
        MATERIAL_ANNOTATION_SPANNER,
        PITCH_ANNOTATION_SPANNER,
        RHYTHM_ANNOTATION_SPANNER,
    ]


def clef_color_tags(path=None) -> typing.List[Tag]:
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
        DEFAULT_CLEF_COLOR,
        DEFAULT_CLEF_REDRAW_COLOR,
        EXPLICIT_CLEF_COLOR,
        EXPLICIT_CLEF_REDRAW_COLOR,
        REAPPLIED_CLEF_COLOR,
        REAPPLIED_CLEF_REDRAW_COLOR,
        REDUNDANT_CLEF_COLOR,
        REDUNDANT_CLEF_REDRAW_COLOR,
    ]
    if path and not path.is_segment() and not path.is_segments():
        tags.append(REAPPLIED_CLEF)
    return tags


def documentation_removal_tags() -> typing.List[Tag]:
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
        CLOCK_TIME,
        FIGURE_NAME,
        LOCAL_MEASURE_NUMBER,
        MEASURE_NUMBER,
        SPACING,
        STAGE_NUMBER,
    ]


def dynamic_color_tags(path=None) -> typing.List[Tag]:
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
        EXPLICIT_DYNAMIC_COLOR,
        REAPPLIED_DYNAMIC,
        REAPPLIED_DYNAMIC_COLOR,
        REDUNDANT_DYNAMIC_COLOR,
    ]


def instrument_color_tags(path=None) -> typing.List[Tag]:
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
        DEFAULT_INSTRUMENT_ALERT,
        DEFAULT_INSTRUMENT_COLOR,
        REDRAWN_DEFAULT_INSTRUMENT_COLOR,
        EXPLICIT_INSTRUMENT_ALERT,
        EXPLICIT_INSTRUMENT_COLOR,
        REAPPLIED_INSTRUMENT_COLOR,
        REAPPLIED_INSTRUMENT_ALERT,
        REDRAWN_EXPLICIT_INSTRUMENT_COLOR,
        REDRAWN_REAPPLIED_INSTRUMENT_COLOR,
        REDUNDANT_INSTRUMENT_ALERT,
        REDUNDANT_INSTRUMENT_COLOR,
        REDRAWN_REDUNDANT_INSTRUMENT_COLOR,
    ]


def layout_removal_tags() -> typing.List[Tag]:
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
        EMPTY_START_BAR,
        EXPLICIT_TIME_SIGNATURE_COLOR,
        LOCAL_MEASURE_NUMBER,
        MEASURE_NUMBER,
        REDUNDANT_TIME_SIGNATURE_COLOR,
        STAGE_NUMBER,
    ]


def margin_markup_color_tags(path=None) -> typing.List[Tag]:
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
        DEFAULT_MARGIN_MARKUP_ALERT,
        DEFAULT_MARGIN_MARKUP_COLOR,
        REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR,
        EXPLICIT_MARGIN_MARKUP_ALERT,
        EXPLICIT_MARGIN_MARKUP_COLOR,
        REAPPLIED_MARGIN_MARKUP_ALERT,
        REAPPLIED_MARGIN_MARKUP_COLOR,
        REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR,
        REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR,
        REDUNDANT_MARGIN_MARKUP_ALERT,
        REDUNDANT_MARGIN_MARKUP_COLOR,
        REDRAWN_REDUNDANT_MARGIN_MARKUP_COLOR,
    ]


def metronome_mark_color_expression_tags(path=None) -> typing.List[Tag]:
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
        EXPLICIT_METRONOME_MARK_WITH_COLOR,
        REAPPLIED_METRONOME_MARK_WITH_COLOR,
        REDUNDANT_METRONOME_MARK_WITH_COLOR,
    ]


def metronome_mark_color_suppression_tags(path=None) -> typing.List[Tag]:
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
    return [EXPLICIT_METRONOME_MARK, REDUNDANT_METRONOME_MARK]


def music_annotation_tags() -> typing.List[Tag]:
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
        CLOCK_TIME,
        FIGURE_NAME,
        INVISIBLE_MUSIC_COLORING,
        LOCAL_MEASURE_NUMBER,
        MATERIAL_ANNOTATION_SPANNER,
        MOCK_COLORING,
        NOT_YET_PITCHED_COLORING,
        OCTAVE_COLORING,
        PITCH_ANNOTATION_SPANNER,
        REPEAT_PITCH_CLASS_COLORING,
        RHYTHM_ANNOTATION_SPANNER,
        SPACING,
        SPACING_OVERRIDE,
        STAGE_NUMBER,
        TACET_COLORING,
    ]


def persistent_indicator_color_expression_tags(path=None) -> typing.List[Tag]:
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
    tags.extend(clef_color_tags(path))
    tags.extend(dynamic_color_tags(path))
    tags.extend(instrument_color_tags(path))
    tags.extend(margin_markup_color_tags(path))
    tags.extend(metronome_mark_color_expression_tags(path))
    tags.extend(staff_lines_color_tags(path))
    tags.extend(time_signature_color_tags(path))
    return tags


def persistent_indicator_color_suppression_tags(path=None) -> typing.List[Tag]:
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
    tags.extend(metronome_mark_color_suppression_tags())
    return tags


def persistent_indicator_tags() -> typing.List[Tag]:
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
        DEFAULT_CLEF,
        EXPLICIT_CLEF,
        REAPPLIED_CLEF,
        REDUNDANT_CLEF,
        #
        EXPLICIT_DYNAMIC,
        REAPPLIED_DYNAMIC,
        REDUNDANT_DYNAMIC,
        #
        DEFAULT_INSTRUMENT,
        EXPLICIT_INSTRUMENT,
        REAPPLIED_INSTRUMENT,
        REDUNDANT_INSTRUMENT,
        #
        DEFAULT_MARGIN_MARKUP,
        EXPLICIT_MARGIN_MARKUP,
        REAPPLIED_MARGIN_MARKUP,
        REDUNDANT_MARGIN_MARKUP,
        #
        EXPLICIT_METRONOME_MARK,
        REAPPLIED_METRONOME_MARK,
        REDUNDANT_METRONOME_MARK,
        #
        EXPLICIT_PERSISTENT_OVERRIDE,
        REAPPLIED_PERSISTENT_OVERRIDE,
        REDUNDANT_PERSISTENT_OVERRIDE,
        #
        EXPLICIT_STAFF_LINES,
        REAPPLIED_STAFF_LINES,
        REDUNDANT_STAFF_LINES,
        #
        EXPLICIT_TIME_SIGNATURE,
        REAPPLIED_TIME_SIGNATURE,
        REDUNDANT_TIME_SIGNATURE,
        #
    ]


def spacing_markup_tags() -> typing.List[Tag]:
    """
    Gets markup spacing tags.

    ..  container:: example

        >>> for tag in abjad.tags.spacing_markup_tags():
        ...     tag
        ...
        Tag('SPACING')
        Tag('SPACING_OVERRIDE')

    """
    return [SPACING, SPACING_OVERRIDE]


def spacing_tags() -> typing.List[Tag]:
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
        SPACING_COMMAND,
        SPACING,
        SPACING_OVERRIDE_COMMAND,
        SPACING_OVERRIDE,
    ]


def staff_lines_color_tags(path=None) -> typing.List[Tag]:
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
        EXPLICIT_STAFF_LINES_COLOR,
        REAPPLIED_STAFF_LINES_COLOR,
        REDUNDANT_STAFF_LINES_COLOR,
    ]
    if path and not path.is_segment():
        tags.append(REAPPLIED_STAFF_LINES)
    return tags


def time_signature_color_tags(path=None) -> typing.List[Tag]:
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
        EXPLICIT_TIME_SIGNATURE_COLOR,
        REAPPLIED_TIME_SIGNATURE_COLOR,
        REDUNDANT_TIME_SIGNATURE_COLOR,
    ]
    if path and not path.is_segment():
        tags.append(REAPPLIED_TIME_SIGNATURE)
    return tags


def has_persistence_tag(tag) -> bool:
    """
    Is true when tag has persistence tag.

    ..  container:: example

        >>> abjad.tags.has_persistence_tag(abjad.Tag('FOO'))
        False

        >>> abjad.tags.has_persistence_tag(abjad.Tag('FOO:DEFAULT_CLEF'))
        True

        >>> abjad.tags.has_persistence_tag(abjad.Tag('DEFAULT_CLEF'))
        True

    """
    tags = persistent_indicator_tags()
    for word in tag:
        if type(tag)(word) in tags:
            return True
    return False
