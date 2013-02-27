import os


def which(name, flags=os.X_OK):
    '''Find executable ``name``, similar to Unix's ``which`` command:

    ::

        >>> iotools.which('python2.7') # doctest: +SKIP
        ['/usr/bin/python2.7']

    Return list of zero or more full paths to ``name``.
    '''
    result = []
    extensions = [x for x in os.environ.get('PATHEXT', '').split(os.pathsep) if x]
    path = os.environ.get('PATH', None)
    if path is None:
        return []
    for path in os.environ.get('PATH', '').split(os.pathsep):
        path = os.path.join(path, name)
        if os.access(path, flags):
            result.append(path)
        for extension in extensions:
            path_extension = path + extension
            if os.access(path_extension, flags):
                result.append(path_extension)
    return result

