# -*- encoding: utf-8 -*-
import abc
import operator
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Inequality(AbjadValueObject):
    '''An inequality.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_operator_string',
        '_operator_function',
        )

    _operator_strings = (
        '!=',
        '<',
        '<=',
        '==',
        '>',
        '>=',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        operator_string='<',
        ):
        assert operator_string in self._operator_strings
        self._operator_string = operator_string
        self._operator_function = {
            '!=': operator.ne,
            '<': operator.lt,
            '<=': operator.le,
            '==': operator.eq,
            '>': operator.gt,
            '>=': operator.ge,
            }[self._operator_string]

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, expr):
        r'''Calls inequality on `expr`.

        Returns boolean.
        '''
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def operator_string(self):
        r'''Gets operator string.

        Returns string.
        '''
        return self._operator_string