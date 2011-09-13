def _leaf_to_pitch_and_rhythm_skeleton(leaf, include_keyword_attributes = False):
    from abjad.tools.chordtools.Chord import Chord
    from abjad.tools.notetools.Note import Note
    from abjad.tools.leaftools._get_leaf_keyword_attributes import _get_leaf_keyword_attributes
    class_name = leaf.__class__.__name__
    duration = repr(leaf.written_duration)
    if include_keyword_attributes:
        keyword_attributes = _get_leaf_keyword_attributes(leaf)
        # a hack
        keyword_attributes = filter(lambda x: not x.startswith('note_head ='), keyword_attributes)
    else:
        keyword_attributes = []
    keyword_attributes = ['\t' + x for x in keyword_attributes]
    if keyword_attributes:
        keyword_attributes = ',\n'.join(keyword_attributes)
        keyword_attributes = '\n' + keyword_attributes
        keyword_attributes = [keyword_attributes]
    if isinstance(leaf, Note):
        arguments = [(str(leaf.written_pitch.named_chromatic_pitch_class), leaf.written_pitch.octave_number),
            duration]
    elif isinstance(leaf, Chord):
        leaf_pairs = tuple([
            (str(note_head.written_pitch.named_chromatic_pitch_class), note_head.written_pitch.octave_number)
            for note_head in leaf])
        arguments = [leaf_pairs, duration]
    else:
        arguments = [duration]
    if leaf.duration_multiplier is not None:
        arguments.append(repr(leaf.duration_multiplier))
    arguments = [str(x) for x in arguments]
    arguments.extend(keyword_attributes)
    arguments = ', '.join(arguments)
    return '%s(%s)' % (class_name, arguments)
