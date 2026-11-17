/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 03: Stack Operations Using an Array
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Implement an integer stack using an array. Provide PUSH, POP, PEEK and DISPLAY
 * operations and detect stack overflow and underflow conditions.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - Stack is a LIFO (Last-In, First-Out) data structure.
 * - TOP pointer points to the most recently inserted item.
 * - Empty state: top == -1.
 * - Full state:  top == capacity - 1.
 * - PUSH: Check if full (Overflow); if not, top++ and store item.
 * - POP:  Check if empty (Underflow); if not, retrieve item and top--.
 * - PEEK: Read stack[top] without removing it.
 * ==============================================================================
 */

#include <stdio.h>
#define MAX 100

int stack[MAX];
int top = -1;
int capacity = 10;

int isEmpty(void) {
    return top == -1;
}

int isFull(void) {
    return top == capacity - 1;
}

void initializeStack(void) {
    top = -1;
    printf("✔ Stack initialized successfully.\n");
}

/*
 * Block 1: push()
 * Inserts an element onto the stack with overflow guard.
 */
void push(int element) {
    if (isFull()) {
        printf("🚨 STACK OVERFLOW: Cannot insert %d. Stack is already full (Capacity = %d)!\n",
               element, capacity);
        return;
    }
    top = top + 1;
    stack[top] = element;
    printf("✔ %d pushed onto the stack. (Current TOP index = %d)\n", element, top);
}

/*
 * Block 2: pop()
 * Removes the top element with underflow guard.
 */
void pop(void) {
    if (isEmpty()) {
        printf("🚨 STACK UNDERFLOW: Stack is completely empty. Nothing to pop!\n");
        return;
    }
    int deleted = stack[top];
    top = top - 1;
    printf("✔ %d popped from the stack.\n", deleted);
}

/*
 * Block 3: peek()
 * Views top element without modifying top.
 */
void peek(void) {
    if (isEmpty()) {
        printf("Stack is empty. No top element to peek.\n");
        return;
    }
    printf("🔍 Element at TOP is: %d (at index %d)\n", stack[top], top);
}

/*
 * Block 4: displayStack()
 * Displays all elements from TOP down to index 0.
 */
void displayStack(void) {
    if (isEmpty()) {
        printf("Stack is empty: [ ]\n");
        return;
    }
    printf("\n--- CURRENT STACK CONTENT (TOP -> BOTTOM) ---\n");
    for (int i = top; i >= 0; i--) {
        if (i == top) {
            printf("  | %4d | <-- [TOP]\n", stack[i]);
        } else {
            printf("  | %4d |\n", stack[i]);
        }
    }
    printf("  +------+\n");
}

/*
 * Block 5: displayStatus()
 * Reports stack diagnostics (used positions, remaining slots, condition).
 */
void displayStatus(void) {
    printf("\n--- STACK DIAGNOSTIC STATUS ---\n");
    printf("Current TOP index   : %d\n", top);
    printf("Stack Capacity      : %d\n", capacity);
    printf("Active Elements     : %d\n", top + 1);
    printf("Available Slots     : %d\n", capacity - (top + 1));
    if (isEmpty()) {
        printf("Condition           : EMPTY (Underflow state)\n");
    } else if (isFull()) {
        printf("Condition           : FULL (Overflow state)\n");
    } else {
        printf("Condition           : NORMAL (Available for PUSH/POP)\n");
    }
}

int main(void) {
    int choice, element;

    printf("================ STACK OPERATIONS (1BCSL306) ================\n");
    printf("Enter maximum size of stack (1 to %d) [VTU Syllabus suggests > 15]: ", MAX);
    if (scanf("%d", &capacity) != 1 || capacity <= 0 || capacity > MAX) {
        printf("Invalid input. Defaulting capacity to 16.\n");
        capacity = 16;
    }

    initializeStack();

    do {
        printf("\n========== STACK MENU (Capacity: %d) ==========\n", capacity);
        printf("1. PUSH an element\n");
        printf("2. POP an element\n");
        printf("3. PEEK (View TOP element)\n");
        printf("4. Display Stack Status & Diagnostics\n");
        printf("5. Display All Stack Elements\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting.\n");
            break;
        }

        switch (choice) {
            case 1:
                printf("Enter integer element to PUSH: ");
                scanf("%d", &element);
                push(element);
                break;
            case 2:
                pop();
                break;
            case 3:
                peek();
                break;
            case 4:
                displayStatus();
                break;
            case 5:
                displayStack();
                break;
            case 6:
                printf("Exiting Stack Operations program.\n");
                break;
            default:
                printf("Invalid choice! Please choose [1 - 6].\n");
        }
    } while (choice != 6);

    return 0;
}

