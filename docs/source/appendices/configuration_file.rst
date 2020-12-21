Configuration file
==================

Abjad creates a ``~/.abjad`` directory the first time it runs. In the ``~/.abjad``
directory you will find an ``abjad.cfg`` file. This is the Abjad configuration file. You
can use the Abjad configuration file to tell Abjad about your preferred PDF file viewer,
MIDI player, LilyPond language and so on.

Your configuration file will look something like this the first time you open it:

::

    # Abjad configuration file created by Abjad on 31 January 2014 00:08:17.
    # File is interpreted by ConfigObj and should follow ini syntax.

    # Set to the directory where all Abjad-generated files
    # (such as PDFs and LilyPond files) should be saved.
    # Defaults to $HOME.abjad/output/
    abjad_output_directory = /Users/username/.abjad/output

    # Comma-separated list of LilyPond files that 
    # Abjad will "\include" in all generated *.ly files
    lilypond_includes = ,

    # Language to use in all generated LilyPond files.
    lilypond_language = english

    # Lilypond executable path. Set to override dynamic lookup.
    lilypond_path = lilypond

    # MIDI player to open MIDI files.
    # When unset your OS should know how to open MIDI files.
    midi_player = 

    # PDF viewer to open PDF files.
    # When unset your OS should know how to open PDFs.
    pdf_viewer = 

    # Text editor to edit text files.
    # When unset your OS should know how to open text files.
    text_editor = 

Follow the basics of ``ini`` syntax when editing the Abjad configuration file. Background
information is available at http://en.wikipedia.org/wiki/INI_file. Under MacOS you might
want to set you ``midi_player`` to iTunes. Under Linux you might want to set your
``pdf_viewer`` to ``evince`` and your ``midi_player`` to ``tiMIDIty``, and so on.
