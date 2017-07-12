# -*- coding: utf-8 -*-
import abjad
import pytest


def test_documentationtools_InheritanceGraph___init___01():
    graph = abjad.documentationtools.InheritanceGraph(
        addresses=(
            abjad,
        )
        )


def test_documentationtools_InheritanceGraph___init___02():
    graph = abjad.documentationtools.InheritanceGraph(
        addresses=(
            abjad,
        ),
        root_addresses=(abjad.abctools.AbjadObject,)
        )


def test_documentationtools_InheritanceGraph___init___03():
    graph = abjad.documentationtools.InheritanceGraph(
        addresses=(
            abjad.Container,
            abjad.scoretools,
            abjad.scoretools,
        )
        )


def test_documentationtools_InheritanceGraph___init___04():
    graph = abjad.documentationtools.InheritanceGraph(
        addresses=(
            'abjad',
        )
        )


def test_documentationtools_InheritanceGraph___init___05():
    graph = abjad.documentationtools.InheritanceGraph(
        addresses=(
            'abjad',
        ),
        root_addresses=(('abjad.tools.abctools.AbjadObject', 'AbjadObject'),)
        )


def test_documentationtools_InheritanceGraph___init___06():
    graph = abjad.documentationtools.InheritanceGraph(
        addresses=(
            ('abjad.tools.scoretools.Container', 'Container'),
            'abjad.tools.scoretools',
            'abjad.tools.scoretools',
        ),
        root_addresses=(('abjad.tools.abctools.AbjadObject', 'AbjadObject'),)
        )


def test_documentationtools_InheritanceGraph___init___07():
    graph = abjad.documentationtools.InheritanceGraph(
        lineage_addresses=(abjad.Container,),
        root_addresses=(('abjad.tools.abctools.AbjadObject', 'AbjadObject'),)
        )
