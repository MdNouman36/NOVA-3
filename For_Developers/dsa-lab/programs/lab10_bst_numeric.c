/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 10: Hierarchical Numeric Data Management Using Binary Search Tree
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Store hierarchical numeric keys using a Binary Search Tree (BST).
 * Implement insertion, searching and tree traversals to display the stored keys.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - BST Property:
 *   For every node X:
 *     All values in left subtree  < X->data
 *     All values in right subtree > X->data
 * - Inorder Traversal of a BST produces elements in strictly ASCENDING sorted order!
 * - Searching takes O(h) time where h is the height of the tree.
 * ==============================================================================
 */

#include <stdio.h>
#include <stdlib.h>

typedef struct BSTNode {
    int key;
    struct BSTNode *left;
    struct BSTNode *right;
} BSTNode;

/*
 * Block 1: insertBST()
 * Recursively inserts a key while enforcing the BST ordering property.
 */
BSTNode* insertBST(BSTNode *root, int val) {
    if (root == NULL) {
        BSTNode *newNode = (BSTNode *)malloc(sizeof(BSTNode));
        if (newNode == NULL) {
            printf("Memory allocation failed!\n");
            exit(1);
        }
        newNode->key = val;
        newNode->left = NULL;
        newNode->right = NULL;
        return newNode;
    }

    if (val < root->key) {
        root->left = insertBST(root->left, val);
    } else if (val > root->key) {
        root->right = insertBST(root->right, val);
    } else {
        printf("Notice: Duplicate key %d ignored (BST stores unique keys).\n", val);
    }
    return root;
}

/*
 * Block 2: searchBST()
 * Iteratively searches for a target key in the BST.
 */
BSTNode* searchBST(BSTNode *root, int target) {
    BSTNode *curr = root;
    while (curr != NULL && curr->key != target) {
        if (target < curr->key) {
            curr = curr->left;
        } else {
            curr = curr->right;
        }
    }
    return curr;
}

/*
 * Block 3: inorder()
 * Inorder traversal (Left, Root, Right) -> Yields ascending sorted output!
 */
void inorder(BSTNode *root) {
    if (root != NULL) {
        inorder(root->left);
        printf("%d ", root->key);
        inorder(root->right);
    }
}

/*
 * Block 4: preorder()
 * Preorder traversal (Root, Left, Right).
 */
void preorder(BSTNode *root) {
    if (root != NULL) {
        printf("%d ", root->key);
        preorder(root->left);
        preorder(root->right);
    }
}

/*
 * Block 5: postorder()
 * Postorder traversal (Left, Right, Root).
 */
void postorder(BSTNode *root) {
    if (root != NULL) {
        postorder(root->left);
        postorder(root->right);
        printf("%d ", root->key);
    }
}

/*
 * Block 6: freeBST()
 */
void freeBST(BSTNode *root) {
    if (root != NULL) {
        freeBST(root->left);
        freeBST(root->right);
        free(root);
    }
}

int main(void) {
    BSTNode *root = NULL;
    int choice, val;

    do {
        printf("\n========== BINARY SEARCH TREE (1BCSL306) ==========\n");
        printf("1. Insert Numeric Key\n");
        printf("2. Search for a Key\n");
        printf("3. Display Inorder Traversal   (Sorted Ascending)\n");
        printf("4. Display Preorder Traversal  (Root -> Left -> Right)\n");
        printf("5. Display Postorder Traversal (Left -> Right -> Root)\n");
        printf("0. Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting.\n");
            break;
        }

        switch (choice) {
            case 1:
                printf("Enter integer key to insert: ");
                scanf("%d", &val);
                root = insertBST(root, val);
                printf("✔ Key %d inserted.\n", val);
                break;
            case 2:
                printf("Enter key to search: ");
                scanf("%d", &val);
                if (searchBST(root, val) != NULL) {
                    printf("✔ Key %d is FOUND in the BST!\n", val);
                } else {
                    printf("❌ Key %d NOT found in the BST.\n", val);
                }
                break;
            case 3:
                if (root == NULL) {
                    printf("BST is empty.\n");
                } else {
                    printf("\nInorder (Sorted) Traversal: ");
                    inorder(root);
                    printf("\n");
                }
                break;
            case 4:
                if (root == NULL) {
                    printf("BST is empty.\n");
                } else {
                    printf("\nPreorder Traversal: ");
                    preorder(root);
                    printf("\n");
                }
                break;
            case 5:
                if (root == NULL) {
                    printf("BST is empty.\n");
                } else {
                    printf("\nPostorder Traversal: ");
                    postorder(root);
                    printf("\n");
                }
                break;
            case 0:
                printf("Exiting BST program. Freeing memory.\n");
                break;
            default:
                printf("Invalid choice! Choose [0 - 5].\n");
        }
    } while (choice != 0);

    freeBST(root);
    return 0;
}

