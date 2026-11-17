/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 01: Library Management Using Structures and Dynamic Memory
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a Program in C:
 * (a) Define a record (structure) titled Book with Book_ID, Title, Author,
 *     Price and Availability Status (Available/Issued).
 * (b) Dynamically allocate memory for N books, where N is entered by the user.
 * (c) Implement create(), display(), search(), issueBook() and returnBook().
 * (d) Provide a menu:
 *     1. Add Book Records
 *     2. Display all Book Records
 *     3. Search Book by Book ID
 *     4. Issue a Book
 *     5. Return a Book
 *     6. Exit
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - Dynamic Memory Allocation: Books are allocated on the Heap using malloc().
 *   Memory required = N * sizeof(Book).
 * - Linear Search: Finds a book in O(N) time by comparing Book_ID.
 * - State Management: Availability_Status is 1 (Available) or 0 (Issued).
 * ==============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int Book_ID;
    char Title[80];
    char Author[60];
    float Price;
    int Availability_Status; // 1 = Available, 0 = Issued
} Book;

// Global pointer to dynamic array of books and count
Book *books = NULL;
int bookCount = 0;

/*
 * Block 1: create()
 * Allocates heap memory for N books and reads their details.
 */
void create(void) {
    int i;
    printf("Enter number of books: ");
    if (scanf("%d", &bookCount) != 1 || bookCount <= 0) {
        printf("Number of books must be a positive integer.\n");
        bookCount = 0;
        return;
    }

    books = (Book *)malloc(bookCount * sizeof(Book));
    if (books == NULL) {
        printf("Error: Heap memory allocation failed!\n");
        bookCount = 0;
        return;
    }

    for (i = 0; i < bookCount; i++) {
        printf("\n--- Enter Details of Book %d ---\n", i + 1);
        printf("Book ID: ");
        scanf("%d", &books[i].Book_ID);
        printf("Title: ");
        scanf(" %79[^\n]", books[i].Title);
        printf("Author: ");
        scanf(" %59[^\n]", books[i].Author);
        printf("Price: ");
        scanf("%f", &books[i].Price);
        books[i].Availability_Status = 1; // Default to Available
    }
    printf("\n✔ %d book records created successfully in heap memory.\n", bookCount);
}

/*
 * Block 2: display()
 * Displays all records in a formatted tabular layout.
 */
void display(void) {
    int i;
    if (books == NULL || bookCount == 0) {
        printf("No book records available. Create records first.\n");
        return;
    }

    printf("\n============================= LIBRARY BOOK RECORDS =============================\n");
    printf("%-10s %-25s %-20s %-10s %-12s\n", "Book ID", "Title", "Author", "Price", "Status");
    printf("--------------------------------------------------------------------------------\n");
    for (i = 0; i < bookCount; i++) {
        printf("%-10d %-25.25s %-20.20s %-10.2f %-12s\n",
               books[i].Book_ID,
               books[i].Title,
               books[i].Author,
               books[i].Price,
               books[i].Availability_Status ? "Available" : "Issued");
    }
    printf("================================================================================\n");
}

/*
 * Block 3: search()
 * Linear search helper returning index of matching Book_ID or -1.
 */
int search(int id) {
    int i;
    for (i = 0; i < bookCount; i++) {
        if (books[i].Book_ID == id) {
            return i;
        }
    }
    return -1;
}

/*
 * Block 4: searchBook()
 * Menu-facing search that displays book information.
 */
void searchBook(void) {
    int id, pos;
    if (books == NULL || bookCount == 0) {
        printf("No book records available.\n");
        return;
    }
    printf("Enter Book ID to search: ");
    scanf("%d", &id);
    pos = search(id);
    if (pos == -1) {
        printf("Book ID %d not found in library records.\n", id);
    } else {
        printf("\n--- Book Details Found ---\n");
        printf("Book ID     : %d\n", books[pos].Book_ID);
        printf("Title       : %s\n", books[pos].Title);
        printf("Author      : %s\n", books[pos].Author);
        printf("Price       : %.2f\n", books[pos].Price);
        printf("Status      : %s\n", books[pos].Availability_Status ? "Available" : "Issued");
    }
}

/*
 * Block 5: issueBook()
 * Changes status from Available (1) to Issued (0).
 */
void issueBook(void) {
    int id, pos;
    if (books == NULL || bookCount == 0) {
        printf("No book records available. Create records first.\n");
        return;
    }
    printf("Enter Book ID to issue: ");
    scanf("%d", &id);
    pos = search(id);
    if (pos == -1) {
        printf("Book ID %d not found.\n", id);
    } else if (books[pos].Availability_Status == 0) {
        printf("Cannot issue: Book is ALREADY issued.\n");
    } else {
        books[pos].Availability_Status = 0;
        printf("✔ Book '%s' (ID: %d) successfully issued!\n", books[pos].Title, id);
    }
}

/*
 * Block 6: returnBook()
 * Changes status from Issued (0) to Available (1).
 */
void returnBook(void) {
    int id, pos;
    if (books == NULL || bookCount == 0) {
        printf("No book records available. Create records first.\n");
        return;
    }
    printf("Enter Book ID to return: ");
    scanf("%d", &id);
    pos = search(id);
    if (pos == -1) {
        printf("Book ID %d not found.\n", id);
    } else if (books[pos].Availability_Status == 1) {
        printf("Cannot return: Book is ALREADY in the library (Available).\n");
    } else {
        books[pos].Availability_Status = 1;
        printf("✔ Book '%s' (ID: %d) successfully returned and marked Available!\n", books[pos].Title, id);
    }
}

int main(void) {
    int choice;
    do {
        printf("\n========== LIBRARY MANAGEMENT SYSTEM (1BCSL306) ==========\n");
        printf("1. Add Book Records (Dynamic Allocation)\n");
        printf("2. Display All Book Records\n");
        printf("3. Search Book by Book ID\n");
        printf("4. Issue a Book\n");
        printf("5. Return a Book\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting.\n");
            break;
        }

        switch (choice) {
            case 1:
                if (books != NULL) {
                    free(books);
                    books = NULL;
                    bookCount = 0;
                }
                create();
                break;
            case 2:
                display();
                break;
            case 3:
                searchBook();
                break;
            case 4:
                issueBook();
                break;
            case 5:
                returnBook();
                break;
            case 6:
                printf("Exiting Library Management System. Freeing allocated memory.\n");
                break;
            default:
                printf("Invalid choice! Please choose [1 - 6].\n");
        }
    } while (choice != 6);

    if (books != NULL) {
        free(books);
        books = NULL;
    }
    return 0;
}

