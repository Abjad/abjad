from abjad.tools import componenttools
from abjad.tools import decoratortools
from abjad.tools import mathtools
from abjad.tools.chordtools.Chord import Chord


@decoratortools.requires(Chord)
def yield_all_subchords_of_chord(chord):
    '''.. versionadded:: 2.0

    Yield all subchords of `chord` in binary string order::

        >>> chord = Chord("<c' d' af' a'>4")

    ::

        >>> for subchord in chordtools.yield_all_subchords_of_chord(chord):
        ...     subchord
        ...
        Rest('r4')
        Note("c'4")
        Note("d'4")
        Chord("<c' d'>4")
        Note("af'4")
        Chord("<c' af'>4")
        Chord("<d' af'>4")
        Chord("<c' d' af'>4")
        Note("a'4")
        Chord("<c' a'>4")
        Chord("<d' a'>4")
        Chord("<c' d' a'>4")
        Chord("<af' a'>4")
        Chord("<c' af' a'>4")
        Chord("<d' af' a'>4")
        Chord("<c' d' af' a'>4")

    Include empty chord as rest.

    Return generator of newly constructed leaves.
    '''
    from abjad.tools import chordtools

    len_chord = len(chord)
    for i in range(2 ** len_chord):
        new_chord = componenttools.copy_components_and_remove_spanners([chord])[0]
        binary_string = mathtools.integer_to_binary_string(i)
        binary_string = binary_string.zfill(len_chord)
        note_heads_to_remove = []
        for j, digit in enumerate(reversed(binary_string)):
            if digit == '0':
                note_heads_to_remove.append(new_chord[j])
        for note_head in note_heads_to_remove:
                new_chord.remove(note_head)
        new_chord = chordtools.change_defective_chord_to_note_or_rest(new_chord)
        yield new_chord
