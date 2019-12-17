def play(argument) -> None:
    """
    Plays ``argument``.

    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> abjad.play(note) # doctest: +SKIP

    Makes MIDI file.

    Appends ``.mid`` filename extension under Windows.

    Appends ``.midi`` filename extension under other operating systems.

    Opens MIDI file.
    """
    import abjad.iox

    return abjad.iox.play(argument)
