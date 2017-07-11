# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class WrapSelectionCallback(AbjadValueObject):
    r'''Wrap selection callback.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_apply_to_each',
        )

    ### INITIALIZER ###

    def __init__(self, apply_to_each=None):
        self._apply_to_each = apply_to_each

    ### SPECIAL METHODS ###

    def __call__(self, argument, rotation=None):
        r'''Wraps `argument` in selection.

        Somewhat like the opposite of flattening.

        Ignores `rotation`.

        Returns tuple.
        '''
        import abjad
        if isinstance(argument, abjad.Component):
            return (argument,)
        elif isinstance(argument, abjad.Selection):
            if self.apply_to_each:
                selections = [abjad.select([_]) for _ in argument]
                return tuple(selections)
            else:
                selection = abjad.select([argument])
                return (selection,)
        elif isinstance(argument, tuple):
            if self.apply_to_each:
                selections = [abjad.select([_]) for _ in argument]
                return tuple(selections)
            else:
                selection = abjad.select(argument[:])
                return (selection,)
        else:
            message = 'neither component, selection nor tuple: {!r}.'
            message = message.format(argument)
            raise TypeError(message)

    ### PUBLIC PROPERTIES ###

    @property
    def apply_to_each(self):
        r'''Is true when selector maps.

        Returns true, false or none.
        '''
        return self._apply_to_each
