import os


def _run_lilypond(lily_file_name):
   os.system('lilypond %s > lily.log 2>&1' % lily_file_name)
   postscript_file_name = lily_file_name.replace('.ly', '.ps')
   os.remove(postscript_file_name)
