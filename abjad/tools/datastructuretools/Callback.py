# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Callback(AbjadObject):
    r'''A callback.

    ..  container:: example

        **Example 1.** Built-in callback:

        ::

            >>> callback = datastructuretools.Callback(
            ...     name='round',
            ...     arguments=(99.25,),
            ...     )

        ::

            >>> callback()
            99.0

        ::

            >>> print(format(callback))
            datastructuretools.Callback(
                name='round',
                arguments=datastructuretools.TypedTuple(
                    (99.25,)
                    ),
                )

    ..  container:: example

        **Example 2.** Function callback:

        ::

            >>> callback = datastructuretools.Callback(
            ...     name='sequencetools.flatten_sequence',
            ...     arguments=([1, 2, [3, [4]], 5],),
            ...     )

        ::

            >>> callback()
            [1, 2, 3, 4, 5]

    ..  container:: example

        **Example 3.** Function callback with keywords:

        ::

            >>> callback = datastructuretools.Callback(
            ...     name='sequencetools.flatten_sequence',
            ...     arguments=([1, 2, [3, [4]], 5],),
            ...     keywords={'depth': 1},
            ...     )

        ::

            >>> callback()
            [1, 2, 3, [4], 5]

    ..  container:: example

        **Example 4.** Class callback:

        ::

            >>> callback = datastructuretools.Callback(
            ...     name='Sequence',
            ...     arguments=(1, 2, [3, 4], 5),
            ...     )

        ::

            >>> callback()
            Sequence(1, 2, [3, 4], 5)

    Returns callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_arguments',
        '_keywords',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        arguments=None,
        keywords=None,
        ):
        from abjad.tools import datastructuretools
        if name is not None:
            assert isinstance(name, str), repr(name)
        self._name = name
        if arguments is not None:
            arguments = datastructuretools.TypedTuple(arguments)
        self._arguments = arguments
        if keywords is not None:
            keywords = dict(keywords)
            keywords = list(sorted(keywords.items()))
            datastructuretools.TypedOrderedDict(keywords)
        self._keywords = keywords

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls callback.
        '''
        import abjad
        items = []
        if self.arguments:
            items_ = [str(_) for _ in self.arguments]
            items.extend(items_)
        if self.keywords:
            for key, value in self.keywords:
                item = '{}={}'
                item = item.format(key, value)
                items.append(item)
        items = ', '.join(items)
        string = '{}({})'
        string = string.format(self.name, items)
        globals_ = abjad.__dict__.copy()
        result = eval(string, globals_)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self):
        r'''Gets positional argument values of callback.

        Returns tuple.
        '''
        return self._arguments

    @property
    def keywords(self):
        r'''Gets keyword argument names of callback.

        Returns tuple.
        '''
        return self._keywords

    @property
    def name(self):
        r'''Gets name of callback.

        Returns string.
        '''
        return self._name