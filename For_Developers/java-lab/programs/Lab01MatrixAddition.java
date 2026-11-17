/*
 * ==============================================================================
 * OILS-3: OOPS WITH JAVA (VTU 2025 Scheme - 1BCS302)
 * Experiment 01: Matrix Addition of Order N
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a Java program to add TWO matrices of suitable order N.
 *
 * 🧠 KEY CONCEPT:
 * - 2D Arrays in Java: Stored as arrays of arrays.
 * - Scanner: Used to read dimensions and matrix integers from standard input.
 * - Addition rule: C[i][j] = A[i][j] + B[i][j] for all matching indices.
 * ==============================================================================
 */

import java.util.Scanner;

public class Lab01MatrixAddition {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("========== EXPERIMENT 01: MATRIX ADDITION ==========");
        try {
            System.out.print("Enter number of rows: ");
            int rows = sc.nextInt();
            System.out.print("Enter number of columns: ");
            int cols = sc.nextInt();

            if (rows <= 0 || cols <= 0) {
                System.out.println("Error: Rows and columns must be positive integers!");
                return;
            }

            int[][] A = new int[rows][cols];
            int[][] B = new int[rows][cols];
            int[][] C = new int[rows][cols];

            System.out.println("\nEnter elements of First Matrix A (" + rows + "x" + cols + "):");
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    A[i][j] = sc.nextInt();
                }
            }

            System.out.println("\nEnter elements of Second Matrix B (" + rows + "x" + cols + "):");
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    B[i][j] = sc.nextInt();
                }
            }

            // Add corresponding elements
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    C[i][j] = A[i][j] + B[i][j];
                }
            }

            System.out.println("\n--- Resultant Matrix Sum (A + B) ---");
            for (int i = 0; i < rows; i++) {
                for (int j = 0; j < cols; j++) {
                    System.out.printf("%5d ", C[i][j]);
                }
                System.out.println();
            }
        } catch (java.util.InputMismatchException e) {
            System.out.println("Error: Invalid numeric input entered!");
        } finally {
            sc.close();
        }
    }
}

