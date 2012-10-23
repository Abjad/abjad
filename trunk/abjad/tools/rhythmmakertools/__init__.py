r'''Module: rhythmmakertools.

The following name changes were made when migrating into Abjad for initial check-in:

    NoteFilledTokens ==> NoteFilledRhythmMaker
    RestFilledTokens ==> RestFilledRhythmMaker
    PatternedTokens ==> TaleaFilledRhythmMaker

    PartForcedChunkWithPatternedTokens ==> OutputBurnishedTaleaFilledRhythmMaker
    PartForcedPatternedTokens ==> DivisionBurnishedTaleaFilledRhythmMaker

    SignalAffixedChunkWithNoteFilledTokens ==> OutputIncisedNoteFilledRhythmMaker
    SignalAffixedChunkWithRestFilledTokens ==> OutputIncisedtRestFilledTimeTokenMaker
    SignalAffixedNoteFilledTokens ==> DivisionIncisedNoteFilledRhythmMaker
    SignalAffixedRestFilledTokens ==> DivisionIncisedRestFilledRhythmMaker

    _PartForcedObjectWithPatternedTokens ==> BurnishedRhythmMaker
    _RhythmicKaleid ==> RhythmMaker
    _SignalAffixedChunkWithFilledTokens ==> OutputIncisedRhythmMaker
    _SignalAffixedFilledTokens ==> DivisionIncisedRhythmMaker
    _SignalAffixedObjectWithFilledTokens ==> IncisedRhythmMaker

These name changes no longer matter when using the public version of the package.
'''
from abjad.tools import importtools

importtools.import_structured_package(__path__[0], globals())

_documentation_section = 'core'
