# -*- encoding: utf-8 -*-
r'''The following name changes were made when migrating into Abjad for initial 
check-in:

    NoteFilledTokens ==> NoteRhythmMaker
    RestFilledTokens ==> RestRhythmMaker
    PatternedTokens ==> TaleaRhythmMaker

    PartForcedChunkWithPatternedTokens ==> OutputBurnishedTaleaRhythmMaker
    PartForcedPatternedTokens ==> DivisionBurnishedTaleaRhythmMaker

    SignalAffixedChunkWithNoteFilledTokens ==> OutputIncisedNoteRhythmMaker
    SignalAffixedChunkWithRestFilledTokens ==> OutputIncisedtRestFilledTimeTokenMaker
    SignalAffixedNoteFilledTokens ==> DivisionIncisedNoteRhythmMaker
    SignalAffixedRestFilledTokens ==> DivisionIncisedRestRhythmMaker

    _PartForcedObjectWithPatternedTokens ==> TaleaRhythmMaker
    _RhythmicKaleid ==> RhythmMaker
    _SignalAffixedChunkWithFilledTokens ==> OutputIncisedRhythmMaker
    _SignalAffixedFilledTokens ==> DivisionIncisedRhythmMaker
    _SignalAffixedObjectWithFilledTokens ==> IncisedRhythmMaker

These name changes no longer matter when using the public version of the 
package.
'''
from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'core'
