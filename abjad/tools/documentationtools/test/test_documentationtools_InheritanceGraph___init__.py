import abjad


def test_documentationtools_InheritanceGraph___init___01():
    abjad.documentationtools.InheritanceGraph(
        addresses=(
            abjad,
            )
        )


def test_documentationtools_InheritanceGraph___init___02():
    abjad.documentationtools.InheritanceGraph(
        addresses=(
            abjad,
        ),
        root_addresses=(abjad.abctools.AbjadObject,)
        )


def test_documentationtools_InheritanceGraph___init___03():
    abjad.documentationtools.InheritanceGraph(
        addresses=(
            abjad.Container,
            abjad.scoretools,
            abjad.scoretools,
            )
        )


def test_documentationtools_InheritanceGraph___init___04():
    abjad.documentationtools.InheritanceGraph(
        addresses=(
            'abjad',
            )
        )


def test_documentationtools_InheritanceGraph___init___05():
    abjad.documentationtools.InheritanceGraph(
        addresses=(
            'abjad',
        ),
        root_addresses=(('abjad.tools.abctools.AbjadObject', 'AbjadObject'),)
        )


def test_documentationtools_InheritanceGraph___init___06():
    abjad.documentationtools.InheritanceGraph(
        addresses=(
            ('abjad.tools.scoretools.Container', 'Container'),
            'abjad.tools.scoretools',
            'abjad.tools.scoretools',
        ),
        root_addresses=(('abjad.tools.abctools.AbjadObject', 'AbjadObject'),)
        )


def test_documentationtools_InheritanceGraph___init___07():
    abjad.documentationtools.InheritanceGraph(
        lineage_addresses=(abjad.Container,),
        root_addresses=(('abjad.tools.abctools.AbjadObject', 'AbjadObject'),)
        )
