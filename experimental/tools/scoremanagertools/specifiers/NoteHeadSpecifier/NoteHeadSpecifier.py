# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.specifiers.ParameterSpecifier \
    import ParameterSpecifier


class NoteHeadSpecifier(ParameterSpecifier):

    ### INITIALIZER ###

    def __init__(
        self,
        description=None,
        note_head_handler_name=None,
        custom_identifier=None,
        source=None,
        ):
        ParameterSpecifier.__init__(
            self,
            description=description,
            custom_identifier=custom_identifier,
            source=source,
            )
        self.note_head_handler_name = note_head_handler_name

    ### PRIVATE PROPERITES ###

    @property
    def _one_line_menuing_summary(self):
        return self.custom_identifier or self.note_head_handler_name
