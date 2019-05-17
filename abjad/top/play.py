import typing
from .persist import persist


def play(argument: typing.Any, test: bool = None) -> None:
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
    from abjad import abjad_configuration
    from abjad.system.IOManager import IOManager

    assert hasattr(argument, "__illustrate__")
    result = persist(argument).as_midi()
    midi_file_path = result[0]
    midi_player = abjad_configuration["midi_player"]
    IOManager.open_file(midi_file_path, application=midi_player, test=test)
