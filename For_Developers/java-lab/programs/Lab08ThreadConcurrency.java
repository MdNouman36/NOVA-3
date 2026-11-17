/*
 * ==============================================================================
 * OILS-3: OOPS WITH JAVA (VTU 2025 Scheme - 1BCS302)
 * Experiment 08: Multithreading and Concurrent Execution
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Develop a program to create a class MyThread with a class constructor,
 * call the base class constructor using super, and start the thread. The run
 * method of the class starts after this. It can be observed that both main
 * thread and created child thread are executed concurrently.
 *
 * 🧠 KEY CONCEPT:
 * - Thread Creation: Extends java.lang.Thread.
 * - Constructor: Calls super(name) to name the thread, and start() to register
 *   it with the JVM Thread Scheduler.
 * - Concurrency: Main thread and Child thread interleave their execution
 *   cooperatively using Thread.sleep(500).
 * ==============================================================================
 */

class MyThread extends Thread {
    public MyThread(String name) {
        super(name); // Call base Thread constructor
        start();     // Immediately start child thread upon construction
    }

    @Override
    public void run() {
        for (int i = 1; i <= 5; i++) {
            System.out.println("  [Child Thread] " + Thread.currentThread().getName() + " Count: " + i);
            try {
                Thread.sleep(500); // Sleep for 500ms
            } catch (InterruptedException e) {
                System.out.println("Child thread interrupted: " + e.getMessage());
            }
        }
    }
}

public class Lab08ThreadConcurrency {
    public static void main(String[] args) {
        System.out.println("========== EXPERIMENT 08: THREAD CONCURRENCY ==========\n");

        // Spawn child thread
        MyThread child = new MyThread("Worker-Child-Thread");

        // Main thread loop
        for (int i = 1; i <= 5; i++) {
            System.out.println("[Main Thread] " + Thread.currentThread().getName() + " Count: " + i);
            try {
                Thread.sleep(500); // Sleep for 500ms
            } catch (InterruptedException e) {
                System.out.println("Main thread interrupted: " + e.getMessage());
            }
        }

        try {
            child.join(); // Wait for child thread to finish
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("\n✔ Concurrent thread interleaving demonstrated successfully!");
    }
}

