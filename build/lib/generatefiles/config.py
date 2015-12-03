__author__ = 'lucas'

from pkg_resources import resource_filename
from os.path import join, sep
from configparser import ConfigParser

class Config(object):

    def __init__(self, config_parser):
        self.__sections = []
        parser_sections = config_parser.items()
        for section_name, section_parser in parser_sections:
            section = Section(section_name, section_parser)
            self.__sections.append(section)

    @property
    def sections(self):
        return [section.name for section in self.__sections]

    def get_section(self, section_name, default=None):
        name = section_name.lower()
        for section in self.__sections:
            if section.name == name:
                return section
        return default

    def get_attribute(self, section_name, attribute, default=None, type_=None):
        section = self.get_section(section_name)
        if section is None:
            raise KeyError('Section not found: %s' % section_name)

        value = section.get(attribute.lower(), default)
        if type_ is not None and value:
            value = type_(value)

class Section(dict):

    def __init__(self, name, parser_section):
        self.name = name.lower()
        super(Section, self).__init__(parser_section.items())

def parse_config():
    instance_dir = resource_filename('generatefiles', '').split('/')[:-5]
    instance_dir = sep.join(instance_dir)
    instance_dir = instance_dir
    ini_file = join(join(instance_dir), 'configure.ini')
    config_parser = ConfigParser()
    config_parser.read(ini_file)
    config = Config(config_parser)
    return config

CONFIG = parse_config()