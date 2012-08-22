from abjad.tools import documentationtools
import inspect
import os


def get_developer_script_classes():
    '''Return a list of all developer script classes.'''

    from abjad.tools import developerscripttools
    from abjad.tools import abjadbooktools

    tools_package_paths = [
        abjadbooktools.__path__[0],
        developerscripttools.__path__[0]
    ]
    script_classes = []
    for tools_package_path in tools_package_paths:
        klasses = documentationtools.ClassCrawler(tools_package_path,
            root_package_name='abjad')()
        for klass in klasses:
            if developerscripttools.DeveloperScript in inspect.getmro(klass) and \
                not inspect.isabstract(klass):
                script_classes.append(klass)

    return list(sorted(script_classes, key=lambda x: x.__name__))
