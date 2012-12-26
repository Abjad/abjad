import abjad
from abjad import *


def test_InheritanceGraph___init___01():
    graph = documentationtools.InheritanceGraph(
        (
            abjad,
        )
        )


def test_InheritanceGraph___init___02():
    graph = documentationtools.InheritanceGraph(
        (
            abjad,
        ),
        root_class=abctools.AbjadObject
        )


def test_InheritanceGraph___init___03():
    graph = documentationtools.InheritanceGraph(
        (
            Container,
            measuretools,
            notetools,
        )
        )


def test_InheritanceGraph___init___04():
    graph = documentationtools.InheritanceGraph(
        (
            'abjad',
        )
        )


def test_InheritanceGraph___init___05():
    graph = documentationtools.InheritanceGraph(
        (
            'abjad',
        ),
        root_class=('abjad.tools.abctools.AbjadObject.AbjadObject', 'AbjadObject')
        )


def test_InheritanceGraph___init___06():
    graph = documentationtools.InheritanceGraph(
        (
            ('abjad.tools.containertools.Container.Container', 'Container'),
            'abjad.tools.measuretools',
            'abjad.tools.notetools',
        ),
        root_class=('abjad.tools.abctools.AbjadObject.AbjadObject', 'AbjadObject')
        )

