def list_package_dependency_versions():

    deps = {}

    # sphinx
    deps['sphinx'] = None
    try:
        import sphinx
        deps['sphinx'] = sphinx.__version__
    except ImportError:
        pass

    # py.test
    deps['py.test'] = None
    try:
        import py.test
        deps['py.test'] = py.test.__version__
    except ImportError:
        pass

    return deps
