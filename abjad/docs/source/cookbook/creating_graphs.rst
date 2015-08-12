Creating graphs
===============

..  abjad::

    lilypond_graph = documentationtools.GraphvizGraph(
        attributes={
            'bgcolor': 'transparent',
            'color': 'lightslategrey',
            'fontname': 'Arial',
            'outputorder': 'edgesfirst',
            'overlap': 'prism',
            'penwidth': 2,
            'splines': 'spline',
            'style': ('dotted', 'rounded'),
            'truecolor': True,
            },
        edge_attributes={
            'color': 'lightsteelblue2',
            'penwidth': 2,
            },
        node_attributes={
            'colorscheme': 'pastel19',
            'fontname': 'Arial',
            'fontsize': 12,
            'penwidth': 2,
            'shape': 'oval',
            'style': ('bold', 'filled', 'rounded'),
            },
        )

..  abjad::

    context_mapping = {}
    all_contexts = lilypondnametools.LilyPondContext.list_all_contexts()
    for i, context in enumerate(all_contexts):
        fillcolor = i % 9 + 1
        name = context.name.replace('-', '_')
        label = r'\n'.join(name.split('_'))
        node_attributes = {
            'fillcolor': fillcolor,
            'label': label,
            }
        node = documentationtools.GraphvizNode(
            name=name,
            attributes=node_attributes,
            )
        context_mapping[context] = node
        lilypond_graph.append(node)

..  abjad::

    for parent_context, parent_node in context_mapping.items():
        for child_context in parent_context.accepts:
            child_node = context_mapping[child_context]
            edge = documentationtools.GraphvizEdge()
            if (
                parent_context.default_child is not None and 
                child_context is parent_context.default_child
                ):
                edge.attributes['color'] = 'black'
            edge.attach(parent_node, child_node)

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(lilypond_graph)
