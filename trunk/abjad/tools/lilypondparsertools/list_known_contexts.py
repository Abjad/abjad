def list_known_contexts():
    '''List all LilyPond contexts recognized by ``LilyPondParser``:

    ::

        >>> for x in lilypondparsertools.list_known_contexts():
        ...     print x
        ...
        ChoirStaff
        ChordNames
        CueVoice
        Devnull
        DrumStaff
        DrumVoice
        Dynamics
        FiguredBass
        FretBoards
        Global
        GrandStaff
        GregorianTranscriptionStaff
        GregorianTranscriptionVoice
        KievanStaff
        KievanVoice
        Lyrics
        MensuralStaff
        MensuralVoice
        NoteNames
        PetrucciStaff
        PetrucciVoice
        PianoStaff
        RhythmicStaff
        Score
        Staff
        StaffGroup
        TabStaff
        TabVoice
        VaticanaStaff
        VaticanaVoice
        Voice

    Return list.
    '''
    from abjad.ly import contexts

    return sorted(contexts.keys())
