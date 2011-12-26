from . import comb_check, comb_instance, tc_check, tc_instance
from conf_tools import ConfigMaster


class TCConfigMaster(ConfigMaster):
    def __init__(self):
        ConfigMaster.__init__(self, 'CBC')

        self.add_class('test_cases', '*.tc.yaml', tc_check, tc_instance)
        self.add_class('combinations', '*.comb.yaml',
                       comb_check, comb_instance)

        self.test_cases = self.specs['test_cases']

    def get_default_dir(self):
        from pkg_resources import resource_filename #@UnresolvedImport
        return resource_filename("cbc", "configs")


TCConfig = TCConfigMaster()


