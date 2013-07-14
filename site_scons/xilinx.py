#Distributed under the MIT licesnse.
#Copyright (c) 2013 Cospan Design (dave.mccoy@cospandesign.com)

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.



import os
import utils
import string

class XilinxNotImplimented(Exception):
    """XilinxNotImplemented

    Errors associated with not implementing stuff
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def test_xst():
    print "Hello"


def initialize_environment(env, xilinx_path = "", build_tool = "ISE", version_number = ""):
    """
    Initialized an environment to contain all the xilinx build tools

    Args:
        env (Scons.Environment): An environment to add all the xilinx tools too
        xilinx_path (string): A user defined path to the xilinx base directory
            (leave empty to use the default system location)
        build_type (string): to use, valid build types are found with
            utils.get_xilinx_tool_types
            (leave empty to use "ISE")
        version_number (string): specify a version number to use for one of the
            tool chains: e.g.
                build_tool = ISE -> version number = 13.2
                build_tool = Vivado -> version number = 2013.1
            (leave empty for the latest version)

    Returns:
        SCons.Environment): with the xilinx tools added

    Raises:
        Configuration Error
    """
    xpath = utils.find_xilinx_path(xilinx_path, build_tool, version_number)

    #print "path to xilinx build tool: %s " % xpath
    env['XIL_SCRIPT_LOC'] = xpath
    env['XILINX_DSP'] = xpath
    env['XILINX_PLANAHEAD'] = os.path.join(xpath, "PlanAhead")
    env['XILINX'] = xpath

    if 'LD_LIBRARY_PATH' not in env:
        env['LD_LIBRARY_PATH'] = ''

    if build_tool.lower() == "ise" or build_tool.lower() == "planahead":
        env.AppendENVPath("PATH", os.path.join(xpath, "PlanAhead", "bin"))
        env.AppendENVPath("PATH", os.path.join(xpath, "ISE", "sysgen", "util"))
        if utils.is_64_bit():
            #64 bit machine
            env.AppendENVPath("PATH", os.path.join(xpath, "common", "bin", "lin64"))
            env.AppendENVPath("PATH", os.path.join(xpath, "ISE", "bin", "lin64"))
            lib_path = os.path.join(xpath, "ISE", "lib", "lin64")
            env['LD_LIBRARY_PATH'] = string.join([lib_path, env['LD_LIBRARY_PATH']], os.pathsep)
            lib_path = os.path.join(xpath, "common", "lib", "lin64")
            env['LD_LIBRARY_PATH'] = string.join([lib_path, env['LD_LIBRARY_PATH']], os.pathsep)
            #print "LD_LIBRARY_PATH: %s" % str(env['LD_LIBRARY_PATH'])
        else:
            #32 bit machine
            env.AppendENVPath("PATH", os.path.join(xpath, "common", "bin", "lin"))
            env.AppendENVPath("PATH", os.path.join(xpath, "ISE", "bin", "lin"))
            lib_path = os.path.join(xpath, "ISE", "lib", "lin")
            env['LD_LIBRARY_PATH'] = string.join([lib_path, env['LD_LIBRARY_PATH']], os.pathsep)
            lib_path = os.path.join(xpath, "common", "lib", "lin")
            env['LD_LIBRARY_PATH'] = string.join([lib_path, env['LD_LIBRARY_PATH']], os.pathsep)
            #print "LD_LIBRARY_PATH: %s" % str(env['LD_LIBRARY_PATH'])
    else:

        raise XilinxNotImplemented("Vivado is not implemented yet")
    return env

def generate_ise_project(config_file = None):
    #Read the configuration files (Default Configuration File)
    config = {}
    if config_file is None:
        config = utils.read_config()
    else:
        config = utils.read_config(config_file)

    #Create an ISE Project
    project_name = config["name"]
    fn = os.path.join(utils.get_project_base(), "%s.prj" % project_name)
    #print "File path: %s" % fn
    #fp = open(fn, "w")
    return None
