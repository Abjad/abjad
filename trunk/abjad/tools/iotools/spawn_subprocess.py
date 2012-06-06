import subprocess


def spawn_subprocess(command):
    '''.. versionadded:: 2.9

    Spawn subprocess, run `command`, redirect stderr to stdout and print result::

        >>> iotools.spawn_subprocess('echo "hello world"') # doctest: +SKIP
        hello world

    The function is basically a reimplementation of the deprecated ``os.system()``
    using Python's ``subprocess`` module.

    The function provides a type of shell access from the Abjad interpreter.

    Return none.
    '''

    subprocess.call(command, shell=True)
    #proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #for line in proc.stdout.read().splitlines():
    #    print line
