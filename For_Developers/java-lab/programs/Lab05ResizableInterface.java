/*
 * ==============================================================================
 * OILS-3: OOPS WITH JAVA (VTU 2025 Scheme - 1BCS302)
 * Experiment 05: Interface Contract Implementation (Resizable)
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a Java program to create an interface Resizable with methods
 * resizeWidth(int width) and resizeHeight(int height) that allow an object to
 * be resized. Create a class Rectangle that implements the Resizable interface
 * and implements the resize methods.
 *
 * 🧠 KEY CONCEPT:
 * - Interface: Pure contract in Java containing abstract method signatures.
 * - Classes implement interfaces using the `implements` keyword.
 * - Provides abstraction and enables multiple inheritance of type in Java.
 * ==============================================================================
 */

interface Resizable {
    void resizeWidth(int width);
    void resizeHeight(int height);
}

class Rectangle implements Resizable {
    private int width;
    private int height;

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public void resizeWidth(int width) {
        this.width = width;
        System.out.println("Width resized to: " + width);
    }

    @Override
    public void resizeHeight(int height) {
        this.height = height;
        System.out.println("Height resized to: " + height);
    }

    public void display() {
        System.out.println("  Width  : " + width);
        System.out.println("  Height : " + height);
        System.out.println("  Area   : " + (width * height));
    }
}

public class Lab05ResizableInterface {
    public static void main(String[] args) {
        System.out.println("========== EXPERIMENT 05: INTERFACE IMPLEMENTATION ==========\n");

        Rectangle r = new Rectangle(10, 5);

        System.out.println("Initial Rectangle Dimensions:");
        r.display();

        System.out.println("\nResizing Rectangle...");
        r.resizeWidth(20);
        r.resizeHeight(15);

        System.out.println("\nAfter Resizing Dimensions:");
        r.display();

        System.out.println("\n✔ Resizable interface contract fulfilled successfully!");
    }
}

