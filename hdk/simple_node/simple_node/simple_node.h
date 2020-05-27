#pragma once

#include <SOP/SOP_Node.h> // import the h file  




class Simple_SOP : public SOP_Node {   //create the new class  then inherit SOP_Node Class

public:
	static OP_Node *Constructor(OP_Network*, const char *, OP_Operator *);  //create the static pointer 

	static PRM_Template myTemplate[]; //create list for the static 

protected:

	Simple_SOP(OP_Network *net, const char *name, OP_Operator *op); //init the class by args
	virtual ~Simple_SOP(); // clean the RAM

	virtual OP_ERROR cookMySop(OP_Context &context); 




};



