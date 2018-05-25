def show(argument, return_timing=False, **keywords):
    r"""
    Shows ``argument``.

    ..  container:: example

        Shows note:

        >>> note = abjad.Note("c'4")
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4

    ..  container:: example

        Shows staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }

    Makes LilyPond input files and output PDF.

    Writes LilyPond input file and output PDF to Abjad output directory.

    Opens output PDF.

    Returns none when ``return_timing`` is false.

    Returns pair of ``abjad_formatting_time`` and ``lilypond_rendering_time``
    when ``return_timing`` is true.
    """
    import abjad
    if not hasattr(argument, '__illustrate__'):
        message = 'must have __illustrate__ method: {!r}.'
        message = message.format(argument)
        raise Exception(message)
    result = abjad.persist(argument).as_pdf(**keywords)
    pdf_file_path = result[0]
    abjad_formatting_time = result[1]
    lilypond_rendering_time = result[2]
    success = result[3]
    if success:
        abjad.IOManager.open_file(pdf_file_path)
    else:
        with open(abjad.abjad_configuration.lilypond_log_file_path, 'r') as fp:
            print(fp.read())
    if return_timing:
        return abjad_formatting_time, lilypond_rendering_time
