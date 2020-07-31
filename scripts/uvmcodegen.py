#!/usr/bin/python3
'''
This module contains the entry point function for utility 'uvmcodegen' script.
uvmcode gen utility can be used to generate Systemverilog uvm testbnech infrastructure
class code from template and input data file.

Usage instrcution can be found by executing following
    uvmcodegen --help

USAGE Example:
    uvmcodegen  <input_directory>  <output_dir> <template_data_file> \
                <header_template_file> <implementation_template_file>

<template_data_directory>       : Directory path where template data file would be searched for
<template_directory>            : Directory path where template file would be searched for
<output_directory>              : Directory path where generated output systemverilog code is placed.
<template_data_file>            : Content from this file are used along with template file for code gen
<header_template_file>          : Header file template
<implementation_template_file>  : Implementation file template
'''

#import logging module
import logging

#Import argument parser module
import argparse

#get Template module
from mako.lookup import TemplateLookup
from mako.template import Template

from base_item_gen import BaseItemGen

def main():
    '''
    Main function
    '''
    uvmcodegen_description = "uvmcodegen  <template_data_directory>  <template_directory> <output_directory> <template_data_file> "
    uvmcodegen_description = uvmcodegen_description + "<header_template_file> <implementation_template_file> "
    parser = argparse.ArgumentParser(description=uvmcodegen_description)
    parser.add_argument('-datadir', '--template_data_directory', type=str, help='Directory to find template data files', default='./')
    parser.add_argument('-tempdir', '--template_directory', type=str, help='Directory to find template files', default='./')
    parser.add_argument('-out', '--output_directory', type=str, help='Directory to store generated output files', default='./')
    parser.add_argument('template_data_file', type=str, help='Template data file')
    parser.add_argument('header_template_file', type=str, help='Header template file')
    parser.add_argument('implementation_template_file', type=str, help='Implementation template file')

    #call parser and process command line argument
    args = parser.parse_args()
    template_directory = args.template_directory
    template_data_directory = args.template_data_directory

    template_data_file = template_data_directory + args.template_data_file
    header_template_file = template_directory + args.header_template_file
    implementation_template_file = template_directory + args.implementation_template_file
    output_directory = args.output_directory

    class_to_gen = BaseItemGen(template_data_file)

    #create template object from template file
    template_lookup = TemplateLookup(directories=[template_directory])
    header_template = Template(filename=header_template_file, lookup=template_lookup)
    implementation_template = Template(filename=implementation_template_file, lookup=template_lookup)

    #use dictonary and template object to render code generation
    fname_header = output_directory + class_to_gen.header_fname()
    try:
        fp_header = open(fname_header, "w+")
    except OSError:
        print("OSError: Could not open file for writing")
    with fp_header:
        fp_header.write(header_template.render(attributes=class_to_gen.item_dictionary))

    fname_implementation = output_directory + class_to_gen.impl_fname()
    try:
        fp2_header = open(fname_implementation, "w+")
    except OSError:
        print("OSError: Could not open file for writing")
    with fp2_header:
        fp2_header.write(implementation_template.render(attributes=class_to_gen.item_dictionary))

if __name__ == "__main__":
    #
    #open and close loggerfile, Do not want to accumulate previous log
    #
    log_fname = 'run.log'
    try:
        log_fp = open(log_fname, 'w')
    except OSError:
        print("OSError: Could not open run.log file for writing")
    with log_fp:
        log_fp.close()

    #get logger object, messages would be logged into file and on screen at same time
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatstr = "[%(filename)s:%(lineno)s - %(funcName)20s() ] - %(levelname)s - %(message)s"

    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter(formatstr)
    #setup logging into file
    logfile_h = logging.FileHandler(log_fname)
    logfile_h.setLevel(logging.DEBUG)
    logfile_h.setFormatter(formatter)
    logger.addHandler(logfile_h)
    #setup logging on sceen
    screen_h = logging.StreamHandler()
    screen_h.setLevel(logging.DEBUG)
    screen_h.setFormatter(formatter)
    logger.addHandler(screen_h)

    logger.info("Running UVM Testbench infrastructure Code generator")
    main()
