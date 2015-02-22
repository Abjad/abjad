# -*- encoding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadValueObject


class PostscriptOperator(AbjadValueObject):
    r'''A Postscript operator.

    ..  container:: example

        ::

            >>> operator = markuptools.PostscriptOperator('rmoveto', 1, 1.5)
            >>> print(format(operator))
            markuptools.PostscriptOperator('rmoveto', 1, 1.5)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_arguments',
        )

    ### INITIALIZER ###

    def __init__(self, name='stroke', *arguments):
        name = str(name)
        self._name = name
        if arguments:
            self._arguments = tuple(arguments)
        else:
            self._arguments = None

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of Postscript operator.

        ::

            >>> operator = markuptools.PostscriptOperator('rmoveto', 1, 1.5)
            >>> str(operator)
            '1 1.5 rmoveto'

        Returns string.
        '''
        def recurse(arguments):
            parts = []
            for argument in arguments:
                if isinstance(argument, (int, float, str)):
                    parts.append(str(argument))
                elif isinstance(argument, collections.Sequence):
                    parts.append('[')
                    parts.extend(recurse(argument))
                    parts.append(']')
                else:
                    raise ValueError(argument)
            return parts
        parts = []
        if self.arguments:
            parts.extend(recurse(self.arguments))
        parts.append(self.name)
        return ' '.join(parts)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        arguments = self.arguments or ()
        positional_argument_values = (self.name,) + arguments
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        r'''Gets Postscript operator name.

        Returns string.
        '''
        return self._name

    @property
    def arguments(self):
        r'''Gets Postscript operator arguments.

        Returns tuple or none.
        '''
        return self._arguments