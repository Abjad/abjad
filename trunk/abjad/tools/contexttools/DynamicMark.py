# -*- encoding: utf-8 -*-
from abjad.tools.contexttools.ContextMark import ContextMark


class DynamicMark(ContextMark):
    r'''A dynamic mark.

    ..  container:: example
    
        **Example 1.** Initialize from dynamic name:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")

        ::

            >>> contexttools.DynamicMark('f')(staff[0])
            DynamicMark('f')(c'8)

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'8 \f
                d'8
                e'8
                f'8
            }

        ::

            >>> show(staff) # doctest: +SKIP

    ..  container:: example

        **Example 2.** Initialize from other dynamic mark:

        ::

            >>> dynamic_mark_1 = contexttools.DynamicMark('f')
            >>> dynamic_mark_2 = contexttools.DynamicMark(dynamic_mark_1)

        ::

            >>> dynamic_mark_1
            DynamicMark('f')

        ::

            >>> dynamic_mark_2
            DynamicMark('f')

    Dynamic marks target the staff context by default.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        repr('f'),
        )

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self, dynamic_name, target_context=None):
        from abjad.tools.stafftools.Staff import Staff
        target_context = target_context or Staff
        ContextMark.__init__(self, target_context=target_context)
        if isinstance(dynamic_name, type(self)):
            dynamic_name = dynamic_name.dynamic_name
        self._dynamic_name = dynamic_name

    ### SPECIAL METHODS ###

    def __call__(self, *args):
        from abjad.tools import spannertools
        if len(args) == 1:
            spanner_classes = (
                spannertools.DynamicTextSpanner, 
                spannertools.HairpinSpanner,
                )
            parentage = args[0]._get_parentage()
            dynamic_spanners = parentage._get_spanners(spanner_classes)
            for dynamic_spanner in dynamic_spanners:
                if not dynamic_spanner._is_exterior_leaf(args[0]):
                    message = 'can not attach dynamic mark'
                    message += ' to interior component of dynamic spanner.'
                    raise WellFormednessError(message)
        return ContextMark.__call__(self, *args)

    def __copy__(self, *args):
        return type(self)(
            self._dynamic_name, target_context=self.target_context)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self._dynamic_name == arg._dynamic_name
        return False

    ### PRIVATE PROPERTIES ###

    _composite_dynamic_name_to_steady_state_dynamic_name = {
        'fp': 'p', 
        'sf': 'f', 
        'sff': 'ff',
        'sp': 'p', 
        'spp': 'pp',
        'sfz': 'f', 
        'sfp': 'p', 
        'rfz': 'f',
    }

    @property
    def _contents_repr_string(self):
        return repr(self._dynamic_name)

    _dynamic_name_to_dynamic_ordinal = {
        'ppppp': -6, 
        'pppp': -5, 
        'ppp': -4, 
        'pp': -3, 
        'p': -2,
        'mp': -1,
        'mf': 1,
        'f': 2, 
        'ff': 3, 
        'fff': 4, 
        'ffff': 5, 
        'fffff': 6,
        }

    _dynamic_names = (
        'ppppp', 
        'pppp', 
        'ppp', 
        'pp', 
        'p',
        'mp', 
        'mf',
        'f', 
        'ff', 
        'fff', 
        'ffff', 
        'fffff',
        'fp', 
        'sf', 
        'sff', 
        'sp', 
        'spp',
        'sfz', 
        'sfp', 
        'rfz',
        )

    _dynamic_ordinal_to_dynamic_name = {
        -6: 'ppppp', 
        -5: 'pppp', 
        -4: 'ppp', 
        -3: 'pp', 
        -2: 'p',
        -1: 'mp',
        1: 'mf',
        2: 'f', 
        3: 'ff', 
        4: 'fff', 
        5: 'ffff', 
        6: 'fffff',
        }

    ### PUBLIC PROPERTIES ###

    @apply
    def dynamic_name():
        def fget(self):
            r'''Get dynamic name:

            ::

                >>> dynamic = contexttools.DynamicMark('f')
                >>> dynamic.dynamic_name
                'f'

            Set dynamic name:

            ::

                >>> dynamic.dynamic_name = 'p'
                >>> dynamic.dynamic_name
                'p'

            Returns string.
            '''
            return self._dynamic_name
        def fset(self, dynamic_name):
            assert isinstance(dynamic_name, str)
            self._dynamic_name = dynamic_name
        return property(**locals())

    @property
    def lilypond_format(self):
        r'''LilyPond input format of dynamic mark:

        ::

            >>> dynamic_mark = contexttools.DynamicMark('f')
            >>> dynamic_mark.lilypond_format
            '\\f'

        Returns string.
        '''
        return r'\%s' % self._dynamic_name

    ### PUBLIC METHODS ###

    @staticmethod
    def composite_dynamic_name_to_steady_state_dynamic_name(dynamic_name):
        r'''Change composite `dynamic_name` to steady state dynamic name:

        ::

            >>> contexttools.DynamicMark.composite_dynamic_name_to_steady_state_dynamic_name('sfp')
            'p'

        Returns string.
        '''
        return DynamicMark._composite_dynamic_name_to_steady_state_dynamic_name[dynamic_name]

    @staticmethod
    def dynamic_name_to_dynamic_ordinal(dynamic_name):
        r'''Change `dynamic_name` to dynamic ordinal:

        ::

            >>> contexttools.DynamicMark.dynamic_name_to_dynamic_ordinal('fff')
            4

        Returns integer.
        '''
        try:
            return DynamicMark._dynamic_name_to_dynamic_ordinal[dynamic_name]
        except KeyError:
            dynamic_name = DynamicMark.composite_dynamic_name_to_steady_state_dynamic_name(
                dynamic_name)
            return DynamicMark._dynamic_name_to_dynamic_ordinal[dynamic_name]

    @staticmethod
    def dynamic_ordinal_to_dynamic_name(dynamic_ordinal):
        r'''Change `dynamic_ordinal` to dynamic name:

        ::

            >>> contexttools.DynamicMark.dynamic_ordinal_to_dynamic_name(-5)
            'pppp'

        Returns string.
        '''
        return DynamicMark._dynamic_ordinal_to_dynamic_name[dynamic_ordinal]

    @staticmethod
    def is_dynamic_name(arg):
        r'''True when `arg` is dynamic name. False otherwise:

        ::

            >>> contexttools.DynamicMark.is_dynamic_name('f')
            True

        Returns boolean.
        '''
        return arg in DynamicMark._dynamic_names
