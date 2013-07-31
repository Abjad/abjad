import inspect
import os
from abjad.tools import documentationtools


def get_developer_script_classes():
    r'''Return a list of all developer script classes.
    '''
    from abjad.tools import developerscripttools
    from abjad.tools import abjadbooktools

    tools_package_paths = [
        abjadbooktools.__path__[0],
        developerscripttools.__path__[0],
    ]
    script_classes = []
    for tools_package_path in tools_package_paths:
        developer_script_classes = documentationtools.ClassCrawler(
            tools_package_path, root_package_name='abjad')()
        for developer_script_class in developer_script_classes:
            if developerscripttools.DeveloperScript in \
                inspect.getmro(developer_script_class) and \
                not inspect.isabstract(developer_script_class):
                script_classes.append(developer_script_class)

    return list(sorted(script_classes, key=lambda x: x.__name__))
