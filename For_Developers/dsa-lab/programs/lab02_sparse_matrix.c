/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 02: Sparse Matrix Triplet Representation, Addition & Transpose
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Read two matrices of equal dimensions. Represent each sparse matrix in
 * three-column triplet form (row, column, value), add the matrices, and
 * compute the transpose.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - A sparse matrix is one where most elements are zero.
 * - Storing every cell in a 2D array wastes memory (e.g. 100x100 = 10,000 ints).
 * - Triplet form: We only store non-zero elements as (row, col, value).
 * - Metadata row at index 0:
 *     a[0].r = total rows in original matrix
 *     a[0].c = total cols in original matrix
 *     a[0].v = total non-zero elements
 * - Addition merges two row-major lists in O(A.v + B.v) time.
 * - Transpose flips (r, c, v) to (c, r, v) and sorts by new row (original col).
 * ==============================================================================
 */

#include <stdio.h>
#define MAX_TERMS 200

typedef struct {
    int r; // Row index
    int c; // Column index
    int v; // Non-zero value
} Term;

/*
 * Block 1: readSparse()
 * Reads original dense matrix elements and compresses them into triplet array.
 */
int readSparse(Term a[]) {
    int rows, cols, val, k = 1;
    printf("Enter number of rows and columns: ");
    if (scanf("%d %d", &rows, &cols) != 2 || rows <= 0 || cols <= 0) {
        printf("Invalid dimensions.\n");
        return -1;
    }

    a[0].r = rows;
    a[0].c = cols;
    a[0].v = 0;

    printf("Enter the matrix elements (%d x %d) row-wise:\n", rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            scanf("%d", &val);
            if (val != 0) {
                if (k >= MAX_TERMS) {
                    printf("Error: Maximum term limit reached!\n");
                    return -1;
                }
                a[k].r = i;
                a[k].c = j;
                a[k].v = val;
                k++;
            }
        }
    }
    a[0].v = k - 1; // Total non-zero terms
    return k;
}

/*
 * Block 2: showSparse()
 * Clearly distinguishes metadata header (row 0) from actual sparse triplets!
 */
void showSparse(const char *name, Term a[]) {
    printf("\n--- Triplet Representation of %s ---\n", name);
    printf("Matrix Dimension: %d Rows x %d Cols | Total Non-Zero Values: %d\n", a[0].r, a[0].c, a[0].v);
    if (a[0].v == 0) {
        printf("(All elements are 0 - Zero Matrix)\n");
        return;
    }
    printf("----------------------------------------\n");
    printf("%-8s %-8s %-8s\n", "Row", "Column", "Value");
    printf("----------------------------------------\n");
    for (int i = 1; i <= a[0].v; i++) {
        printf("%-8d %-8d %-8d\n", a[i].r, a[i].c, a[i].v);
    }
    printf("----------------------------------------\n");
}

/*
 * Block 3: addSparse()
 * Merges two sparse matrices A and B into S in row-major order.
 */
int addSparse(Term a[], Term b[], Term s[]) {
    if (a[0].r != b[0].r || a[0].c != b[0].c) {
        return 0; // Dimension mismatch
    }

    int i = 1, j = 1, k = 1;
    s[0].r = a[0].r;
    s[0].c = a[0].c;

    while (i <= a[0].v && j <= b[0].v) {
        int posA = a[i].r * a[0].c + a[i].c;
        int posB = b[j].r * b[0].c + b[j].c;

        if (posA < posB) {
            s[k++] = a[i++];
        } else if (posB < posA) {
            s[k++] = b[j++];
        } else {
            // Same position (same row and col)
            int sumVal = a[i].v + b[j].v;
            if (sumVal != 0) {
                s[k].r = a[i].r;
                s[k].c = a[i].c;
                s[k].v = sumVal;
                k++;
            }
            i++;
            j++;
        }
    }

    // Append remaining terms of A
    while (i <= a[0].v) {
        s[k++] = a[i++];
    }
    // Append remaining terms of B
    while (j <= b[0].v) {
        s[k++] = b[j++];
    }

    s[0].v = k - 1;
    return 1;
}

/*
 * Block 4: transposeSparse()
 * Computes transpose by scanning columns 0..cols-1 and converting col -> row.
 */
void transposeSparse(Term a[], Term t[]) {
    t[0].r = a[0].c;
    t[0].c = a[0].r;
    t[0].v = a[0].v;

    int k = 1;
    for (int col = 0; col < a[0].c; col++) {
        for (int i = 1; i <= a[0].v; i++) {
            if (a[i].c == col) {
                t[k].r = a[i].c;
                t[k].c = a[i].r;
                t[k].v = a[i].v;
                k++;
            }
        }
    }
}

int main(void) {
    Term a[MAX_TERMS], b[MAX_TERMS], s[MAX_TERMS], t[MAX_TERMS];

    printf("================ SPARSE MATRIX PROCESSING (1BCSL306) ================\n");
    printf("\n[Step 1] Enter Matrix A:\n");
    if (readSparse(a) < 0) return 1;

    printf("\n[Step 2] Enter Matrix B (same dimensions for addition):\n");
    if (readSparse(b) < 0) return 1;

    showSparse("Matrix A", a);
    showSparse("Matrix B", b);

    // Addition
    if (addSparse(a, b, s)) {
        showSparse("Matrix Sum (A + B)", s);
    } else {
        printf("\n❌ Error: Matrices have different dimensions (%dx%d vs %dx%d); cannot add!\n",
               a[0].r, a[0].c, b[0].r, b[0].c);
    }

    // Transpose
    transposeSparse(a, t);
    showSparse("Transpose of Matrix A", t);

    return 0;
}

