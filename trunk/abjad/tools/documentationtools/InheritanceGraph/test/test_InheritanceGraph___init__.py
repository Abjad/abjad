import abjad
from abjad import *


def test_InheritanceGraph___init___01():
    graph = documentationtools.InheritanceGraph(
        addresses=(
            abjad,
        )
        )


def test_InheritanceGraph___init___02():
    graph = documentationtools.InheritanceGraph(
        addresses=(
            abjad,
        ),
        root_addresses=(abctools.AbjadObject,)
        )


def test_InheritanceGraph___init___03():
    graph = documentationtools.InheritanceGraph(
        addresses=(
            Container,
            measuretools,
            notetools,
        )
        )


def test_InheritanceGraph___init___04():
    graph = documentationtools.InheritanceGraph(
        addresses=(
            'abjad',
        )
        )


def test_InheritanceGraph___init___05():
    graph = documentationtools.InheritanceGraph(
        addresses=(
            'abjad',
        ),
        root_addresses=(('abjad.tools.abctools.AbjadObject.AbjadObject', 'AbjadObject'),)
        )


def test_InheritanceGraph___init___06():
    graph = documentationtools.InheritanceGraph(
        addresses=(
            ('abjad.tools.containertools.Container.Container', 'Container'),
            'abjad.tools.measuretools',
            'abjad.tools.notetools',
        ),
        root_addresses=(('abjad.tools.abctools.AbjadObject.AbjadObject', 'AbjadObject'),)
        )


def test_InheritanceGraph___init___07():
    graph = documentationtools.InheritanceGraph(
        lineage_addresses=(containertools.Container,),
        root_addresses=(('abjad.tools.abctools.AbjadObject.AbjadObject', 'AbjadObject'),)
        )
