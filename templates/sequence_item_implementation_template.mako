<%
header_list = attributes['header_list']
class_name  = attributes['class_name']
class_name_upper  = attributes['class_name'].upper()
class_data_list  = attributes['class_data_list']
class_automation_list  = attributes['class_automation_list']
blank_line = "\n"
%>
//
// Implementation details
//
`include "${class_name}.svh"

`ifndef ${class_name_upper}_SV
`define ${class_name_upper}_SV

function ${class_name}::new (string name="${class_name}");
	super.new(name);
	//User code below
	user_new(name);
endfunction: new

`endif
