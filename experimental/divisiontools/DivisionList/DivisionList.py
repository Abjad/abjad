from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import helpertools


class DivisionList(AbjadObject):
    r'''.. versionadded:: 1.0

    Division lists model time-contiguous divisions.

    Segment division lists model the **parts of** all
    divisions that intersect some segment.

    Segment division lists break divisions that cross segment boundaries.

    Segment division lists contrast with division region division lists.
    The best way to show this is with an example::

        >>> from abjad import *
        >>> from experimental import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> segment = score_specification.make_segment('red')

    ::

        >>> setting = segment.set_time_signatures([(4, 8), (3, 8)])
        >>> setting = segment.set_divisions([(3, 16)], contexts=segment.v1)
        >>> setting = segment.set_rhythm(library.thirty_seconds)

    ::

        >>> segment = score_specification.make_segment('blue')
        >>> segment = score_specification.make_segment('green')

    ::

        >>> score = score_specification.interpret()


    ``'Voice 1'`` has only one division region division list::

        >>> len(score_specification.contexts['Voice 1']['division_region_expressions'])
        1

    ::

        >>> z(score_specification.contexts['Voice 1']['division_region_expressions'][0])
        settingtools.OffsetPositionedDivisionList(
            divisiontools.DivisionList(
                [Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), 
                Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), 
                Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), 
                Division('[3, 16]'), Division('[3, 16]')]
            ),
            voice_name='Voice 1',
            start_offset=durationtools.Offset(0, 1),
            stop_offset=durationtools.Offset(21, 8)
            )

    The reason that ``'Voice 1'`` has only one division region division list is that the 
    composer specified only one division-maker for the entire score.

    But ``'Voice 1'`` has three different segment division lists::

        >>> for x in score_specification.contexts['Voice 1']['segment_division_lists']: x
        ... 
        DivisionList('[3, 16], [3, 16], [3, 16], [3, 16], [2, 16)')
        DivisionList('(1, 16], [3, 16], [3, 16], [3, 16], [3, 16], [1, 16)')
        DivisionList('(2, 16], [3, 16], [3, 16], [3, 16], [3, 16]')

    The reason that ``'Voice 1'`` has three different segment division lists
    is that the composer specified three different segments.

    Note that composers may specify an arbitrary number of division-makers for any given voice.
    This results in an arbitrary number of division regions per voice.

    Note also that composers may specify an arbitrary number of segments per score.
    This results in an arbtirary number of segments per voice.

    Taken together these two facts mean that the division region division lists attaching 
    to a voice and the segment division lists attaching to that same voice do not 
    relate to each other in any systematic way.

    Composers do not specify division lists because division lists 
    arise as a byproduct of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, divisions, voice_name=None):
        from experimental import divisiontools
        assert isinstance(divisions, list), repr(divisions)
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        self._divisions = [divisiontools.Division(x) for x in divisions]
        self._voice_name = voice_name
        assert self.is_well_formed

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        '''Concatenate division lists.

            >>> left = divisiontools.DivisionList([(1, 16), (2, 16)])
            >>> right = divisiontools.DivisionList([(3, 16), (4, 16)])

        ::

            >>> left + right
            DivisionList('[1, 16], [2, 16], [3, 16], [4, 16]')

        Return newly constructed division list.
        '''
        assert isinstance(expr, type(self)), repr(expr)
        if self.is_right_open and expr.is_left_open:
            return self._add_open_division_lists(self, expr)
        elif self.is_right_closed and expr.is_left_closed:
            return self._add_closed_division_lists(self, expr)
        else:
            raise ValueError

    def __getitem__(self, expr):
        return self.divisions.__getitem__(expr)

    def __len__(self):
        return len(self.divisions)

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self._contents_string)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _contents_string(self):
        contents_string = [str(x) for x in self.divisions]
        contents_string = ', '.join(contents_string)
        return contents_string

    ### PRIVATE METHODS ###

    def _add_closed_division_lists(self, left, right):
        divisions = []
        divisions.extend(left)
        divisions.extend(right)
        return type(left)(divisions)

    def _add_open_division_lists(self, left, right):
        divisions = []
        divisions.extend(left[:-1])
        divisions.append(left[-1] + right[0])
        divisions.extend(right[1:])
        return type(left)(divisions)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def divisions(self):
        return self._divisions

    @property
    def duration(self):
        return sum([division.duration for division in self.divisions])

    @property
    def is_closed(self):
        return self.is_left_closed and self.is_right_closed

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def divisions(self):
        return self._divisions

    @property
    def duration(self):
        return sum([division.duration for division in self.divisions])

    @property
    def is_closed(self):
        return self.is_left_closed and self.is_right_closed

    @property
    def is_half_closed(self):
        return not self.is_left_closed == self.is_right_closed

    @property
    def is_half_open(self):
        return not self.is_left_open == self.is_right_open

    @property
    def is_left_closed(self):
        return self[0].is_left_closed

    @property
    def is_left_open(self):
        return self[0].is_left_open

    @property
    def is_right_closed(self):
        return self[-1].is_right_closed

    @property
    def is_right_open(self):
        return self[-1].is_right_open

    @property
    def is_open(self):
        return not self.is_left_closed and not self.is_right_closed

    @property
    def is_well_formed(self):
        if 1 < len(self) and self[0].is_right_open:
            return False
        if 1 < len(self) and self[-1].is_left_open:
            return False
        return True

    @property
    def pairs(self):
        return [division.pair for division in self]

    @property
    def voice_name(self):
        return self._voice_name
