# -*- coding: utf-8 -*-
import functools
from abjad.tools.abctools import AbjadObject


class Callback(AbjadObject):
    r'''A callback.

    ..  container:: example

        **Example 1.** Built-in callback:

        ::

            >>> callback = expressiontools.Callback(name='int')

        ::

            >>> callback(99.25)
            99

        ::

            >>> print(format(callback))
            expressiontools.Callback(
                name='int',
                )

    ..  container:: example

        **Example 2.** Function callback:

        ::

            >>> callback = expressiontools.Callback(
            ...     name='sequencetools.flatten_sequence',
            ...     )

        ::

            >>> list_ = [1, 2, [3, [4]], 5]
            >>> callback(list_)
            [1, 2, 3, 4, 5]

    ..  container:: example

        **Example 3.** Function callback with keywords:

        ::

            >>> callback = expressiontools.Callback(
            ...     name='sequencetools.flatten_sequence',
            ...     keywords={'depth': 1},
            ...     )

        ::

            >>> list_ = [1, 2, [3, [4]], 5]
            >>> callback(list_)
            [1, 2, 3, [4], 5]

    ..  container:: example

        **Example 4.** Class callback:

        ::

            >>> callback = expressiontools.Callback(
            ...     name='Sequence',
            ...     )

        ::

            >>> list_ = [1, 2, [3, [4]], 5]
            >>> callback(list_)
            Sequence((1, 2, [3, [4]], 5))

    Initializer returns callback.

    Call returns object.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_keywords',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        keywords=None,
        ):
        from abjad.tools import datastructuretools
        if name is not None:
            assert isinstance(name, str), repr(name)
        self._name = name
        if keywords is not None:
            keywords = dict(keywords)
            keywords = list(sorted(keywords.items()))
            datastructuretools.TypedOrderedDict(keywords)
        self._keywords = keywords

    ### SPECIAL METHODS ###

    def __call__(self, *args, **kwargs):
        r'''Calls callback on `args` and `kwargs`.

        Returns object.
        '''
        import abjad
        import experimental
        arguments = []
        if self.keywords:
            for key, value in self.keywords:
                argument = '{}={!r}'
                argument = argument.format(key, value)
                arguments.append(argument)
        arguments = ', '.join(arguments)
        string = 'functools.partial({}, {})'
        string = string.format(self.name, arguments)
        globals_ = {}
        globals_.update(abjad.__dict__.copy())
        globals_.update(experimental.__dict__.copy())
        globals_['functools'] = functools
        partial = eval(string, globals_)
        result = partial(*args, **kwargs)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def keywords(self):
        r'''Gets keyword arguments of callback.

        Returns dictionary or none.
        '''
        return self._keywords

    @property
    def name(self):
        r'''Gets name of callback.

        Returns string.
        '''
        return self._name