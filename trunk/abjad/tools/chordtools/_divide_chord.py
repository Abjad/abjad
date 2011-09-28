from abjad.tools.chordtools.Chord import Chord
from abjad.tools import pitchtools
from abjad.tools.chordtools.change_defective_chord_to_note_or_rest import change_defective_chord_to_note_or_rest
import copy


def _divide_chord(chord, pitch=pitchtools.NamedChromaticPitch('b', 3), 
    attr='numbered_chromatic_pitch'):
    r'''Divide `chord` according to chromatic or diatonic pitch number of `pitch`.

    Return pair of newly created leaves.
    '''
    from abjad.tools.leaftools._Leaf import _Leaf
    from abjad.tools import markuptools
    from abjad.tools import notetools
    from abjad.tools import resttools

    if not isinstance(chord, _Leaf):
        raise TypeError('%s is not a note, rest or chord.' % str(chord))

    pitch = pitchtools.NamedChromaticPitch(pitch)
    assert attr in ('numbered_chromatic_pitch', 'numbered_diatonic_pitch')

    treble = copy.copy(chord)
    bass = copy.copy(chord)

    markuptools.remove_markup_attached_to_component(treble)
    markuptools.remove_markup_attached_to_component(bass)

    if isinstance(treble, notetools.Note):
        if getattr(treble.written_pitch, attr) < getattr(pitch, attr):
            treble = resttools.Rest(treble)
    elif isinstance(treble, resttools.Rest):
        pass
    elif isinstance(treble, Chord):
        for note_head in treble.note_heads:
            if getattr(note_head.written_pitch, attr) < getattr(pitch, attr):
                treble.remove(note_head)
    else:
        raise ValueError('must be note, rest or chord.')

    if isinstance(bass, notetools.Note):
        if getattr(pitch, attr) <= getattr(bass.written_pitch, attr):
            bass = resttools.Rest(bass)
    elif isinstance(bass, resttools.Rest):
        pass
    elif isinstance(bass, Chord):
        for note_head in bass.note_heads:
            if getattr(pitch, attr) <= getattr(note_head.written_pitch, attr):
                bass.remove(note_head)
    else:
        raise ValueError('must be note, rest or chord.')

    treble = change_defective_chord_to_note_or_rest(treble)
    bass = change_defective_chord_to_note_or_rest(bass)

    up_markup = markuptools.get_up_markup_attached_to_component(chord)
    up_markup = [copy.copy(markup) for markup in up_markup]

    down_markup = markuptools.get_down_markup_attached_to_component(chord)
    down_markup = [copy.copy(markup) for markup in down_markup]

    for markup in up_markup:
        markup(treble)

    for markup in down_markup:
        markup(bass)

    return treble, bass
