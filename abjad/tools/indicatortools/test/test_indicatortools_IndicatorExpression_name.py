# -*- coding: utf-8 -*-
import abjad


def test_indicatortools_IndicatorExpression_name_01():
    component = abjad.Note("c'4")
    articulation = abjad.Articulation('accent', Up)
    abjad.attach(articulation, component)
    indicator_expression = abjad.inspect(component).get_indicators(unwrap=False)[0]
    assert indicator_expression.name is None


def test_indicatortools_IndicatorExpression_name_02():
    component = abjad.Note("c'4")
    articulation = abjad.Articulation('accent', Up)
    abjad.attach(articulation, component, name='foo')
    indicator_expression = abjad.inspect(component).get_indicators(unwrap=False)[0]
    assert indicator_expression.name == 'foo'


def test_indicatortools_IndicatorExpression_name_03():
    leaf_a = abjad.Note("c'4")
    articulation = abjad.Articulation('accent', Up)
    abjad.attach(articulation, leaf_a)
    indicator_expression_a = abjad.inspect(leaf_a).get_indicators(unwrap=False)[0]
    assert indicator_expression_a.name is None
    leaf_b = abjad.Note("g'4")
    abjad.attach(indicator_expression_a, leaf_b)
    indicator_expression_b = abjad.inspect(leaf_b).get_indicators(unwrap=False)[0]
    assert indicator_expression_a is not indicator_expression_b
    assert indicator_expression_b.name is None


def test_indicatortools_IndicatorExpression_name_04():
    leaf_a = abjad.Note("c'4")
    articulation = abjad.Articulation('accent', Up)
    abjad.attach(articulation, leaf_a, name='foo')
    indicator_expression_a = abjad.inspect(leaf_a).get_indicators(unwrap=False)[0]
    assert indicator_expression_a.name == 'foo'
    leaf_b = abjad.Note("g'4")
    abjad.attach(indicator_expression_a, leaf_b)
    indicator_expression_b = abjad.inspect(leaf_b).get_indicators(unwrap=False)[0]
    assert indicator_expression_a is not indicator_expression_b
    assert indicator_expression_b.name == 'foo'


def test_indicatortools_IndicatorExpression_name_05():
    leaf_a = abjad.Note("c'4")
    articulation = abjad.Articulation('accent', Up)
    abjad.attach(articulation, leaf_a, name='foo')
    indicator_expression_a = abjad.inspect(leaf_a).get_indicators(unwrap=False)[0]
    assert indicator_expression_a.name == 'foo'
    leaf_b = abjad.Note("g'4")
    abjad.attach(indicator_expression_a, leaf_b, name='bar')
    indicator_expression_b = abjad.inspect(leaf_b).get_indicators(unwrap=False)[0]
    assert indicator_expression_a is not indicator_expression_b
    assert indicator_expression_b.name == 'bar'
