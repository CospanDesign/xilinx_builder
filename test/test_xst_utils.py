#! /usr/bin/python
import unittest
import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__),
                             os.pardir,
                             "site_scons"))

import utils
import xst_utils

class Test (unittest.TestCase):
    """Unit test for the verilog pre-processor module"""

    def setUp(self):
        self.dbg = False

    def test_get_xilinx_tool_types(self):
        """generate a define table given a file"""
        config_fn = os.path.join(utils.get_project_base(), "config.json")
        config = json.load(open(config_fn, "r"))
        flags = xst_utils.get_xst_flags(config)
        #print "Flags: %s" % str(flags)
        self.assertIn("-iob", flags.keys())

    def test_create_xst_project_file(self):
        config_fn = os.path.join(utils.get_project_base(), "config.json")
        config = utils.read_config(config_fn)
        xst_utils.create_xst_project_file(config)


    def test_create_xst_script(self):
        config_fn = os.path.join(utils.get_project_base(), "config.json")
        config = utils.read_config(config_fn)
        xst_utils.create_xst_script(config)


if __name__ == "__main__":
  unittest.main()

