# -*- coding: utf-8 -*-
import functools
import inspect
from abjad.tools.abctools import AbjadObject


class Callback(AbjadObject):
    r'''Callback.

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

        **Example 3.** Function callback with arguments:

        ::

            >>> callback = expressiontools.Callback(
            ...     name='sequencetools.flatten_sequence',
            ...     arguments={'depth': 1},
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
        '_arguments',
        '_module_names',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        arguments=None,
        module_names=None,
        ):
        from abjad.tools import datastructuretools
        if name is not None:
            assert isinstance(name, str), repr(name)
        self._name = name
        if arguments is not None:
            arguments = dict(arguments)
            arguments = list(sorted(arguments.items()))
            datastructuretools.TypedOrderedDict(arguments)
        self._arguments = arguments
        self._module_names = module_names

    ### SPECIAL METHODS ###

    def __call__(self, *args, **kwargs):
        r'''Calls callback on `args` and `kwargs`.

        Returns object.
        '''
        import abjad
        globals_ = {}
        globals_.update(abjad.__dict__.copy())
        try:
            import experimental
            globals_.update(experimental.__dict__.copy())
        except ImportError:
            pass
        globals_['functools'] = functools
        module_names = self.module_names or ()
        for module_name in module_names:
            module = __import__(module_name)
            globals_[module_name] = module
        arguments = []
        if self.arguments:
            for key, value in self.arguments:
                if (inspect.isclass(value) and
                    not value.__name__ in globals_):
                    globals_[value.__name__] = value
                if '<' in repr(value) and '>' in repr(value):
                    value = value.__name__
                else:
                    value = repr(value)
                argument = '{}={}'
                argument = argument.format(key, value)
                arguments.append(argument)
        arguments = ', '.join(arguments)
        string = 'functools.partial({}, {})'
        string = string.format(self.name, arguments)
        partial = eval(string, globals_)
        result = partial(*args, **kwargs)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self):
        r'''Gets arguments of callback.

        Set to dictionary or none.

        Defaults to none.

        Returns dictionary or none.
        '''
        return self._arguments

    @property
    def module_names(self):
        r'''Gets module names of callback.

        Set to strings or none.

        Defaults to none.

        Returns strings or none.
        '''
        return self._module_names

    @property
    def name(self):
        r'''Gets name of callback.

        Set to string.

        Returns string.
        '''
        return self._name
