#include <iostream>
#include "linkedlist_class.h"
using namespace std;
using namespace linkedlist;

/*
Create a header file that defines a class called linked list
Learn what a header file is
header is the structure


node class contains a pointer to the next node and a payload
int payload node* next

Within your class define these functions:

Add node(1 paramter) node*

int Count returns the number of nodes in a list

remove() take away a node

clear /Empties l
*/

List::List() {
    head = NULL;
    curr = NULL;
    temp = NULL;
}

void List::AddNode(int addData) 
{
    node* n = new node;
    n->next = NULL;
    n->data = addData;

    //Checking to see if there is already an item/data in the list
    //if so advance through the list until a NULL/ BLANK NODE is reached and replace that node with the new one
    //else if the node is already blank than the start is now the added node
    if (head != NULL)
    {
        curr = head;
        while (curr->next != NULL)
        {
            curr = curr->next;
        }
        curr->next = n;
    }
    else
    {
        head = n;
    }
}

void List::DeleteNode(int delData) 
{
    node* delPtr = NULL;
    temp = head;
    curr = head;
    while (curr != NULL and curr->data != delData)
    {
        temp = curr;
        curr = curr->next;
    }
    if (curr == NULL)
    {
        std::cout << delData << "Was not in the list" << std::endl;
        delete delPtr;
    }
    else
    {
        delPtr = curr;
        curr = curr->next;
        temp->next = curr;
        if (delPtr == head)
        {
            head = head->next;
            temp = NULL;
        }
        delete delPtr;
        std::cout << "The value " << delData << "was deleted" << std::endl;
    }
}

void List::PrintList()
{
    curr = head;
    while (curr != NULL)
    {
        std::cout << curr->data << std::endl;
        curr = curr->next;
    }
}



int main()
{
    List Me;
    Me.AddNode(3);
    Me.AddNode(5);
    Me.AddNode(7);
    Me.PrintList();

    Me.DeleteNode(3);
    Me.PrintList();
}