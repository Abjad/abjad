# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools.Selection import Selection


class MutationInterface(Selection):
    r'''The Abjad mutators defined against a single component.
    '''

    ### PUBLIC METHODS ###

    def splice(
        self,
        components,
        direction=Right,
        grow_spanners=True,
        ):
        r'''Splices `components` to the right or left of selection.

        Returns list of components.
        '''
        if direction == Right:
            reference_component = self[-1]
        else:
            reference_component = self[0]
        return reference_component._splice(
            components,
            direction=direction, 
            grow_spanners=grow_spanners,
            )
