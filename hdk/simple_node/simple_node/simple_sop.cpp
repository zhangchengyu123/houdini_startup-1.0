#include "simple_node.h"
#include <OP/OP_OperatorTable.h>
#include <UT/UT_DSOVersion.h>
#include <OP/OP_Node.h>


PRM_Template 
Simple_SOP::myTemplate[] = {
		PRM_Template()


};

OP_Node * Simple_SOP::Constructor(OP_Network *net, const char *name, OP_Operator *op){


	return new Simple_SOP(net, name, op);


}
Simple_SOP::Simple_SOP (OP_Network *net, const char *name, OP_Operator *op):SOP_Node(net, name, op)
{

}

Simple_SOP::~Simple_SOP(){}

OP_ERROR Simple_SOP::cookMySop(OP_Context &context) {

	return error();

}

void
newSopOperator(OP_OperatorTable *table)
{
	OP_Operator *op;
	op = new OP_Operator("simple_node",                // Internal name
		"Simple",                    // UI name
		Simple_SOP::Constructor,   // How to build the SOP
		Simple_SOP::myTemplate,  // My parameters
		0,                         // Min # of sources
		0,                         // Max # of sources
		0,     // Local variables
		OP_FLAG_GENERATOR);        // Generates new geo
// After addOperator(), 'table' will take ownership of 'op'
	table->addOperator(op);


}