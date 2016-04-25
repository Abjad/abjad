# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Expression(AbjadObject):
    r'''Expression.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_callbacks',
        '_client_class',
        )

    ### INITIALIZER ###

    def __init__(self, callbacks=None):
        if callbacks is not None:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks
        self._client_class = None

    ### PRIVATE METHODS ###

    def _append_callback(self, callback):
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def _make_callback(self, name, arguments=None, module_names=None):
        from abjad.tools import expressiontools
        callback = expressiontools.Callback(
            name=name,
            arguments=arguments,
            module_names=module_names,
            )
        return self._append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets callbacks.

        Returns tuple or none.
        '''
        return self._callbacks
