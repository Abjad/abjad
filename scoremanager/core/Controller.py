# -*- encoding: utf -*-
from abjad.tools import stringtools
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class Controller(ScoreManagerObject):
    r'''Controller.
    '''

    ### INTIIALIZER ###

    def __init__(self, session=None):
        assert session is not None
        superclass = super(Controller, self)
        superclass.__init__(session=session)

    ### PRIVATE PROPERTIES ###

    @property
    def _user_input_to_action(self):
        result = {
            }
        return result

    ### PRIVATE METHODS ###

    def _get_view_from_disk(self):
        pass

    def _make_asset_menu_entries(
        self, 
        extensions=False, 
        include_asset_name=True,
        include_year=False,
        packages_instead_of_paths=False,
        sort_by_annotation=False, 
        ):
        paths = self._list_visible_asset_paths()
        strings = []
        for path in paths:
            string = self._path_to_human_readable_name(
                path, 
                extension=extensions,
                )
            annotation = self._path_to_annotation(path, year=include_year)
            if include_asset_name:
                string = '{} ({})'.format(string, annotation)
            else:
                string = str(annotation)
            strings.append(string)
        pairs = zip(strings, paths)
        if sort_by_annotation:
            tmp = stringtools.strip_diacritics_from_binary_string
            pairs.sort(key=lambda x: tmp(x[0]))
        entries = []
        for string, path in pairs:
            if packages_instead_of_paths:
                path = self._configuration.path_to_package_path(path)
            entry = (string, None, None, path)
            entries.append(entry)
        view = self._get_view_from_disk()
        if view is not None:
            entries = self._sort_asset_menu_entries_by_view(entries, view)
        return entries

    def _make_directory_menu_section(self, menu, is_permanent=False):
        section = menu.make_command_section(
            is_hidden=True,
            name='directory',
            )
        section.append(('directory - list', 'ls'))
        section.append(('directory - list long', 'll'))
        section.append(('directory - pwd', 'pwd'))
        if not is_permanent:
            section.append(('directory - remove', 'rm'))
            section.append(('directory - rename', 'ren'))
        return section

    def _make_done_menu_section(self, menu):
        section = menu.make_command_section(
            name='zzz - done',
            )
        section.append(('done', 'done'))
        return section

    def _make_initializer_menu_section(self, menu, has_initializer=True):
        if not has_initializer:
            section = menu.make_command_section(name='initializer')
            section.title = "package has no initializer: use 'ins'."
        section = menu.make_command_section(
            is_hidden=True,
            match_on_display_string=False,
            name='initializer',
            )
        section.append(('initializer - boilerplate', 'inbp'))
        section.append(('initializer - remove', 'inrm'))
        section.append(('initializer - stub', 'ins'))
        section.append(('initializer - view', 'inv'))
        return section

    def _make_material_tour_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            name='materials - tour',
            )
        section.append(('materials - tour next', 'mtn'))
        section.append(('materials - tour previous', 'mtp'))
        return section

    def _make_metadata_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            match_on_display_string=False,
            name='metadatum',
            )
        section.append(('metadatum - add', 'mma'))
        section.append(('metadatum - get', 'mmg'))
        section.append(('metadatum - remove', 'mmrm'))
        return section

    def _make_metadata_module_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            match_on_display_string=False,
            name='metadata module',
            )
        section.append(('metadata module - remove', 'mmmrm'))
        section.append(('metadata module - rewrite', 'mmmrw'))
        section.append(('metadata module - view', 'mmmv'))
        return section

    def _make_views_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            match_on_display_string=False,
            name='views',
            )
        section.append(('views - list', 'vwl'))
        section.append(('views - new', 'vwn'))
        section.append(('views - select', 'vws'))
        return section

    def _make_views_module_menu_section(self, menu):
        section = menu.make_command_section(
            is_hidden=True,
            match_on_display_string=False,
            name='views module',
            )
        section.append(('views module - remove', 'vwmrm'))
        section.append(('views module - view', 'vwmv'))
        return section
        
    def _path_to_annotation(self, path, year=False):
        from scoremanager import managers
        score_storehouses = (
            self._configuration.abjad_score_packages_directory_path,
            self._configuration.user_score_packages_directory_path,
            )
        if path.startswith(score_storehouses):
            score_path = self._configuration._path_to_score_path(path)
            manager = managers.ScorePackageManager(
                path=score_path,
                session=self._session,
                )
            metadata = manager._get_metadata()
            year_of_completion = metadata.get('year_of_completion')
            title = metadata.get('title')
            if year and year_of_completion:
                annotation = '{} ({})'.format(title, year_of_completion)
            else:
                annotation = str(title)
        elif path.startswith(self._abjad_storehouse_path):
            annotation = 'Abjad'
        elif path.startswith(self._user_storehouse_path):
            annotation = self._configuration.composer_last_name
        else:
            annotation = None
        return annotation

    @staticmethod
    def _sort_asset_menu_entries_by_view(entries, view):
        entries_found_in_view = len(entries) * [None]
        entries_not_found_in_view = []
        for entry in entries:
            name = entry[0]
            if name in view:
                index = view.index(name)
                entries_found_in_view[index] = entry
            else:
                entries_not_found_in_view.append(entry)
        entries_found_in_view = [
            x for x in entries_found_in_view 
            if not x is None
            ]
        sorted_entries = entries_found_in_view + entries_not_found_in_view
        assert len(sorted_entries) == len(entries)
        return sorted_entries
