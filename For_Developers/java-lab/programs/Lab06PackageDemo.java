/*
 * ==============================================================================
 * OILS-3: OOPS WITH JAVA (VTU 2025 Scheme - 1BCS302)
 * Experiment 06: User-Defined Packages
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a Java program to create a package named mypack and import &
 * implement it in a suitable class.
 *
 * 🧠 KEY CONCEPT:
 * - Package: Namespace mechanism in Java that groups related classes and
 *   prevents naming collisions.
 * - Directory mapping: Class file must be located inside folder matching
 *   package declaration (mypack/MyPackageClass.java).
 * ==============================================================================
 */

import mypack.MyPackageClass;

public class Lab06PackageDemo {
    public static void main(String[] args) {
        System.out.println("========== EXPERIMENT 06: PACKAGES DEMO ==========\n");

        // Instantiate class imported from custom package 'mypack'
        MyPackageClass myObj = new MyPackageClass();
        myObj.displayMessage();

        int sum = MyPackageClass.addNumbers(15, 27);
        System.out.println("Result of utility static method from mypack: 15 + 27 = " + sum);

        System.out.println("\n✔ Package imported and executed successfully!");
    }
}

