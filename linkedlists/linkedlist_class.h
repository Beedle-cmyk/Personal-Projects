#pragma once

namespace linkedlist
{
	class List
	{
	private:

		struct node
		{
			int data;
			node* next;

		};
		typedef struct node* nodePtr;

		nodePtr head;
		nodePtr curr;
		nodePtr temp;


	public:

		List();
		void AddNode(int addData);
		void DeleteNode(int delData);
		void PrintList();
	}
	

}
