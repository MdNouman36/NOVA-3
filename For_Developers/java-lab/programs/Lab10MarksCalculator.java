/*
 * ==============================================================================
 * OILS-3: OOPS WITH JAVA (VTU 2025 Scheme - 1BCS302)
 * Experiment 10: Wrapper Classes and Autoboxing / Unboxing
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a Java program to read the marks of three subjects as strings,
 * convert them into wrapper objects, calculate the total and average using
 * autoboxing/unboxing and display the result.
 *
 * 🧠 KEY CONCEPT:
 * - Wrapper Classes (Double, Integer): Wrap primitive values in objects.
 * - Double.valueOf(String): Parses numeric string into Double wrapper object.
 * - Unboxing: Automatic extraction of primitive double from Double object in (+).
 * - Autoboxing: Automatic boxing of primitive double result back into Double.
 * - NumberFormatException: Caught if user enters non-numeric text.
 * ==============================================================================
 */

import java.util.Scanner;

public class Lab10MarksCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("========== EXPERIMENT 10: WRAPPER CLASSES & AUTOBOXING ==========\n");
        System.out.print("Enter marks for Subject 1 (as string): ");
        String strMark1 = scanner.next();
        System.out.print("Enter marks for Subject 2 (as string): ");
        String strMark2 = scanner.next();
        System.out.print("Enter marks for Subject 3 (as string): ");
        String strMark3 = scanner.next();

        try {
            // Converting strings into Wrapper objects (Double)
            Double mark1 = Double.valueOf(strMark1);
            Double mark2 = Double.valueOf(strMark2);
            Double mark3 = Double.valueOf(strMark3);

            // Calculation using Autoboxing and Unboxing:
            // 1. Unboxing occurs automatically when wrapper objects are used in arithmetic (+)
            // 2. Autoboxing occurs when the primitive double is assigned to Double total
            Double total = mark1 + mark2 + mark3;
            Double average = total / 3.0;

            System.out.println("\n----------------- RESULTS -----------------");
            System.out.printf("Subject 1 Mark : %.2f%n", mark1);
            System.out.printf("Subject 2 Mark : %.2f%n", mark2);
            System.out.printf("Subject 3 Mark : %.2f%n", mark3);
            System.out.printf("Total Marks    : %.2f%n", total);
            System.out.printf("Average Marks  : %.2f%n", average);
            System.out.println("-------------------------------------------");
            System.out.println("[OK] Wrapper parsing and autoboxing/unboxing verified!");
        } catch (NumberFormatException e) {
            System.out.println("\n[ERROR] Error: Please enter valid numeric values for marks (e.g., 85.5)!");
        } finally {
            scanner.close();
        }
    }
}

