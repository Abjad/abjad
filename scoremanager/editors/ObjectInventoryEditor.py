# -*- encoding: utf-8 -*-
from scoremanager.editors.ListEditor import ListEditor


class ObjectInventoryEditor(ListEditor):
    r'''ObjectInventory editor.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
    )
    
    ### PUBLIC PROPERTIES ###

    @property
    def _target_name(self):
        if self.target is not None:
            return 'edit'

    @property
    def _target_summary_lines(self):
        result = []
        if self.target is not None:
            for item in self.target:
                result.append(repr(item))
        return result