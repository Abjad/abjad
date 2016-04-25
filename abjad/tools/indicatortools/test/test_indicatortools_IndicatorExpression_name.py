# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_IndicatorExpression_name_01():
    component = Note("c'4")
    articulation = Articulation('accent', Up)
    attach(articulation, component)
    indicator_expression = inspect_(component).get_indicators(unwrap=False)[0]
    assert indicator_expression.name is None


def test_indicatortools_IndicatorExpression_name_02():
    component = Note("c'4")
    articulation = Articulation('accent', Up)
    attach(articulation, component, name='foo')
    indicator_expression = inspect_(component).get_indicators(unwrap=False)[0]
    assert indicator_expression.name == 'foo'


def test_indicatortools_IndicatorExpression_name_03():
    leaf_a = Note("c'4")
    articulation = Articulation('accent', Up)
    attach(articulation, leaf_a)
    indicator_expression_a = inspect_(leaf_a).get_indicators(unwrap=False)[0]
    assert indicator_expression_a.name is None
    leaf_b = Note("g'4")
    attach(indicator_expression_a, leaf_b)
    indicator_expression_b = inspect_(leaf_b).get_indicators(unwrap=False)[0]
    assert indicator_expression_a is not indicator_expression_b
    assert indicator_expression_b.name is None


def test_indicatortools_IndicatorExpression_name_04():
    leaf_a = Note("c'4")
    articulation = Articulation('accent', Up)
    attach(articulation, leaf_a, name='foo')
    indicator_expression_a = inspect_(leaf_a).get_indicators(unwrap=False)[0]
    assert indicator_expression_a.name == 'foo'
    leaf_b = Note("g'4")
    attach(indicator_expression_a, leaf_b)
    indicator_expression_b = inspect_(leaf_b).get_indicators(unwrap=False)[0]
    assert indicator_expression_a is not indicator_expression_b
    assert indicator_expression_b.name == 'foo'


def test_indicatortools_IndicatorExpression_name_05():
    leaf_a = Note("c'4")
    articulation = Articulation('accent', Up)
    attach(articulation, leaf_a, name='foo')
    indicator_expression_a = inspect_(leaf_a).get_indicators(unwrap=False)[0]
    assert indicator_expression_a.name == 'foo'
    leaf_b = Note("g'4")
    attach(indicator_expression_a, leaf_b, name='bar')
    indicator_expression_b = inspect_(leaf_b).get_indicators(unwrap=False)[0]
    assert indicator_expression_a is not indicator_expression_b
    assert indicator_expression_b.name == 'bar'
