DSA_VIVA_GAUNTLET = [
    {
        "q": "What is the difference between malloc() and calloc() in C dynamic memory allocation?",
        "options": [
            "A) malloc() initializes memory to zero; calloc() leaves garbage values.",
            "B) malloc() allocates uninitialized memory; calloc() allocates and initializes all bytes to zero.",
            "C) malloc() works on the Stack; calloc() works on the Heap.",
            "D) malloc() cannot fail; calloc() can fail."
        ],
        "ans": "B",
        "tip": "calloc(n, size) clears memory to zero. malloc(bytes) leaves whatever garbage bits were previously in RAM.",
        "praise": "Spot on! Examiners love asking this to test your understanding of heap initialization.",
        "roast": "Careful! calloc() zeroes out memory; malloc() leaves raw uninitialized garbage values."
    },
    {
        "q": "What is a 'Dangling Pointer' in C and how does it happen?",
        "options": [
            "A) A pointer that was declared but never assigned NULL.",
            "B) A pointer pointing to a memory location that has already been freed via free().",
            "C) A pointer that points to another pointer.",
            "D) A pointer initialized to point to address 0x0."
        ],
        "ans": "B",
        "tip": "After free(ptr), the pointer still holds the old address. Accessing it is undefined behavior! Always do ptr = NULL after free.",
        "praise": "Excellent! Setting ptr = NULL after free() is the mark of a professional C programmer.",
        "roast": "A dangling pointer still points to a memory address that the OS has already freed."
    },
    {
        "q": "Why is a Circular Queue superior to a standard Linear Queue implemented with an array?",
        "options": [
            "A) Circular queues use half the memory of linear queues.",
            "B) Linear queues suffer from 'false overflow' where rear reaches the end even if front slots are empty; circular queues reuse freed slots.",
            "C) Circular queues can store strings; linear queues can only store integers.",
            "D) Circular queues do not need front or rear pointers."
        ],
        "ans": "B",
        "tip": "In a linear queue, when elements are dequeued, front moves forward leaving vacant slots behind that can never be reused. Modulo arithmetic (rear+1)%MAX wraps around.",
        "praise": "Bingo! Modulo arithmetic solves the false overflow problem in circular queues.",
        "roast": "In a linear queue, once rear reaches MAX-1, it reports overflow even if index 0, 1, 2 are completely vacant!"
    },
    {
        "q": "Why do we use a dummy 'Header Node' in a Circular Linked List for Polynomial addition?",
        "options": [
            "A) Because C requires every list to have at least two nodes.",
            "B) It eliminates special-case checks for inserting into an empty list or deleting the first term.",
            "C) It automatically doubles the speed of CPU multiplication.",
            "D) It stores the degree of the polynomial in its coefficient."
        ],
        "ans": "B",
        "tip": "With a header node, the list is NEVER empty (header is always present). Insertion and deletion logic never have to branch for head == NULL.",
        "praise": "True systems engineering insight! Header nodes simplify pointer manipulation boundary conditions.",
        "roast": "Header nodes prevent messy 'if (head == NULL)' checks when manipulating linked lists."
    },
    {
        "q": "What is the worst-case time complexity of searching an element in an un-balanced Binary Search Tree (BST)?",
        "options": [
            "A) O(1)",
            "B) O(log N)",
            "C) O(N)",
            "D) O(N log N)"
        ],
        "ans": "C",
        "tip": "If elements are inserted in strictly sorted order (1, 2, 3, 4, 5), the BST degenerates into a linear linked list (skewed tree) of height N, taking O(N) time.",
        "praise": "Correct! When a BST degenerates into a skewed tree, it performs identically to a linked list.",
        "roast": "In the worst case (skewed tree), height = N, so search degrades from O(log N) to O(N)!"
    },
    {
        "q": "In Open Addressing Hash Tables, why must deleted slots be marked with a 'DELETED' tombstone instead of EMPTY?",
        "options": [
            "A) Because the OS does not allow changing an array slot to EMPTY.",
            "B) Because linear probe searches terminate on EMPTY; if marked EMPTY, keys inserted after it become permanently unreachable.",
            "C) Because EMPTY slots consume more RAM than DELETED slots.",
            "D) DELETED slots encrypt the data for cybersecurity."
        ],
        "ans": "B",
        "tip": "Linear probing stops searching as soon as it hits an EMPTY slot. If you reset a slot to EMPTY, you break the probe chain for collided keys!",
        "praise": "Outstanding! You understand collision resolution probe chains at an architectural level.",
        "roast": "If you mark a slot EMPTY upon deletion, any future search for collided keys behind it will prematurely abort and say 'Not Found'!"
    }
]

# ==============================================================================
# INTERACTIVE DATA STRUCTURE VISUALIZERS
# ==============================================================================