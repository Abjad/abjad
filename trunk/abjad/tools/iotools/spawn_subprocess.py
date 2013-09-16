# -*- encoding: utf-8 -*-
import subprocess


def spawn_subprocess(command):
    r'''Spawns subprocess and runs `command`.
    
    Redirects stderr to stdout.

    ::

        >>> iotools.spawn_subprocess('echo "hello world"') # doctest: +SKIP
        hello world

    The function is basically a reimplementation of the 
    deprecated ``os.system()`` using Python's ``subprocess`` module.

    Returns integer result code.
    '''

    return subprocess.call(command, shell=True)
