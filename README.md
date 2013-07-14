#Project: Xilinx Builder

#Goal: sCons based command line tools to interface with Xilinx tools

#How to use:

Edit the config.json file to setup a build environment, the keywords are as follows:
  * "name": Name of the project to be created ex: "project"
  * "build\_dir": Output directory of the project ex: "build"
  * "device": Device part number ex: "xc6slx9tqg144-3"
  * "verilog": A list of verilog files or paths
    * If the entry is a directory then all items in the diretory will be added
      * If the "recursive" flag is set to true then it will also be recusively searched
  * "top\_module": Top verilog module in the project
  * "constraint\_files": List of constraint files to be used
  * "xst": Setting for xst synthesizer
    * "flags": Flags that can be set for the synthesizer, any flag specified
      by the user will override the default values set in
        site_scons/sxt_default_flags.json

#To Do:

Add support for vhdl
