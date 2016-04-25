# -*- coding: utf-8 -*-
from abjad import documentationtools
from abjad import stringtools


def test_documentationtools_GraphvizGraph_01():

    graph = documentationtools.GraphvizGraph()
    graph.node_attributes['shape'] = 'record'

    struct_1 = documentationtools.GraphvizNode()
    struct_1_field_0 = documentationtools.GraphvizField(label='left')
    struct_1.append(struct_1_field_0)
    struct_1_field_1 = documentationtools.GraphvizField(label='middle')
    struct_1.append(struct_1_field_1)
    struct_1_field_2 = documentationtools.GraphvizField(label='right')
    struct_1.append(struct_1_field_2)

    struct_2 = documentationtools.GraphvizNode()
    struct_2_field_0 = documentationtools.GraphvizField(label='one')
    struct_2.append(struct_2_field_0)
    struct_2_field_1 = documentationtools.GraphvizField(label='two')
    struct_2.append(struct_2_field_1)

    struct_3 = documentationtools.GraphvizNode()
    struct_3_field_hello = documentationtools.GraphvizField(
        label='hello')
    struct_3.append(struct_3_field_hello)
    outer_group = documentationtools.GraphvizGroup()
    struct_3.append(outer_group)
    struct_3_field_b = documentationtools.GraphvizField(label='b')
    outer_group.append(struct_3_field_b)
    inner_group = documentationtools.GraphvizGroup()
    outer_group.append(inner_group)
    struct_3_field_c = documentationtools.GraphvizField(label='c')
    inner_group.append(struct_3_field_c)
    struct_3_field_d = documentationtools.GraphvizField(label='d')
    inner_group.append(struct_3_field_d)
    struct_3_field_e = documentationtools.GraphvizField(label='e')
    inner_group.append(struct_3_field_e)
    struct_3_field_f = documentationtools.GraphvizField(label='f')
    outer_group.append(struct_3_field_f)
    struct_3_field_g = documentationtools.GraphvizField(label='g')
    struct_3.append(struct_3_field_g)
    struct_3_field_h = documentationtools.GraphvizField(label='h')
    struct_3.append(struct_3_field_h)

    graph.extend((struct_1, struct_2, struct_3))

    documentationtools.GraphvizEdge().attach(
        struct_1_field_1,
        struct_2_field_0,
        )
    documentationtools.GraphvizEdge().attach(
        struct_1_field_2,
        struct_3_field_d,
        )

    graphviz_format = str(graph)

    assert graphviz_format == stringtools.normalize(
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
