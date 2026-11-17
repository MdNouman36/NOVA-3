/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 09: Manufacturing Parts Inventory Management Using Hash Table
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * A manufacturing unit needs to manage machine parts. Each part has an
 * alphanumeric Part Number, Part Name, Model Number and Description.
 * Develop a C program to add a new part, remove an obsolete part by part number
 * or model number, and search/display part details by part number or model number.
 * Use a hash table with linear probing keyed by Part Number.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - Hash Function: Polynomial rolling hash on the alphanumeric Part Number string
 *   modulo TABLE_SIZE.
 * - Linear Probing: When a collision occurs at index h, try (h + 1) % TABLE_SIZE,
 *   (h + 2) % TABLE_SIZE, etc.
 * - Slot Status (EMPTY, OCCUPIED, DELETED):
 *   When a part is removed, mark as DELETED rather than EMPTY so the linear
 *   probe chain is not broken for later inserted keys!
 * ==============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 101
#define FIELD_SIZE 80

typedef enum {
    EMPTY,
    OCCUPIED,
    DELETED
} SlotStatus;

typedef struct {
    char partNumber[30];
    char partName[FIELD_SIZE];
    char modelNumber[30];
    char description[FIELD_SIZE];
    SlotStatus status;
} Part;

Part inventory[TABLE_SIZE];

/*
 * Block 1: hashString()
 * Computes hash index for alphanumeric key.
 */
unsigned int hashString(const char key[]) {
    unsigned int hash = 0;
    for (int i = 0; key[i] != '\0'; i++) {
        hash = (hash * 31 + (unsigned char)key[i]) % TABLE_SIZE;
    }
    return hash;
}

/*
 * Block 2: findByPartNumber()
 * O(1) average lookup using hash function and linear probing.
 */
int findByPartNumber(const char partNumber[]) {
    unsigned int start = hashString(partNumber);
    for (int i = 0; i < TABLE_SIZE; i++) {
        unsigned int index = (start + i) % TABLE_SIZE;
        if (inventory[index].status == EMPTY) {
            return -1; // Unoccupied slot means key was never inserted
        }
        if (inventory[index].status == OCCUPIED &&
            strcmp(inventory[index].partNumber, partNumber) == 0) {
            return (int)index;
        }
    }
    return -1;
}

/*
 * Block 3: findByModelNumber()
 * Scans occupied slots since table is indexed by Part Number.
 */
int findByModelNumber(const char modelNumber[]) {
    for (int i = 0; i < TABLE_SIZE; i++) {
        if (inventory[i].status == OCCUPIED &&
            strcmp(inventory[i].modelNumber, modelNumber) == 0) {
            return i;
        }
    }
    return -1;
}

/*
 * Block 4: addPart()
 * Inserts a new part using linear probing into first available (EMPTY or DELETED) slot.
 */
void addPart(void) {
    Part newPart;
    int availableIndex = -1;

    printf("\n--- Add New Machine Part ---\n");
    printf("Enter Part Number (alphanumeric, e.g. P1001): ");
    scanf(" %29s", newPart.partNumber);

    if (findByPartNumber(newPart.partNumber) != -1) {
        printf("❌ Error: Part Number '%s' already exists in inventory!\n", newPart.partNumber);
        return;
    }

    printf("Enter Part Name: ");
    scanf(" %79[^\n]", newPart.partName);
    printf("Enter Model Number: ");
    scanf(" %29s", newPart.modelNumber);
    printf("Enter Description: ");
    scanf(" %79[^\n]", newPart.description);

    unsigned int start = hashString(newPart.partNumber);
    for (int i = 0; i < TABLE_SIZE; i++) {
        unsigned int index = (start + i) % TABLE_SIZE;
        if (inventory[index].status == EMPTY || inventory[index].status == DELETED) {
            availableIndex = (int)index;
            break;
        }
    }

    if (availableIndex == -1) {
        printf("🚨 Error: Inventory Hash Table is completely FULL!\n");
        return;
    }

    newPart.status = OCCUPIED;
    inventory[availableIndex] = newPart;
    printf("✔ Part '%s' added successfully at Hash Table Index [%d].\n",
           newPart.partNumber, availableIndex);
}

/*
 * Block 5: displayPart()
 */
void displayPart(int index) {
    printf("---------------------------------------------------\n");
    printf("Slot Index   : [%d]\n", index);
    printf("Part Number  : %s\n", inventory[index].partNumber);
    printf("Part Name    : %s\n", inventory[index].partName);
    printf("Model Number : %s\n", inventory[index].modelNumber);
    printf("Description  : %s\n", inventory[index].description);
}

/*
 * Block 6: searchPart()
 */
void searchPart(void) {
    int choice, index = -1;
    char key[30];
    printf("\nSearch By: 1. Part Number  2. Model Number\nChoice: ");
    if (scanf("%d", &choice) != 1) return;

    if (choice == 1) {
        printf("Enter Part Number: ");
        scanf(" %29s", key);
        index = findByPartNumber(key);
    } else if (choice == 2) {
        printf("Enter Model Number: ");
        scanf(" %29s", key);
        index = findByModelNumber(key);
    } else {
        printf("Invalid search option.\n");
        return;
    }

    if (index == -1) {
        printf("❌ Part '%s' not found in inventory.\n", key);
    } else {
        printf("\n✔ Matching Part Found:");
        displayPart(index);
    }
}

/*
 * Block 7: removePart()
 * Deletes part by marking slot DELETED (tombstone).
 */
void removePart(void) {
    int choice, index = -1;
    char key[30];
    printf("\nRemove By: 1. Part Number  2. Model Number\nChoice: ");
    if (scanf("%d", &choice) != 1) return;

    if (choice == 1) {
        printf("Enter Part Number: ");
        scanf(" %29s", key);
        index = findByPartNumber(key);
    } else if (choice == 2) {
        printf("Enter Model Number: ");
        scanf(" %29s", key);
        index = findByModelNumber(key);
    } else {
        printf("Invalid option.\n");
        return;
    }

    if (index == -1) {
        printf("❌ Part '%s' not found.\n", key);
        return;
    }

    inventory[index].status = DELETED; // Mark tombstone
    printf("✔ Part '%s' removed from slot [%d] (Marked as DELETED).\n", key, index);
}

/*
 * Block 8: displayInventory()
 */
void displayInventory(void) {
    int count = 0;
    printf("\n======================== CURRENT INVENTORY ========================\n");
    for (int i = 0; i < TABLE_SIZE; i++) {
        if (inventory[i].status == OCCUPIED) {
            displayPart(i);
            count++;
        }
    }
    printf("===================================================================\n");
    printf("Total active parts in inventory: %d\n", count);
}

int main(void) {
    int choice;
    // Global array inventory has default status EMPTY (0)

    do {
        printf("\n========== MACHINE PARTS INVENTORY HASH TABLE (1BCSL306) ==========\n");
        printf("1. Add a New Part\n");
        printf("2. Remove an Obsolete Part\n");
        printf("3. Search & Display Part Details\n");
        printf("4. Display Complete Inventory\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting.\n");
            break;
        }

        switch (choice) {
            case 1:
                addPart();
                break;
            case 2:
                removePart();
                break;
            case 3:
                searchPart();
                break;
            case 4:
                displayInventory();
                break;
            case 5:
                printf("Exiting Parts Inventory System.\n");
                break;
            default:
                printf("Invalid choice! Choose [1 - 5].\n");
        }
    } while (choice != 5);

    return 0;
}

