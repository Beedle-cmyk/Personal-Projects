#pragma once


class DoublyLinkedList
{
private:
	struct node
	{
		int data;
		node* next;
		node* prev;
	};
	node* pHead;

public:
	DoublyLinkedList();
	~DoublyLinkedList();
	void InsertFront(int addData);
	void PrintForwards();
	void PrintBackwards();
	void DeleteNode(int delData);
	int CountList();
};