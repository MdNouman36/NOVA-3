/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 08: Student Record Management Using Singly Linked List (SLL)
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Manage student records using a linked list. Store USN, Name, Semester and
 * Department. Support insertion, display all, display by semester, insertion
 * after a specified name, and deletion by USN or name.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - Dynamic Node: Allocated via malloc() with data fields and next pointer.
 * - Insertion at End: Traverse to last node (p->next == NULL), attach new node.
 * - Insertion After Name: Find node where strcmp(p->name, target) == 0:
 *     newNode->next = p->next;
 *     p->next = newNode;
 * - Deletion with Traversal: Track previous pointer (prev):
 *     if deleting head : *head = p->next;
 *     else             : prev->next = p->next;
 *     free(p);
 * ==============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct StudentNode {
    char usn[20];
    char name[50];
    char dept[30];
    int sem;
    struct StudentNode *next;
} StudentNode;

/*
 * Block 1: createStudent()
 * Allocates heap memory for one student record.
 */
StudentNode* createStudent(void) {
    StudentNode *n = (StudentNode *)malloc(sizeof(StudentNode));
    if (n == NULL) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    printf("  USN        : ");
    scanf(" %19s", n->usn);
    printf("  Name       : ");
    scanf(" %49[^\n]", n->name);
    printf("  Semester   : ");
    scanf("%d", &n->sem);
    printf("  Department : ");
    scanf(" %29[^\n]", n->dept);
    n->next = NULL;
    return n;
}

/*
 * Block 2: addStudent() [Insert at End]
 */
void addStudent(StudentNode **head) {
    StudentNode *newNode = createStudent();
    if (*head == NULL) {
        *head = newNode;
        printf("✔ Student record added as the first node.\n");
        return;
    }
    StudentNode *p = *head;
    while (p->next != NULL) {
        p = p->next;
    }
    p->next = newNode;
    printf("✔ Student record appended at the end of the list.\n");
}

/*
 * Block 3: displayStudents()
 */
void displayStudents(StudentNode *head) {
    if (head == NULL) {
        printf("No student records found. List is empty.\n");
        return;
    }
    printf("\n============================= STUDENT RECORDS =============================\n");
    printf("%-15s %-22s %-6s %-15s\n", "USN", "Name", "Sem", "Department");
    printf("---------------------------------------------------------------------------\n");
    StudentNode *p = head;
    int count = 0;
    while (p != NULL) {
        printf("%-15s %-22.22s %-6d %-15s\n", p->usn, p->name, p->sem, p->dept);
        count++;
        p = p->next;
    }
    printf("===========================================================================\n");
    printf("Total registered students: %d\n", count);
}

/*
 * Block 4: displayBySemester()
 */
void displayBySemester(StudentNode *head, int targetSem) {
    if (head == NULL) {
        printf("List is empty.\n");
        return;
    }
    printf("\n--- Students in Semester %d ---\n", targetSem);
    StudentNode *p = head;
    int found = 0;
    while (p != NULL) {
        if (p->sem == targetSem) {
            printf("• %-15s | %-20s | Dept: %s\n", p->usn, p->name, p->dept);
            found++;
        }
        p = p->next;
    }
    if (found == 0) {
        printf("No students found in Semester %d.\n", targetSem);
    }
}

/*
 * Block 5: insertAfterName()
 */
void insertAfterName(StudentNode **head) {
    if (*head == NULL) {
        printf("List is empty! Add initial students first.\n");
        return;
    }
    char targetName[50];
    printf("Enter existing Student Name after whom to insert: ");
    scanf(" %49[^\n]", targetName);

    StudentNode *p = *head;
    while (p != NULL && strcmp(p->name, targetName) != 0) {
        p = p->next;
    }

    if (p == NULL) {
        printf("❌ Student with name '%s' not found!\n", targetName);
        return;
    }

    printf("\nEnter details of the new student to insert after '%s':\n", targetName);
    StudentNode *newNode = createStudent();
    newNode->next = p->next;
    p->next = newNode;
    printf("✔ New student inserted directly after '%s'!\n", targetName);
}

/*
 * Block 6: deleteStudent()
 * FIXED: Uses %49[^\n] so deletion by multi-word names works reliably!
 */
void deleteStudent(StudentNode **head) {
    if (*head == NULL) {
        printf("List is empty. Nothing to delete.\n");
        return;
    }

    int mode;
    char key[50];
    printf("Delete by: 1. USN  2. Name\nChoice: ");
    if (scanf("%d", &mode) != 1 || (mode != 1 && mode != 2)) {
        printf("Invalid choice.\n");
        return;
    }

    printf("Enter %s to delete: ", (mode == 1) ? "USN" : "Name");
    scanf(" %49[^\n]", key); // FIX: reads spaces in names!

    StudentNode *p = *head;
    StudentNode *prev = NULL;

    while (p != NULL) {
        int match = (mode == 1) ? (strcmp(p->usn, key) == 0)
                                : (strcmp(p->name, key) == 0);
        if (match) {
            if (prev == NULL) {
                *head = p->next; // Deleting head node
            } else {
                prev->next = p->next; // Bypass p
            }
            printf("✔ Student '%s' (USN: %s) deleted and memory freed.\n", p->name, p->usn);
            free(p);
            return;
        }
        prev = p;
        p = p->next;
    }

    printf("❌ Student with %s '%s' not found!\n", (mode == 1) ? "USN" : "Name", key);
}

/*
 * Block 7: freeAll()
 */
void freeAll(StudentNode *head) {
    while (head != NULL) {
        StudentNode *temp = head;
        head = head->next;
        free(temp);
    }
}

int main(void) {
    StudentNode *head = NULL;
    int choice, sem;

    do {
        printf("\n========== STUDENT RECORD MANAGEMENT SLL (1BCSL306) ==========\n");
        printf("1. Add Student Record (Append to SLL)\n");
        printf("2. Display All Student Records\n");
        printf("3. Display Students by Semester\n");
        printf("4. Insert Student After a Specific Name\n");
        printf("5. Delete Student (by USN or Name)\n");
        printf("0. Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting.\n");
            break;
        }

        switch (choice) {
            case 1:
                addStudent(&head);
                break;
            case 2:
                displayStudents(head);
                break;
            case 3:
                printf("Enter semester to filter: ");
                scanf("%d", &sem);
                displayBySemester(head, sem);
                break;
            case 4:
                insertAfterName(&head);
                break;
            case 5:
                deleteStudent(&head);
                break;
            case 0:
                printf("Exiting Student Record Management. Freeing SLL memory.\n");
                break;
            default:
                printf("Invalid option! Choose [0 - 5].\n");
        }
    } while (choice != 0);

    freeAll(head);
    return 0;
}

