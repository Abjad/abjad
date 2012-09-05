import os


# TODO: make public and possibly improve function name
def _run_lilypond(lilypond_file_name, lilypond_path):
    from abjad.tools import iotools

    if not lilypond_path:
        lilypond_path = 'lilypond'
    command = '{} -dno-point-and-click {} > lily.log 2>&1'.format(lilypond_path, lilypond_file_name)
    iotools.spawn_subprocess(command)
    postscript_file_name = lilypond_file_name.replace('.ly', '.ps')
    try:
        os.remove(postscript_file_name)
    except OSError:
        # no such file...
        pass
