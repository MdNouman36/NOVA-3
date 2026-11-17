/*
 * ==============================================================================
 * OILS-3: OOPS WITH JAVA (VTU 2025 Scheme - 1BCS302)
 * Experiment 07: User-Defined Exception Handling (Division By Zero)
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a Java program to raise a custom exception (user-defined exception)
 * for Division By Zero using try, catch, throw and finally.
 *
 * 🧠 KEY CONCEPT:
 * - Custom Exception: Created by extending the base java.lang.Exception class.
 * - `throw`: Explicitly triggers an exception object.
 * - `throws`: Declares in method signature that method may cause this exception.
 * - `try-catch-finally`:
 *   * try: Code that may fail.
 *   * catch: Intercepts and recovers from specific exception.
 *   * finally: ALWAYS executes regardless of whether an exception occurred.
 * ==============================================================================
 */

class DivisionByZeroException extends Exception {
    public DivisionByZeroException(String message) {
        super(message);
    }
}

public class Lab07CustomException {
    static double divide(int numerator, int denominator) throws DivisionByZeroException {
        if (denominator == 0) {
            throw new DivisionByZeroException("Custom Exception: Cannot divide " + numerator + " by zero!");
        }
        return (double) numerator / denominator;
    }

    public static void main(String[] args) {
        System.out.println("========== EXPERIMENT 07: CUSTOM EXCEPTION HANDLING ==========\n");

        int[] numerators   = { 20, 10 };
        int[] denominators = { 4,  0  };

        for (int i = 0; i < 2; i++) {
            System.out.println("Test Case " + (i + 1) + ": " + numerators[i] + " / " + denominators[i]);
            try {
                double result = divide(numerators[i], denominators[i]);
                System.out.println("  Result of division: " + result);
            } catch (DivisionByZeroException e) {
                System.out.println("  🚨 Exception Caught: " + e.getMessage());
            } finally {
                System.out.println("  🔒 Finally block executed: Cleanup and logging complete.\n");
            }
        }

        System.out.println("✔ Custom exception handled cleanly without abnormal crash!");
    }
}

