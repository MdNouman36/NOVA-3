DSA_DISASTER_SCENARIOS = [
    {
        "title": "🚨 DISASTER 1: The 2:00 AM Segfault on Single-Node Deletion",
        "story": "You are presenting your Singly Linked List to the examiner. With an evil smile, the examiner asks you to create a list with just ONE student and select 'Delete from End'.\n\nYou press Enter, and BAM!\n\033[91mSegmentation fault (core dumped)\033[0m\nYour screen freezes and the examiner reaches for their red pen!",
        "prompt": "Why did the deletion crash on a single-node list?",
        "choices": [
            "Your while loop did 'while (p->next->next != NULL)' without checking if 'p->next' was NULL first! Dereferencing NULL->next crashed the CPU.",
            "Linux GCC does not support deleting memory on Tuesdays.",
            "You used 'scanf' instead of 'gets_s'.",
            "You forgot to include <math.h> for pointer calculations."
        ],
        "ans_idx": 1,
        "reaction": "EXACTLY! In a 1-node list, head->next is NULL. Checking head->next->next is an illegal memory access on NULL, triggering instant SIGSEGV!"
    },
    {
        "title": "🚨 DISASTER 2: The Infinite Modulo Loop in Circular Queue",
        "story": "Your Circular Queue accepted the first 3 characters fine. But when the queue wrapped around, your program locked up at 100% CPU utilization and stopped responding to keyboard input!",
        "prompt": "What algorithmic blunder caused the circular queue to freeze?",
        "choices": [
            "You wrote '(rear + 1) / MAX' instead of '(rear + 1) % MAX' (integer division instead of modulo remainder), keeping rear stuck at 0 forever!",
            "You declared the queue array as 'char' instead of 'int'.",
            "Circular queues require dynamic memory allocation via calloc().",
            "Modulo operator only works on floating point numbers in C."
        ],
        "ans_idx": 1,
        "reaction": "NAILED IT! Modulo remainder (%) is required for wrapping around. Integer division (/) calculates quotient, collapsing rear to 0 and trapping the while loop!"
    },
    {
        "title": "🚨 DISASTER 3: The Valgrind Memory Leak Nightmare",
        "story": "Your Polynomial Addition program calculated 8x^3 + 4x^2 + 2x + 3 correctly. But the external examiner runs:\n  valgrind --leak-check=full ./poly\n\nValgrind reports in blazing red:\n\033[91mLEAK SUMMARY: definitely lost: 1,024 bytes in 16 blocks\033[0m!",
        "prompt": "What did you forget to do before the program exited?",
        "choices": [
            "You calculated POLYSUM but never traversed the circular linked lists to free() each allocated term node and header node!",
            "You used malloc() instead of realloc().",
            "Circular linked list headers cannot be freed by modern OS kernels.",
            "You passed the pointers by value instead of double pointers."
        ],
        "ans_idx": 1,
        "reaction": "SPOT ON! Every malloc() MUST have a matching free(). For a circular list, you must traverse until p == head, freeing each node along the way."
    },
    {
        "title": "🚨 DISASTER 4: The Dangling Pointer Zombie Dereference",
        "story": "To save memory in your Binary Search Tree, you called:\n  free(root);\nAnd on the very next line you wrote:\n  printf(\"%d\", root->data);\n\nThe examiner stares at you and taps the desk with a pen.",
        "prompt": "What catastrophic bug did you just commit?",
        "choices": [
            "Use-After-Free / Dangling Pointer! Memory was already handed back to the OS; reading root->data is undefined behavior.",
            "Stack overflow condition.",
            "A syntax error caught by the preprocessor.",
            "Memory thrashing."
        ],
        "ans_idx": 1,
        "reaction": "BINGO! Calling free(root) does not erase the address inside 'root'. It creates a Dangling Pointer. Always set root = NULL after free()!"
    },
    {
        "title": "🚨 DISASTER 5: The Infix-to-Postfix Stack Overflow Disaster",
        "story": "You tested 'A + B * C' and it worked. Then the examiner typed an expression with 20 nested brackets: '((((...A+B...))))'. Your stack immediately crashed!",
        "prompt": "What boundary check was missing in push()?",
        "choices": [
            "You did not check 'if (top == MAX - 1)' before incrementing top, corrupting adjacent program memory on deep bracket nesting!",
            "Parentheses cannot be stored in char arrays.",
            "Operator precedence only supports up to 3 levels in computer science.",
            "You need to use a linked list because arrays cannot store characters."
        ],
        "ans_idx": 1,
        "reaction": "CORRECT! Always enforce overflow guards: 'if (top >= MAX - 1) { report_overflow(); return; }'."
    },
    {
        "title": "🚨 DISASTER 6: The Hash Table Infinite Linear Probe Lockup",
        "story": "You have a Hash Table of size 17. You insert 17 employees. Then you search for an employee that doesn't exist. The terminal completely hangs and never returns!",
        "prompt": "Why did linear probing loop indefinitely during search on a full table?",
        "choices": [
            "Linear probing stops searching ONLY when it finds an EMPTY slot. Since the table was 100% full, it had zero EMPTY slots and looped in an endless circle!",
            "Employee number modulo 17 returned a negative index.",
            "The hash function corrupted the CPU registers.",
            "Linear probing cannot be used with prime table sizes."
        ],
        "ans_idx": 1,
        "reaction": "BRILLIANT! If load factor reaches 1.0 (no EMPTY slots), linear probing will spin forever unless you limit the loop to TABLE_SIZE iterations!"
    },
    {
        "title": "🚨 DISASTER 7: The Graph DFS Infinite Cycle Loop",
        "story": "You built a road map between City A, City B, and City C where roads form a triangle (A-B, B-C, C-A). You run DFS from City A to check connectivity, but your program crashes with a Stack Overflow due to infinite recursive calls!",
        "prompt": "What crucial data structure flag did you fail to check?",
        "choices": [
            "You forgot to check 'if (!visited[v])' before recurring, causing DFS to cycle endlessly A -> B -> C -> A -> B -> C...",
            "Graphs cannot have cycles in C.",
            "Adjacency matrices only support directed trees.",
            "Depth-First Search cannot be implemented with recursion."
        ],
        "ans_idx": 1,
        "reaction": "EXACTLY RIGHT! In cyclic graphs, the 'visited[u] = 1' flag is the lifeline that stops traversal from looping indefinitely."
    },
    {
        "title": "🚨 DISASTER 8: The SLL Reverse-Link Orphan Catastrophe",
        "story": "You wanted to insert a new node 'newNode' after node 'p'. You wrote:\n  p->next = newNode;\n  newNode->next = p->next;\n\nSuddenly, your entire list after node 'p' vanished into the void!",
        "prompt": "Why did the rest of the list disappear from memory?",
        "choices": [
            "You overwrote p->next FIRST! Now newNode->next points to itself (infinite circular trap) and the rest of the list was orphaned in RAM!",
            "You forgot to call malloc() twice.",
            "Nodes can only be inserted at the beginning of an SLL.",
            "Singly Linked Lists do not support pointers."
        ],
        "ans_idx": 1,
        "reaction": "GOLDEN RULE OF POINTERS! Always attach the new node's leash FIRST: 'newNode->next = p->next;' and THEN 'p->next = newNode;'!"
    }
]


# Extract DSA experiments & visualizers from dsa_engine

# ==============================================================================