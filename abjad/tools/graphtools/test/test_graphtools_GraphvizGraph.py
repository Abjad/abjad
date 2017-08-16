import abjad


def test_graphtools_GraphvizGraph_01():

    graph = abjad.graphtools.GraphvizGraph()
    graph.node_attributes['shape'] = 'record'

    struct_1 = abjad.graphtools.GraphvizNode()
    struct_1_field_0 = abjad.graphtools.GraphvizField(label='left')
    struct_1.append(struct_1_field_0)
    struct_1_field_1 = abjad.graphtools.GraphvizField(label='middle')
    struct_1.append(struct_1_field_1)
    struct_1_field_2 = abjad.graphtools.GraphvizField(label='right')
    struct_1.append(struct_1_field_2)

    struct_2 = abjad.graphtools.GraphvizNode()
    struct_2_field_0 = abjad.graphtools.GraphvizField(label='one')
    struct_2.append(struct_2_field_0)
    struct_2_field_1 = abjad.graphtools.GraphvizField(label='two')
    struct_2.append(struct_2_field_1)

    struct_3 = abjad.graphtools.GraphvizNode()
    struct_3_field_hello = abjad.graphtools.GraphvizField(
        label='hello')
    struct_3.append(struct_3_field_hello)
    outer_group = abjad.graphtools.GraphvizGroup()
    struct_3.append(outer_group)
    struct_3_field_b = abjad.graphtools.GraphvizField(label='b')
    outer_group.append(struct_3_field_b)
    inner_group = abjad.graphtools.GraphvizGroup()
    outer_group.append(inner_group)
    struct_3_field_c = abjad.graphtools.GraphvizField(label='c')
    inner_group.append(struct_3_field_c)
    struct_3_field_d = abjad.graphtools.GraphvizField(label='d')
    inner_group.append(struct_3_field_d)
    struct_3_field_e = abjad.graphtools.GraphvizField(label='e')
    inner_group.append(struct_3_field_e)
    struct_3_field_f = abjad.graphtools.GraphvizField(label='f')
    outer_group.append(struct_3_field_f)
    struct_3_field_g = abjad.graphtools.GraphvizField(label='g')
    struct_3.append(struct_3_field_g)
    struct_3_field_h = abjad.graphtools.GraphvizField(label='h')
    struct_3.append(struct_3_field_h)

    graph.extend((struct_1, struct_2, struct_3))

    abjad.graphtools.GraphvizEdge().attach(
        struct_1_field_1,
        struct_2_field_0,
        )
    abjad.graphtools.GraphvizEdge().attach(
        struct_1_field_2,
        struct_3_field_d,
        )

    graphviz_format = str(graph)

    assert graphviz_format == abjad.String.normalize(
        '''
        digraph G {
            node [shape=record];
            node_0 [label="<f_0> left | <f_1> middle | <f_2> right"];
            node_1 [label="<f_0> one | <f_1> two"];
            node_2 [label="<f_0> hello | { <f_1_0> b | { <f_1_1_0> c | <f_1_1_1> d | <f_1_1_2> e } | <f_1_2> f } | <f_2> g | <f_3> h"];
            node_0:f_1 -> node_1:f_0;
            node_0:f_2 -> node_2:f_1_1_1;
        }
        '''
        )
