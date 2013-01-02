from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTTOCDirective(ReSTDirective):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def directive(self):
        return 'toc'

    @property
    def node_klass(self):
        from abjad.tools import documentationtools
        return (
            documentationtools.ReSTTOCItem,
            )
