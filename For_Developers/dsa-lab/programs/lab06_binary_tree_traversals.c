/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 06: Binary Tree Creation and Traversals
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a Program in C to create a Binary Tree by inserting integer elements
 * as keys entered by the user in level order. Implement createTree(),
 * preorder(), inorder() and postorder(). Provide a menu-driven interface to
 * create the tree and display each traversal.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - Binary Tree: Non-linear hierarchical data structure where each node has
 *   at most two children (left and right).
 * - Level-Order Insertion: Inserts nodes top-down, left-to-right using a Queue.
 *   1. Root is placed in Queue.
 *   2. For each new node, inspect front of queue. Attach as left child if empty,
 *      else attach as right child and dequeue parent.
 * - Tree Traversals:
 *   * Preorder  : Root -> Left -> Right
 *   * Inorder   : Left -> Root -> Right
 *   * Postorder : Left -> Right -> Root
 * ==============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#define MAX_QUEUE 200

typedef struct TreeNode {
    int data;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

/*
 * Block 1: createNode()
 * Allocates and initializes a single tree node.
 */
TreeNode* createNode(int value) {
    TreeNode *newNode = (TreeNode *)malloc(sizeof(TreeNode));
    if (newNode == NULL) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    newNode->data = value;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

/*
 * Block 2: createTree()
 * Builds a binary tree in level order using a helper queue.
 */
TreeNode* createTree(void) {
    TreeNode *root = NULL;
    TreeNode *queue[MAX_QUEUE];
    int front = 0, rear = 0;
    int value, choice = 1;

    printf("\n--- Level-Order Binary Tree Creation ---\n");
    printf("Enter root node key: ");
    if (scanf("%d", &value) != 1) return NULL;

    root = createNode(value);
    queue[rear++] = root; // Enqueue root

    while (choice == 1) {
        printf("Add another node? (1-Yes / 0-No): ");
        if (scanf("%d", &choice) != 1 || choice != 1) break;

        printf("Enter key for new node: ");
        scanf("%d", &value);
        TreeNode *newNode = createNode(value);

        TreeNode *parent = queue[front];
        if (parent->left == NULL) {
            parent->left = newNode;
            printf("  Attached %d as LEFT child of %d\n", value, parent->data);
        } else {
            parent->right = newNode;
            printf("  Attached %d as RIGHT child of %d\n", value, parent->data);
            front++; // Parent now has both children full, dequeue it!
        }

        if (rear < MAX_QUEUE) {
            queue[rear++] = newNode; // Enqueue new child for its future children
        }
    }

    printf("✔ Binary Tree created successfully!\n");
    return root;
}

/*
 * Block 3: Preorder Traversal (Root, Left, Right)
 */
void preorder(TreeNode *root) {
    if (root != NULL) {
        printf("%d ", root->data);
        preorder(root->left);
        preorder(root->right);
    }
}

/*
 * Block 4: Inorder Traversal (Left, Root, Right)
 */
void inorder(TreeNode *root) {
    if (root != NULL) {
        inorder(root->left);
        printf("%d ", root->data);
        inorder(root->right);
    }
}

/*
 * Block 5: Postorder Traversal (Left, Right, Root)
 */
void postorder(TreeNode *root) {
    if (root != NULL) {
        postorder(root->left);
        postorder(root->right);
        printf("%d ", root->data);
    }
}

/*
 * Block 6: freeTree()
 * Deallocates entire tree using Postorder traversal logic.
 */
void freeTree(TreeNode *root) {
    if (root != NULL) {
        freeTree(root->left);
        freeTree(root->right);
        free(root);
    }
}

int main(void) {
    TreeNode *root = NULL;
    int choice;

    do {
        printf("\n========== BINARY TREE OPERATIONS (1BCSL306) ==========\n");
        printf("1. Create / Recreate Binary Tree (Level-Order)\n");
        printf("2. Display Preorder Traversal  (Root -> Left -> Right)\n");
        printf("3. Display Inorder Traversal   (Left -> Root -> Right)\n");
        printf("4. Display Postorder Traversal (Left -> Right -> Root)\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting.\n");
            break;
        }

        switch (choice) {
            case 1:
                if (root != NULL) {
                    freeTree(root);
                    root = NULL;
                }
                root = createTree();
                break;
            case 2:
                if (root == NULL) {
                    printf("Tree is empty! Create a tree first.\n");
                } else {
                    printf("\nPreorder Traversal: ");
                    preorder(root);
                    printf("\n");
                }
                break;
            case 3:
                if (root == NULL) {
                    printf("Tree is empty! Create a tree first.\n");
                } else {
                    printf("\nInorder Traversal: ");
                    inorder(root);
                    printf("\n");
                }
                break;
            case 4:
                if (root == NULL) {
                    printf("Tree is empty! Create a tree first.\n");
                } else {
                    printf("\nPostorder Traversal: ");
                    postorder(root);
                    printf("\n");
                }
                break;
            case 5:
                printf("Exiting Binary Tree program. Freeing memory.\n");
                break;
            default:
                printf("Invalid choice! Choose [1 - 5].\n");
        }
    } while (choice != 5);

    if (root != NULL) {
        freeTree(root);
        root = NULL;
    }
    return 0;
}

