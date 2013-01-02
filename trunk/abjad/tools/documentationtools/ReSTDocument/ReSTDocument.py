from abjad.tools.datastructuretools.TreeContainer import TreeContainer


class ReSTDocument(TreeContainer):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def node_klass(self):
        from abjad.tools import documentationtools
        return (
            documentationtools.ReSTDirective, 
            documentationtools.ReSTHeading, 
            documentationtools.ReSTHorizontalRule, 
            documentationtools.ReSTParagraph,
            )
