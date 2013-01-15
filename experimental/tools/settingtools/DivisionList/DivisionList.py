from abjad.tools.mathtools.BoundedObject import BoundedObject
from experimental.tools import helpertools


class DivisionList(BoundedObject):
    r'''Division list.

    Division lists model time-contiguous divisions.

    Division region division list example::

        >>> from abjad import *
        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> setting = red_segment.set_time_signatures([(4, 8), (3, 8)])
        >>> setting = red_segment.set_divisions([(3, 16)], contexts=['Voice 1'])
        >>> setting = red_segment.set_rhythm(library.thirty_seconds)

    ::

        >>> blue_segment = score_specification.append_segment(name='blue')
        >>> green_segment = score_specification.append_segment(name='green')

    ::

        >>> score = score_specification.interpret()


    ``'Voice 1'`` has only one division region division list::

        >>> len(score_specification.contexts['Voice 1'].division_region_products)
        1

    ::

        >>> z(score_specification.contexts['Voice 1'].division_region_products[0])
        settingtools.DivisionRegionProduct(
            payload=settingtools.DivisionList(
                [Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), 
                Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), 
                Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), 
                Division('[3, 16]'), Division('[3, 16]')]
            ),
            voice_name='Voice 1',
            timespan=timespantools.Timespan(
                start_offset=durationtools.Offset(0, 1),
                stop_offset=durationtools.Offset(21, 8)
                )
            )

    The reason that ``'Voice 1'`` has only one division region division list is that the 
    composer specified only one division-maker for the entire score.

    Note that composers may specify an arbitrary number of division-makers for any given voice.
    This results in an arbitrary number of division regions per voice.

    Composers do not create division lists because division lists 
    arise as a byproduct of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, divisions, voice_name=None):
        from experimental.tools import settingtools
        divisions = [settingtools.Division(x) for x in divisions]
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        self._divisions = divisions
        self._voice_name = voice_name
        assert self.is_well_formed

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        '''Concatenate division lists.

            >>> left = settingtools.DivisionList([(1, 16), (2, 16)])
            >>> right = settingtools.DivisionList([(3, 16), (4, 16)])

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

    ### PUBLIC METHODS ###

    def new(self, **kwargs):
        positional_argument_dictionary = self._positional_argument_dictionary
        keyword_argument_dictionary = self._keyword_argument_dictionary
        for key, value in kwargs.iteritems():
            if key in positional_argument_dictionary:
                positional_argument_dictionary[key] = value
            elif key in keyword_argument_dictionary:
                keyword_argument_dictionary[key] = value
            else:
                raise KeyError(key)
        positional_argument_values = []
        for positional_argument_name in self._positional_argument_names:
            positional_argument_value = positional_argument_dictionary[positional_argument_name]
            positional_argument_values.append(positional_argument_value)
        result = type(self)(*positional_argument_values, **keyword_argument_dictionary)
        return result

    def reflect(self):
        '''Reflect division list about axis.

        .. note:: add example.

        Operate in place and return none.
        '''
        self.divisions.reverse()
