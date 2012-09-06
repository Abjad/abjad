def list_package_dependency_versions():
    r'''List package dependency versions::

        >>> from abjad.tools import configurationtools

    ::

        >>> configurationtools.list_package_dependency_versions() # doctest: +SKIP
        {'sphinx': '1.1.2', 'py.test': '2.1.2'}

    Return dictionary.  
    '''

    deps = {}

    deps['configobj'] = None
    try:
        import configobj
        deps['configobj'] = configobj.__version__
    except ImportError:
        pass

    deps['ply'] = None
    try:
        from ply import lex
        deps['ply'] = lex.__version__
    except ImportError:
        pass

    # py.test
    deps['py.test'] = None
    try:
        import py.test
        deps['py.test'] = py.test.__version__
    except ImportError:
        pass

    # sphinx
    deps['sphinx'] = None
    try:
        import sphinx
        deps['sphinx'] = sphinx.__version__
    except ImportError:
        pass

    return deps
