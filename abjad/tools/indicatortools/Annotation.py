# -*- encoding: utf-8 -*-
import copy
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools import new


class Annotation(AbjadValueObject):
    r'''An annotation.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> pitch = NamedPitch('ds')
        >>> annotation = indicatortools.Annotation('special pitch', pitch)
        >>> attach(annotation, staff[0])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Annotations contribute no formatting.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(self, name='annotation', value=None):
        if isinstance(name, type(self)):
            expr = name
            name = expr.name
            value = value or expr.value
        name = copy.copy(name)
        value = copy.copy(value)
        self._name = name
        self._value = value

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        r'''Name of annotation.

        ::

            >>> annotation.name
            'special pitch'

        Returns string.
        '''
        return self._name

    @property
    def value(self):
        r'''Value of annotation.

        ::

            >>> annotation.value
            NamedPitch('ds')

        Returns arbitrary object.
        '''
        return self._value