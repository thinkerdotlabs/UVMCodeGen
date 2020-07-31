<%
header_list = attributes['header_list']
class_name  = attributes['class_name']
class_extends  = attributes['class_extends']
class_parent  = attributes['class_parent']
class_parameter_list  = attributes['class_parameter_list']
class_vif_list  = attributes['class_vif_list']
class_methods_list  = attributes['class_methods_list']
class_name_upper  = attributes['class_name'].upper()
class_data_list  = attributes['class_data_list']
class_constraints_list  = attributes['class_constraints_list']
class_automation_list  = attributes['class_automation_list']
blank_line = "\n"

%>

`ifndef ${class_name_upper}_SVH
`define ${class_name_upper}_SVH
//
// Provide user specific header content here
//
//
// User defined macros, typedef , enum etc. Test
//
% for line in header_list :
${line}
% endfor

${blank_line}
//
// Description of class
//
class ${class_name} extends ${class_extends} ${class_parameter_list}; 
//Register class
`uvm_components_utils(${class_name})
//
//Class virtual interface list
//
% for line in  class_vif_list:
${line};
% endfor

//
// Class attributes details
//
% for line in  class_data_list:
${line};
% endfor


//
//Constraints
//
% for line in  class_constraints_list:
${line}
% endfor

//
// Class attributes automation macros
//
`${class_parent}_utils_begin(${class_name})
% for line in  class_automation_list:
${line}
% endfor
`${class_parent}_utils_end
//
// Class constructor declaration
//
extern function new (string name="${class_name}",${class_parent} parent );
extern function user_new ();
extern virtual function void connect_phase(uvm_phase phase);
extern virtual function void user_connect_phase(uvm_phase phase);
extern virtual task run_phase(uvm_phase phase);
extern virtual task user_run_phase(uvm_phase phase);

% for line in  class_methods_list:
${line};
% endfor

endclass : ${class_name}

`endif
