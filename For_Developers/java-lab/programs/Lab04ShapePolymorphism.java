/*
 * ==============================================================================
 * OILS-3: OOPS WITH JAVA (VTU 2025 Scheme - 1BCS302)
 * Experiment 04: Runtime Polymorphism and Method Overriding
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a Java program to create a class named Shape. Create three subclasses,
 * namely: Circle, Triangle and Square. Each class has two member functions named
 * draw and erase. Demonstrate the concepts of polymorphism by developing
 * appropriate methods, defining member data, and implementing the main program.
 *
 * 🧠 KEY CONCEPT:
 * - Dynamic Method Dispatch (Runtime Polymorphism): A call to an overridden method
 *   is resolved at runtime based on the actual object being pointed to, not the
 *   reference type.
 * - `Shape s = new Circle(); s.draw();` dynamically calls Circle's draw() method.
 * ==============================================================================
 */

class Shape {
    void draw() {
        System.out.println("Drawing a generic Shape");
    }

    void erase() {
        System.out.println("Erasing a generic Shape");
    }
}

class Circle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing a Circle ⭕");
    }

    @Override
    void erase() {
        System.out.println("Erasing a Circle");
    }
}

class Triangle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing a Triangle 🔺");
    }

    @Override
    void erase() {
        System.out.println("Erasing a Triangle");
    }
}

class Square extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing a Square ⬛");
    }

    @Override
    void erase() {
        System.out.println("Erasing a Square");
    }
}

public class Lab04ShapePolymorphism {
    public static void main(String[] args) {
        System.out.println("========== EXPERIMENT 04: RUNTIME POLYMORPHISM ==========\n");

        // Superclass reference pointing to subclass objects at runtime
        Shape s;

        System.out.println("1. Demonstrating Circle Object via Shape Reference:");
        s = new Circle();
        s.draw();
        s.erase();
        System.out.println();

        System.out.println("2. Demonstrating Triangle Object via Shape Reference:");
        s = new Triangle();
        s.draw();
        s.erase();
        System.out.println();

        System.out.println("3. Demonstrating Square Object via Shape Reference:");
        s = new Square();
        s.draw();
        s.erase();
        System.out.println();

        System.out.println("✔ Dynamic Method Dispatch demonstrated successfully!");
    }
}

