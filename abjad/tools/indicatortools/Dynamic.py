# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Dynamic(AbjadValueObject):
    r'''Dynamic.

    ::

        >>> import abjad

    ..  container:: example

        Initializes from dynamic name:

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> dynamic = abjad.Dynamic('f')
            >>> abjad.attach(dynamic, staff[0])

        ..  docs::

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

        Initializes from other dynamic:

        ::

            >>> dynamic_1 = abjad.Dynamic('f')
            >>> dynamic_2 = abjad.Dynamic(dynamic_1)

        ::

            >>> dynamic_1
            Dynamic('f')

        ::

            >>> dynamic_2
            Dynamic('f')

    ..  container:: example

        Niente is possible, but provides no formatting.

        ::

            >>> dynamic = abjad.Dynamic('niente')
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
        'sfffz',
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

            Gets storage format of forte:

            ::

                >>> dynamic = abjad.Dynamic('f')
                >>> print(format(dynamic))
                abjad.Dynamic('f')

        ..  container:: example

            Gets LilyPond format of forte:

            ::

                >>> dynamic = abjad.Dynamic('f')
                >>> print(format(dynamic, 'lilypond'))
                \f

        Returns string.
        '''
        if format_specification == 'lilypond':
            if self.name == 'niente':
                return ''
            elif self.name not in self._lilypond_dynamic_commands:
                message = '{!r} is not a LilyPond dynamic command.'
                message = message.format(self.name)
                raise Exception(message)
            return self._get_lilypond_format()
        superclass = super(Dynamic, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self._name)

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, component_expression):
        from abjad.tools import scoretools
        if not isinstance(component_expression, scoretools.Leaf):
            return False
        if self.name not in self._lilypond_dynamic_commands:
            return False
        return True

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            self,
            repr_is_indented=False,
            storage_format_args_values=[self.name],
            storage_format_is_indented=False,
            )

    def _get_lilypond_format(self):
        return r'\{}'.format(self.name)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.right.articulations.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def composite_dynamic_name_to_steady_state_dynamic_name(name):
        r'''Changes composite `name` to steady state dynamic name.

        ..  container:: example

            Steady state of sfp is piano:

            ::

                >>> abjad.Dynamic.composite_dynamic_name_to_steady_state_dynamic_name('sfp')
                'p'

        ..  container:: example

            Steady state of rfz is forte:

            ::

                >>> abjad.Dynamic.composite_dynamic_name_to_steady_state_dynamic_name('rfz')
                'f'

        Returns string.
        '''
        return Dynamic._composite_dynamic_name_to_steady_state_dynamic_name[
            name]

    @staticmethod
    def dynamic_name_to_dynamic_ordinal(name):
        r'''Changes `name` to dynamic ordinal.

        ..  container:: example

            Louder dynamics change to positive integers:

            ::

                >>> abjad.Dynamic.dynamic_name_to_dynamic_ordinal('fff')
                4

        ..  container:: example

            Niente changes to negative infinity:

            ::

                >>> abjad.Dynamic.dynamic_name_to_dynamic_ordinal('niente')
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

            Negative values change to quiet dynamics:

            ::

                >>> abjad.Dynamic.dynamic_ordinal_to_dynamic_name(-5)
                'pppp'

        ..  container:: example

            Negative infinity changes to niente:

            ::

                >>> negative_infinity = abjad.mathtools.NegativeInfinity()
                >>> abjad.Dynamic.dynamic_ordinal_to_dynamic_name(negative_infinity)
                'niente'

        Returns string.
        '''
        if dynamic_ordinal == mathtools.NegativeInfinity():
            return 'niente'
        else:
            return Dynamic._dynamic_ordinal_to_dynamic_name[dynamic_ordinal]

    @staticmethod
    def is_dynamic_name(argument):
        r'''Is true when `argument` is dynamic name. Otherwise false.

        ..  container:: example

            Some usual dynamic names:

            ::

                >>> abjad.Dynamic.is_dynamic_name('f')
                True

            ::

                >>> abjad.Dynamic.is_dynamic_name('sfz')
                True

        ..  container:: example

            Niente is also a dynamic name:

            ::

                >>> abjad.Dynamic.is_dynamic_name('niente')
                True

        Returns true or false.
        '''
        return argument in Dynamic._dynamic_names

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of dynamic.

        ..  container:: example

            Forte:

            ::

                >>> dynamic = abjad.Dynamic('f')
                >>> dynamic.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        ..  container:: example

            Piano:

            ::

                >>> dynamic = abjad.Dynamic('p')
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

            Forte:

            ::

                >>> abjad.Dynamic('f').name
                'f'

        ..  container:: example

            Piano:

            ::

                >>> abjad.Dynamic('p').name
                'p'

        ..  container:: example

            Double sforzando:

            ::

                >>> abjad.Dynamic('sffz').name
                'sffz'

        ..  container:: example

            Double sforzando-piano:

            ::

                >>> abjad.Dynamic('sffp').name
                'sffp'

        Returns string.
        '''
        return self._name

    @property
    def ordinal(self):
        r'''Gets ordinal value of dynamic.

        ..  container:: example

            Forte:

            ::

                >>> abjad.Dynamic('f').ordinal
                2

        ..  container:: example

            Piano:

            ::

                >>> abjad.Dynamic('p').ordinal
                -2

        Returns integer.
        '''
        name = self.name
        if name in self._composite_dynamic_name_to_steady_state_dynamic_name:
            name = self._composite_dynamic_name_to_steady_state_dynamic_name[
                name]
        ordinal = self._dynamic_name_to_dynamic_ordinal[name]
        return ordinal
