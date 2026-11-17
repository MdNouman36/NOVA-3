# 🌳 Data Structures & Algorithms Lab (DSA) — 1BCSL306 (3rd Sem)

Welcome to the **DSA Lab** module of **OILS-3** (*Oops, I Learnt Something!*), fully updated for the **VTU 2025 Scheme**.

> **Status:** ✅ All 12 Lab Experiments Verified, Bug-Free, and Ready to Compile!

---

## 📌 Experiment Directory

All verified programs are located in [`programs/`](programs/):

### PART A: FIXED EXPERIMENTS
1. **[Lab 01: Library Management](programs/lab01_library_management.c)**
   * *Concepts:* Structures, Heap dynamic memory allocation (`malloc`), linear search.
   * *Operations:* Add, Display, Search by ID, Issue book, Return book.
2. **[Lab 02: Sparse Matrix Triplet Representation](programs/lab02_sparse_matrix.c)**
   * *Concepts:* 3-column triplet representation `(row, col, value)`, Transpose, Addition.
   * *Fix:* Clean metadata header representation separating dimensions from matrix values.
3. **[Lab 03: Stack Operations Using Array](programs/lab03_stack_operations.c)**
   * *Concepts:* LIFO ADT, `push()`, `pop()`, `peek()`, `display()`, Overflow & Underflow detection.
   * *Fix:* Removed crash when testing with small stack capacities.
4. **[Lab 04: Printer Queue Simulation](programs/lab04_printer_queue.c)**
   * *Concepts:* FIFO ADT, Linear queue with single-element pointer reset (`front == rear`).
   * *Operations:* Add print job, process job, pending count, diagnostics.
5. **[Lab 05: Polynomial Addition](programs/lab05_polynomial_addition.c)**
   * *Concepts:* Singly Circular Linked List with Header Node (`head->next == head`).
   * *Fix:* Automatic descending exponent sort on insertion so terms entered in any order are summed accurately.
6. **[Lab 06: Binary Tree Creation & Traversals](programs/lab06_binary_tree_traversals.c)**
   * *Concepts:* Level-order insertion using Queue, Preorder, Inorder, and Postorder recursive traversals.

### PART B: OPEN-ENDED EXPERIMENTS
7. **[Lab 07: Infix to Postfix Conversion](programs/lab07_infix_to_postfix.c)**
   * *Concepts:* Compiler expression parser, bracket validation `()`, `{}`, `[]`, operator precedence and associativity (`^`, `*`, `/`, `+`, `-`).
8. **[Lab 08: Student Record Management SLL](programs/lab08_student_sll.c)**
   * *Concepts:* Singly Linked List, Insert after name, Delete by USN/Name.
   * *Fix:* Fixed `%49s` to `%49[^\n]` so multi-word names delete cleanly without corrupting the input buffer.
9. **[Lab 09: Manufacturing Parts Inventory](programs/lab09_parts_hash_table.c)**
   * *Concepts:* Hash Table, String polynomial rolling hash, Linear Probing collision resolution, `DELETED` tombstone markers.
10. **[Lab 10: Hierarchical Numeric Data BST](programs/lab10_bst_numeric.c)**
    * *Concepts:* Binary Search Tree (BST), Duplicate rejection, Search, Inorder ascending traversal.
11. **[Lab 11: Employee Records Hash Table](programs/lab11_employee_hash_table.c)**
    * *Concepts:* Hash Table of size 17, modulo hashing, linear probing, department filtering.
12. **[Lab 12: City Connectivity Using Graphs](programs/lab12_city_connectivity.c)**
    * *Concepts:* Graph representation with $N \times N$ Adjacency Matrix, Depth-First Search (DFS) traversal, Reachability and pairwise path verification.

---

## 🛠️ How to Compile & Run Any Program:

```bash
# Using GCC (Linux / macOS / MinGW):
gcc programs/lab01_library_management.c -o lab01
./lab01
```

Or just launch the interactive arcade:
```bash
python play.py
```
*(Choose Option `[2] 🌳 DSA Lab Studio`)*
