#! /usr/bin/python

#Distributed under the MIT licesnse.
#Copyright (c) 2013 Dave McCoy (dave.mccoy@cospandesign.com)

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in 
#the Software without restriction, including without limitation the rights to 
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
#of the Software, and to permit persons to whom the Software is furnished to do 
#so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be coresd in all 
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
#SOFTWARE.


import sys
import os
import argparse
import zipfile
import shutil


base = os.path.join( os.path.dirname(__file__))

DESCRIPTION = "\n" \
"Create a new Xilinx project structure" \

EPILOG = "\n" \
"Examples:\n" \
"\n" \
"Generate a new xilinx project in the directory given:\n" \
"\ngenerate_xilinx_project.py </path/to/new_project/>\n" \
"\n"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
        description=DESCRIPTION,
        epilog=EPILOG
    )
    global debug 
    debug = False
 
    #Add an argument to the parser
    parser.add_argument("-d", "--debug", action='store_true', help="Output test debug information")
    parser.add_argument("directory", type = str, nargs=1,  default="all", help="Directory where to create the project")
    parser.parse_args()
    args = parser.parse_args()
 
    if args.debug:
        print "Debug Enable"
        debug = True
    directory = args.directory[0]


    if debug: print "Generating Project at: %s" % directory
    if not os.path.exists(directory):
        if debug: print "Path does not exist"
        os.makedirs(directory)
        if debug: print "Created directory"
 
    #Create the rtl directory
    source_path = os.path.join(directory, "rtl")
    if not os.path.exists(source_path):
        if debug: print "Source dir does not exist"
        os.makedirs(source_path)
        if debug: print "Made source path"
    #Create the cores directory
    cores_path = os.path.join(directory, "cores")
    if not os.path.exists(cores_path):
        if debug: print "Include directory does not exist"
        os.makedirs(cores_path)
        if debug: print "Made cores directory"
    #Create the constraints directory
    assem_path = os.path.join(directory, "constraints")
    if not os.path.exists(assem_path):
        if debug: print "Assembly directory does not exist"
        os.makedirs(assem_path)
        if debug: print "Made constraints directory"

    #Copy a tree
    scons_dir = os.path.join(directory, "site_scons")
    if os.path.exists(scons_dir):
        if debug: print "site scons exits, remove the previous version"
        shutil.rmtree(scons_dir)
    shutil.copytree("site_scons", scons_dir)

    sconstruct_path = os.path.join(directory, "SConstruct")
    shutil.copy2("SConstruct", sconstruct_path)

    #Copy the config.json file
    config_path = os.path.join(directory, "config.json")
    if not os.path.exists(config_path):
        if debug: print "config.json does not exists, adding it"
        shutil.copy2("config.json", config_path)

