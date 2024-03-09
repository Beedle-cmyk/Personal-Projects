#pragma once

//Creation of a class called List with namespace linkedlist
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


		node* head;
		node* curr;
		node* temp;

	public:

		List();
		void AddNode(int addData);
		void DeleteNode(int delData);
		void PrintList();
	};
	

}
