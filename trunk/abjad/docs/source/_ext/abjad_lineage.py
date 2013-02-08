import importlib
import pickle
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
            # The following is a hack.
            # We need to guarantee that everything is imported before
            # the first diagram in the entire document is drawn,
            # otherwise the InheritanceGraph doesn't see anything... why?
            module = importlib.import_module(module_name)
            #lineage = documentationtools.InheritanceGraph(
            #    addresses=addresses,
            #    lineage_addresses=((module_name, class_name),)
            #    ) 
            lineage = documentationtools.InheritanceGraph(
                addresses=addresses,
                lineage_addresses=((module_name, class_name),)
                ) 
            graph = lineage.graphviz_graph

        except InheritanceException, err:
            return [node.document.reporter.warning(err.args[0],
                                                   line=self.lineno)]

        maximum_node_count = 30

        # begin pruning
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=addresses,
                lineage_addresses=((module_name, class_name),),
                lineage_prune_distance=2,
                )
            graph = lineage.graphviz_graph

        # keep pruning if still too many nodes
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=addresses,
                lineage_addresses=((module_name, class_name),),
                lineage_prune_distance=1,
                )
            graph = lineage.graphviz_graph

        # finally, revert to subclass-less version if still too many nodes
        if maximum_node_count < len(graph.leaves):
            lineage = documentationtools.InheritanceGraph(
                addresses=((module_name, class_name),),
                )
            
            def get_node_name(original_name):
                parts = original_name.split('.')
                name = [parts[0]]
                for part in parts[1:]:
                    if part != name[-1]:
                        name.append(part)
                if name[0] in ('abjad', 'experimental'):
                    return str('.'.join(name[2:]))
                return str('.'.join(name))

            node_name = get_node_name(module_name + '.' + class_name)
            graph = lineage.graphviz_graph
            graph_node = graph[node_name]
            graph_node.attributes['color'] = 'black'
            graph_node.attributes['fontcolor'] = 'white'
            graph_node.attributes['style'] = ('filled', 'rounded')

        node['code'] = pickle.dumps(graph)
        node['kind'] = 'graphviz'
        node['is_pickled'] = True
        node['keep_original'] = True

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
