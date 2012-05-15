from abjad.tools.spannertools._DirectedSpanner._DirectedSpanner import _DirectedSpanner


class HairpinSpanner(_DirectedSpanner):
    r'''Abjad hairpin spanner that includes rests::

        abjad> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

    ::

        abjad> f(staff)
        \new Staff {
            r4
            c'8
            d'8
            e'8
            f'8
            r4
        }

    ::

        abjad> spannertools.HairpinSpanner(staff[:], 'p < f', include_rests = True)
        HairpinSpanner(r4, c'8, d'8, e'8, f'8, r4)

    ::

        abjad> f(staff)
        \new Staff {
            r4 \< \p
            c'8
            d'8
            e'8
            f'8
            r4 \f
        }

    Abjad hairpin spanner that does not include rests::

        abjad> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

    ::

        abjad> f(staff)
        \new Staff {
            r4
            c'8
            d'8
            e'8
            f'8
            r4
        }

    ::

        abjad> spannertools.HairpinSpanner(staff[:], 'p < f', include_rests = False)
        HairpinSpanner(r4, c'8, d'8, e'8, f'8, r4)

    ::

        abjad> f(staff)
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
        _DirectedSpanner.__init__(self, components=components, direction=direction)
        self.include_rests = include_rests
        start_dynamic_string, shape_string, stop_dynamic_string = self._parse_descriptor(descriptor)
        self.shape_string = shape_string
        self.start_dynamic_string = start_dynamic_string
        self.stop_dynamic_string = stop_dynamic_string

    ### PRIVATE METHODS ###

    def _format_right_of_leaf(self, leaf):
        from abjad.tools.chordtools.Chord import Chord
        from abjad.tools.notetools.Note import Note
        from abjad.tools import contexttools
        result = []
        effective_dynamic = contexttools.get_effective_dynamic(leaf)
        direction_string = ''
        if self.direction is not None:
            direction_string = '%s ' % self.direction
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
            if self._is_my_first(leaf, (Chord, Note)):
                result.append('%s\\%s' % (direction_string, self.shape_string))
                if self.start_dynamic_string:
                    result.append('%s\\%s' % (direction_string, self.start_dynamic_string))
            if self._is_my_last(leaf, (Chord, Note)):
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

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f', include_rests = True)
                abjad> hairpin.include_rests
                True

            Set boolean hairpin rests setting::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f', include_rests = True)
                abjad> hairpin.include_rests = False
                abjad> hairpin.include_rests
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

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                abjad> hairpin.shape_string
                '<'

            Set hairpin shape string::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                abjad> hairpin.shape_string = '>'
                abjad> hairpin.shape_string
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

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                abjad> hairpin.start_dynamic_string
                'p'

            Set hairpin start dynamic string::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                abjad> hairpin.start_dynamic_string = 'mf'
                abjad> hairpin.start_dynamic_string
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

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                abjad> hairpin.stop_dynamic_string
                'f'

            Set hairpin stop dynamic string::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> hairpin = spannertools.HairpinSpanner(staff[:], 'p < f')
                abjad> hairpin.stop_dynamic_string = 'mf'
                abjad> hairpin.stop_dynamic_string
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

            abjad> spannertools.HairpinSpanner.is_hairpin_shape_string('<')
            True

        Return boolean.
        '''
        return arg in HairpinSpanner._hairpin_shape_strings

    # TODO: reimplement static method as API function
    @staticmethod
    def is_hairpin_token(arg):
        '''True when `arg` is a hairpin token. Otherwise false::

            abjad> spannertools.HairpinSpanner.is_hairpin_token(('p', '<', 'f'))
            True

        ::

            abjad> spannertools.HairpinSpanner.is_hairpin_token(('f', '<', 'p'))
            False

        Return boolean.
        ''' 
        from abjad.tools import contexttools
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
