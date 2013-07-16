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
        site_scons/xst_default_flags.json
  * "ngd": Settings for ngdbuild translator
    * "flags": Flags that can be set for the translator, any flag specified
      by the user will override the default values set in
        site_scons/ngd_default_flags.json
  * "map": Settings for map
    * "flags": Flags that can be set for the translator, any flag specified
      by the user will override the default values set in
        site_scons/map_default_flags.json
  * "par": Settings for place and route
    * "flags": Flags that can be set for the translator, any flag specified
      by the user will override the default values set in
        site_scons/par_default_flags.json
  * "trace": Settings for trace timing analysis
    * "flags": Flags that can be set for the translator, any flag specified
      by the user will override the default values set in
        site_scons/trace_default_flags.json
  * "bitgen": Settings for bitgen
    * "flags": Flags that can be set for the translator, any flag specified
      by the user will override the default values set in
        site_scons/bitgen_default_flags.json
    * "configuration": Override the default configuration, any value set in
      this block will override the default vlues set in
        site_scons/bitgen_configuration.json

#Command Line Options:

Targets:
  * xst: synthesize (verilog, [cores]) -> .ncd
  * ngd\_build: netlist translation (from abstract constructs to Xilinx 
      specific constructs)
      (.ngc -> .ngd)
  * map: mapping the xilinx specific netlist (logical design) into the
      specified xilinx component (using slices, BRAMs, and I/Os) 
      (.ngd -> .ncd)
  * par: place and route the component within the FPGA
      (.ncd -> _par.ncd)
  * bitgen: generating a bit file that can be downloaded to the FPGA
      (_par.ncd -> .bit)
  * trace: analyzing the design for timing violations
      (_par.ncd -> .twr)

Flags:
  * --debug\_build: view debug messages helpful to debug the builder
  * --config\_file: specify a different configuration file than 'config.json'
  * --clean\_build: remove all directories create by the build process
    config["build\_dir"] directory
    _xmsgs directory

#To Do:

Add support for vhdl
Add support for multiple verilog/VHDL libraries
Add support for cores
Add support for bmm
