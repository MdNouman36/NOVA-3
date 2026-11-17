/*
 * ==============================================================================
 * OILS-3: OOPS WITH JAVA (VTU 2025 Scheme - 1BCS302)
 * Experiment 02: Stack Operations Using Class and Encapsulation
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a stack class to hold a maximum of 10 integers with suitable methods.
 * Develop a Java main method to illustrate Stack operations.
 *
 * 🧠 KEY CONCEPT:
 * - Encapsulation: Grouping stack data (arr, top) and methods (push, pop, display)
 *   inside a dedicated class.
 * - LIFO (Last-In, First-Out) operations with overflow and underflow checks.
 * ==============================================================================
 */

import java.util.Scanner;

class Stack {
    private int[] arr = new int[10];
    private int top = -1;

    public void push(int value) {
        if (top == 9) {
            System.out.println("🚨 STACK OVERFLOW: Cannot push " + value + ". Stack is full (Max: 10)!");
        } else {
            arr[++top] = value;
            System.out.println("✔ " + value + " pushed into stack. (Current TOP: " + top + ")");
        }
    }

    public void pop() {
        if (top == -1) {
            System.out.println("🚨 STACK UNDERFLOW: Stack is empty. Nothing to pop!");
        } else {
            System.out.println("✔ " + arr[top] + " popped from stack.");
            top--;
        }
    }

    public void display() {
        if (top == -1) {
            System.out.println("Stack is currently EMPTY.");
        } else {
            System.out.println("\n--- Current Stack Elements (TOP -> BOTTOM) ---");
            for (int i = top; i >= 0; i--) {
                System.out.println("  | " + arr[i] + " |" + (i == top ? " <-- [TOP]" : ""));
            }
            System.out.println("  +------+");
        }
    }

    public void isEmpty() {
        if (top == -1) {
            System.out.println("Stack status: EMPTY (Underflow condition)");
        } else {
            System.out.println("Stack status: NOT EMPTY (" + (top + 1) + " elements active)");
        }
    }

    public void isFull() {
        if (top == 9) {
            System.out.println("Stack status: FULL (Overflow condition)");
        } else {
            System.out.println("Stack status: NOT FULL (" + (9 - top) + " slots remaining)");
        }
    }
}

public class Lab02StackOperations {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Stack s = new Stack();
        int choice, value;

        do {
            System.out.println("\n========== EXPERIMENT 02: JAVA STACK MENU ==========");
            System.out.println("1. Push");
            System.out.println("2. Pop");
            System.out.println("3. Display Stack Elements");
            System.out.println("4. Check isEmpty");
            System.out.println("5. Check isFull");
            System.out.println("6. Exit");
            System.out.print("Enter your choice: ");
            try {
                choice = sc.nextInt();
            } catch (java.util.InputMismatchException e) {
                System.out.println("Invalid input! Please enter a number [1 - 6].");
                sc.nextLine(); // clear buffer
                choice = 0;
                continue;
            }

            switch (choice) {
                case 1:
                    System.out.print("Enter integer value to push: ");
                    try {
                        value = sc.nextInt();
                        s.push(value);
                    } catch (java.util.InputMismatchException e) {
                        System.out.println("Invalid input! Value must be an integer.");
                        sc.nextLine(); // clear buffer
                    }
                    break;
                case 2:
                    s.pop();
                    break;
                case 3:
                    s.display();
                    break;
                case 4:
                    s.isEmpty();
                    break;
                case 5:
                    s.isFull();
                    break;
                case 6:
                    System.out.println("Program terminated.");
                    break;
                default:
                    System.out.println("Invalid choice! Choose [1 - 6].");
            }
        } while (choice != 6);

        sc.close();
    }
}

