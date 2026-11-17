/*
 * ==============================================================================
 * OILS-3: OOPS WITH JAVA (VTU 2025 Scheme - 1BCS302)
 * Experiment 03: Student Class and Array of Objects
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Create a Java class called Student with the USN, Name, Branch, Phone details
 * as variables within it. Write a Java program to create N Student objects and
 * print the USN, Name, Branch, and Phone of these objects with suitable headings.
 *
 * 🧠 KEY CONCEPT:
 * - Constructors and `this` keyword: Initializes instance state.
 * - Array of References: Student[] students = new Student[n]; allocates an array
 *   of references; each slot must then be instantiated with `new Student(...)`.
 * - Formatted tabular output using System.out.printf().
 * ==============================================================================
 */

import java.util.Scanner;

class Student {
    String USN;
    String Name;
    String Branch;
    String Phone;

    // Parameterized Constructor
    Student(String USN, String Name, String Branch, String Phone) {
        this.USN = USN;
        this.Name = Name;
        this.Branch = Branch;
        this.Phone = Phone;
    }

    void display() {
        System.out.printf("%-15s %-20s %-15s %-15s%n", USN, Name, Branch, Phone);
    }
}

public class Lab03StudentDemo {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("========== EXPERIMENT 03: STUDENT OBJECT ARRAY ==========");
        int n = 0;
        try {
            System.out.print("Enter the number of students: ");
            n = sc.nextInt();
            sc.nextLine(); // Consume newline
            if (n <= 0) {
                System.out.println("Error: Number of students must be a positive integer!");
                sc.close();
                return;
            }
        } catch (java.util.InputMismatchException e) {
            System.out.println("Error: Invalid numeric input entered!");
            sc.close();
            return;
        }

        Student[] students = new Student[n];

        for (int i = 0; i < n; i++) {
            System.out.println("\n--- Enter Details of Student " + (i + 1) + " ---");
            System.out.print("USN    : ");
            String usn = sc.nextLine();
            System.out.print("Name   : ");
            String name = sc.nextLine();
            System.out.print("Branch : ");
            String branch = sc.nextLine();
            System.out.print("Phone  : ");
            String phone = sc.nextLine();

            students[i] = new Student(usn, name, branch, phone);
        }

        System.out.println("\n=========================== STUDENT DETAILS ===========================");
        System.out.printf("%-15s %-20s %-15s %-15s%n", "USN", "Name", "Branch", "Phone");
        System.out.println("-----------------------------------------------------------------------");
        for (int i = 0; i < n; i++) {
            students[i].display();
        }
        System.out.println("=======================================================================");

        sc.close();
    }
}

