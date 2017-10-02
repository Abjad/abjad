import abjad


def test_systemtools_StorageFormatAgent_get_import_statements_01():
    subject = abjad.NamedPitch()
    agent = abjad.StorageFormatAgent(subject)
    assert agent.get_import_statements() == (
        'from abjad.tools import pitchtools',
        )


def test_systemtools_StorageFormatAgent_get_import_statements_02():
    subject = abjad.Selector().by_leaf()
    agent = abjad.StorageFormatAgent(subject)
    assert agent.get_import_statements() == (
        'from abjad.tools import scoretools',
        'from abjad.tools import selectortools',
        )


def test_systemtools_StorageFormatAgent_get_import_statements_03():
    subject = [
        abjad.TimeSignature((3, 4)),
        abjad.TimeSignature((4, 4)),
        ]
    agent = abjad.StorageFormatAgent(subject)
    assert agent.get_import_statements() == (
        'from abjad.tools import indicatortools',
        )
