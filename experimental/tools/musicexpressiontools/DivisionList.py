# -*- encoding: utf-8 -*-
import copy
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools import new


class DivisionList(AbjadObject):
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
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
                durationtools.Division(3, 16),
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
        start_offset = start_offset or durationtools.Offset(0)
        start_offset = durationtools.Offset(start_offset)
        self._start_offset = start_offset
        divisions = [durationtools.Division(_) for _ in divisions]
        self._divisions = divisions
        self._voice_name = voice_name

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Concatenate division lists.

            >>> left = musicexpressiontools.DivisionList([(1, 16), (2, 16)])
            >>> right = musicexpressiontools.DivisionList([(3, 16), (4, 16)])

        ::

            >>> left + right
            DivisionList('1/16, 2/16, 3/16, 4/16')

        Returns newly constructed division list.
        '''
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
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(3, 16),
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
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)
            Division(3, 16)

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
        return sum([
            durationtools.Duration(division) for division in self.divisions
            ])

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
        return self._start_offset

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
                    durationtools.Division(4, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(4, 16),
                    durationtools.Division(3, 16),
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
                    durationtools.Division(4, 16),
                    durationtools.Division(3, 16),
                    durationtools.Division(4, 16),
                    durationtools.Division(3, 16),
                    ],
                start_offset=durationtools.Offset(5, 1),
                voice_name='Voice 1',
                )

        Emit newly constructed division list.
        '''
        divisions = sequencetools.rotate_sequence(self.divisions, rotation)
        return new(self, divisions=divisions)