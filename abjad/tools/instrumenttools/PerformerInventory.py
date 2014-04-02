# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class PerformerInventory(TypedList):
    r'''Abjad model of an ordered list of performers.

    Performer inventories implement the list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _item_creator_class(self):
        from scoremanager import wizards
        return wizards.PerformerCreationWizard

    @property
    def _item_creator_class_kwargs(self):
        return {'is_ranged': True}