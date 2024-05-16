#include <iostream>
#include "doublylinkedlist.h"
using namespace std;

DoublyLinkedList::DoublyLinkedList() 
{
    pHead = NULL;
}

void DoublyLinkedList::InsertFront(int addData)
{
    node* n = new node;
    n->next = pHead;
    n->prev = NULL;
    n->data = addData;


    if (pHead != NULL)
    {
        pHead->prev = n;
    }
    pHead = n;
}

void DoublyLinkedList::PrintForwards()
{
    node* pCurrent = pHead;
    while (pCurrent != NULL)
    {
        std::cout << pCurrent->data << std::endl;
        pCurrent = pCurrent->next;
    }
}

void DoublyLinkedList::PrintBackwards()
{
    node* pCurrent = pHead;
    while (pCurrent->next != NULL)
    {
        pCurrent = pCurrent->next;
    }
    while (pCurrent != NULL)
    {
        std::cout << pCurrent->data << std::endl;
        pCurrent = pCurrent->prev;
    }
}

void DoublyLinkedList::DeleteNode(int delData)
{
    node* delPtr = NULL;
    node* pTemp = pHead;
    node* pCurrent = pHead;
    node* ABC = NULL;
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
    delPtr = pCurrent;
    if (delPtr == pHead)
    {
        pHead = pHead->next;
        pHead->prev = NULL;
        pTemp = NULL;
        delete delPtr;
        std::cout << "The value " << delData << "was deleted" << std::endl;
    }
    else
    {
        ABC = pCurrent->prev;
        pCurrent = pCurrent->next;
        pTemp->next = pCurrent;
        pCurrent->prev = ABC;
        delete delPtr;
        std::cout << "The value " << delData << "was deleted" << std::endl;
    }
}

int DoublyLinkedList::CountList()
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

DoublyLinkedList::~DoublyLinkedList()
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
    DoublyLinkedList InstantiatedObject;
    InstantiatedObject.InsertFront(3);
    InstantiatedObject.InsertFront(4);
    InstantiatedObject.InsertFront(5);
    InstantiatedObject.PrintForwards();
    InstantiatedObject.CountList();
    InstantiatedObject.PrintBackwards();
    InstantiatedObject.~DoublyLinkedList();
    InstantiatedObject.CountList();
}


