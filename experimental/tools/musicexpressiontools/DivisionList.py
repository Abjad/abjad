# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.mathtools.BoundedObject import BoundedObject
from abjad.tools.topleveltools import new


class DivisionList(BoundedObject):
    r'''Division list.

    Preparatory definitions:

    ::

        >>> score_template = \
        ...     templatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=1)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> set_expression = red_segment.set_time_signatures(
        ...     [(4, 8), (3, 8)])
        >>> set_expression = red_segment.set_divisions(
        ...     [(3, 16)], contexts=['Voice 1'])
        >>> set_expression = red_segment.set_rhythm(library.thirty_seconds)

    ::

        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> green_segment = score_specification.append_segment(name='green')

    ::

        >>> score = score_specification.interpret()


    Example. ``'Voice 1'`` has only one division region division list:

    ::

        >>> voice_proxy = \
        ...     score_specification.specification.voice_data_structures_by_voice[
        ...     'Voice 1']
        >>> len(voice_proxy.payload_expressions_by_attribute['divisions'])
        1

    ::

        >>> division_list = \
        ...     voice_proxy.payload_expressions_by_attribute[
        ...     'divisions'][0].payload

    ::

        >>> print(format(division_list))
        musicexpressiontools.DivisionList(
            [
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(0, 1),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(3, 16),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(3, 8),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(9, 16),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(3, 4),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(15, 16),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(9, 8),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(21, 16),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(3, 2),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(27, 16),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(15, 8),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(33, 16),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(9, 4),
                    ),
                musicexpressiontools.Division(
                    '[3, 16)',
                    start_offset=durationtools.Offset(39, 16),
                    ),
                ],
            start_offset=durationtools.Offset(0, 1),
            voice_name='Voice 1',
            )

    Interpreter byproduct.
    '''

    ### INITIALIZER ###

    def __init__(self, divisions, start_offset=None, voice_name=None):
        from experimental.tools import musicexpressiontools
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        if start_offset is not None:
            start_offset = durationtools.Offset(start_offset)
        positioned_divisions = []
        total_duration = start_offset or durationtools.Duration(0)
        for division in divisions:
            division_start_offset = durationtools.Offset(total_duration)
            positioned_division = musicexpressiontools.Division(
                division, start_offset=division_start_offset)
            positioned_divisions.append(positioned_division)
            total_duration += positioned_division.duration
        divisions = positioned_divisions
        assert all(x.start_offset is not None for x in divisions)
        self._divisions = divisions
        self._voice_name = voice_name
        #assert self.is_well_formed

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Concatenate division lists.

            >>> left = musicexpressiontools.DivisionList([(1, 16), (2, 16)])
            >>> right = musicexpressiontools.DivisionList([(3, 16), (4, 16)])

        ::

            >>> left + right
            DivisionList('[1, 16), [2, 16), [3, 16), [4, 16)')

        Returns newly constructed division list.
        '''
        assert self.is_left_closed and expr.is_left_closed
        assert self.is_right_open and expr.is_right_open
        divisions = []
        divisions.extend(self[:])
        divisions.extend(expr[:])
        return type(self)(divisions)

    def __format__(self, format_specification=''):
        r'''Formats division list.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> print(format(division_list))
            musicexpressiontools.DivisionList(
                [
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(0, 1),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(3, 16),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(3, 8),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(9, 16),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(3, 4),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(15, 16),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(9, 8),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(21, 16),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(3, 2),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(27, 16),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(15, 8),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(33, 16),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(9, 4),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(39, 16),
                        ),
                    ],
                start_offset=durationtools.Offset(0, 1),
                voice_name='Voice 1',
                )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getitem__(self, expr):
        r'''Get division list item.

        Returns division.
        '''
        return self.divisions.__getitem__(expr)

    def __len__(self):
        r'''Division list length.

        Returns nonnegative integer.
        '''
        return len(self.divisions)

    def __repr__(self):
        r'''Division list interpreter representation.

        Returns string.
        '''
        return '{}({!r})'.format(type(self).__name__, self._contents_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_string(self):
        contents_string = [str(x) for x in self.divisions]
        contents_string = ', '.join(contents_string)
        return contents_string

    ### PUBLIC PROPERTIES ###

    @property
    def divisions(self):
        r'''Division list divisions.

            >>> for division in division_list.divisions: division
            Division('[3, 16)', start_offset=Offset(0, 1))
            Division('[3, 16)', start_offset=Offset(3, 16))
            Division('[3, 16)', start_offset=Offset(3, 8))
            Division('[3, 16)', start_offset=Offset(9, 16))
            Division('[3, 16)', start_offset=Offset(3, 4))
            Division('[3, 16)', start_offset=Offset(15, 16))
            Division('[3, 16)', start_offset=Offset(9, 8))
            Division('[3, 16)', start_offset=Offset(21, 16))
            Division('[3, 16)', start_offset=Offset(3, 2))
            Division('[3, 16)', start_offset=Offset(27, 16))
            Division('[3, 16)', start_offset=Offset(15, 8))
            Division('[3, 16)', start_offset=Offset(33, 16))
            Division('[3, 16)', start_offset=Offset(9, 4))
            Division('[3, 16)', start_offset=Offset(39, 16))

        Returns list.
        '''
        return self._divisions

    @property
    def duration(self):
        r'''Division list duration.

        ::

            >>> division_list.duration
            Duration(21, 8)

        Returns duration.
        '''
        return sum([division.duration for division in self.divisions])

    @property
    def is_left_closed(self):
        r'''Is true when first division in division is left closed.

        ::

            >>> division_list.is_left_closed
            True

        Returns boolean.
        '''
        return self[0].is_left_closed

    @property
    def is_left_open(self):
        r'''Is true when first division in division is left open.

        ::

            >>> division_list.is_left_open
            False

        Returns boolean.
        '''
        return self[0].is_left_open

    @property
    def is_right_closed(self):
        r'''Is true when first division in division is right closed.

        ::

            >>> division_list.is_right_closed
            False

        Returns boolean.
        '''
        return self[-1].is_right_closed

    @property
    def is_right_open(self):
        r'''Is true when first division in division is right open.

        ::

            >>> division_list.is_right_open
            True

        Returns boolean.
        '''
        return self[-1].is_right_open

#    @property
#    def is_well_formed(self):
#        r'''Is true when division list is well-formed.
#        Otherwise false.
#
#        ::
#
#            >>> division_list.is_well_formed
#            True
#
#        Returns boolean.
#        '''
#        if 1 < len(self) and self[0].is_right_open:
#            return False
#        if 1 < len(self) and self[-1].is_left_open:
#            return False
#        return True

    @property
    def pairs(self):
        r'''Division list pairs.

        ::

            >>> for pair in division_list.pairs: pair
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)
            (3, 16)

        Returns list.
        '''
        return [division.pair for division in self]

    @property
    def start_offset(self):
        r'''Division list start offset.

        ::

            >>> division_list.start_offset
            Offset(0, 1)

        Returns offset.
        '''
        if self:
            return self[0].start_offset

    @property
    def voice_name(self):
        r'''Division list voice name.

        ::

            >>> division_list.voice_name
            'Voice 1'

        Returns string.
        '''
        return self._voice_name

    ### PUBLIC METHODS ###

    def reflect(self):
        r'''Reflect division list about axis.

        ::

            >>> divisions = [(3, 16), (4, 16), (3, 16), (4, 16)]
            >>> division_list = musicexpressiontools.DivisionList(
            ...     divisions, Offset(5), 'Voice 1')

        ::

            >>> result = division_list.reflect()

        ::

            >>> print(format(result))
            musicexpressiontools.DivisionList(
                [
                    musicexpressiontools.Division(
                        '[4, 16)',
                        start_offset=durationtools.Offset(5, 1),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(21, 4),
                        ),
                    musicexpressiontools.Division(
                        '[4, 16)',
                        start_offset=durationtools.Offset(87, 16),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(91, 16),
                        ),
                    ],
                start_offset=durationtools.Offset(5, 1),
                voice_name='Voice 1',
                )

        Emit newly constructed division list.
        '''
        return new(self, divisions=reversed(self.divisions))

    def rotate(self, rotation):
        r'''Rotate division list by `rotation`.

        ::

            >>> divisions = [(3, 16), (4, 16), (3, 16), (4, 16)]
            >>> division_list = musicexpressiontools.DivisionList(
            ...     divisions, Offset(5), 'Voice 1')

        ::

            >>> result = division_list.rotate(-1)

        ::

            >>> print(format(result))
            musicexpressiontools.DivisionList(
                [
                    musicexpressiontools.Division(
                        '[4, 16)',
                        start_offset=durationtools.Offset(5, 1),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(21, 4),
                        ),
                    musicexpressiontools.Division(
                        '[4, 16)',
                        start_offset=durationtools.Offset(87, 16),
                        ),
                    musicexpressiontools.Division(
                        '[3, 16)',
                        start_offset=durationtools.Offset(91, 16),
                        ),
                    ],
                start_offset=durationtools.Offset(5, 1),
                voice_name='Voice 1',
                )

        Emit newly constructed division list.
        '''
        divisions = sequencetools.rotate_sequence(self.divisions, rotation)
        return new(self, divisions=divisions)