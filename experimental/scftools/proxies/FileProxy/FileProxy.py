from scftools.proxies.AssetProxy import AssetProxy
import os


class FileProxy(AssetProxy):

    ### CLASS ATTRIBUTES ###

    generic_class_name = 'file'
    temporary_asset_short_name = 'temporary_file.txt'

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def extension(self):
        return ''

    @property
    def file_lines(self):
        result = []
        if self.path_name:
            if os.path.exists(self.path_name):
                file_pointer = file(self.path_name)
                result.extend(file_pointer.readlines())
                file_pointer.close()
        return result

    @property
    def format(self):
        return ''.join(self.formatted_lines)

    @property
    def formatted_lines(self):
        return self.file_lines

    ### PUBLIC METHODS ###

    def conditionally_make_empty_asset(self, is_interactive=False):
        if not os.path.exists(self.path_name):
            file_reference = file(self.path_name, 'w')
            file_reference.write('')
            file_reference.close()
        self.proceed(is_interactive=is_interactive)

    def display_formatted_lines(self):
        self.display(self.formatted_lines)

    def edit(self):
        os.system('vi + {}'.format(self.path_name))

    def fix(self):
        pass

    def has_line(self, line):
        file_reference = open(self.path_name, 'r')
        for file_line in file_reference.readlines():
            if file_line == line:
                file_reference.close()
                return True
        file_reference.close()
        return False

    def profile(self):
        pass

    def view(self):
        os.system('vi -R {}'.format(self.path_name))
