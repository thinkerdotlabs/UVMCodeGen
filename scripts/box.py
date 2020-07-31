'''
This file contains various utility functions used by script
'''

#import logging module
import logging

logger = logging.getLogger()
#
# Filter input_list to remove comment lines
#
def remove_comment_lines(input_list, output_list):
    '''
    Remove comment line from input list
    '''
    #iterate main list and find for comment lines
    for line in input_list:
        if (("----" in line) or (not line)):
            pass
        else:
            output_list.append(line)
            logger.debug(line)

#
# Filter input_list for lines to be inserted before class declaration
# and push these lines in output list
#
def filter_header_lines(input_list, output_list):
    '''
    Seperate header lines to be placed above class declaration.
    '''
    #iterate main list and find for header lines
    header_found = 0
    for line in input_list:
        if '{HEADER' in line:
            #we found start of header lines
            header_found = 1
            continue
        if '}HEADER' in line:
            header_found = 0
        if header_found:
            logger.debug(line)
            output_list.append(line)

#
# Filter input_list for lines to be inserted in class for 
# methods (functions and task ) of class
#
def filter_methods_lines(input_list, output_list):
    '''
    Seperate methods declaration lines to be placed inside class declaration.
    '''
    #iterate main list and find for header lines
    methods_found = 0
    for line in input_list:
        if '{METHODS' in line:
            #we found start of interface declaration lines
            methods_found = 1
            continue
        if '}METHODS' in line:
            methods_found = 0
        if methods_found:
            logger.debug(line)
            output_list.append(line)

#
# Filter input_list for lines to be inserted in class for 
# virtual interface declaration
#
def filter_vif_lines(input_list, output_list):
    '''
    Seperate virtual interface declaration lines to be placed inside class declaration.
    '''
    #iterate main list and find for header lines
    vif_found = 0
    for line in input_list:
        if '{VIF' in line:
            #we found start of interface declaration lines
            vif_found = 1
            continue
        if '}VIF' in line:
            vif_found = 0
        if vif_found:
            logger.debug(line)
            output_list.append(line)

#
# Filter class name from the list
#
def filter_class_name(input_list):
    '''
    Filter class name and parametrs to be passed during extension of parent
    class into list and return the list
    '''
    #iterate main list and find for class name
    class_name_found = 0
    class_name_and_parameters = []
    for line in input_list:
        if '{CLASS' in line:
            class_name_found = 1
            continue
        if '}CLASS' in line:
            class_name_found = 0
            #we found class name split the line and return argument after class_name
        if class_name_found:
            logger.debug(line)
            tokens = line.split()
            class_name_and_parameters.append(tokens[1])
    return class_name_and_parameters

#
# Filter input_list
# populate class member data list and utility macro list.
#
def filter_class_data(input_list, data_list, util_macro_list):
    '''
    Filter input list for class attributes and populate output lists
    '''
    #iterate main list and find for class data
    class_data_found = 0
    class_data_member_end_found = 0
    # int =1, float = 2, enum =3
    class_data_type = 1
    usr_given_data_type = ' '
    for line in input_list:
        if '{ATTRIBUTE' in line:
            #we found start of header lines
            class_data_found = 1
            continue

        if '}ATTRIBUTE' in line:
            if ((class_data_found == 1) and (class_data_member_end_found == 1)):
                # create string to declare class data member
                str_final = " ".join([str1, str2])
                data_list.append(str_final)

                #create list to print in utility macro declaration section
                if str3.upper() != 'NONE':
                    if class_data_type == 1:
                        str_final = " ".join(["\t`uvm_field_int(", str2, ",", str3, ")"])
                    if class_data_type == 2:
                        str_final = " ".join(["\t`uvm_field_real(", str2, ",", str3, ")"])
                    if class_data_type == 3:
                        str_final = " ".join(["\t`uvm_field_enum(", usr_given_data_type, ",", str2, ",", str3, ")"])
                    util_macro_list.append(str_final)
                class_data_member_end_found = 0
            class_data_found = 0

        if class_data_found == 1:
            #split the line and create list of words
            tokens = line.split()
            if 'bit ' in  line:
                class_data_type = 1
            if 'real ' in  line:
                class_data_type = 2
            if 'enum ' in  line:
                class_data_type = 3
            if tokens[0] == 'TYPE':
                tokens.remove('TYPE')
                usr_given_data_type = tokens[1]
                str1 = ' '.join(map(str, tokens))
            if tokens[0] == 'NAME':
                tokens.remove('NAME')
                str2 = ' '.join(map(str, tokens))
            if tokens[0] == 'POLICY':
                tokens.remove('POLICY')
                str3 = ' '.join(map(str, tokens))
                class_data_member_end_found = 1

#
# Filter input_list for lines for constraint lines
# and push these lines in output list
#
def filter_class_constraints(input_list, output_list):
    '''
    Filter lines from input_list related to constraint block and
    push these lines into output list
    '''
    #iterate main list and find for header lines
    constraint_found = 0
    for line in input_list:
        if '{CONSTRAINT' in line:
            #we found start of header lines
            constraint_found = 1
            continue
        if '}CONSTRAINT' in line:
            constraint_found = 0
            logger.debug("List of constraints")
            logger.debug(output_list)
        if constraint_found:
            output_list.append(line)
