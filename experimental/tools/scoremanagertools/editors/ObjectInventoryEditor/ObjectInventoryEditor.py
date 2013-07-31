# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.editors.ListEditor import ListEditor


class ObjectInventoryEditor(ListEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_name(self):
        if self.target is not None:
            return self.target.name
