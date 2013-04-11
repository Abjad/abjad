from experimental.tools.scftools.specifiers.ParameterSpecifier import ParameterSpecifier


class NoteHeadSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(self, description=None, note_head_handler_name=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.note_head_handler_name = note_head_handler_name

    ### READ-ONLY PROPERITES ###

    @property
    def one_line_menuing_summary(self):
        return self.name or self.note_head_handler_name
