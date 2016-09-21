# -*- coding: utf-8 -*-
from abjad.tools import systemtools
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
        from abjad.tools import markuptools
        parts = []
        if self.arguments:
            for argument in self.arguments:
                parts.append(markuptools.Postscript._format_argument(argument))
        parts.append(self.name)
        string = ' '.join(parts)
        return string

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.name] + list(self.arguments or ())
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self):
        r'''Gets Postscript operator arguments.

        Returns tuple or none.
        '''
        return self._arguments

    @property
    def name(self):
        r'''Gets Postscript operator name.

        Returns string.
        '''
        return self._name
