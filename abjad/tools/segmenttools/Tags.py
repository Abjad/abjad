from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Tags(AbjadValueObject):
    r'''Tags.

    Attributes always return as strings.

    ..  container:: example

        Abjad-level singleton:

        >>> abjad.tags
        Tags()
        
    ..  container:: example

        Class is also available:

        >>> abjad.Tags
        <class 'abjad.tools.segmenttools.Tags.Tags'>

        >>> abjad.Tags()
        Tags()

    ..  container:: example

        >>> abjad.tags.RIGHT_OPEN_TIE
        'RIGHT_OPEN_TIE'

        >>> abjad.tags.LEFT_OPEN_REPEAT_TIE
        'LEFT_OPEN_REPEAT_TIE'

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _known_tags:tuple = (

        ### DOCUMENT COMMANDS ###

        'BREAK',
        'EMPTY_START_BAR',
        'EOL_FERMATA',
        'SHIFTED_CLEF',
        'SPACING',
        'SPACING_OVERRIDE',

        ### DOCUMENT MARKUP ###

        'CLOCK_TIME_MARKUP',
        'FIGURE_NAME_MARKUP',
        'MEASURE_NUMBER_MARKUP',
        'SPACING_MARKUP',
        'SPACING_OVERRIDE_MARKUP',
        'STAGE_NUMBER_MARKUP',

        ### DOCUMENT TYPES ###

        'BUILD',
        'SEGMENT',

        ### LEFT-OPEN SPANNERS ###

        'LEFT_OPEN_BEAM',
        'LEFT_OPEN_GLISSANDO',
        'LEFT_OPEN_HAIRPIN_START',
        'LEFT_OPEN_METRONOME_MARK_SPANNER',
        'LEFT_OPEN_OCTAVATION_SPANNER',
        'LEFT_OPEN_PHRASING_SLUR',
        'LEFT_OPEN_REPEAT_TIE',
        'LEFT_OPEN_SLUR',
        'LEFT_OPEN_TEXT_SPANNER',
        'LEFT_OPEN_TRILL',

        ### RIGHT-OPEN SPANNERS ###

        'RIGHT_OPEN_BEAM',
        'RIGHT_OPEN_GLISSANDO',
        'RIGHT_OPEN_HAIRPIN_STOP',
        'RIGHT_OPEN_METRONOME_MARK_SPANNER',
        'RIGHT_OPEN_OCTAVATION_SPANNER',
        'RIGHT_OPEN_PHRASING_SLUR',
        'RIGHT_OPEN_SLUR',
        'RIGHT_OPEN_TIE',
        'RIGHT_OPEN_TEXT_SPANNER',
        'RIGHT_OPEN_TRILL',

        ### PITCH HANDLING ###

        'ALLOW_REPEAT_PITCH',
        'DO_NOT_TRANSPOSE',

    )

    ### SPECIAL METHODS ###

    def __getattr__(self, tag):
        r'''Gets `tag`.

        Raise attribute error when `tag` is unknown.

        Returns strings.
        '''
        if tag not in self._known_tags:
            raise AttributeError('unknown tag: {!r}.'.format(tag))
        return tag

    ### PUBLIC METHODS ###

    @staticmethod
    def all_score_annotation_tags():
        r'''Gets all score annotation tags.

        ..  container:: example

            >>> for tag in abjad.tags.all_score_annotation_tags():
            ...     tag
            ...
            'CLOCK_TIME_MARKUP'
            'FIGURE_NAME_MARKUP'
            'MEASURE_NUMBER_MARKUP'
            'SPACING_MARKUP'
            'SPACING_OVERRIDE_MARKUP'
            'STAGE_NUMBER_MARKUP'

        Returns list of strings.
        '''
        import abjad
        return [
            abjad.tags.CLOCK_TIME_MARKUP,
            abjad.tags.FIGURE_NAME_MARKUP,
            abjad.tags.MEASURE_NUMBER_MARKUP,
            abjad.tags.SPACING_MARKUP,
            abjad.tags.SPACING_OVERRIDE_MARKUP,
            abjad.tags.STAGE_NUMBER_MARKUP,
            ]

    @staticmethod
    def document(document):
        r'''Gets document name.

        ..  container:: example

            Document only:

            >>> abjad.tags.document('11x17-landscape')
            '11_X_17_LANDSCAPE'

        Returns string.
        '''
        import abjad
        assert isinstance(document, str), repr(document)
        words = abjad.String(document).delimit_words()
        document = '_'.join(words)
        document = document.upper()
        return document

    @staticmethod
    def spacing_tags():
        r'''Gets spacing tags.

        ..  container:: example

            >>> for tag in abjad.tags.spacing_tags():
            ...     tag
            ...
            'SPACING'
            'SPACING_MARKUP'
            'SPACING_OVERRIDE'
            'SPACING_OVERRIDE_MARKUP'

        Returns list of strings.
        '''
        import abjad
        return [
            abjad.tags.SPACING,
            abjad.tags.SPACING_MARKUP,
            abjad.tags.SPACING_OVERRIDE,
            abjad.tags.SPACING_OVERRIDE_MARKUP,
            ]
