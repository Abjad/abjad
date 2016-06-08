Creating graphs
===============

Key points:

#. Build graphs from nodes, edges and subgraphs.
#. Learn about Abjad's model of LilyPond contexts.
#. Use mappings to coordinate between data structures.
#. Style and render graphs via Graphviz.

..  abjad::
    :hide:
    :reveal-label: summary
    :strip-prompt:

    def create_context_graph():
        # Create context graph with subgraphs and styling.
        context_graph = documentationtools.GraphvizGraph(
            name='All Contexts',
            children=[
                documentationtools.GraphvizSubgraph(name='Global Contexts'),
                documentationtools.GraphvizSubgraph(name='Score Contexts'),
                documentationtools.GraphvizSubgraph(name='StaffGroup Contexts'),
                documentationtools.GraphvizSubgraph(name='Staff Contexts'),
                documentationtools.GraphvizSubgraph(name='Bottom Contexts'),
                ],
            attributes=dict(
                bgcolor='transparent',
                color='lightslategrey',
                output_order='edgesfirst',
                overlap='prism',
                penwidth=2,
                root='Global',
                splines='spline',
                style=('dotted', 'rounded'),
                truecolor=True,
                ),
            edge_attributes=dict(
                color='lightsteelblue2',
                penwidth=2,
                ),
            node_attributes=dict(
                colorscheme='pastel19',
                fontname='Arial',
                fontsize=12,
                penwidth=2,
                shape='box',
                style=('bold', 'filled', 'rounded'),
                ),
            )
        # Build context mapping.
        context_mapping = {}
        for i, context in enumerate(lilypondnametools.LilyPondContext.list_all_contexts()):
            name = context.name
            fillcolor = i % 9 + 1
            label = r'\n'.join(stringtools.delimit_words(name))
            node_attributes = {'label': label}
            node = documentationtools.GraphvizNode(
                name=context.name,
                attributes=dict(fillcolor=fillcolor, label=label),
                )
            context_mapping[context] = node
            # Add context nodes to subgraphs.
            if context.is_global_context:
                context_graph['Global Contexts'].append(node)
            elif context.is_score_context:
                context_graph['Score Contexts'].append(node)
            elif context.is_staff_group_context:
                context_graph['StaffGroup Contexts'].append(node)
            elif context.is_staff_context:
                context_graph['Staff Contexts'].append(node)
            elif context.is_bottom_context:
                context_graph['Bottom Contexts'].append(node)
        # Attach edges.
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
        # All done!
        return context_graph

..  abjad::
    :hide:
    :no-resize:
    :no-trim:
    :with-thumbnail:

    context_graph = create_context_graph()
    graph(context_graph)

Graph basics
------------

..  abjad::

    my_graph = documentationtools.GraphvizGraph()

..  abjad::

    node_a = documentationtools.GraphvizNode(name='A', attributes={'label': 'A'})
    node_b = documentationtools.GraphvizNode(name='B', attributes={'label': 'B'})
    node_c = documentationtools.GraphvizNode(name='C', attributes={'label': 'C'})
    node_d = documentationtools.GraphvizNode(name='D', attributes={'label': 'D'})

..  abjad::

    my_graph.extend([node_a, node_b, node_c, node_d])
    graph(my_graph)

..  abjad::

    my_graph['B'].attributes['shape'] = 'diamond'
    graph(my_graph)

..  abjad::

    ab_edge = my_graph['A'].attach(my_graph['B'])
    bc_edge = my_graph['B'].attach(my_graph['C'])
    bd_edge = my_graph['B'].attach(my_graph['D'])
    graph(my_graph)

..  abjad::

    bc_edge.attributes['style'] = 'dotted'
    bd_edge.attributes['style'] = 'dashed'
    my_graph.attributes['bgcolor'] = 'transparent'
    my_graph.node_attributes.update(
        fontname='Arial',
        penwidth=2,
        )
    my_graph.edge_attributes.update(
        color='grey',
        penwidth=2,
        )
    graph(my_graph)
    print(format(my_graph, 'graphviz'))

Collecting data for the graph
-----------------------------

..  abjad::

    for context in lilypondnametools.LilyPondContext.list_all_contexts():
        print(context.name)
        for child_context in context.accepts:
            print('\t' + child_context.name)

Populating the graph
--------------------

..  abjad::

    context_graph = documentationtools.GraphvizGraph(name='All Contexts')

..  abjad::

    global_subgraph = documentationtools.GraphvizSubgraph(name='Global Contexts')
    score_subgraph = documentationtools.GraphvizSubgraph(name='Score Contexts')
    staff_group_subgraph = documentationtools.GraphvizSubgraph(name='StaffGroup Contexts')
    staff_subgraph = documentationtools.GraphvizSubgraph(name='Staff Contexts')
    bottom_subgraph = documentationtools.GraphvizSubgraph(name='Bottom Contexts')

..  abjad::

    context_graph.extend([
        global_subgraph,
        score_subgraph,
        staff_group_subgraph,
        staff_subgraph,
        bottom_subgraph,
        ])

..  abjad::

    context_mapping = {}
    for context in lilypondnametools.LilyPondContext.list_all_contexts():
        node = documentationtools.GraphvizNode(
            name=context.name,
            attributes={'label': context.name},
            )
        context_mapping[context] = node

..  abjad::

    for context, node in context_mapping.items():
        if context.is_global_context:
            global_subgraph.append(node)
        elif context.is_score_context:
            score_subgraph.append(node)
        elif context.is_staff_group_context:
            staff_group_subgraph.append(node)
        elif context.is_staff_context:
            staff_subgraph.append(node)
        elif context.is_bottom_context:
            bottom_subgraph.append(node)

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

Configuring the graph's attributes
----------------------------------

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(context_graph)

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(context_graph, layout='twopi')

..  abjad::

    context_graph.attributes.update(
        output_order='edgesfirst',
        overlap='prism',
        root='Global',
        splines='spline',
        )

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(context_graph)

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(context_graph, layout='twopi')

..  abjad::

    context_graph.attributes.update(
        bgcolor='transparent',
        color='lightslategrey',
        penwidth=2,
        style=('dotted', 'rounded'),
        truecolor=True,
        )

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(context_graph)

..  abjad::

    context_graph.edge_attributes.update(
        color='lightsteelblue2',
        penwidth=2,
        )

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(context_graph)

..  abjad::

    context_graph.node_attributes.update(
        fontname='Arial',
        fontsize=12,
        penwidth=2,
        shape='box',
        style=('bold', 'filled', 'rounded'),
        )

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(context_graph)

..  abjad::

    context_graph.node_attributes['colorscheme'] = 'pastel19'
    for i, node in enumerate(context_mapping.values()):
        fillcolor = i % 9 + 1
        node.attributes['fillcolor'] = fillcolor

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(context_graph)

..  abjad::

    for node in context_mapping.values():
        label = node.attributes['label']
        words = stringtools.delimit_words(label)
        node.attributes['label'] = r'\n'.join(words)

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(context_graph)

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    graph(context_graph, layout='twopi')

Putting it all together
-----------------------

..  reveal:: summary

..  abjad::
    :no-resize:
    :no-trim:
    :with-thumbnail:

    context_graph = create_context_graph()
    graph(context_graph)
