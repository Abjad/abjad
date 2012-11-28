import os
import shutil
import subprocess
import tempfile


def compare_images(image_one, image_two):
    '''Compare `image_one` against `image_two` using ImageMagick's `compare`
    commandline tool.

    Return `True` if images are the same, otherwise `False`.
    '''

    assert os.path.exists(image_one)
    assert os.path.exists(image_two)

    tempdir = tempfile.mkdtemp()
    comparison = os.path.join(tempdir, 'comparison.png')

    command = 'compare -metric ae {} {} {}'.format(
        image_one, image_two, comparison)
    process = subprocess.Popen(command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )

    stderr = process.stderr.read()
    result = True
    if stderr.startswith('compare: image widths or heights differ'):
        result = False
    else:
        result = int(stderr.split('\n')[0].split()[0]) is 0

    shutil.rmtree(tempdir)
    return result
