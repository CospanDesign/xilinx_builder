#Project: Xilinx Builder

#Goal: sCons based command line tools to interface with Xilinx tools

#How to use:

Edit the config.json file to setup a build environment, the keywords are as
    follows:
  * "name": Name of the project to be created ex: "project"
  * "build\_dir": Output directory of the project ex: "build"
  * "device": Device part number ex: "xc6slx9tqg144-3"
  * "verilog": A list of verilog files or paths
    * If the entry is a directory then all items in the diretory will be added
      * If the "recursive" flag is set to true then it will also be recusively
        searched
  * "top\_module": Top verilog module in the project
  * "constraint\_files": List of constraint files to be used
  * "xst": Setting for xst synthesizer
    * "flags": Flags that can be set for the synthesizer, any flag specified
      by the user will override the default values set in
        site_scons/sxt_default_flags.json

#Command Line Options:

Targets:
  * xst: synthesize (verilog, [cores]) -> .ncd
  * ngd\_build: netlist translation (from abstract constructs to Xilinx 
      specific constructs)
      (.ngc -> .ncd)
Flags:
  * --debug\_build: view debug messages helpful to debug the builder
  * --config\_file: specify a different configuration file than 'config.json'
  * --clean\_build: remove all directories create by the build process
    config["build\_dir"] directory
    _xmsgs directory

#To Do:

Add support for vhdl
Add support for multiple verilog/VHDL libraries
