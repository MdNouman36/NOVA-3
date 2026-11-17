/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 05: Polynomial Addition Using Header-Node Circular Linked List
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Represent polynomials using header-node singly circular linked lists.
 * Each term stores a coefficient and an exponent. Read two polynomials,
 * display them, and add them into POLYSUM.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - A dummy header node represents the list: head->next == head when empty.
 * - Circular structure avoids NULL checks at the end of the list.
 * - Terms are sorted in descending order of exponents.
 * - Addition compares powers of terms from both lists:
 *   * If exp(A) == exp(B): Add coefficients. If sum != 0, append to result.
 *   * If exp(A) > exp(B) : Append term A to result and advance list A.
 *   * If exp(B) > exp(A) : Append term B to result and advance list B.
 * ==============================================================================
 */

#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int c; // Coefficient
    int e; // Exponent (power)
    struct Node *next;
} Node;

/*
 * Block 1: createHeader()
 * Creates a circular header node pointing to itself.
 */
Node* createHeader(void) {
    Node *h = (Node *)malloc(sizeof(Node));
    if (h == NULL) {
        printf("Error: Heap memory allocation failed!\n");
        exit(1);
    }
    h->c = 0;
    h->e = -1; // Sentinel value
    h->next = h; // Circular loop
    return h;
}

/*
 * Block 2: insertSorted()
 * Inserts a term in descending order of exponent, merging duplicate powers.
 */
void insertSorted(Node *h, int c, int e) {
    if (c == 0) return; // Skip zero terms

    Node *prev = h;
    Node *curr = h->next;

    // Traverse until we find where to insert (maintaining descending order)
    while (curr != h && curr->e > e) {
        prev = curr;
        curr = curr->next;
    }

    if (curr != h && curr->e == e) {
        // Exponent already exists: combine coefficients!
        curr->c += c;
        if (curr->c == 0) {
            // Term cancelled out to 0: delete node
            prev->next = curr->next;
            free(curr);
        }
        return;
    }

    // Allocate new node
    Node *newNode = (Node *)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Memory allocation error.\n");
        exit(1);
    }
    newNode->c = c;
    newNode->e = e;
    newNode->next = curr;
    prev->next = newNode;
}

/*
 * Block 3: readPolynomial()
 * Reads non-zero terms from user.
 */
void readPolynomial(Node *h, const char *polyName) {
    int n, c, e;
    printf("\n--- Reading %s ---\n", polyName);
    printf("Enter number of non-zero terms: ");
    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("No terms entered.\n");
        return;
    }

    for (int i = 0; i < n; i++) {
        printf("  Term %d (Enter coefficient and exponent, e.g., '3 2' for 3x^2): ", i + 1);
        scanf("%d %d", &c, &e);
        insertSorted(h, c, e);
    }
}

/*
 * Block 4: displayPolynomial()
 * Formats polynomial nicely into algebra notation.
 */
void displayPolynomial(Node *h) {
    Node *p = h->next;
    if (p == h) {
        printf("0");
        return;
    }

    int first = 1;
    while (p != h) {
        if (!first && p->c > 0) {
            printf(" + ");
        } else if (!first && p->c < 0) {
            printf(" - ");
        } else if (first && p->c < 0) {
            printf("-");
        }

        int absCoef = (p->c < 0) ? -p->c : p->c;

        if (p->e == 0) {
            printf("%d", absCoef);
        } else if (p->e == 1) {
            if (absCoef == 1) printf("x");
            else printf("%dx", absCoef);
        } else {
            if (absCoef == 1) printf("x^%d", p->e);
            else printf("%dx^%d", absCoef, p->e);
        }

        first = 0;
        p = p->next;
    }
}

/*
 * Block 5: addPolynomials()
 * Adds two polynomials into a newly allocated POLYSUM header list.
 */
Node* addPolynomials(Node *a, Node *b) {
    Node *sum = createHeader();
    Node *p = a->next;
    Node *q = b->next;

    while (p != a && q != b) {
        if (p->e == q->e) {
            int combined = p->c + q->c;
            if (combined != 0) {
                insertSorted(sum, combined, p->e);
            }
            p = p->next;
            q = q->next;
        } else if (p->e > q->e) {
            insertSorted(sum, p->c, p->e);
            p = p->next;
        } else {
            insertSorted(sum, q->c, q->e);
            q = q->next;
        }
    }

    while (p != a) {
        insertSorted(sum, p->c, p->e);
        p = p->next;
    }
    while (q != b) {
        insertSorted(sum, q->c, q->e);
        q = q->next;
    }

    return sum;
}

/*
 * Block 6: freePolynomial()
 * Frees all allocated heap nodes in the circular list.
 */
void freePolynomial(Node *h) {
    if (h == NULL) return;
    Node *curr = h->next;
    while (curr != h) {
        Node *temp = curr;
        curr = curr->next;
        free(temp);
    }
    free(h);
}

int main(void) {
    printf("================ POLYNOMIAL ADDITION (1BCSL306) ================\n");
    printf("Representation: Singly Circular Linked List with Header Node.\n");

    Node *poly1 = createHeader();
    Node *poly2 = createHeader();

    readPolynomial(poly1, "Polynomial P(x)");
    readPolynomial(poly2, "Polynomial Q(x)");

    printf("\n---------------------------------------------------------------\n");
    printf("P(x)       = ");
    displayPolynomial(poly1);
    printf("\nQ(x)       = ");
    displayPolynomial(poly2);
    printf("\n---------------------------------------------------------------\n");

    Node *polySum = addPolynomials(poly1, poly2);
    printf("POLYSUM(x) = ");
    displayPolynomial(polySum);
    printf("\n===============================================================\n");

    freePolynomial(poly1);
    freePolynomial(poly2);
    freePolynomial(polySum);

    return 0;
}

