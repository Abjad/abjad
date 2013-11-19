# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class Dynamic(AbjadObject):
    r'''A dynamic.

    ..  container:: example
    
        **Example 1.** Initializes from dynamic name:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> dynamic = Dynamic('f')
            >>> attach(dynamic, staff[0])

        ..  doctest::

            >>> print format(staff)
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

    def __init__(self, name):
        from abjad.tools import scoretools
        if isinstance(name, type(self)):
            name = name.name
        self._name = name
        self._default_scope = scoretools.Staff

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies dynamic.

        Returns new dynamic.
        '''
        return type(self)(self._name)

    def __eq__(self, arg):
        r'''True when `arg` is a dynamic with a name equal to the name of this
        dynamic. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            return self._name == arg._name
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self._name)

    @property
    def _lilypond_format(self):
        return r'\{}'.format(self.name)

    ### PUBLIC PROPERTIES ###


    @property
    def name(self):
        r'''Name of dynamic.

        ::

            >>> dynamic.name
            'f'

        Returns string.
        '''
        return self._name

    ### PUBLIC METHODS ###

    @staticmethod
    def composite_dynamic_name_to_steady_state_dynamic_name(name):
        r'''Changes composite `name` to steady state dynamic name.

        ::

            >>> Dynamic.composite_dynamic_name_to_steady_state_dynamic_name('sfp')
            'p'

        Returns string.
        '''
        return Dynamic._composite_dynamic_name_to_steady_state_dynamic_name[name]

    @staticmethod
    def dynamic_name_to_dynamic_ordinal(name):
        r'''Changes `name` to dynamic ordinal.

        ::

            >>> Dynamic.dynamic_name_to_dynamic_ordinal('fff')
            4

        Returns integer.
        '''
        try:
            return Dynamic._dynamic_name_to_dynamic_ordinal[name]
        except KeyError:
            name = Dynamic.composite_dynamic_name_to_steady_state_dynamic_name(
                name)
            return Dynamic._dynamic_name_to_dynamic_ordinal[name]

    @staticmethod
    def dynamic_ordinal_to_dynamic_name(dynamic_ordinal):
        r'''Changes `dynamic_ordinal` to dynamic name.

        ::

            >>> Dynamic.dynamic_ordinal_to_dynamic_name(-5)
            'pppp'

        Returns string.
        '''
        return Dynamic._dynamic_ordinal_to_dynamic_name[dynamic_ordinal]

    @staticmethod
    def is_dynamic_name(arg):
        r'''True when `arg` is dynamic name. Otherwise false.

        ::

            >>> Dynamic.is_dynamic_name('f')
            True

        Returns boolean.
        '''
        return arg in Dynamic._dynamic_names
