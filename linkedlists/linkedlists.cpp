#include <iostream>
#include "linkedlist_class.h"
using namespace std;
using namespace BeedlecmykInterviewQuestions;

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

LinkedList::LinkedList() {
    pHead = NULL;
}

void LinkedList::AddNode(int addData)
{
    node* n = new node;
    n->next = NULL;
    n->data = addData;

    //Checking to see if there is already an item/data in the list
    //if so advance through the list until a NULL/ BLANK NODE is reached and replace that node with the new one
    //else if the node is already blank than the start is now the added node
    if (pHead != NULL)
    {
        node* pCurrent = pHead;
        while (pCurrent->next != NULL)
        {
            pCurrent = pCurrent->next;
        }
        pCurrent->next = n;
    }
    else
    {
        pHead = n;
    }
}

void LinkedList::DeleteNode(int delData)
{
    node* delPtr = NULL;
    node* pTemp = pHead;
    node* pCurrent = pHead;
    while (pCurrent != NULL and pCurrent->data != delData)
    {
        pTemp = pCurrent;
        pCurrent = pCurrent->next;
    }
    if (pCurrent == NULL)
    {
        std::cout << delData << "Was not in the list" << std::endl;
        delete delPtr;
    }
    else
    {
        delPtr = pCurrent;
        pCurrent = pCurrent->next;
        pTemp->next = pCurrent;
        if (delPtr == pHead)
        {
            pHead = pHead->next;
            pTemp = NULL;
        }
        delete delPtr;
        std::cout << "The value " << delData << "was deleted" << std::endl;
    }
}

void LinkedList::PrintList()
{
    node* pCurrent = pHead;
    while (pCurrent != NULL)
    {
        std::cout << pCurrent->data << std::endl;
        pCurrent = pCurrent->next;
    }
}

void LinkedList::ReverseList()
{
    node* pCurrent = pHead;
    node* pPrev = NULL;
    node* Temp = NULL;

    while (pCurrent != NULL)
    {
        Temp = pCurrent->next;
        pCurrent->next = pPrev;
        pPrev = pCurrent;
        pCurrent = Temp;
    }
    pHead = pPrev;

}

//7  5  3

LinkedList::node* LinkedList::ReverseRecursively(node* pCurrent)
{


    if (pCurrent == NULL || pCurrent->next == NULL)
    {
        return pCurrent;
    }

    node* reversedLidHead = ReverseRecursively(pCurrent->next);
    pCurrent->next->next = pCurrent;
    pCurrent->next = NULL;
    return reversedLidHead;

}

int LinkedList::CountList()
{
    node* pCurrent = pHead;
    int count = 0;
    while (pCurrent != NULL)
    {
        count += 1;
        pCurrent = pCurrent->next;
    }
    cout << "Number of items in list:" << count << endl;
    return count;
}

LinkedList::~LinkedList()
{
    node* pCurrent = pHead;
    while (pCurrent != NULL) 
    {
        node* pTemp = pCurrent->next;
        delete pCurrent;
        pCurrent = pTemp;
    }
    pHead = NULL;
}

int main()
{
    LinkedList Me;
    Me.AddNode(3);
    Me.AddNode(5);
    Me.AddNode(7);
    Me.AddNode(9);
    Me.PrintList(); 
    Me.CountList();
    Me.~LinkedList();
    Me.AddNode(3);
    Me.AddNode(5);
    Me.AddNode(7);
    Me.PrintList();
    printf("vvvvvvvvvvvvvvv\n");
    Me.ReverseList();
    Me.PrintList();
    Me.ReverseRecursively();
    Me.PrintList();
}