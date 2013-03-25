import os
import shutil
import subprocess
import tempfile


def compare_images(image_one, image_two):
    '''Compare `image_one` against `image_two` using ImageMagick's `compare`
    commandline tool.

    Return `True` if images are the same, otherwise `False`.

    If `compare` is not available, return `False`.
    '''
    from abjad.tools import iotools

    assert os.path.exists(image_one)
    assert os.path.exists(image_two)

    result = False

    if iotools.which('compare'):

        tempdir = tempfile.mkdtemp()
        comparison = os.path.join(tempdir, 'comparison.png')

        command = 'compare -metric ae {} {} {}'.format(
            image_one, image_two, comparison)
        process = subprocess.Popen(command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )

        stderr = process.stderr.read()
        stdout = process.stdout.read()

        if stderr:
            part = stderr.split()[0]
            if part.isdigit():
                result = int(part) is 0
        elif stdout:
            part = stdout.split()[0]                                                     
            if part.isdigit():                                                           
                result = int(part) is 0

        shutil.rmtree(tempdir)

    return result
