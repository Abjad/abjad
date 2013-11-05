# -*- encoding: utf-8 -*-


def list_all_abjad_classes():
    r'''Lists all public classes defined in Abjad.

    ::

        >>> all_classes = documentationtools.list_all_abjad_classes()

    '''
    from abjad import abjad_configuration
    from abjad.tools import documentationtools
    class_documenter = documentationtools.ClassCrawler(
        abjad_configuration.abjad_directory_path,
        root_package_name='abjad',
        )
    all_classes = tuple(class_documenter())
    return all_classes
