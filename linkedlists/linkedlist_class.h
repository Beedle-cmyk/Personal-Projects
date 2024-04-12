#pragma once

//Creation of a class called List with namespace linkedlist
namespace BeedlecmykInterviewQuestions
{
	class LinkedList
	{
	private:
		struct node
		{
			int data;
			node* next;
		};
		node* pHead;

	public:
		LinkedList();
		~LinkedList();
		void AddNode(int addData);
		void DeleteNode(int delData);
		void PrintList();
		int CountList();
		void ReverseList();
	};
}