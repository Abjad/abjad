# -*- encoding: utf-8 -*-
from scoremanager.editors.ListEditor import ListEditor


class ObjectInventoryEditor(ListEditor):
    r'''ObjectInventory editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        if self.target is not None:
            return 'edit'

    @property
    def target_summary_lines(self):
        result = []
        for item in self.target:
            result.append(repr(item))
        return result
