# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Dynamic(AbjadValueObject):
    r'''A dynamic.

    ..  container:: example

        **Example 1.** Initializes from dynamic name:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> dynamic = Dynamic('f')
            >>> attach(dynamic, staff[0])

        ..  doctest::

            >>> print(format(staff))
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
            Dynamic(name='f')

        ::

            >>> dynamic_2
            Dynamic(name='f')

    ..  container:: example

        **Example 3.** Niente is possible, but provides no formatting.

        ::

            >>> dynamic = Dynamic('niente')
            >>> format(dynamic, 'lilypond')
            ''

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_name',
        )

    _format_slot = 'right'

    _composite_dynamic_name_to_steady_state_dynamic_name = {
        'fp': 'p',
        'sf': 'f',
        'sff': 'ff',
        'sfp': 'p',
        'sfpp': 'pp',
        'sffp': 'p',
        'sffpp': 'pp',
        'sfz': 'f',
        'sp': 'p',
        'spp': 'pp',
        'rfz': 'f',
        }

    _dynamic_name_to_dynamic_ordinal = {
        'ppppp': -6,
        'pppp': -5,
        'ppp': -4,
        'pp': -3,
        'p': -2,
        'niente': mathtools.NegativeInfinity(),
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
        'sffz',
        'sffp',
        'sffpp',
        'sfp',
        'sfpp',
        'rfz',
        'niente',
        )

    _dynamic_ordinal_to_dynamic_name = {
        -6: 'ppppp',
        -5: 'pppp',
        -4: 'ppp',
        -3: 'pp',
        -2: 'p',
        -1: 'mp',
        mathtools.NegativeInfinity(): 'niente',
        1: 'mf',
        2: 'f',
        3: 'ff',
        4: 'fff',
        5: 'ffff',
        6: 'fffff',
        }

    _lilypond_dynamic_commands = [
        _ for _ in _dynamic_names if not _ == 'niente'
        ]

    ### INITIALIZER ###

    def __init__(self, name='f'):
        from abjad.tools import scoretools
        if isinstance(name, type(self)):
            name = name.name
        assert name in self._dynamic_names, repr(name)
        self._name = name
        self._default_scope = scoretools.Staff

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats dynamic.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            **Example 1.** Gets storage format of forte:

            ::

                >>> dynamic = Dynamic('f')
                >>> print(format(dynamic))
                indicatortools.Dynamic(
                    name='f',
                    )

        ..  container:: example

            **Example 2.** Gets LilyPond format of forte:

            ::

                >>> dynamic = Dynamic('f')
                >>> print(format(dynamic, 'lilypond'))
                \f

        Returns string.
        '''
        if format_specification == 'lilypond':
            if self.name == 'niente':
                return ''
            elif self.name not in self._lilypond_dynamic_commands:
                message = 'dynamic name {!r} is not a LilyPond dynamic command.'
                message = message.format(self.name)
                raise Exception(message)
            return self._lilypond_format
        superclass = super(Dynamic, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, component_expression):
        from abjad.tools import scoretools
        if not isinstance(component_expression, scoretools.Leaf):
            return False
        if self.name not in self._lilypond_dynamic_commands:
            return False
        return True

    ### PUBLIC METHODS ###

    @staticmethod
    def composite_dynamic_name_to_steady_state_dynamic_name(name):
        r'''Changes composite `name` to steady state dynamic name.

        ..  container:: example

            **Example 1.** Steady state of sfp is piano:

            ::

                >>> Dynamic.composite_dynamic_name_to_steady_state_dynamic_name('sfp')
                'p'

        ..  container:: example

            **Example 2.** Steady state of rfz is forte:

            ::

                >>> Dynamic.composite_dynamic_name_to_steady_state_dynamic_name('rfz')
                'f'

        Returns string.
        '''
        return Dynamic._composite_dynamic_name_to_steady_state_dynamic_name[
            name]

    @staticmethod
    def dynamic_name_to_dynamic_ordinal(name):
        r'''Changes `name` to dynamic ordinal.

        ..  container:: example

            **Example 1.** Louder dynamics change to positive integers:

            ::

                >>> Dynamic.dynamic_name_to_dynamic_ordinal('fff')
                4

        ..  container:: example

            **Example 2.** Niente changes to negative infinity:

            ::

                >>> Dynamic.dynamic_name_to_dynamic_ordinal('niente')
                NegativeInfinity

        Returns integer or negative infinity.
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

        ..  container:: example

            **Example 1.** Negative values change to quiet dynamics:

            ::

                >>> Dynamic.dynamic_ordinal_to_dynamic_name(-5)
                'pppp'

        ..  container:: example

            **Example 2.** Negative infinity changes to niente:

            ::

                >>> negative_infinity = mathtools.NegativeInfinity()
                >>> Dynamic.dynamic_ordinal_to_dynamic_name(negative_infinity)
                'niente'

        Returns string.
        '''
        if dynamic_ordinal == mathtools.NegativeInfinity():
            return 'niente'
        else:
            return Dynamic._dynamic_ordinal_to_dynamic_name[dynamic_ordinal]

    @staticmethod
    def is_dynamic_name(arg):
        r'''Is true when `arg` is dynamic name. Otherwise false.

        ..  container:: example

            **Example 1.** Some usual dynamic names:

            ::

                >>> Dynamic.is_dynamic_name('f')
                True

            ::

                >>> Dynamic.is_dynamic_name('sfz')
                True

        ..  container:: example

            **Example 2.** Niente is also a dynamic name:

            ::

                >>> Dynamic.is_dynamic_name('niente')
                True

        Returns true or false.
        '''
        return arg in Dynamic._dynamic_names

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self._name)

    @property
    def _lilypond_format(self):
        return r'\{}'.format(self.name)

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of dynamic.

        ..  container:: example

            **Example 1.** Forte:

            ::

                >>> dynamic = Dynamic('f')
                >>> dynamic.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        ..  container:: example

            **Example 2.** Piano:

            ::

                >>> dynamic = Dynamic('p')
                >>> dynamic.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        Dynamics are staff-scoped by default.

        Returns staff.
        '''
        return self._default_scope

    @property
    def name(self):
        r'''Gets name of dynamic.

        ..  container:: example

            **Example 1.** Forte:

            ::

                >>> Dynamic('f').name
                'f'

        ..  container:: example

            **Example 2.** Piano:

            ::

                >>> Dynamic('p').name
                'p'

        ..  container:: example

            **Example 3.** Double sforzando:

            ::

                >>> Dynamic('sffz').name
                'sffz'

        ..  container:: example

            **Example 4.** Double sforzando-piano:

            ::

                >>> Dynamic('sffp').name
                'sffp'

        Returns string.
        '''
        return self._name

    @property
    def ordinal(self):
        r'''Gets ordinal value of dynamic.

        ..  container:: example

            **Example 1.** Forte:

            ::

                >>> Dynamic('f').ordinal
                2

        ..  container:: example

            **Example 2.** Piano:

            ::

                >>> Dynamic('p').ordinal
                -2

        Returns integer.
        '''
        name = self.name
        if name in self._composite_dynamic_name_to_steady_state_dynamic_name:
            name = self._composite_dynamic_name_to_steady_state_dynamic_name[
                name]
        ordinal = self._dynamic_name_to_dynamic_ordinal[name]
        return ordinal
