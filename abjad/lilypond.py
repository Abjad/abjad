def lilypond(argument):
    """
    Gets LilyPond format of ``argument``.
    """
    if not hasattr(argument, "_get_lilypond_format"):
        raise Exception(f"no LilyPond format defined for {argument!r}.")
    return argument._get_lilypond_format()
