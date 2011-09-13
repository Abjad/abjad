import os


def _verify_output_directory(directory):
    if not os.path.isdir(directory):
        raw_input('Attention: "%s" does not exist in your system.\n\
        Abjad will now create it to store all generated output files. \n\
        Press any key to continue.' % directory)
        os.makedirs(directory)
