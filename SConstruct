import os

import xilinx


debug = False


#Help("""
#Type: 'scons debug': debug build
#""")

AddOption("--build_debug",
          dest='build_debug',
          action="store_true",
          help='view messages for debugging the build',
          default=False)
AddOption("--config_file",
          type="string",
          dest='config_file',
          action="store",
          help="specify a config file",
          default='config.json')

#Create an environment
env = Environment()

debug = GetOption('build_debug')
env['CONFIG_FILE'] = GetOption('config_file')


#Add the both the XIL_SCRIPT_LOC and
#   the required paths to the environmental paths
xilinx.initialize_environment(env = env,
                              xilinx_path = "",
                              build_tool = "ISE",
                              version_number = "")

#get the xst tool
env.Tool('xst')

if debug == True:
  d = env.Dictionary()
  keys = d.keys()
  keys.sort()
  #print "Paths: %s" % str(d['ENV'])
  print "Tools: %s" % str(d["TOOLS"])
  #for key in keys:
  #  print "\t%s: %s" % (key, str(d[key]))

env.xst()

