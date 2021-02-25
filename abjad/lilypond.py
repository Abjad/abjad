from .format import remove_tags


def lilypond(argument, tags=False):
    """
    Gets LilyPond format of ``argument``.
    """
    if not hasattr(argument, "_get_lilypond_format"):
        raise Exception(f"no LilyPond format defined for {argument!r}.")
    string = argument._get_lilypond_format()
    if tags:
        return string
    string = remove_tags(string)
    return string
