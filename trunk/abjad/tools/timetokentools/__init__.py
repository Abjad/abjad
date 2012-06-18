r'''Module: timetokentools.

The following name changes were made when migrating into Abjad for initial check-in:

    NoteFilledTokens ==> NoteFilledTimeTokenMaker
    RestFilledTokens ==> RestFilledTimeTokenMaker
    PatternedTokens ==> SignalFilledTimeTokenMaker

    PartForcedChunkWithPatternedTokens ==> OutputBurnishedSignalFilledTimeTokenMaker
    PartForcedPatternedTokens ==> TokenBurnishedSignalFilledTimeTokenMaker

    SignalAffixedChunkWithNoteFilledTokens ==> OutputIncisedNoteFilledTimeTokenMaker
    SignalAffixedChunkWithRestFilledTokens ==> OutputIncisedtRestFilledTimeTokenMaker
    SignalAffixedNoteFilledTokens ==> TokenIncisedNoteFilledTimeTokenMaker
    SignalAffixedRestFilledTokens ==> TokenIncisedRestFilledTimeTokenMaker

    _PartForcedObjectWithPatternedTokens ==> BurnishedTimeTokenMaker
    _RhythmicKaleid ==> TimeTokenMaker
    _SignalAffixedChunkWithFilledTokens ==> OutputIncisedTimeTokenMaker
    _SignalAffixedFilledTokens ==> TokenIncisedTimeTokenMaker
    _SignalAffixedObjectWithFilledTokens ==> IncisedTimeTokenMaker

These name changes no longer matter when using the public version of the package.
'''
from abjad.tools import importtools

importtools.import_structured_package(__path__[0], globals())

_documentation_section = 'core'
