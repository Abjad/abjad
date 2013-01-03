import hashlib
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive
from abjad.docs.source._ext.abjad_book import \
    visit_abjad_book_html, visit_abjad_book_latex



class InheritanceException(Exception):
    pass


class abjad_lineage(nodes.General, nodes.Element):
    pass


class AbjadLineage(Directive):

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    def run(self):
        from abjad.tools import documentationtools

        node = abjad_lineage()
        node.document = self.state.document
        env = self.state.document.settings.env
        parts = self.arguments[0].rpartition('.')
        module_name, class_name = parts[0], parts[2]

        # Create a graph starting with the list of classes
        try:
            if module_name.startswith('abjad'):
                addresses = ('abjad',)
            elif module_name.startswith('experimental'):
                addresses = ('abjad', 'experimental')
            else:
                raise InheritanceException(
                    'Could not import class {!r} specified for '
                    'inheritance diagram'.format(self.arguments[0]))
            lineage = documentationtools.InheritanceGraph(
                addresses=addresses,
                lineage_addresses=((module_name, class_name),)
                ) 
        except InheritanceException, err:
            return [node.document.reporter.warning(err.args[0],
                                                   line=self.lineno)]

        node['code'] = lineage.graphviz_format
        node['kind'] = 'graphviz'
        node['linked'] = True

        return [node]


def skip(self, node):
    raise nodes.SkipNode


def setup(app):
    app.setup_extension('sphinx.ext.graphviz')
    app.add_node(
        abjad_lineage,
        latex=(visit_abjad_book_latex, None),
        html=(visit_abjad_book_html, None),
        text=(skip, None),
        man=(skip, None),
        texinfo=(skip, None))
    app.add_directive('abjad-lineage', AbjadLineage)
