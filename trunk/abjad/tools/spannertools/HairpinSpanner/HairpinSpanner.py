from abjad.tools import chordtools
from abjad.tools import notetools
from abjad.tools import contexttools
from abjad.tools import stringtools
from abjad.tools.spannertools.DirectedSpanner.DirectedSpanner import DirectedSpanner


class HairpinSpanner(DirectedSpanner):
    r'''Abjad hairpin spanner that includes rests::

        >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

    ::

        >>> f(staff)
        \new Staff {
            r4
            c'8
            d'8
            e'8
            f'8
            r4
        }

    ::

        >>> spannertools.HairpinSpanner(staff[:], 'p < f', include_rests = True)
        HairpinSpanner(r4, c'8, d'8, e'8, f'8, r4)

    ::

        >>> f(staff)
        \new Staff {
            r4 \< \p
            c'8
            d'8
            e'8
            f'8
            r4 \f
        }

    Abjad hairpin spanner that does not include rests::

        >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

    ::

        >>> f(staff)
        \new Staff {
            r4
            c'8
            d'8
            e'8
            f'8
            r4
        }

    ::

        >>> spannertools.HairpinSpanner(staff[:], 'p < f', include_rests = False)
        HairpinSpanner(r4, c'8, d'8, e'8, f'8, r4)

    ::

        >>> f(staff)
        \new Staff {
            r4
            c'8 \< \p
            d'8
            e'8
            f'8 \f
            r4
        }

    Return hairpin spanner.
    '''

    ### CLASS ATTRIBUTES ###

    _hairpin_shape_strings = ('<', '>')

    ### INITIALIZER ###

    def __init__(self, components=None, descriptor='<', include_rests=True, direction=None):
        DirectedSpanner.__init__(self, components=components, direction=direction)
        self.include_rests = include_rests
        start_dynamic_string, shape_string, stop_dynamic_string = self._parse_descriptor(descriptor)
        self.shape_string = shape_string
        self.start_dynamic_string = start_dynamic_string
        self.stop_dynamic_string = stop_dynamic_string

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        DirectedSpanner._copy_keyword_args(self, new)
        new.include_rests = self.include_rests
        new.shape_string = self.shape_string
        new.start_dynamic_string = self.start_dynamic_string
        new.stop_dynamic_string = self.stop_dynamic_string

    def _format_right_of_leaf(self, leaf):
        result = []
        effective_dynamic = contexttools.get_effective_dynamic(leaf)
        direction_string = ''
        if self.direction is not None:
            direction_string = '{} '.format(stringtools.arg_to_tridirectional_lilypond_symbol(self.direction))
        if self.include_rests:
            if self._is_my_first_leaf(leaf):
                result.append('%s\\%s' % (direction_string, self.shape_string))
                if self.start_dynamic_string:
                    result.append('%s\\%s' % (direction_string, self.start_dynamic_string))
            if self._is_my_last_leaf(leaf):
                if self.stop_dynamic_string:
                    result.append('%s\\%s' % (direction_string, self.stop_dynamic_string))
                elif effective_dynamic is None or \
                    effective_dynamic not in \
                    leaf._marks_for_which_component_functions_as_start_component:
                    result.append('\\!')
        else:
            if self._is_my_first(leaf, (chordtools.Chord, notetools.Note)):
                result.append('%s\\%s' % (direction_string, self.shape_string))
                if self.start_dynamic_string:
                    result.append('%s\\%s' % (direction_string, self.start_dynamic_string))
            if self._is_my_last(leaf, (chordtools.Chord, notetools.Note)):
                if self.stop_dynamic_string:
                    result.append('%s\\%s' % (direction_string, self.stop_dynamic_string))
                elif effective_dynamic is None:
                    result.append('\\!')
        return result

    def _parse_descriptor(self, descriptor):
        '''Example descriptors:
            '<'
            'p <'
            'p < f'
        '''
        assert isinstance(descriptor, str)
        parts = descriptor.split()
        num_parts = len(parts)
        start, shape, stop = None, None, None
        if parts[0] in ('<', '>'):
            assert 1 <= num_parts <= 2
            if num_parts == 1:
                shape = parts[0]
            else:
                shape = parts[0]
                stop = parts[1]
        else:
            assert 2 <= num_parts <= 3
            if num_parts == 2:
                start = parts[0]
                shape = parts[1]
            else:
                start = parts[0]
                shape = parts[1]
                stop = parts[2]
        assert shape in ('<', '>')
        return start, shape, stop

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def include_rests():
        def fget(self):
            r'''Get boolean hairpin rests setting::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f', include_rests = True)
                >>> hairpin.include_rests
                True

            Set boolean hairpin rests setting::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f', include_rests = True)
                >>> hairpin.include_rests = False
                >>> hairpin.include_rests
                False

            Set boolean.
            '''
            return self._include_rests
        def fset(self, arg):
            self._include_rests = arg
        return property(**locals())

    @apply
    def shape_string():
        def fget(self):
            r'''Get hairpin shape string::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                >>> hairpin.shape_string
                '<'

            Set hairpin shape string::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                >>> hairpin.shape_string = '>'
                >>> hairpin.shape_string
                '>'

            Set string.
            '''
            return self._shape
        def fset(self, arg):
            assert arg in ('<', '>')
            self._shape = arg
        return property(**locals())

    @apply
    def start_dynamic_string():
        def fget(self):
            r'''Get hairpin start dynamic string::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                >>> hairpin.start_dynamic_string
                'p'

            Set hairpin start dynamic string::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                >>> hairpin.start_dynamic_string = 'mf'
                >>> hairpin.start_dynamic_string
                'mf'

            Set string.
            '''
            return self._start
        def fset(self, arg):
            self._start = arg
        return property(**locals())

    @apply
    def stop_dynamic_string():
        def fget(self):
            r'''Get hairpin stop dynamic string::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                >>> hairpin.stop_dynamic_string
                'f'

            Set hairpin stop dynamic string::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                >>> hairpin.stop_dynamic_string = 'mf'
                >>> hairpin.stop_dynamic_string
                'mf'

            Set string.
            '''
            return self._stop
        def fset(self, arg):
            self._stop = arg
        return property(**locals())

    ### PUBLIC METHODS ###

    # TODO: reimplement static method as API function
    @staticmethod
    def is_hairpin_shape_string(arg):
        '''True when `arg` is a hairpin shape string. Otherwise false::

            >>> spannertools.HairpinSpanner.is_hairpin_shape_string('<')
            True

        Return boolean.
        '''
        return arg in HairpinSpanner._hairpin_shape_strings

    # TODO: reimplement static method as API function
    @staticmethod
    def is_hairpin_token(arg):
        '''True when `arg` is a hairpin token. Otherwise false::

            >>> spannertools.HairpinSpanner.is_hairpin_token(('p', '<', 'f'))
            True

        ::

            >>> spannertools.HairpinSpanner.is_hairpin_token(('f', '<', 'p'))
            False

        Return boolean.
        ''' 
        if isinstance(arg, tuple) and \
            len(arg) == 3 and \
            (not arg[0] or contexttools.DynamicMark.is_dynamic_name(arg[0])) and \
            HairpinSpanner.is_hairpin_shape_string(arg[1]) and \
            (not arg[2] or contexttools.DynamicMark.is_dynamic_name(arg[2])):
            if arg[0] and arg[2]:
                start_ordinal = contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal(arg[0])
                stop_ordinal = contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal(arg[2])
                if arg[1] == '<':
                    return start_ordinal < stop_ordinal
                else:
                    return stop_ordinal < start_ordinal
            else:
                return True
        else:
            return False
