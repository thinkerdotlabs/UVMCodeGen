<%
header_list 			= attributes['header_list']
class_name  			= attributes['class_name']
class_parent  			= attributes['class_parent']
class_name_upper  		= attributes['class_name'].upper()
class_data_list  		= attributes['class_data_list']
class_automation_list  		= attributes['class_automation_list']
blank_line = "\n"
class_vif_list  		= attributes['class_vif_list']
for line in class_vif_list:
	tokens = line.split()
%>
//
// Implementation details
//
`include "${class_name}.svh"

`ifndef ${class_name_upper}_SV
`define ${class_name_upper}_SV

//new functions
function ${class_name}::new (string name="${class_name}", ${class_parent} parent);
	super.new(name,parent);
	//User code below
	user_new();
endfunction: new

//
//connect phase
//
function void ${class_name}::connect_phase(uvm_phase phase);
  super.connect_phase(phase);
% for line in  class_vif_list:
  if(!uvm_config_db#(virtual ${line.split()[1]} )::get(this,"","${line.split()[2]}",${line.split()[2]}))
	`uvm_error("IFERROR", {"Virtual Interface should be set for - ", get_full_name(),".${line.split()[2]}"})
% endfor
  user_connect_phase(phase);
endfunction : connect_phase

//
//run phase
//
function void ${class_name}::run_phase(uvm_phase phase);
  super.run_phase(phase);
  user_run_phase(phase);
endfunction : run_phase


`endif
