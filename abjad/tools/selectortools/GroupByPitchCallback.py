# -*- coding: utf-8 -*-
import collections
from abjad.tools import datastructuretools
from abjad.tools import mathtools
from abjad.tools import selectiontools
from abjad.tools.abctools import AbjadValueObject


class GroupByPitchCallback(AbjadValueObject):
    r'''Group-by-pitch selector callback.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_allow_discontiguity',
        )

    ### INITIALIZER ###

    def __init__(self, allow_discontiguity=False):
        if allow_discontiguity is not None:
            allow_discontiguity = bool(allow_discontiguity)
        self._allow_discontiguity = allow_discontiguity

    ### SPECIAL METHODS ###

    def __call__(
        self,
        argument,
        rotation=None,
        ):
        r'''Calls selector callback on iterable `argument`.

        Returns tuple of selections.
        '''
        import abjad
        assert isinstance(argument, collections.Iterable), repr(argument)
        if len(argument) == 1 and isinstance(argument[0], abjad.Selection):
            selection = argument[0]
        else:
            selection = abjad.select(argument)
        selections = selection.group_by(self._get_written_pitches)
        selections = self._map_contiguity(selections)
        selections = [selectiontools.Selection(_) for _ in selections]
        return tuple(selections)
    
    ### PRIVATE METHODS ###

    @staticmethod
    def _get_written_pitches(argument):
        import abjad
        if isinstance(argument, abjad.Note):
            return argument.written_pitch
        elif isinstance(argument, abjad.Chord):
            return argument.written_pitches
        elif (isinstance(argument, abjad.selectiontools.LogicalTie) and
            isinstance(argument.head, abjad.Note)):
            return argument.head.written_pitch
        elif (isinstance(argument, abjad.selectiontools.LogicalTie) and
            isinstance(argument.head, abjad.Chord)):
            return argument.head.written_pitches
        else:
            return None

    def _map_contiguity(self, selections):
        from abjad.tools import selectortools
        if self.allow_discontiguity:
            return selections
        selector = selectortools.ContiguitySelectorCallback()
        result = []
        for selection in selections:
            parts = selector(selection)
            result.extend(parts)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def allow_discontiguity(self):
        r'''Is true when selector allow discontiguity.

        Otherwise selector further groups by contiguity.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._allow_discontiguity
