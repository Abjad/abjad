def play(argument):
    r'''Plays `argument`.

    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> abjad.play(note) # doctest: +SKIP

    Makes MIDI file.

    Appends ``.mid`` filename extension under Windows.

    Appends ``.midi`` filename extension under other operating systems.

    Opens MIDI file.

    Returns none.
    '''
    from abjad import abjad_configuration
    from abjad.tools import systemtools
    from abjad.tools import topleveltools
    assert hasattr(argument, '__illustrate__')
    result = topleveltools.persist(argument).as_midi()
    midi_file_path, abjad_formatting_time, lilypond_rendering_time = result
    midi_player = abjad_configuration['midi_player']
    systemtools.IOManager.open_file(midi_file_path, midi_player)
