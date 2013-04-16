from experimental.tools.scoremanagementtools.editors.ListEditor import ListEditor


class ObjectInventoryEditor(ListEditor):

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def target_name(self):
        if self.target is not None:
            return self.target.name
