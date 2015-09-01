# -*- encoding: utf-8 -*-
import inspect
from abjad.tools import documentationtools


def get_developer_script_classes():
    r'''Returns a list of all developer script classes.
    '''
    from abjad.tools import abjadbooktools
    from abjad.tools import developerscripttools
    tools_package_paths = []
    tools_package_paths.extend(abjadbooktools.__path__)
    tools_package_paths.extend(developerscripttools.__path__)
    script_classes = []
    for tools_package_path in tools_package_paths:
        generator = documentationtools.yield_all_classes(
            code_root=tools_package_path,
            root_package_name='abjad',
            )
        for developer_script_class in generator:
            if developerscripttools.DeveloperScript in \
                inspect.getmro(developer_script_class) and \
                not inspect.isabstract(developer_script_class):
                script_classes.append(developer_script_class)
    return list(sorted(script_classes, key=lambda x: x.__name__))