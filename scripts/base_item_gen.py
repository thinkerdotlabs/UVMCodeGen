'''
This module contains class implementation.
'''
#import logging module
import logging

import box

class BaseItemGen:
    '''
    This class uses data file provided to uvmcodegen script and creates various
    lists and directories(python) that would be used by mako utility
    '''
    def __init__(self, template_data_file):
        '''
        init function to process data file.
        '''
        logger = logging.getLogger()
        self.template_data_file = template_data_file

        #open template data file and create list of lines as content list
        #process template data file to create dictonary to be used by mako
        with open(template_data_file) as fp_template_data:
            self.content = fp_template_data.read().splitlines()

        #list to hold filtered lines, removing comments
        self.filtered_content = []
        box.remove_comment_lines(self.content, self.filtered_content)
        logger.debug(self.filtered_content)

        #itrate filetered list and create various lists that needs to be used in template file
        self.header_list = []
        box.filter_header_lines(self.filtered_content, self.header_list)

        #create dictionary to be sent to template code
        self.item_dictionary = {}

        #Add header list to dictionary for template
        self.item_dictionary.setdefault('header_list', self.header_list)
        logger.debug(self.item_dictionary)

        # find class name from template data.
        self.class_name_and_parameters = box.filter_class_name(self.filtered_content)
        self.class_name = self.class_name_and_parameters[0]
        self.class_extends = self.class_name_and_parameters[1]
        self.class_parent = self.class_name_and_parameters[2]
        self.class_parameter_list = ''
        self.class_parameter_valid = 0
        if self.class_name_and_parameters[3] != 'none':
            logger.debug(self.class_name_and_parameters[3])
            self.class_parameter_list = '#(' + self.class_name_and_parameters[3]
            self.class_parameter_valid = 1
        if self.class_name_and_parameters[4] != 'none':
            logger.debug(self.class_name_and_parameters[4])
            self.class_parameter_list = self.class_parameter_list + self.class_name_and_parameters[4]
        if self.class_parameter_valid:
            self.class_parameter_list = self.class_parameter_list + ')'


        logger.debug(self.class_name_and_parameters)

        #add class name to dictionary
        self.item_dictionary.setdefault('class_name', self.class_name)
        self.item_dictionary.setdefault('class_extends', self.class_extends)
        self.item_dictionary.setdefault('class_parent', self.class_parent)
        self.item_dictionary.setdefault('class_parameter_list', self.class_parameter_list)

        #itrate filetered list and create interface lists that needs to be used in template file
        self.vif_list = []
        box.filter_vif_lines(self.filtered_content, self.vif_list)
        self.item_dictionary.setdefault('class_vif_list', self.vif_list)

        #itrate filetered list and create user methods lists that needs to be used in template file
        self.methods_list = []
        box.filter_methods_lines(self.filtered_content, self.methods_list)
        self.item_dictionary.setdefault('class_methods_list', self.methods_list)

        # create class member data and utility and automation macros input data.
        self.class_data_list = []
        self.class_automation_list = []
        box.filter_class_data(self.filtered_content, self.class_data_list, self.class_automation_list)
        self.item_dictionary.setdefault('class_data_list', self.class_data_list)
        self.item_dictionary.setdefault('class_automation_list', self.class_automation_list)

        #create constraint list
        self.class_constraints_list = []
        box.filter_class_constraints(self.filtered_content, self.class_constraints_list)
        self.item_dictionary.setdefault('class_constraints_list', self.class_constraints_list)
        logger.debug(self.class_constraints_list)

    def header_fname(self):
        '''
        This function returns the header file name
        '''
        return self.class_name + ".svh"
    def impl_fname(self):
        '''
        This fucntion returns the implementation file name
        '''
        return self.class_name + ".sv"
