"""
arcade.dsa.experiments_data — 12 VTU DSA Lab Experiments (1BCSL306, 2025 Scheme).
Features:
  - Tier 1: The Big Picture Story (What the program actually does from start to finish in plain English)
  - Tier 2: End-to-End Functional Code Blocks (First line to last line coverage)
  - Fast & Fun 3-Bullet Breakdown:
      1) 🎯 What we are doing
      2) 🔍 How it works (concise bullets on variables & mechanics)
      3) 💡 Real-world intuition / Watch out (relatable analogy or exam trap)
"""

DSA_EXPERIMENTS = [
    # ── Experiment 01 ─────────────────────────────────────────────────────────
    {
        "num": 1,
        "part": "A",
        "title": "Library Book Management (Structures & Dynamic Memory)",
        "file": "dsa-lab/programs/lab01_library_management.c",
        "story": "Imagine running a college library: instead of guessing how many books you'll get and wasting fixed memory, you ask the user for N, book the exact room on the computer's Heap using malloc(), and then let users view, search, issue, and return books by flipping a simple 1 (Available) or 0 (Issued) flag. When quitting, you free the memory so your computer doesn't get a memory leak hangover!",
        "problem": "Define Book structure (Book_ID, Title, Author, Price, Status). Dynamically allocate memory for N books on the heap using malloc(). Implement create(), display(), search(), issueBook(), returnBook(), and main menu.",
        "concept": "Dynamic heap allocation using malloc(N * sizeof(Book)). Pointers allow allocating exact bytes at runtime rather than fixed array sizes.",
        "blocks": [
            {
                "title": "Part 1: The Book Blueprint & Global Pointers",
                "code": "typedef struct {\n    int Book_ID;\n    char Title[80];\n    char Author[60];\n    float Price;\n    int Availability_Status; // 1 = Available, 0 = Issued\n} Book;\n\nBook *books = NULL; // Points to the dynamic heap array\nint bookCount = 0;   // How many books currently stored",
                "doing": "We pack all the info about a single book (ID, title, author, price, and status) into one custom data type called 'Book', and set up a pointer to hold the collection.",
                "how": [
                    "`Book` bundles 5 different variables together so they move as one block.",
                    "`books = NULL` starts as an empty pointer sitting safely at memory address 0x0.",
                    "`Availability_Status`: acts like a simple light switch — 1 for on-shelf, 0 for borrowed."
                ],
                "watchout": "Always initialize pointers to NULL. A wild uninitialized pointer points to random garbage RAM!"
            },
            {
                "title": "Part 2: create() — Reserving Heap Space & Reading Data",
                "code": "void create(void) {\n    printf(\"Enter number of books: \");\n    scanf(\"%d\", &bookCount);\n\n    // Ask the OS for exact bytes on the Heap\n    books = (Book *)malloc(bookCount * sizeof(Book));\n    if (books == NULL) {\n        printf(\"Memory allocation failed!\\n\");\n        return;\n    }\n    for (int i = 0; i < bookCount; i++) {\n        // Read Book_ID, Title, Author, Price, set Status = 1\n    }\n}",
                "doing": "Asks the user how many books they have, orders the exact amount of RAM from the operating system, and fills in the book details.",
                "how": [
                    "`malloc(bookCount * sizeof(Book))` asks the OS for N book slots sitting contiguously on the Heap.",
                    "`if (books == NULL)` is our safety airbag — if the laptop is out of RAM, malloc returns NULL.",
                    "The loop populates each book and marks its availability flag to 1 (ready to borrow)."
                ],
                "watchout": "Think of malloc like booking hotel rooms for N guests: always check if the hotel gave you rooms before sending guests inside!"
            },
            {
                "title": "Part 3: display() & search() — Reading the Records",
                "code": "void display(void) {\n    for (int i = 0; i < bookCount; i++) {\n        printf(\"%-8d %-25s %-20s %-8.2f %s\\n\",\n            books[i].Book_ID, books[i].Title, books[i].Author,\n            books[i].Price, books[i].Availability_Status ? \"Available\" : \"Issued\");\n    }\n}\n\nint search(int id) {\n    for (int i = 0; i < bookCount; i++) {\n        if (books[i].Book_ID == id) return i; // Found at index i!\n    }\n    return -1; // Not found\n}",
                "doing": "Prints a neat formatted table of all books and provides a search function to locate any book by its ID number.",
                "how": [
                    "`display()` loops through 0 to `bookCount - 1` and uses a ternary `? :` operator to print 'Available' or 'Issued'.",
                    "`search(id)` compares `books[i].Book_ID == id` one by one (Linear Search, O(N)).",
                    "Returns the array index `i` if found, or `-1` if the book doesn't exist."
                ],
                "watchout": "Always return -1 for 'not found' because index 0 is a completely valid array slot!"
            },
            {
                "title": "Part 4: issueBook() & returnBook() — Flipping the Flag",
                "code": "void issueBook(int id) {\n    int idx = search(id);\n    if (idx == -1) { printf(\"Book not found!\\n\"); return; }\n    if (books[idx].Availability_Status == 0) {\n        printf(\"Already issued!\\n\");\n    } else {\n        books[idx].Availability_Status = 0;\n        printf(\"Book %d successfully issued!\\n\", id);\n    }\n}\n\nvoid returnBook(int id) {\n    int idx = search(id);\n    if (idx != -1 && books[idx].Availability_Status == 0) {\n        books[idx].Availability_Status = 1; // Mark returned\n    }\n}",
                "doing": "Checks if the book is available to borrow (switches flag 1 -> 0) or returns it back to the shelf (switches flag 0 -> 1).",
                "how": [
                    "Calls our `search(id)` helper first to find where the book lives in memory.",
                    "If already 0, warns you cannot borrow an already-borrowed book.",
                    "If available, flips `Availability_Status` to 0; `returnBook` flips it back to 1."
                ],
                "watchout": "Never issue a book without checking its current status first — double-issuing is a classic exam bug."
            },
            {
                "title": "Part 5: main() Menu & Freeing Heap Memory",
                "code": "int main(void) {\n    int choice, id;\n    while (1) {\n        // Menu: 1.Create 2.Display 3.Search 4.Issue 5.Return 6.Exit\n        scanf(\"%d\", &choice);\n        if (choice == 6) break;\n        // switch-case dispatch...\n    }\n    // Cleanup before program exits\n    if (books != NULL) {\n        free(books);\n        books = NULL;\n    }\n    return 0;\n}",
                "doing": "Runs the interactive console menu loop, and cleanly returns the borrowed heap memory back to the OS before shutting down.",
                "how": [
                    "`while (1)` keeps the application running until the student selects choice 6 (Exit).",
                    "`free(books)` hands the heap memory block back to the operating system.",
                    "`books = NULL` prevents a Dangling Pointer bug so nothing can accidentally access freed RAM."
                ],
                "watchout": "Rule of C: Every malloc() in your code must have a matching free() before your program says goodbye!"
            }
        ],
        "challenge": {
            "prompt": "What happens if you run free(books) but forget to set 'books = NULL', and later write 'books[0].Price = 200'?",
            "opts": [
                "A) The compiler catches the error at compile time.",
                "B) The computer automatically re-allocates a new array.",
                "C) Use-After-Free (Dangling Pointer) crash or memory corruption, because that RAM was already surrendered to the OS.",
                "D) Nothing happens, it is completely valid code in C."
            ],
            "correct_opt": "C",
            "hint": "free() marks the RAM as available to other programs. Accessing it is illegal memory access.",
            "praise": "Spot on! That's the classic Dangling Pointer trap examiners love to test.",
            "roast": "Accessing memory after free() causes undefined behavior and segmentation faults!"
        }
    },

    # ── Experiment 02 ─────────────────────────────────────────────────────────
    {
        "num": 2,
        "part": "A",
        "title": "Sparse Matrix Triplet Representation, Addition & Transpose",
        "file": "dsa-lab/programs/lab02_sparse_matrix.c",
        "story": "Imagine a giant 1000x1000 game map that is 99% empty ocean with just 4 islands. Storing all 1,000,000 zeroes wastes massive RAM! Instead, a Sparse Matrix saves only the non-zero cells as a 3-column table: (Row, Col, Value). In this experiment, row 0 acts as the header holding matrix size and island count, and we learn how to add two maps and flip rows with columns (transpose) super fast!",
        "problem": "Represent two sparse matrices in triplet form (row, column, value) where element [0] stores matrix metadata (rows, columns, total non-zeros). Perform addition and transpose.",
        "concept": "A sparse matrix is one where most elements are zero. Triplet representation stores only non-zero elements as (row, col, value), reducing space from O(M*N) to O(non_zeros).",
        "blocks": [
            {
                "title": "Part 1: The Triplet Definition & Header Metadata",
                "code": "typedef struct {\n    int row;\n    int col;\n    int val;\n} Term;\n\nTerm a[MAX], b[MAX], c[MAX];\n// a[0] is the HEADER: a[0].row = total_rows, a[0].col = total_cols, a[0].val = count_non_zeros",
                "doing": "Defines a 3-field coordinate tuple and reserves index [0] to hold the blueprint size of the matrix.",
                "how": [
                    "`Term` stores the exact grid coordinates `(row, col)` and the actual non-zero number `val`.",
                    "`a[0]` is special: it doesn't store a matrix cell! It stores `(total_rows, total_cols, total_non_zeros)`.",
                    "Elements `a[1]` through `a[k]` store the actual non-zero entries in row-major order."
                ],
                "watchout": "Remember matrix index 0 is the metadata label, not the first matrix element!"
            },
            {
                "title": "Part 2: readMatrix() — Storing Only Non-Zeroes",
                "code": "void readMatrix(Term a[], int r, int c) {\n    a[0].row = r;\n    a[0].col = c;\n    int k = 1, elem;\n    for (int i = 0; i < r; i++) {\n        for (int j = 0; j < c; j++) {\n            scanf(\"%d\", &elem);\n            if (elem != 0) {\n                a[k].row = i;\n                a[k].col = j;\n                a[k].val = elem;\n                k++;\n            }\n        }\n    }\n    a[0].val = k - 1; // Total non-zero elements found\n}",
                "doing": "Scans the normal 2D grid input and filters out all the useless zeroes, recording only the living non-zero numbers.",
                "how": [
                    "Scans every cell `(i, j)`. If `elem == 0`, it simply skips it!",
                    "If `elem != 0`, packs `(i, j, elem)` into `a[k]` and increments `k`.",
                    "At the end, `a[0].val = k - 1` records the total count of non-zero entries."
                ],
                "watchout": "Notice space drops from N*M down to just `(non-zeros + 1) * 3` integers!"
            },
            {
                "title": "Part 3: addSparse() — The Two-Pointer Zipper Merge",
                "code": "void addSparse(Term a[], Term b[], Term c[]) {\n    int i = 1, j = 1, k = 1;\n    while (i <= a[0].val && j <= b[0].val) {\n        if (a[i].row == b[j].row && a[i].col == b[j].col) {\n            c[k] = a[i];\n            c[k].val = a[i].val + b[j].val;\n            i++; j++; k++;\n        } else if (a[i].row < b[j].row || (a[i].row == b[j].row && a[i].col < b[j].col)) {\n            c[k++] = a[i++];\n        } else {\n            c[k++] = b[j++];\n        }\n    }\n    // Copy leftovers from a or b...\n}",
                "doing": "Zips together two sorted triplet lists: if two elements share the exact same cell, we add them; otherwise, we take whichever comes first in order.",
                "how": [
                    "Pointers `i` and `j` walk through matrices A and B like runners on a track.",
                    "Match: same `(row, col)`? Add their values: `c[k].val = a[i].val + b[j].val`.",
                    "Mismatch: whichever coordinate comes earlier in row-major order gets copied to C first."
                ],
                "watchout": "Think of this like merging two sorted decks of cards — runs in fast O(NonZeros_A + NonZeros_B) time!"
            },
            {
                "title": "Part 4: transpose() — Swapping Rows and Columns",
                "code": "void transpose(Term a[], Term b[]) {\n    b[0].row = a[0].col;\n    b[0].col = a[0].row;\n    b[0].val = a[0].val;\n    int k = 1;\n    for (int col = 0; col < a[0].col; col++) {\n        for (int i = 1; i <= a[0].val; i++) {\n            if (a[i].col == col) {\n                b[k].row = a[i].col;\n                b[k].col = a[i].row;\n                b[k].val = a[i].val;\n                k++;\n            }\n        }\n    }\n}",
                "doing": "Turns the matrix sideways by swapping every element's row with its column, keeping the result sorted.",
                "how": [
                    "`b[0].row = a[0].col` and `b[0].col = a[0].row` inverts the matrix dimensions in the header.",
                    "Outer loop checks columns `0, 1, ..., col-1` in ascending order.",
                    "Whenever it finds a matching column, it swaps `(col, row)` into matrix B so the output stays row-major sorted!"
                ],
                "watchout": "A common mistake is forgetting to swap row and column dimensions in the header element `b[0]`."
            }
        ],
        "challenge": {
            "prompt": "If a 10x10 matrix has only 3 non-zero elements, how many rows will its triplet representation array occupy?",
            "opts": [
                "A) Exactly 3 rows",
                "B) 100 rows",
                "C) 30 rows",
                "D) 4 rows (1 header row + 3 data rows)"
            ],
            "correct_opt": "D",
            "hint": "Don't forget row [0] is reserved for the header metadata!",
            "praise": "Bingo! 1 header row at index 0 plus 3 data rows = 4 rows total.",
            "roast": "Remember: index 0 is the header (rows, cols, non-zeros), so total entries is non-zeros + 1!"
        }
    },

    # ── Experiment 03 ─────────────────────────────────────────────────────────
    {
        "num": 3,
        "part": "A",
        "title": "Stack Operations Using an Array (PUSH, POP, PEEK)",
        "file": "dsa-lab/programs/lab03_stack_operations.c",
        "story": "Think of a spring-loaded stack of cafeteria trays: you can only place a tray on top (PUSH), remove the tray from the top (POP), or inspect what's currently on top without touching it (PEEK). That's LIFO (Last-In, First-Out)! In this lab, we build this using an integer array and a single pointer variable called 'top'.",
        "problem": "Implement a Stack of integers using a 1D array of fixed size MAX. Support PUSH, POP, PEEK, and DISPLAY operations with boundary overflow and underflow checks.",
        "concept": "LIFO (Last-In, First-Out) linear data structure. All insertions (push) and deletions (pop) occur at a single end called 'top'.",
        "blocks": [
            {
                "title": "Part 1: The Stack Storage & Empty State",
                "code": "#define MAX 5\nint stack[MAX];\nint top = -1; // -1 means empty stack!",
                "doing": "Creates the memory slots for the stack and initializes the top tracker to -1.",
                "how": [
                    "`stack[MAX]` is our contiguous storage box in RAM of size 5.",
                    "`top = -1` indicates that 0 items are in the stack. Since index 0 is a valid slot, -1 safely marks 'empty'."
                ],
                "watchout": "Why not top = 0? Because stack[0] is the first real element! top = -1 means nothing exists yet."
            },
            {
                "title": "Part 2: push() — Adding with Overflow Protection",
                "code": "void push(int val) {\n    if (top == MAX - 1) {\n        printf(\"Stack Overflow! Stack is full\\n\");\n        return;\n    }\n    top = top + 1;\n    stack[top] = val;\n    printf(\"%d pushed successfully\\n\", val);\n}",
                "doing": "Checks if there is space in the stack, climbs up one slot (`top++`), and writes the new number into memory.",
                "how": [
                    "`if (top == MAX - 1)`: The Overflow guard! In an array of size 5, slots are 0 to 4. If top is 4, it's packed.",
                    "`top = top + 1` advances the pointer to the next free slot.",
                    "`stack[top] = val` puts the value inside."
                ],
                "watchout": "Always check boundary BEFORE incrementing top, or you'll corrupt memory outside the array!"
            },
            {
                "title": "Part 3: pop() & peek() — Removing & Inspecting",
                "code": "int pop(void) {\n    if (top == -1) {\n        printf(\"Stack Underflow! Stack is empty\\n\");\n        return -1;\n    }\n    int item = stack[top];\n    top = top - 1; // Drop pointer down one level\n    return item;\n}\n\nvoid peek(void) {\n    if (top != -1) printf(\"Top item: %d\\n\", stack[top]);\n}",
                "doing": "Pulls the topmost item off the stack (`pop`) or peeks at it without removing anything (`peek`).",
                "how": [
                    "`if (top == -1)`: The Underflow guard! You can't pull a tray out of an empty cafeteria dispenser.",
                    "`item = stack[top]` grabs the top number.",
                    "`top = top - 1` drops the boundary down. The old number stays in RAM but is now logically dead."
                ],
                "watchout": "Pop actually modifies 'top' (O(1)); peek only reads 'stack[top]' without touching 'top'."
            },
            {
                "title": "Part 4: display() & main() Menu Loop",
                "code": "void display(void) {\n    if (top == -1) { printf(\"Stack is empty\\n\"); return; }\n    for (int i = top; i >= 0; i--) {\n        printf(\"| %4d | %s\\n\", stack[i], (i == top) ? \"<-- TOP\" : \"\");\n    }\n}\n\nint main(void) {\n    // Interactive menu loop with 1.Push 2.Pop 3.Peek 4.Display 5.Exit\n}",
                "doing": "Prints the stack vertically from top down to index 0, and runs the interactive menu loop.",
                "how": [
                    "Loop starts at `i = top` and counts DOWN to `0` to reflect real LIFO visual order.",
                    "`(i == top) ? \"<-- TOP\" : \"\"` tags the topmost item so the student can see the pointer."
                ],
                "watchout": "Examiners will ask: 'Does popping an item overwrite the RAM with 0?' Answer: No! It just moves 'top' down."
            }
        ],
        "challenge": {
            "prompt": "If you perform PUSH(10), PUSH(20), POP(), PUSH(30) on an empty stack, what does PEEK() return?",
            "opts": [
                "A) 10",
                "B) 30",
                "C) 20",
                "D) -1"
            ],
            "correct_opt": "B",
            "hint": "Push 10 -> [10]. Push 20 -> [10, 20]. Pop() removes 20 -> [10]. Push 30 -> [10, 30].",
            "praise": "Spot on! 30 is at the top of the stack.",
            "roast": "Trace it: 20 was popped, and 30 was pushed right on top of 10!"
        }
    },

    # ── Experiment 04 ─────────────────────────────────────────────────────────
    {
        "num": 4,
        "part": "A",
        "title": "Printer Queue Simulation Using an Array",
        "file": "dsa-lab/programs/lab04_printer_queue.c",
        "story": "Imagine an office network printer: print jobs must be printed in the exact order they arrive — First-In, First-Out (FIFO)! But in a plain array, once rear hits the end, you get a 'False Overflow' even if the front slots are totally empty. A Circular Queue fixes this with the magic of Modulo Arithmetic (% MAX), making the array wrap around like a clock!",
        "problem": "Simulate a printer job queue using a Circular Queue of size MAX. Implement insert (enqueue), delete (dequeue), and display using modulo wrap-around arithmetic.",
        "concept": "FIFO (First-In, First-Out) linear structure. Elements are inserted at REAR and removed from FRONT. Circular queues resolve the 'false overflow' limitation of linear arrays.",
        "blocks": [
            {
                "title": "Part 1: Queue Storage & Pointer Initialization",
                "code": "#define MAX 5\nint queue[MAX];\nint front = -1, rear = -1; // -1 means queue is empty",
                "doing": "Sets up the print queue array and two pointers: 'front' (where jobs leave) and 'rear' (where new jobs arrive).",
                "how": [
                    "`front`: points to the oldest job waiting in line.",
                    "`rear`: points to the newest job that just joined the line.",
                    "Both start at `-1` because the queue is initially empty."
                ],
                "watchout": "Queue has TWO ends: additions at REAR, deletions from FRONT. Unlike Stack which has only ONE end (TOP)."
            },
            {
                "title": "Part 2: enqueue() — Circular Insertion & Full Check",
                "code": "void enqueue(int job_id) {\n    // Check if the next slot wraps around and hits front\n    if ((rear + 1) % MAX == front) {\n        printf(\"Printer Queue Full! (Circular Overflow)\\n\");\n        return;\n    }\n    if (front == -1) front = 0; // First job arrival\n    rear = (rear + 1) % MAX;    // Wrap around to 0 if at MAX-1\n    queue[rear] = job_id;\n}",
                "doing": "Inserts a new print job at the circular rear, wrapping around to index 0 if space was freed up front.",
                "how": [
                    "`(rear + 1) % MAX == front`: The Circular Full formula! If advancing rear lands on front, the ring is full.",
                    "`front == -1`: When the very first element arrives, front moves from -1 to 0.",
                    "`rear = (rear + 1) % MAX`: Modulo operator `% 5` turns `4 + 1` into index `0` seamlessly!"
                ],
                "watchout": "Modulo arithmetic (% MAX) is the secret sauce that stops False Overflow dead in its tracks."
            },
            {
                "title": "Part 3: dequeue() — Processing Jobs & Empty Reset",
                "code": "int dequeue(void) {\n    if (front == -1) {\n        printf(\"Printer Queue Empty! No jobs to print.\\n\");\n        return -1;\n    }\n    int job = queue[front];\n    if (front == rear) {\n        // Exactly ONE job was left — queue is now empty\n        front = -1;\n        rear = -1;\n    } else {\n        front = (front + 1) % MAX; // Circularly advance front\n    }\n    return job;\n}",
                "doing": "Takes the job at the front of the line, sends it to the printer, and resets the queue when the last job finishes.",
                "how": [
                    "`front == -1`: Underflow check — can't print when no jobs exist.",
                    "`front == rear`: The last job check! When front catches rear, reset both to `-1` so the queue starts fresh.",
                    "`front = (front + 1) % MAX`: Circularly moves front to the next waiting customer."
                ],
                "watchout": "Always remember the `front == rear` reset check! Forgetting it leaves front wandering forever."
            },
            {
                "title": "Part 4: display() & Main Menu",
                "code": "void display(void) {\n    if (front == -1) { printf(\"Queue is empty\\n\"); return; }\n    int i = front;\n    while (1) {\n        printf(\"[%d] Job #%d\\n\", i, queue[i]);\n        if (i == rear) break;\n        i = (i + 1) % MAX; // Circular loop traversal\n    }\n}",
                "doing": "Traverses and displays all jobs from front to rear along the circular ring buffer.",
                "how": [
                    "Starts at `i = front` and advances with `i = (i + 1) % MAX`.",
                    "Stops the moment `i == rear` because rear marks the end of the line."
                ],
                "watchout": "You cannot use a simple `for(i=front; i<=rear; i++)` in circular queues because rear can be smaller than front!"
            }
        ],
        "challenge": {
            "prompt": "In a circular queue of size 5, if front = 2 and rear = 1, is the queue full or empty?",
            "opts": [
                "A) The queue is empty.",
                "B) The queue has an error state.",
                "C) The queue is completely full, because (rear + 1) % 5 == (1 + 1) % 5 == 2 == front.",
                "D) The queue has only 1 element."
            ],
            "correct_opt": "C",
            "hint": "Calculate (rear + 1) % 5: (1 + 1) % 5 = 2. Since this equals front (2), the ring is full!",
            "praise": "Brilliant math! When (rear + 1) % MAX == front, every single slot in the ring is occupied.",
            "roast": "Calculate (rear + 1) % MAX: (1 + 1) % 5 = 2 == front, meaning it is completely full!"
        }
    },

    # ── Experiment 05 ─────────────────────────────────────────────────────────
    {
        "num": 5,
        "part": "A",
        "title": "Polynomial Addition Using Circular Linked List with Header",
        "file": "dsa-lab/programs/lab05_polynomial_addition.c",
        "story": "Algebra time! How do you add polynomials like (5x^3 + 4x^2 + 2) and (3x^3 + 6x + 1)? In C, each term is a node: (Coefficient, Exponent, Next). By connecting the last term back to a dummy Header Node (with exponent -1), we turn the list into a circle! This eliminates annoying NULL checks and makes polynomial addition a clean 3-case comparison.",
        "problem": "Represent two multivariate or single-variable polynomials using circular singly linked lists with a header node. Implement polynomial addition and display the resulting polynomial.",
        "concept": "Polynomials represented as linked lists of terms (coeff, exp). A circular header node (exp = -1) eliminates NULL pointer edge-case checks and keeps the list cyclic.",
        "blocks": [
            {
                "title": "Part 1: The Term Node & Circular Header",
                "code": "typedef struct Node {\n    int coeff;\n    int exp;\n    struct Node *next;\n} Node;\n\nNode* create_header(void) {\n    Node *head = (Node *)malloc(sizeof(Node));\n    head->coeff = 0;\n    head->exp = -1;    // Sentinel exponent: smaller than any valid power (>= 0)\n    head->next = head; // Points to ITSELF in a circle!\n    return head;\n}",
                "doing": "Defines each math term node and creates a special sentinel Header Node that loops back to itself.",
                "how": [
                    "`coeff` stores the multiplier (e.g., 5), `exp` stores the power of x (e.g., 3).",
                    "`head->exp = -1`: A dummy exponent so it never accidentally matches real terms (which have powers >= 0).",
                    "`head->next = head`: A circle with 0 terms points right back to itself."
                ],
                "watchout": "The header node is not a real math term! It's an anchor that keeps the list in an unbroken loop."
            },
            {
                "title": "Part 2: attach() — Appending Terms to the Ring",
                "code": "void attach(int c, int e, Node *head) {\n    Node *newNode = (Node *)malloc(sizeof(Node));\n    newNode->coeff = c;\n    newNode->exp = e;\n\n    // Find the last node before the header\n    Node *curr = head;\n    while (curr->next != head) {\n        curr = curr->next;\n    }\n    newNode->next = head; // New node points back to header\n    curr->next = newNode; // Old tail points to new node\n}",
                "doing": "Creates a new term node and splices it in right before the header, keeping the circular ring intact.",
                "how": [
                    "Allocates memory for `newNode` and sets its coefficient and exponent.",
                    "`while (curr->next != head)` walks until it reaches the current last term.",
                    "Wired: `curr -> newNode -> head`."
                ],
                "watchout": "Always connect `newNode->next = head` first before severing the old tail link!"
            },
            {
                "title": "Part 3: add_poly() — The 3-Case Algebra Matcher",
                "code": "void add_poly(Node *h1, Node *h2, Node *h3) {\n    Node *p1 = h1->next;\n    Node *p2 = h2->next;\n    while (p1 != h1 && p2 != h2) {\n        if (p1->exp == p2->exp) {\n            int sum = p1->coeff + p2->coeff;\n            if (sum != 0) attach(sum, p1->exp, h3);\n            p1 = p1->next; p2 = p2->next;\n        } else if (p1->exp > p2->exp) {\n            attach(p1->coeff, p1->exp, h3);\n            p1 = p1->next;\n        } else {\n            attach(p2->coeff, p2->exp, h3);\n            p2 = p2->next;\n        }\n    }\n    // Attach remaining terms from p1 or p2...\n}",
                "doing": "Compares powers of terms from Polynomial 1 and 2, adding like terms and copying higher powers first.",
                "how": [
                    "Case 1 (`exp1 == exp2`): Like powers! Add coefficients (`5 + 3 = 8`) and advance both pointers.",
                    "Case 2 (`exp1 > exp2`): Term 1 has higher power -> attach `p1` term to result, advance `p1`.",
                    "Case 3 (`exp1 < exp2`): Term 2 has higher power -> attach `p2` term to result, advance `p2`."
                ],
                "watchout": "Loop ends when a pointer hits its `head` sentinel, leaving leftover terms to be attached after."
            },
            {
                "title": "Part 4: display() & Memory Deallocation",
                "code": "void display_poly(Node *head) {\n    Node *curr = head->next;\n    if (curr == head) { printf(\"0\\n\"); return; }\n    while (curr != head) {\n        printf(\"%dx^%d \", curr->coeff, curr->exp);\n        curr = curr->next;\n        if (curr != head) printf(\"+ \");\n    }\n    printf(\"\\n\");\n}",
                "doing": "Walks the circular list until it circles back to the header, printing standard polynomial math format.",
                "how": [
                    "`curr = head->next` skips the dummy header and starts at the highest term.",
                    "Prints each `coeff` and `exp` separated by `+` signs.",
                    "`while (curr != head)` safely terminates the loop once a full lap is completed."
                ],
                "watchout": "Notice there is zero check for NULL anywhere in this function! That's the beauty of circular headers."
            }
        ],
        "challenge": {
            "prompt": "What is the loop termination condition when traversing a circular linked list with a header node?",
            "opts": [
                "A) curr == NULL",
                "B) curr->next == NULL",
                "C) curr == head (we completed a full circle back to the header)",
                "D) curr->exp == 0"
            ],
            "correct_opt": "C",
            "hint": "The list is circular! It never ends in NULL — it loops back to the header node.",
            "praise": "Exactly right! Circular lists terminate when the pointer cycles back to the header.",
            "roast": "In a circular list there is no NULL! The loop stops when `curr == head`."
        }
    },

    # ── Experiment 06 ─────────────────────────────────────────────────────────
    {
        "num": 6,
        "part": "A",
        "title": "Binary Tree Creation & Traversals (Level-Order via Queue)",
        "file": "dsa-lab/programs/lab06_binary_tree_traversals.c",
        "story": "Trees are how computers organize file folders, game decisions, and search indexes! A Binary Tree gives every parent at most 2 children: Left and Right. You can explore a tree by diving deep down branches (DFS: Inorder, Preorder, Postorder) or by touring level-by-level like floors in a building (BFS: Level-Order using a Queue).",
        "problem": "Create a Binary Tree dynamically. Implement recursive Inorder, Preorder, Postorder traversals, and Breadth-First Level-Order traversal using an auxiliary Queue.",
        "concept": "Non-linear hierarchical data structure. Each node has at most two children (left and right). Level-order traversal uses a FIFO queue to visit nodes level by level.",
        "blocks": [
            {
                "title": "Part 1: The Binary Tree Node & Allocation",
                "code": "typedef struct Node {\n    int data;\n    struct Node *left;\n    struct Node *right;\n} Node;\n\nNode* create_node(int val) {\n    Node *newNode = (Node *)malloc(sizeof(Node));\n    newNode->data = val;\n    newNode->left = NULL;\n    newNode->right = NULL;\n    return newNode;\n}",
                "doing": "Defines a tree node holding a number and two branch pointers (left and right), and a creator function.",
                "how": [
                    "`data`: the value inside this branch fork.",
                    "`*left` and `*right`: pointers to child nodes down the hierarchy.",
                    "Both child pointers start as `NULL` because newly born nodes are leaves with no children yet."
                ],
                "watchout": "Always initialize left and right to NULL. Uninitialized pointers cause wild crashes during traversals."
            },
            {
                "title": "Part 2: The 3 Recursive DFS Traversals",
                "code": "void inorder(Node *root) {   // Left -> Root -> Right\n    if (root == NULL) return;\n    inorder(root->left);\n    printf(\"%d \", root->data);\n    inorder(root->right);\n}\nvoid preorder(Node *root) {  // Root -> Left -> Right\n    if (root == NULL) return;\n    printf(\"%d \", root->data);\n    preorder(root->left);\n    preorder(root->right);\n}\nvoid postorder(Node *root) { // Left -> Right -> Root\n    if (root == NULL) return;\n    postorder(root->left);\n    postorder(root->right);\n    printf(\"%d \", root->data);\n}",
                "doing": "Visits every node in the tree using recursion. The only difference is WHEN you print the root!",
                "how": [
                    "Inorder: Left first, then print Root, then Right.",
                    "Preorder: Print Root FIRST, then dive Left and Right.",
                    "Postorder: Dive Left and Right first, then print Root LAST (used for deleting trees!)."
                ],
                "watchout": "Base case `if (root == NULL) return` is critical — without it, recursion never stops and crashes the stack."
            },
            {
                "title": "Part 3: Level-Order (BFS) Traversal using Queue",
                "code": "void level_order(Node *root) {\n    if (root == NULL) return;\n    enqueue(root); // Put root on queue\n    while (!is_empty()) {\n        Node *curr = dequeue(); // Pop front node\n        printf(\"%d \", curr->data);\n        // Push its children to queue for next level\n        if (curr->left != NULL) enqueue(curr->left);\n        if (curr->right != NULL) enqueue(curr->right);\n    }\n}",
                "doing": "Visits the tree level-by-level (floor 1, floor 2, floor 3) using a FIFO queue.",
                "how": [
                    "`enqueue(root)`: Starts by putting the top node in line.",
                    "`dequeue()`: Takes a node, prints it, and lines up its left and right children in the queue.",
                    "Because a queue is First-In First-Out, all nodes on the current level get printed before the next level starts!"
                ],
                "watchout": "DFS uses the Call Stack (recursion); BFS uses a Queue (iterative). Examiners love asking this difference!"
            }
        ],
        "challenge": {
            "prompt": "If a binary tree has root 1 with left child 2 and right child 3, what is its Inorder traversal?",
            "opts": [
                "A) 1 2 3",
                "B) 2 1 3",
                "C) 3 2 1",
                "D) 2 3 1"
            ],
            "correct_opt": "B",
            "hint": "Inorder is Left -> Root -> Right. Left is 2, Root is 1, Right is 3.",
            "praise": "Spot on! Left (2) -> Root (1) -> Right (3) = 2 1 3.",
            "roast": "Inorder rule: Left -> Root -> Right. So 2 then 1 then 3!"
        }
    },

    # ── Experiment 07 ─────────────────────────────────────────────────────────
    {
        "num": 7,
        "part": "B",
        "title": "Infix-to-Postfix Conversion with Bracket Validation",
        "file": "dsa-lab/programs/lab07_infix_to_postfix.c",
        "story": "Humans love Infix notation like (A + B) * C, but compilers hate parentheses because they require scanning back and forth! Computers convert this into Postfix notation: A B + C *. In postfix, operators come right after their operands, eliminating all parentheses. We use Dijkstra's famous Shunting-Yard operator stack algorithm to do this conversion.",
        "problem": "Convert an infix expression containing operators (+, -, *, /, ^) and parentheses into postfix form using a character Stack, validating matching brackets.",
        "concept": "Translates human-readable infix expressions (A + B) into parenthesis-free postfix expressions (A B +) using Dijkstra's Shunting-Yard operator stack algorithm.",
        "blocks": [
            {
                "title": "Part 1: Operator Precedence Hierarchy",
                "code": "int precedence(char op) {\n    switch (op) {\n        case '^': return 3; // Exponents bind tightest\n        case '*':\n        case '/':\n        case '%': return 2; // Multiplications & divisions\n        case '+':\n        case '-': return 1; // Additions & subtractions\n        default:  return 0; // Parentheses & others\n    }\n}",
                "doing": "Gives each math symbol an authority rank so the computer knows who gets evaluated first (BODMAS).",
                "how": [
                    "`^` (Power) has the highest priority (3).",
                    "`*` and `/` have medium priority (2).",
                    "`+` and `-` have lowest priority (1)."
                ],
                "watchout": "Parentheses return 0 so they stay pinned inside the stack until their closing partner arrives."
            },
            {
                "title": "Part 2: The Shunting-Yard Conversion Algorithm",
                "code": "for (int i = 0; infix[i] != '\\0'; i++) {\n    char ch = infix[i];\n    if (isalnum(ch)) {\n        postfix[k++] = ch; // Operands (A, B, 5) go straight to output!\n    } else if (ch == '(') {\n        push(ch);          // Open paren waits on stack\n    } else if (ch == ')') {\n        while (top != -1 && stack[top] != '(') {\n            postfix[k++] = pop(); // Empty operators between ( and )\n        }\n        pop(); // Discard the '('\n    } else {\n        // Operator arrived: pop higher/equal precedence operators first!\n        while (top != -1 && precedence(stack[top]) >= precedence(ch)) {\n            postfix[k++] = pop();\n        }\n        push(ch);\n    }\n}",
                "doing": "Reads the math expression letter by letter: operands pass straight to output, while operators wait on the stack until their turn.",
                "how": [
                    "Letters/numbers (`isalnum`) bypass the stack directly into `postfix`.",
                    "Opening `(` goes on stack; closing `)` pops everything back until `(` is reached.",
                    "Operators: If the incoming operator has LOWER priority than what's on top of stack, pop the top operator first!"
                ],
                "watchout": "Notice that parentheses NEVER appear in the postfix output! They do their job and get thrown away."
            },
            {
                "title": "Part 3: Flushing the Stack to Output",
                "code": "// Pop all remaining operators left in the stack\nwhile (top != -1) {\n    postfix[k++] = pop();\n}\npostfix[k] = '\\0'; // Null-terminate postfix string",
                "doing": "Drains whatever operators remain on the stack into the final postfix output string and null-terminates it.",
                "how": [
                    "Pops all remaining operators in LIFO order.",
                    "Adds string terminator `'\\0'` so printf can print the completed postfix formula."
                ],
                "watchout": "Always null-terminate strings in C (`\\0`). Forgetting this prints garbage memory characters."
            }
        ],
        "challenge": {
            "prompt": "What is the postfix equivalent of the infix expression: A + B * C?",
            "opts": [
                "A) A B C * +",
                "B) A B + C *",
                "C) + A * B C",
                "D) A B * C +"
            ],
            "correct_opt": "A",
            "hint": "* has higher precedence than +, so B * C evaluates first (BC*), then adds to A giving ABC*+.",
            "praise": "Spot on! Multiplication binds first: B * C -> BC*, then + A -> ABC*+.",
            "roast": "* has higher precedence than +, so BC* happens first, then + A -> ABC*+!"
        }
    },

    # ── Experiment 08 ─────────────────────────────────────────────────────────
    {
        "num": 8,
        "part": "B",
        "title": "Student Record Management Using Singly Linked List (SLL)",
        "file": "dsa-lab/programs/lab08_student_sll.c",
        "story": "Arrays have a big problem: resizing them is expensive and inserting at the front requires shifting every element. A Singly Linked List (SLL) fixes this! Each student is an independent node on the Heap holding data and a leash (`next` pointer) to the next student. You can add or drop students at the front or back instantaneously just by moving pointer leashes!",
        "problem": "Create a Singly Linked List of Student nodes (USN, Name, Branch, Sem, Phone). Implement insert front, insert end, delete front, delete end, and display with node count.",
        "concept": "Dynamic linear chain of nodes connected by forward pointers. Memory is allocated on the heap per node, enabling dynamic sizing without pre-allocating fixed arrays.",
        "blocks": [
            {
                "title": "Part 1: The Student Node Definition",
                "code": "typedef struct Student {\n    char usn[20];\n    char name[50];\n    char branch[10];\n    int sem;\n    char phno[15];\n    struct Student *next; // The leash pointing to the next student!\n} Student;\n\nStudent *head = NULL; // Points to the first student in list",
                "doing": "Defines the student node with all personal details plus a pointer that links to the next student in line.",
                "how": [
                    "`struct Student *next`: Self-referential pointer. Stores the RAM address of the next node.",
                    "`head = NULL`: When the list is empty, head points to nowhere (NULL)."
                ],
                "watchout": "Head is not a student! Head is just a pointer variable holding the address of the first student."
            },
            {
                "title": "Part 2: insert_front() & insert_end() — Adding Students",
                "code": "Student* insert_front(Student *head) {\n    Student *newNode = (Student *)malloc(sizeof(Student));\n    // read student data...\n    newNode->next = head; // 1. Attach new node's leash to current first node\n    head = newNode;       // 2. Head now points to new node!\n    return head;\n}\n\nStudent* insert_end(Student *head) {\n    Student *newNode = (Student *)malloc(sizeof(Student));\n    newNode->next = NULL; // It's going to be the new tail\n    if (head == NULL) return newNode;\n    Student *curr = head;\n    while (curr->next != NULL) curr = curr->next; // Walk to tail\n    curr->next = newNode; // Attach to old tail\n    return head;\n}",
                "doing": "Adds a student to the very beginning (O(1)) or walks to the very end of the chain to attach them (O(N)).",
                "how": [
                    "`insert_front`: Point `newNode->next = head`, then update `head = newNode`. Takes instantaneous O(1) time!",
                    "`insert_end`: Walks `while (curr->next != NULL)` until finding the node that has no successor, then attaches `newNode`."
                ],
                "watchout": "In insert_front, ALWAYS connect `newNode->next = head` FIRST before moving `head`! Otherwise you lose the whole list."
            },
            {
                "title": "Part 3: delete_front() & delete_end() — Removing Safely",
                "code": "Student* delete_front(Student *head) {\n    if (head == NULL) { printf(\"List empty\\n\"); return NULL; }\n    Student *temp = head; // Save address of node being deleted\n    head = head->next;    // Move head to second node\n    free(temp);           // Free memory!\n    return head;\n}\n\nStudent* delete_end(Student *head) {\n    if (head == NULL || head->next == NULL) { free(head); return NULL; }\n    Student *curr = head;\n    while (curr->next->next != NULL) curr = curr->next; // Stop 1 step before tail\n    free(curr->next);     // Free tail\n    curr->next = NULL;    // Sever link\n    return head;\n}",
                "doing": "Deletes the first or last student, advancing pointers and freeing heap memory so no RAM is leaked.",
                "how": [
                    "`delete_front`: Save `temp = head`, move `head = head->next`, then `free(temp)`.",
                    "`delete_end`: Lookahead loop `curr->next->next != NULL` stops at the second-to-last node, freeing `curr->next` and setting `curr->next = NULL`."
                ],
                "watchout": "Lookahead trap: On a 1-node list, checking `curr->next->next` crashes with segfault! Always handle 1-node lists separately."
            }
        ],
        "challenge": {
            "prompt": "What is the time complexity to insert a new node at the FRONT of a singly linked list?",
            "opts": [
                "A) O(1) constant time",
                "B) O(N) linear time",
                "C) O(N^2) quadratic time",
                "D) O(log N)"
            ],
            "correct_opt": "A",
            "hint": "You just point new_node->next = head and head = new_node. No loop needed!",
            "praise": "Exactly right! Insert at front is instantaneous O(1) because no traversal is required.",
            "roast": "Insert at front does not need to traverse! It is always O(1) constant time."
        }
    },

    # ── Experiment 09 ─────────────────────────────────────────────────────────
    {
        "num": 9,
        "part": "B",
        "title": "Manufacturing Parts Inventory Using Hash Table & Linear Probing",
        "file": "dsa-lab/programs/lab09_parts_hash_table.c",
        "story": "Searching an array of 10,000 car parts one by one takes forever (O(N)). A Hash Table gives you instant O(1) speed! You pass the Part ID into a mathematical Hash Function (`key % TABLE_SIZE`), which directly tells you the exact index where that part lives! When two different parts hash to the same bucket (Collision), we use Linear Probing: just park in the very next open slot!",
        "problem": "Create a Hash Table of size M to store manufacturing part records (Part_ID, Part_Name). Implement division hash function and linear probing collision resolution.",
        "concept": "Direct addressing using a hash function (key % TABLE_SIZE) provides O(1) average lookup. Collisions (two keys hashing to the same bucket) are resolved via Linear Probing.",
        "blocks": [
            {
                "title": "Part 1: The Hash Table Bucket Storage",
                "code": "#define TABLE_SIZE 10\ntypedef struct {\n    int part_id;\n    char part_name[50];\n    int occupied; // 1 = contains part, 0 = empty slot\n} HashEntry;\n\nHashEntry table[TABLE_SIZE];",
                "doing": "Defines an array of table slots where each slot has an `occupied` flag to distinguish empty slots from filled ones.",
                "how": [
                    "`part_id` and `part_name`: the data being stored.",
                    "`occupied`: initialized to 0 across all slots so we know which buckets are currently free."
                ],
                "watchout": "Always initialize occupied flags to 0! Without it, garbage memory looks like real records."
            },
            {
                "title": "Part 2: The Hash Function & Linear Probing Insert",
                "code": "int hash(int key) {\n    return key % TABLE_SIZE; // Division hash method\n}\n\nvoid insert(int id, char *name) {\n    int index = hash(id);\n    int start = index;\n    while (table[index].occupied == 1) {\n        if (table[index].part_id == id) { printf(\"Duplicate ID!\\n\"); return; }\n        index = (index + 1) % TABLE_SIZE; // Step to next slot\n        if (index == start) { printf(\"Hash Table Full!\\n\"); return; }\n    }\n    table[index].part_id = id;\n    strcpy(table[index].part_name, name);\n    table[index].occupied = 1;\n}",
                "doing": "Calculates the home index with modulo, and if another car part is already parked there, probes step-by-step for the next open slot.",
                "how": [
                    "`hash(id) = id % 10`: Maps any number to indices `0..9`.",
                    "`while (table[index].occupied == 1)`: Loop detects collision and steps forward with `(index + 1) % 10`.",
                    "`if (index == start)`: If we loop all the way around back to where we started, the table is 100% full!"
                ],
                "watchout": "Think of linear probing like looking for a parking spot: if spot 3 is taken, you check 4, then 5, until you find an empty spot."
            },
            {
                "title": "Part 3: search() — Tracing the Probe Chain",
                "code": "int search(int id) {\n    int index = hash(id);\n    int start = index;\n    while (table[index].occupied == 1) {\n        if (table[index].part_id == id) return index; // Found!\n        index = (index + 1) % TABLE_SIZE;\n        if (index == start) break;\n    }\n    return -1; // Hit an empty slot or full circle -> doesn't exist\n}",
                "doing": "Jumps directly to the hash bucket and follows the same probe chain until finding the key or hitting an empty slot.",
                "how": [
                    "Computes `index = hash(id)` and checks if `table[index].part_id == id`.",
                    "If not, steps along the probe chain.",
                    "Crucial rule: If it hits an empty slot (`occupied == 0`), it STOPS immediately — because if the key existed, it would have been placed there!"
                ],
                "watchout": "Hitting an empty slot proves the item doesn't exist, preventing needless full table scans."
            }
        ],
        "challenge": {
            "prompt": "If TABLE_SIZE is 7, what index does Part ID 23 hash to initially?",
            "opts": [
                "A) Index 3",
                "B) Index 2 (because 23 % 7 = 2)",
                "C) Index 5",
                "D) Index 1"
            ],
            "correct_opt": "B",
            "hint": "Divide 23 by 7: 7 * 3 = 21, leaving remainder 2.",
            "praise": "Correct! 23 % 7 leaves remainder 2.",
            "roast": "Modulo arithmetic: 23 % 7 = 2 (since 21 + 2 = 23)!"
        }
    },

    # ── Experiment 10 ─────────────────────────────────────────────────────────
    {
        "num": 10,
        "part": "B",
        "title": "Hierarchical Numeric Data Using Binary Search Tree (BST)",
        "file": "dsa-lab/programs/lab10_bst_numeric.c",
        "story": "What if a tree could organize numbers so you can search a million items in just 20 questions? That's a Binary Search Tree (BST)! The rule is simple: everything SMALLER than the root goes to the LEFT; everything LARGER goes to the RIGHT. Best of all: if you print a BST using Inorder traversal (Left-Root-Right), the numbers come out automatically sorted in ascending order!",
        "problem": "Construct a Binary Search Tree of integers dynamically. Implement iterative/recursive insert, inorder traversal (sorted order), and search for a given key.",
        "concept": "Binary Search Tree property: for every node, all values in its Left Subtree are smaller, and all values in its Right Subtree are greater. Inorder traversal produces sorted output.",
        "blocks": [
            {
                "title": "Part 1: The BST Node Structure",
                "code": "typedef struct Node {\n    int data;\n    struct Node *left;\n    struct Node *right;\n} Node;\n\nNode *root = NULL; // Initially tree is empty",
                "doing": "Defines the binary tree node holding a number and two branch pointers (left and right), with root initialized to NULL.",
                "how": [
                    "`data`: the integer number.",
                    "`*left`: holds the subtree containing strictly smaller values.",
                    "`*right`: holds the subtree containing strictly larger values."
                ],
                "watchout": "BSTs generally discard duplicate values because every key represents a unique slot."
            },
            {
                "title": "Part 2: insert() — The Left vs Right Decision Loop",
                "code": "Node* insert(Node *root, int val) {\n    if (root == NULL) {\n        Node *newNode = (Node *)malloc(sizeof(Node));\n        newNode->data = val;\n        newNode->left = newNode->right = NULL;\n        return newNode;\n    }\n    if (val < root->data) {\n        root->left = insert(root->left, val);   // Smaller -> go Left!\n    } else if (val > root->data) {\n        root->right = insert(root->right, val); // Larger -> go Right!\n    }\n    return root;\n}",
                "doing": "Recursively compares the new number with current nodes: steers Left if smaller, steers Right if larger, and creates a leaf when hitting NULL.",
                "how": [
                    "`val < root->data`: Routes the insertion into the Left subtree.",
                    "`val > root->data`: Routes the insertion into the Right subtree.",
                    "`root == NULL`: Reached the empty spot where this number belongs; allocates new node and returns it up the tree."
                ],
                "watchout": "Notice recursion naturally attaches the new node to the parent's pointer as the stack unwinds."
            },
            {
                "title": "Part 3: inorder() & search() — Sorted Output & O(log N) Lookup",
                "code": "void inorder(Node *root) {\n    if (root == NULL) return;\n    inorder(root->left);       // 1. Visit all smaller numbers\n    printf(\"%d \", root->data); // 2. Print current root\n    inorder(root->right);      // 3. Visit all larger numbers\n}\n\nNode* search(Node *root, int key) {\n    if (root == NULL || root->data == key) return root;\n    if (key < root->data) return search(root->left, key);  // Left\n    return search(root->right, key);                       // Right\n}",
                "doing": "Inorder traversal prints numbers in perfectly sorted order, and search finds keys in fast O(log N) average time.",
                "how": [
                    "Inorder (Left -> Root -> Right): visits smallest numbers first, yielding natural ascending sort order.",
                    "Search: Discards half the entire tree with every comparison: if `key < root->data`, skip the whole right branch!"
                ],
                "watchout": "Examiner favorite viva question: 'How do you sort numbers using a BST?' Answer: Insert them and run Inorder traversal!"
            }
        ],
        "challenge": {
            "prompt": "If you insert keys 50, 30, 70, 20, 40 into an empty BST, where does 40 end up?",
            "opts": [
                "A) Left child of 20",
                "B) Right child of 70",
                "C) Left child of 50",
                "D) Right child of 30 (since 40 < 50 goes Left to 30, and 40 > 30 goes Right)"
            ],
            "correct_opt": "D",
            "hint": "40 is less than 50 (go Left to 30), and 40 is greater than 30 (go Right).",
            "praise": "Spot on! 40 < 50 branches left, then 40 > 30 branches right.",
            "roast": "Trace it from root: 40 < 50 (left to 30), then 40 > 30 (right of 30)!"
        }
    },

    # ── Experiment 11 ─────────────────────────────────────────────────────────
    {
        "num": 11,
        "part": "B",
        "title": "Employee Record Management Using Hash Table & Linear Probing",
        "file": "dsa-lab/programs/lab11_employee_hash_table.c",
        "story": "Similar to car parts, human resource departments store thousands of employee files. In this experiment, each employee has an ID, Name, and Salary. We hash the 4-digit Employee ID into a table using `emp_id % MAX_SIZE`, resolve collisions using Linear Probing, and inspect table occupancy.",
        "problem": "Create a Hash Table to manage Employee records (Emp_ID, Name, Salary). Implement division hash function, linear probing for collisions, and search by Emp_ID.",
        "concept": "Hash Table implementation storing structured multi-field records. Demonstrates primary key hashing and collision handling.",
        "blocks": [
            {
                "title": "Part 1: The Employee Record & Table Array",
                "code": "#define MAX_SIZE 10\ntypedef struct {\n    int emp_id;\n    char name[50];\n    float salary;\n    int occupied; // 0 = empty, 1 = filled\n} Employee;\n\nEmployee emp_table[MAX_SIZE];",
                "doing": "Sets up the table of employee slots with flags indicating whether each desk is occupied.",
                "how": [
                    "`emp_id`: Primary key used to calculate the hash address.",
                    "`occupied`: Prevents reading uninitialized data when searching empty buckets."
                ],
                "watchout": "Remember that employee records can have multiple data fields, but the hash function operates only on the Primary Key."
            },
            {
                "title": "Part 2: insert() — Hash Mapping & Collisions",
                "code": "void insert_employee(int id, char *name, float sal) {\n    int index = id % MAX_SIZE;\n    int start = index;\n    while (emp_table[index].occupied == 1) {\n        if (emp_table[index].emp_id == id) {\n            printf(\"Duplicate Employee ID!\\n\");\n            return;\n        }\n        index = (index + 1) % MAX_SIZE;\n        if (index == start) { printf(\"Table Full!\\n\"); return; }\n    }\n    emp_table[index].emp_id = id;\n    strcpy(emp_table[index].name, name);\n    emp_table[index].salary = sal;\n    emp_table[index].occupied = 1;\n}",
                "doing": "Hashes the employee ID to a bucket and probes linearly if another coworker already has that bucket.",
                "how": [
                    "Takes `id % MAX_SIZE` as the ideal bucket.",
                    "If occupied, slides to `(index + 1) % MAX_SIZE`.",
                    "Saves all details once an empty slot is claimed."
                ],
                "watchout": "If table size is 10, IDs 1012 and 1022 will collide because both end in 2!"
            },
            {
                "title": "Part 3: search_employee() — Probing for the Key",
                "code": "void search_employee(int id) {\n    int index = id % MAX_SIZE;\n    int start = index;\n    while (emp_table[index].occupied != 0) {\n        if (emp_table[index].occupied == 1 && emp_table[index].emp_id == id) {\n            printf(\"Found: %s, Salary: %.2f at index %d\\n\", emp_table[index].name, emp_table[index].salary, index);\n            return;\n        }\n        index = (index + 1) % MAX_SIZE;\n        if (index == start) break;\n    }\n    printf(\"Employee ID %d Not Found!\\n\", id);\n}",
                "doing": "Locates an employee by recalculating the hash and scanning forward until the record is found or an empty slot indicates they do not exist.",
                "how": [
                    "Begins search at `id % MAX_SIZE`.",
                    "Follows the same linear probe trail until `emp_id` matches.",
                    "Stops immediately if an unoccupied slot (`occupied == 0`) is reached."
                ],
                "watchout": "If you hit an empty slot, the search terminates early with 'Not Found' because any valid insertion would have stopped right there."
            }
        ],
        "challenge": {
            "prompt": "If Employee ID 1012 and 1022 are inserted into a hash table of size 10, what happens?",
            "opts": [
                "A) They collide at index 2; 1022 probes forward to the next available slot (index 3).",
                "B) The computer throws an exception.",
                "C) 1022 overwrites 1012 and erases it.",
                "D) The table expands automatically."
            ],
            "correct_opt": "A",
            "hint": "1012 % 10 = 2, and 1022 % 10 = 2. A collision occurs, resolved by linear probing.",
            "praise": "Correct! They collide at index 2, and linear probing places 1022 in slot 3.",
            "roast": "Both keys hash to index 2 (remainder 2), causing a collision resolved by linear probing!"
        }
    },

    # ── Experiment 12 ─────────────────────────────────────────────────────────
    {
        "num": 12,
        "part": "B",
        "title": "City Connectivity Using Graphs & Depth-First Search (DFS)",
        "file": "dsa-lab/programs/lab12_city_connectivity.c",
        "story": "Are all cities connected by roads, or is some town stranded on an island? In this experiment, we model cities as Graph Vertices and roads as Edges in a 2D Adjacency Matrix. Using Depth-First Search (DFS), we start at City 0 and dive down road after road as far as we can go. If our `visited` array shows every city was reached, the whole country is connected!",
        "problem": "Represent city road networks as a Graph using an Adjacency Matrix. Implement Depth-First Search (DFS) to determine if all cities are reachable from a starting city.",
        "concept": "Graph traversal using an Adjacency Matrix. DFS explores as deep as possible along each branch before backtracking, determining connected components and reachability.",
        "blocks": [
            {
                "title": "Part 1: The Adjacency Matrix & Visited Array",
                "code": "#define MAX 10\nint adj[MAX][MAX];     // adj[i][j] = 1 if road exists, 0 if not\nint visited[MAX] = {0}; // visited[i] = 1 once city i is reached\nint n;                  // Total number of cities",
                "doing": "Represents the road map as a grid where cell (i, j) = 1 means a direct road connects City i to City j.",
                "how": [
                    "`adj[i][j]`: 2D matrix storing road connections.",
                    "`visited[i]`: Keeps track of cities we have already explored so we don't run in endless circles!"
                ],
                "watchout": "The visited array is essential in graphs — without it, circular roads cause infinite loops!"
            },
            {
                "title": "Part 2: dfs() — The Deep Dive Explorer",
                "code": "void dfs(int u) {\n    visited[u] = 1; // Mark city u as visited\n    printf(\"Visited City %d\\n\", u);\n    for (int v = 0; v < n; v++) {\n        // If direct road exists AND city v has not been visited yet:\n        if (adj[u][v] == 1 && !visited[v]) {\n            dfs(v); // Drive down this road recursively!\n        }\n    }\n}",
                "doing": "Visits city `u`, marks it off on our map, and immediately drives down the first unexplored road it finds.",
                "how": [
                    "Marks `visited[u] = 1` immediately.",
                    "Loops through all possible destinations `v` from 0 to `n-1`.",
                    "If `adj[u][v] == 1` and `visited[v] == 0`, recurses into `dfs(v)`."
                ],
                "watchout": "DFS uses the system Call Stack to remember its path, backtracking automatically when hitting a dead end."
            },
            {
                "title": "Part 3: Connectivity Verification",
                "code": "int is_connected = 1;\nfor (int i = 0; i < n; i++) {\n    if (visited[i] == 0) {\n        is_connected = 0; // City i was never reached!\n        break;\n    }\n}\nif (is_connected) printf(\"All cities are connected!\\n\");\nelse printf(\"Graph is disconnected!\\n\");",
                "doing": "Checks our checklist after DFS finishes: if every city has a checkmark (visited = 1), the network is fully connected.",
                "how": [
                    "Scans `visited[0]` through `visited[n-1]`.",
                    "If even a single city has `visited[i] == 0`, it means that city was cut off from the start node."
                ],
                "watchout": "In directed graphs, starting city matters! Starting at an isolated vertex won't reach the rest of the graph."
            }
        ],
        "challenge": {
            "prompt": "What data structure does recursive Depth-First Search (DFS) implicitly rely on for backtracking?",
            "opts": [
                "A) Queue",
                "B) Hash Table",
                "C) Call Stack (Function recursion stack)",
                "D) Circular Linked List"
            ],
            "correct_opt": "C",
            "hint": "Function calls push stack frames onto the Call Stack and pop them when returning (backtracking).",
            "praise": "Exactly right! Recursion uses the CPU Call Stack for DFS traversal.",
            "roast": "DFS relies on a Stack (the system recursion call stack); BFS relies on a Queue!"
        }
    }
]
