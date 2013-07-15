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
import json
import platform
import glob


PROJECT_BASE = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), os.pardir))

DEFAULT_CONFIG_FILE = "config.json"
DEFAULT_BUILD_DIR = "build"
TOOL_TYPES=("ise",
            "planahead",
            "vivado")

LINUX_XILINX_DEFAULT_BASE = "/opt/Xilinx"
WINDOWS_XILINX_DEFAULT_BASE = "Xilinx"

class ConfigurationError(Exception):
    """
    Errors associated with configuration:
        getting the configuration file for the project
        getting the default xilinx toolchain
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def get_project_base():
    """
    Returns the project base directory

    Args:
        Nothing

    Returns:
        Path (String) to base directory

    Raises:
        Nothing
    """
    return PROJECT_BASE

def read_config(env):
    """
    Read the build configuration file and creates a dictionary to be used
    throughout the project

    Args:
        env: Environmental variable where the config file is

    Return:
        Dictionary of the configuration

    Raises:
        ConfigurationError
    """

    #Open the configuration file
    fn = env["CONFIG_FILE"]
    if not os.path.exists(fn):
        #if the configuration file name doesn't exists then
        #maybe it is at the base directory of the project
        fn = os.path.join(get_project_base(), fn)


    #if fn == DEFAULT_CONFIG_FILE:
    #    fn = os.path.join(PROJECT_BASE,
    #                      DEFAULT_CONFIG_FILE)
    try:
        config = json.load(open(fn, "r"))
    except TypeError as err:
        raise ConfigurationError(
                "Error parsing json file: %s" % str(err))

    except ValueError as err:
        raise ConfigurationError(
                "Error parsing json file: %s" % str(err))

    except IOError as err:
        raise ConfigurationError(
                "Error openning file: %s: Err: %s" % (fn, str(err)))

    #Return the configuration dicationary
    if "verilog" in config.keys():
        #Fix the verilog paths
        paths = config["verilog"]
        #print "paths: %s" % str(paths)
        vpaths = []
        for vpath in paths:
            #print "vpath: %s" % str(vpath)
            #split the space separaed folders to a
            if "/" in vpath["path"]:
                #Fix linux style paths
                vpath["path"] = vpath["path"].split("/")
            elif "\\" in vpath["path"]:
                #fix windows style paths
                vpath["path"] = vpath["path"].split("\\")
            else:
                vpath["path"] = vpath["path"].split()

            for p in vpath["path"]:
                path = PROJECT_BASE
                #Detect if user gave an actual (absolute) path or a relative path
                if not os.path.isabs(p):
                    #User gave a relative path name
                    path = os.path.join(path, p)

            #print "working path: %s" % path

            if not os.path.exists(path):
                raise ConfigurationError(
                        "Verilog path: (%s) " \
                        "doesn't point to an actual directory or file" % path)

            #if this is a file just append it to vpath
            if os.path.isfile(path):
                #print "Found a file: %s" % path
                vpath.append(path)

            #this is a directory so now I need to see if this is a recursive
            #directory
            if "recursive" in vpath.keys() and vpath["recursive"]:
                #print "Recursively retreiving files"
                vfs = _get_vfiles(path)
                #print "List of verilog files: %s" % str(vfs)
                vpaths.extend(vfs)
            else:
                #print "Found a directory: %s" % path
                search_pattern = os.path.join(path, "*.v")
                vfs = glob.glob(search_pattern)
                #print "Found files: %s" % str(vfs)
                vpaths.extend(vfs)

        config["verilog"] = vpaths

    #Check to see if the XST flags exists
    if "xst" not in config.keys():
        config["xst"] = {}
    if "flags" not in config["xst"]:
        config["xst"]["flags"] = {}

    #Check to see if the NGD flags exist
    if "ngd" not in config.keys():
        config["ngd"] = {}
    if "flags" not in config["ngd"]:
        config["ngd"]["flags"] = {}

    return config

def _get_vfiles(path):
    """Recursive inner loop"""
    #print "get recursive files for: %s" % str(path)
    file_path = []
    #dirname, dirs, fs = os.walk(path)
    for base, dirs, _ in os.walk(path):
        for d in dirs:
            p = os.path.join(base, d)
            #print "dir: %s" % p
            file_path.extend(_get_vfiles(p))

    search_path = os.path.join(path, "*.v")
    p = glob.glob(search_path)
    file_path.extend(p)
    return file_path
    

def get_xilinx_tool_types():
    """
    Returns a tuple of the xilinx build tool types

    Args:
        Nothing

    Returns:
        Tuple of build tools (string)

    Raises:
        Nothing
    """
    return TOOL_TYPES

def is_64_bit():
    """
    Returns true if the machine is 64 bits, false if 32 bits

    Args:
        Nothing

    Returns:
        Boolean:
            True: 64 bits
            False: 32 bits

    Raises:
        Nothing
    """
    return platform.machine().endswith('64')

def get_window_drives():
    """
    Returns a list of drives for a windows box

    Args:
        Nothing

    Return:
        Returns a list of drives in a list
    """
    if os.name != "nt":
        raise ConfigurationError("Not a windows box")

    import string
    from ctypes import windll

    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        #For every letter of the alphabet (string.uppercase)
        if bitmask & 1:
            #if the associated bit for that letter is set
            drives.append(letter)
        bitmaks >>= 1

    return drives

def find_xilinx_path(path = "", build_tool = "ISE", version_number = ""):
    """
    Finds the path of the xilinx build tool specified by the user

    Args:
        path (string): a path to the base directory of xilinx
            (leave empty to use the default location)
        build_type (string): to use, valid build types are found with
            get_xilinx_tool_types
            (leave empty for "ISE")
        version_number (string): specify a version number to use
            for one of the tool chain: EG
                build_tool = ISE version_number     = 13.2
                build_tool = Vivado version_number  = 2013.1
            (leave empty for the latest version)


    Returns:
        A path to the build tool, None if not found

    Raises:
        Configuration Error
    """

    #Searches for the xilinx tool in the default locations in Linux and windows
    if build_tool.lower() not in TOOL_TYPES:
        raise ConfigurationError("Build tool: (%s) not recognized \
                                  the following build tools are valid: %s" %
                                  (build_tool, str(TOOL_TYPES)))

    xilinx_base = ""
    if os.name == "posix":
        #Linux
        if len(path) > 0:
            xilinx_base = path
        else:
            xilinx_base = LINUX_XILINX_DEFAULT_BASE
            #print "linux base: %s" % xilinx_base

        #if not os.path.exists(xilinx_base):
        if not os.path.exists(xilinx_base):
            #print "path (%s) does not exists" % LINUX_XILINX_DEFAULT_BASE
            return None

    elif os.name == "nt":
        if path is not None or len(path) > 0:
            xilinx_base = path
        else:
            #Windows
            drives = get_window_drives()
            for drive in drives:
                #Check each base directory
                try:
                    dirnames = os.listdir("%s:" % drive)
                    if WINDOWS_XLINX_DEFAULT_BASE in dirnames:
                        xilinx_base = os.path.join("%s:" % drive,
                                WINDOWS_XILINX_DEFUALT_BASE)
                        if os.path.exists(xilinx_base):
                            #this doesn't exists
                            continue
                        #Found the first occurance of Xilinx drop out
                        break

                except WindowsError, err:
                    #This drive is not usable
                    pass

        if len(xiilinx_base) == 0:
                return None

    #Found the Xilinx base
    dirnames = os.listdir(xilinx_base)

    if build_tool.lower() == "ise" or build_tool.lower() == "planahead":
        "ISE and Plan Ahead"
        if len(version_number) > 0:
            if version_number not in dirnames:
                raise ConfigurationError(
                        "Version number: %s not found in %s" %
                        (version_number, xilinx_base))
            return os.path.join(xilinx_base, version_number, "ISE_DS")

        #get the ISE/planahead base
        f = -1.0
        max_float_dir = ""
        for fdir in os.listdir(xilinx_base):
            #print "fdir: %s" % fdir
            try:
                if f < float(fdir):
                    f = float(fdir)
                    #print "Found a float: %f" % f
                    max_float_dir = fdir
            except ValueError, err:
                #Not a valid numeric directory
                pass
        return os.path.join(xilinx_base, max_float_dir, "ISE_DS")

    else:
        if "Vivado" not in dirnames:
            raise ConfigurationError(
                    "Vivado is not in the xilinx directory")

        xilinx_base = os.path.join(xilinx_base, "Vivado")

        if len(os.listdir(xilinx_base)) == 0:
            raise ConfigurationError(
                    "Vivado directory is empty!")

        if len(version_number) > 0:
            if version_number in os.listdir(xilinx_base):
                xilinx_base = os.path.join(xilinx_base, version_number)
                return xilinx_base

        float_max = float(os.listdir(xilinx_base)[0])
        for f in os.listdir(xilinx_base):
            if float(f) > float_max:
                float_max = float(f)

        xilinx_base = os.path.join(xilinx_base, str(float_max))
        return xilinx_base


def create_build_directory(config):
    """
    Reads in a config dictionary and creates a output build directory

    Args:
        config: Config dictionary

    Return:
        Nothing

    Raises:
        Nothing
    """
    build_dir = DEFAULT_BUILD_DIR
    if "build_dir" in config.keys():
        build_dir = config["build_dir"]

    build_dir = os.path.join(get_project_base(), build_dir)
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    return build_dir

def get_build_directory(config, absolute = False):
    """Returns the project output directory location

    Args:
        config (dictionary): configuration dictionary
        absolute (boolean):
            False (default): Relative to project base
            True: Absolute

    Returns:
        (string): strin representation of the path to the output

    Raises:
        Nothing
    """
    build_dir = DEFAULT_BUILD_DIR
    if "build_dir" in config.keys():
        build_dir = config["build_dir"]

    if absolute:
        build_dir = os.path.join(get_project_base(), build_dir)

    return build_dir


