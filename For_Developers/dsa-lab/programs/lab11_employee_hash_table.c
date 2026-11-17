/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 11: Employee Record Management Using Hash Table & Linear Probing
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Manage employee records in a hash table. Store employee number, name,
 * designation and department. Implement insertion, search and deletion by
 * employee number, and display by department. Resolve collisions using
 * linear probing.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - Hash Function: h(key) = employeeNumber % TABLE_SIZE (e.g. 17).
 * - Linear Probing: When slot h is taken, probe (h+1)%SIZE, (h+2)%SIZE...
 * - Slot States:
 *   * EMPTY    : Slot was never used. Stops linear probe search.
 *   * OCCUPIED : Slot contains active record.
 *   * DELETED  : Slot had a deleted record. Search continues past DELETED slots!
 * ==============================================================================
 */

#include <stdio.h>
#include <string.h>

#define SIZE 17
#define NAME_SIZE 40
#define FIELD_SIZE 30

typedef enum {
    EMPTY,
    OCCUPIED,
    DELETED
} SlotState;

typedef struct {
    int employeeNumber;
    char name[NAME_SIZE];
    char designation[FIELD_SIZE];
    char department[FIELD_SIZE];
    SlotState state;
} Employee;

Employee table[SIZE];

int hashFunction(int empNum) {
    int idx = empNum % SIZE;
    if (idx < 0) idx += SIZE;
    return idx;
}

/*
 * Block 1: searchEmployee()
 * Returns slot index if found, else -1.
 */
int searchEmployee(int empNum) {
    int start = hashFunction(empNum);
    for (int i = 0; i < SIZE; i++) {
        int index = (start + i) % SIZE;
        if (table[index].state == EMPTY) {
            return -1; // End of probe chain
        }
        if (table[index].state == OCCUPIED && table[index].employeeNumber == empNum) {
            return index;
        }
    }
    return -1;
}

/*
 * Block 2: insertEmployee()
 * Inserts with collision resolution using first available slot (EMPTY or DELETED).
 */
void insertEmployee(void) {
    Employee emp;
    printf("\n--- Insert Employee Record ---\n");
    printf("Enter Employee Number: ");
    if (scanf("%d", &emp.employeeNumber) != 1) return;

    if (searchEmployee(emp.employeeNumber) != -1) {
        printf("❌ Error: Employee #%d already exists in the hash table!\n", emp.employeeNumber);
        return;
    }

    printf("Enter Name: ");
    scanf(" %39[^\n]", emp.name);
    printf("Enter Designation: ");
    scanf(" %29[^\n]", emp.designation);
    printf("Enter Department: ");
    scanf(" %29[^\n]", emp.department);

    int start = hashFunction(emp.employeeNumber);
    int firstDeleted = -1;

    for (int i = 0; i < SIZE; i++) {
        int index = (start + i) % SIZE;
        if (table[index].state == DELETED && firstDeleted == -1) {
            firstDeleted = index;
        }
        if (table[index].state == EMPTY) {
            if (firstDeleted != -1) {
                index = firstDeleted; // Reuse tombstone
            }
            emp.state = OCCUPIED;
            table[index] = emp;
            printf("✔ Employee inserted at Hash Slot [%d].\n", index);
            return;
        }
    }

    if (firstDeleted != -1) {
        emp.state = OCCUPIED;
        table[firstDeleted] = emp;
        printf("✔ Employee inserted at recycled Hash Slot [%d].\n", firstDeleted);
    } else {
        printf("🚨 Hash Table is completely full! Insertion failed.\n");
    }
}

/*
 * Block 3: deleteEmployee()
 * Marks slot as DELETED (tombstone) preserving future search probe chains.
 */
void deleteEmployee(void) {
    int empNum;
    printf("Enter Employee Number to delete: ");
    scanf("%d", &empNum);

    int pos = searchEmployee(empNum);
    if (pos == -1) {
        printf("❌ Employee #%d not found.\n", empNum);
        return;
    }

    table[pos].state = DELETED;
    printf("✔ Employee #%d at slot [%d] deleted (marked as DELETED).\n", empNum, pos);
}

/*
 * Block 4: displayByDepartment()
 */
void displayByDepartment(void) {
    char dept[FIELD_SIZE];
    printf("Enter Department Name to filter: ");
    scanf(" %29[^\n]", dept);

    printf("\n--- Employees in Department '%s' ---\n", dept);
    int found = 0;
    for (int i = 0; i < SIZE; i++) {
        if (table[i].state == OCCUPIED && strcmp(table[i].department, dept) == 0) {
            printf("• Slot [%2d] | #%-6d | %-20s | %s\n",
                   i, table[i].employeeNumber, table[i].name, table[i].designation);
            found++;
        }
    }
    if (!found) {
        printf("No employees found in department '%s'.\n", dept);
    }
}

/*
 * Block 5: displayHashTable()
 * Full diagnostic view of all table slots.
 */
void displayHashTable(void) {
    printf("\n============================= HASH TABLE DUMP =============================\n");
    printf("%-6s %-12s %-20s %-15s %-10s\n", "Slot", "Emp Number", "Name", "Department", "Status");
    printf("---------------------------------------------------------------------------\n");
    for (int i = 0; i < SIZE; i++) {
        if (table[i].state == OCCUPIED) {
            printf("[%2d]   %-12d %-20.20s %-15.15s OCCUPIED\n",
                   i, table[i].employeeNumber, table[i].name, table[i].department);
        } else if (table[i].state == DELETED) {
            printf("[%2d]   %-12s %-20s %-15s DELETED\n", i, "-", "-", "-");
        } else {
            printf("[%2d]   %-12s %-20s %-15s EMPTY\n", i, "-", "-", "-");
        }
    }
    printf("===========================================================================\n");
}

int main(void) {
    int choice, empNum;

    do {
        printf("\n========== EMPLOYEE HASH TABLE (1BCSL306) ==========\n");
        printf("1. Insert Employee (Linear Probing)\n");
        printf("2. Search Employee by Number\n");
        printf("3. Delete Employee by Number\n");
        printf("4. Display Employees by Department\n");
        printf("5. Display Full Hash Table Status\n");
        printf("0. Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) break;

        switch (choice) {
            case 1:
                insertEmployee();
                break;
            case 2:
                printf("Enter Employee Number to search: ");
                scanf("%d", &empNum);
                int pos = searchEmployee(empNum);
                if (pos != -1) {
                    printf("\n✔ Found at Slot [%d]:\n", pos);
                    printf("  Name        : %s\n", table[pos].name);
                    printf("  Designation : %s\n", table[pos].designation);
                    printf("  Department  : %s\n", table[pos].department);
                } else {
                    printf("❌ Employee #%d not found.\n", empNum);
                }
                break;
            case 3:
                deleteEmployee();
                break;
            case 4:
                displayByDepartment();
                break;
            case 5:
                displayHashTable();
                break;
            case 0:
                printf("Exiting Employee Hash Table.\n");
                break;
            default:
                printf("Invalid choice! Choose [0 - 5].\n");
        }
    } while (choice != 0);

    return 0;
}

