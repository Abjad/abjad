# -*- encoding: utf-8 -*-


def list_all_abjad_functions():
    r'''Lists all public functions defined in Abjad.

    ::

        >>> all_functions = documentationtools.list_all_abjad_functions()

    '''
    from abjad import abjad_configuration
    from abjad.tools import documentationtools
    function_documenter = documentationtools.FunctionCrawler(
        abjad_configuration.abjad_directory_path,
        root_package_name='abjad',
        )
    all_functions = tuple(function_documenter())
    return all_functions
