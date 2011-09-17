import os


def _run_lilypond(lilypond_file_name, lilypond_path):
    if not lilypond_path:
        lilypond_path = 'lilypond'
    os.system('%s -dno-point-and-click %s > lily.log 2>&1' %
        (lilypond_path, lilypond_file_name))
    postscript_file_name = lilypond_file_name.replace('.ly', '.ps')
    try:
        os.remove(postscript_file_name)
    except OSError:
        # No such file...
        pass
