# -*- encoding: utf-8 -*-
from scoremanager.idetools import predicates


def test_predicates_01():

    assert predicates.is_boolean(True)
    assert predicates.is_boolean(False)

    assert not predicates.is_boolean(None)
    assert not predicates.is_boolean('')
    assert not predicates.is_boolean(0)
    assert not predicates.is_boolean(1)


def test_predicates_02():

    assert predicates.is_identifier('foo_bar')
    assert predicates.is_identifier('FooBar')
    assert predicates.is_identifier('_foo_bar')
    assert predicates.is_identifier('__foo_bar')
    assert predicates.is_identifier('_')
    assert predicates.is_identifier('f')

    assert not predicates.is_boolean(None)
    assert not predicates.is_boolean('')
    assert not predicates.is_boolean('1')
    assert not predicates.is_boolean('foo_!')
    assert not predicates.is_boolean('foo_#')
    assert not predicates.is_boolean('foo_@')


def test_predicates_03():

    assert predicates.is_page_layout_unit('in')
    assert predicates.is_page_layout_unit('mm')
    assert predicates.is_page_layout_unit('cm')
    assert predicates.is_page_layout_unit('pt')
    assert predicates.is_page_layout_unit('pica')

    assert not predicates.is_page_layout_unit('foo')
    assert not predicates.is_page_layout_unit(None)
    assert not predicates.is_page_layout_unit(-1)
    assert not predicates.is_page_layout_unit(1)


def test_predicates_04():

    assert predicates.is_paper_dimension_string('8.5 x 11 in')
    assert predicates.is_paper_dimension_string('11 x 8.5 in')
    assert predicates.is_paper_dimension_string('11 x 17 in')
    assert predicates.is_paper_dimension_string('17 x 11 in')
    assert predicates.is_paper_dimension_string('210 x 297 mm')
    assert predicates.is_paper_dimension_string('297 x 210 mm')

    assert not predicates.is_paper_dimension_string('8.5 x 11')
    assert not predicates.is_paper_dimension_string('8.5x11')
    assert not predicates.is_paper_dimension_string('8.5x11in')
    assert not predicates.is_paper_dimension_string('A4')
    assert not predicates.is_paper_dimension_string('foo')
    assert not predicates.is_paper_dimension_string(None)
    assert not predicates.is_paper_dimension_string(-1)
    assert not predicates.is_paper_dimension_string(1)