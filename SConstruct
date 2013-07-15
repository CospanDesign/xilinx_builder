import os

import xilinx


debug = False


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
AddOption("--clean_build",
          dest="clean_build",
          action="store_true",
          help="Clean the build environment",
          default=False)

#Create an environment
env = Environment()

#parse options from the command line
debug = GetOption('build_debug')
clean_build = GetOption('clean_build')

env['CONFIG_FILE'] = GetOption('config_file')


#Add the both the XIL_SCRIPT_LOC and
#   the required paths to the environmental paths
xilinx.initialize_environment(env = env,
                              xilinx_path = "",
                              build_tool = "ISE",
                              version_number = "")


if clean_build:
  #Create a clean target
  xilinx.clean_build(env)
  Exit(0)

#get the xst tool
env.Tool('xst')
env.Tool('ngd')
env.Tool('map')
env.Tool('par')
env.Tool('trace')

if debug == True:
  d = env.Dictionary()
  keys = d.keys()
  keys.sort()
  print "WSTHIS : %s" % str(d['ENV'])
  #print "Tools: %s" % str(d["TOOLS"])
  #for key in keys:
  #  print "\t%s: %s" % (key, str(d[key]))

#Alias recognizable builder commands
env.Alias("xst", xilinx.get_xst_targets(env))
env.Alias("ngd", xilinx.get_ngd_targets(env))
env.Alias("map", xilinx.get_map_targets(env))
env.Alias("par", xilinx.get_par_targets(env))
env.Alias("trace", xilinx.get_trace_targets(env))

ngc_file = env.xst(xilinx.get_xst_targets(env), None)
ngd_file = env.ngd(xilinx.get_ngd_targets(env), ngc_file)
map_file = env.map(xilinx.get_map_targets(env), ngd_file)
par_file = env.par(xilinx.get_par_targets(env), map_file)
trace_file = env.trace(xilinx.get_trace_targets(env), par_file)







