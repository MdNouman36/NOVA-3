/*
 * ==============================================================================
 * OILS-3: OOPS WITH JAVA (VTU 2025 Scheme - 1BCS302)
 * Experiment 09: Java Enumerations and valueOf() Method
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a Java program using an enumeration called Department containing
 * CSE, ISE, ECE, and MECH. Accept a department name as input and display the
 * selected department using valueOf().
 *
 * 🧠 KEY CONCEPT:
 * - Enum: Type-safe fixed set of named constants.
 * - `Enum.valueOf(String)`: Translates a string token into its matching enum constant.
 * - Exception safety: If user inputs an unknown string, valueOf() throws an
 *   IllegalArgumentException, which is caught gracefully.
 * ==============================================================================
 */

import java.util.Scanner;

enum Department {
    CSE, ISE, ECE, MECH
}

public class Lab09DepartmentEnum {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("========== EXPERIMENT 09: ENUMERATIONS & valueOf() ==========\n");
        System.out.println("Available Departments: CSE, ISE, ECE, MECH");
        System.out.print("Enter department name: ");
        String input = scanner.next().trim().toUpperCase();

        try {
            // Convert user string into enum constant
            Department selectedDept = Department.valueOf(input);
            System.out.println("\n[OK] Successfully selected valid department: " + selectedDept);
            System.out.println("  Ordinal Index: " + selectedDept.ordinal());
        } catch (IllegalArgumentException e) {
            System.out.println("\n[ERROR] Error: '" + input + "' is NOT a recognized college department!");
            System.out.println("   Please choose from [CSE, ISE, ECE, MECH].");
        } finally {
            scanner.close();
        }
    }
}

