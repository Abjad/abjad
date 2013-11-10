# -*- encoding: utf-8 -*-
from abjad.tools.marktools.ContextMark import ContextMark


class Dynamic(ContextMark):
    r'''A dynamic.

    ..  container:: example
    
        **Example 1.** Initializes from dynamic name:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> dynamic = Dynamic('f')
            >>> attach(dynamic, staff[0])

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

        **Example 2.** Initializes from other dynamic:

        ::

            >>> dynamic_1 = Dynamic('f')
            >>> dynamic_2 = Dynamic(dynamic_1)

        ::

            >>> dynamic_1
            Dynamic('f')

        ::

            >>> dynamic_2
            Dynamic('f')

    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        repr('f'),
        )

    _format_slot = 'right'

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

    ### INITIALIZER ###

    def __init__(self, dynamic_name):
        ContextMark.__init__(self)
        if isinstance(dynamic_name, type(self)):
            dynamic_name = dynamic_name.dynamic_name
        self._dynamic_name = dynamic_name

    ### SPECIAL METHODS ###

    def __call__(self, *args):
        from abjad.tools import spannertools
        if len(args) == 1:
            spanner_classes = (
                spannertools.DynamicTextSpanner, 
                spannertools.Hairpin,
                )
            parentage = args[0]._get_parentage()
            dynamic_spanners = parentage._get_spanners(spanner_classes)
            for dynamic_spanner in dynamic_spanners:
                if not dynamic_spanner._is_exterior_leaf(args[0]):
                    message = 'can not attach dynamic'
                    message += ' to interior component of dynamic spanner.'
                    raise WellFormednessError(message)
        return ContextMark.__call__(self, *args)

    def __copy__(self, *args):
        return type(self)(self._dynamic_name)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self._dynamic_name == arg._dynamic_name
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self._dynamic_name)

    @property
    def _lilypond_format(self):
        return r'\%s' % self._dynamic_name

    ### PUBLIC PROPERTIES ###

    @apply
    def dynamic_name():
        def fget(self):
            r'''Get dynamic name:

            ::

                >>> dynamic = Dynamic('f')
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

    ### PUBLIC METHODS ###

    @staticmethod
    def composite_dynamic_name_to_steady_state_dynamic_name(dynamic_name):
        r'''Change composite `dynamic_name` to steady state dynamic name:

        ::

            >>> Dynamic.composite_dynamic_name_to_steady_state_dynamic_name('sfp')
            'p'

        Returns string.
        '''
        return Dynamic._composite_dynamic_name_to_steady_state_dynamic_name[dynamic_name]

    @staticmethod
    def dynamic_name_to_dynamic_ordinal(dynamic_name):
        r'''Change `dynamic_name` to dynamic ordinal:

        ::

            >>> Dynamic.dynamic_name_to_dynamic_ordinal('fff')
            4

        Returns integer.
        '''
        try:
            return Dynamic._dynamic_name_to_dynamic_ordinal[dynamic_name]
        except KeyError:
            dynamic_name = Dynamic.composite_dynamic_name_to_steady_state_dynamic_name(
                dynamic_name)
            return Dynamic._dynamic_name_to_dynamic_ordinal[dynamic_name]

    @staticmethod
    def dynamic_ordinal_to_dynamic_name(dynamic_ordinal):
        r'''Change `dynamic_ordinal` to dynamic name:

        ::

            >>> Dynamic.dynamic_ordinal_to_dynamic_name(-5)
            'pppp'

        Returns string.
        '''
        return Dynamic._dynamic_ordinal_to_dynamic_name[dynamic_ordinal]

    @staticmethod
    def is_dynamic_name(arg):
        r'''True when `arg` is dynamic name. False otherwise:

        ::

            >>> Dynamic.is_dynamic_name('f')
            True

        Returns boolean.
        '''
        return arg in Dynamic._dynamic_names
