# -*- coding: utf-8 -*-
import copy
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.topleveltools import new


class Annotation(AbjadValueObject):
    r'''An annotation.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> pitch = NamedPitch('ds')
            >>> annotation = indicatortools.Annotation('modifier', pitch)
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
        '_default_scope',
        '_name',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(self, name='annotation', value=None):
        self._default_scope = None
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
    def default_scope(self):
        r'''Gets default scope of annotation.

        ..  container:: example

            ::

                >>> pitch = NamedPitch('ds')
                >>> annotation = indicatortools.Annotation('modifier', pitch)
                >>> annotation.default_scope is None
                True

        Annotations are not scoped.

        Returns none.
        '''
        return self._default_scope

    @property
    def name(self):
        r'''Gets name of annotation.

        ..  container:: example

            ::

                >>> pitch = NamedPitch('ds')
                >>> annotation = indicatortools.Annotation('modifier', pitch)
                >>> annotation.name
                'modifier'

        Returns string.
        '''
        return self._name

    @property
    def value(self):
        r'''Gest value of annotation.

        ..  container:: example

            ::

                >>> pitch = NamedPitch('ds')
                >>> annotation = indicatortools.Annotation('modifier', pitch)
                >>> annotation.value
                NamedPitch('ds')

        Returns arbitrary object.
        '''
        return self._value
