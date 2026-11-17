"""
arcade.java.experiments_data — 10 VTU Java OOP Lab Experiments (1BCS302, 2025 Scheme).
Features:
  - Tier 1: The Big Picture Story (What the program actually does from start to finish in plain English)
  - Tier 2: End-to-End Functional Code Blocks (First line to last line coverage)
  - Fast & Fun 3-Bullet Breakdown:
      1) 🎯 What we are doing
      2) 🔍 How it works (concise bullets on variables & mechanics)
      3) 💡 Real-world intuition / Watch out (relatable analogy or exam trap)
"""

JAVA_EXPERIMENTS = [
    # ── Experiment 01 ─────────────────────────────────────────────────────────
    {
        "num": 1,
        "title": "Matrix Addition of Order N",
        "file": "java-lab/programs/Lab01MatrixAddition.java",
        "story": "Imagine two digital photo filters adding their pixel intensities together! In Java, matrices are not flat grids in RAM: they are 'arrays of arrays' floating on the JVM Heap. In this lab, we read the grid size N using a Scanner, dynamically create three 2D array objects on the Heap, add corresponding cells (C[i][j] = A[i][j] + B[i][j]), and print the clean result grid.",
        "problem": "Develop a Java program to add TWO matrices of suitable order N using 2D arrays and Scanner input.",
        "concept": "In Java, multi-dimensional arrays are objects containing references to 1D arrays on the Heap. Matrix addition computes element-wise sums: C[i][j] = A[i][j] + B[i][j].",
        "blocks": [
            {
                "title": "Part 1: Scanner Setup & Dynamic 2D Array Heap Allocation",
                "code": "import java.util.Scanner;\n\npublic class Lab01MatrixAddition {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        System.out.print(\"Enter matrix order N: \");\n        int n = sc.nextInt();\n\n        // Dynamic heap allocation for 2D array objects\n        int[][] a = new int[n][n];\n        int[][] b = new int[n][n];\n        int[][] c = new int[n][n];\n    }\n}",
                "doing": "Sets up the console scanner and asks the JVM Heap for three 2D grid objects of dimension N x N.",
                "how": [
                    "`Scanner sc = new Scanner(System.in)`: Wraps keyboard input stream for easy token reading.",
                    "`int[][] a = new int[n][n]`: In Java, this allocates 1 parent array containing N references, each pointing to a separate row array on the Heap.",
                    "Java automatically zero-initializes all numeric array slots to 0."
                ],
                "watchout": "In C, arrays are contiguous blocks of memory; in Java, 2D arrays are objects pointing to other objects on the Heap!"
            },
            {
                "title": "Part 2: Reading Matrix Cells with Nested Loops",
                "code": "System.out.println(\"Enter elements for Matrix A:\");\nfor (int i = 0; i < n; i++) {\n    for (int j = 0; j < n; j++) {\n        a[i][j] = sc.nextInt();\n    }\n}\nSystem.out.println(\"Enter elements for Matrix B:\");\nfor (int i = 0; i < n; i++) {\n    for (int j = 0; j < n; j++) {\n        b[i][j] = sc.nextInt();\n    }\n}",
                "doing": "Uses double loops (rows `i` and columns `j`) to read numbers from the user and populate Matrix A and B.",
                "how": [
                    "Outer loop `i` steps through row 0 to row N - 1.",
                    "Inner loop `j` steps through columns in that row.",
                    "`sc.nextInt()` grabs the next space-separated integer."
                ],
                "watchout": "Always verify matrix dimensions match! You cannot add an MxN matrix to a PxQ matrix unless M=P and N=Q."
            },
            {
                "title": "Part 3: Element-Wise Summation & Formatted Printing",
                "code": "// Compute C = A + B\nfor (int i = 0; i < n; i++) {\n    for (int j = 0; j < n; j++) {\n        c[i][j] = a[i][j] + b[i][j];\n    }\n}\n\n// Display result matrix\nSystem.out.println(\"Resultant Matrix C (A + B):\");\nfor (int i = 0; i < n; i++) {\n    for (int j = 0; j < n; j++) {\n        System.out.print(c[i][j] + \"\\t\");\n    }\n    System.out.println(); // New line after each row\n}\nsc.close();",
                "doing": "Adds corresponding cells together, prints the result in a clean tabular grid, and closes the scanner.",
                "how": [
                    "`c[i][j] = a[i][j] + b[i][j]`: Evaluates corresponding cells and stores sum in C.",
                    "`\"\\t\"` prints a tab space between numbers so columns line up neatly.",
                    "`sc.close()` releases the system input resource."
                ],
                "watchout": "Time complexity is O(N^2) because we visit every cell twice (once for input, once for addition)."
            }
        ],
        "challenge": {
            "prompt": "What does Java allocate in memory when you execute 'int[][] matrix = new int[3][4]'?",
            "opts": [
                "A) A single flat block of 12 bytes.",
                "B) A top-level array of 3 reference pointers on the Heap, each pointing to a separate 4-element integer array.",
                "C) A pointer on the stack pointing directly to video RAM.",
                "D) Nothing, arrays are only allocated when elements are inserted."
            ],
            "correct_opt": "B",
            "hint": "In Java, multi-dimensional arrays are 'arrays of arrays' sitting as distinct objects on the Heap.",
            "praise": "Spot on! Java arrays are objects, and 2D arrays are arrays of row references.",
            "roast": "In Java, 2D arrays are objects containing references to row array objects on the Heap!"
        }
    },

    # ── Experiment 02 ─────────────────────────────────────────────────────────
    {
        "num": 2,
        "title": "Stack Class and Object Encapsulation",
        "file": "java-lab/programs/Lab02StackOperations.java",
        "story": "How do you protect your data so other programmers can't mess it up? Encapsulation! By making the stack array and top pointer 'private', no outside code can tamper with them directly. Instead, outside code must use our clean public methods: push(), pop(), and display(). We can create multiple Stack objects (s1, s2) that operate completely independently on the Heap!",
        "problem": "Develop a Stack class in Java to implement Stack operations (push, pop, display). Create at least two separate stack objects to prove independent encapsulation.",
        "concept": "Object-Oriented Encapsulation. The internal representation of the Stack (array and top pointer) is hidden (private), exposed only through well-defined public methods (push, pop, display).",
        "blocks": [
            {
                "title": "Part 1: The Encapsulated Stack Class & Constructor",
                "code": "class Stack {\n    private int[] s;        // Hidden storage array\n    private int top;        // Hidden top pointer\n    private int capacity;   // Hidden maximum size\n\n    public Stack(int cap) {\n        this.capacity = cap;\n        this.s = new int[capacity]; // Heap array for THIS stack\n        this.top = -1;              // Starts empty\n    }\n}",
                "doing": "Hides the internal array and pointer behind the `private` wall, and provides a constructor to set up each new stack instance.",
                "how": [
                    "`private`: Information Hiding! External classes cannot write `s.top = 999` and corrupt our boundary.",
                    "`this.capacity = cap`: Resolves shadow variable collision between constructor argument and instance field.",
                    "`s = new int[capacity]`: Allocates a unique array for each stack object on the Heap."
                ],
                "watchout": "If you don't use 'private', anyone can bypass push() and corrupt your stack pointer directly!"
            },
            {
                "title": "Part 2: The Public API — push() and pop()",
                "code": "public void push(int item) {\n    if (top == capacity - 1) {\n        System.out.println(\"Stack Overflow!\");\n        return;\n    }\n    s[++top] = item; // Pre-increment advances top before writing\n}\n\npublic int pop() {\n    if (top == -1) {\n        System.out.println(\"Stack Underflow!\");\n        return -1;\n    }\n    return s[top--]; // Returns top item then decrements pointer\n}",
                "doing": "Provides the controlled gateway for adding and removing items with built-in overflow and underflow protection.",
                "how": [
                    "`s[++top] = item`: Pre-increment (`++top`) moves top up first, then deposits the item.",
                    "`s[top--]`: Post-decrement (`top--`) captures the item, then drops top down by 1.",
                    "Checks boundaries before modifying memory."
                ],
                "watchout": "Notice `++top` vs `top++`: push uses pre-increment (`++top`), while pop uses post-decrement (`top--`)."
            },
            {
                "title": "Part 3: Independent Instances in main()",
                "code": "public class Lab02StackOperations {\n    public static void main(String[] args) {\n        Stack s1 = new Stack(5); // First independent stack object\n        Stack s2 = new Stack(5); // Second independent stack object\n\n        s1.push(10);\n        s1.push(20);\n        s2.push(99);\n\n        System.out.println(\"s1 pop: \" + s1.pop()); // Pops 20\n        System.out.println(\"s2 pop: \" + s2.pop()); // Pops 99 (s2 is completely unaffected!)\n    }\n}",
                "doing": "Creates two distinct stack objects on the JVM Heap to prove that mutating one does not affect the other.",
                "how": [
                    "`s1` and `s2` are separate object instances located at different heap RAM addresses.",
                    "Pushing into `s1` modifies only `s1.s` and `s1.top`. `s2` remains completely untouched!"
                ],
                "watchout": "This is the core definition of an Object: state + behavior bundled together independently."
            }
        ],
        "challenge": {
            "prompt": "Why are the fields 's' and 'top' marked 'private' inside the Stack class?",
            "opts": [
                "A) To save battery power on mobile devices.",
                "B) So external code cannot accidentally or maliciously modify 'top' or access array elements directly without going through boundary checks (Encapsulation).",
                "C) Because Java requires all variables to be private.",
                "D) To make the program run 10x faster."
            ],
            "correct_opt": "B",
            "hint": "Private enforces data hiding: only public methods (push/pop) can touch the internal state.",
            "praise": "Exactly right! Encapsulation ensures internal state can only be modified through validated public methods.",
            "roast": "Private enforces Encapsulation: it protects internal data structures from external corruption!"
        }
    },

    # ── Experiment 03 ─────────────────────────────────────────────────────────
    {
        "num": 3,
        "title": "Student Class and Array of Objects",
        "file": "java-lab/programs/Lab03StudentDemo.java",
        "story": "Need to manage student records? In Java, an 'Array of Objects' is actually an Array of References (pointers). When you write `new Student[5]`, you do NOT have 5 students yet — you just have 5 empty slots holding `null`! You must call `new Student()` for each slot to bring the actual students to life on the Heap.",
        "problem": "Create a Java class Student (USN, Name, Branch, Phone). Write a program to read N student records and print them in a tabular format.",
        "concept": "In Java, an 'Array of Objects' is actually an Array of References. Declaring 'Student[] s = new Student[N]' allocates N null pointers; each object must be instantiated individually.",
        "blocks": [
            {
                "title": "Part 1: The Student Class Blueprint",
                "code": "class Student {\n    String usn;\n    String name;\n    String branch;\n    String phone;\n\n    // Parameterized constructor\n    public Student(String u, String n, String b, String p) {\n        this.usn = u;\n        this.name = n;\n        this.branch = b;\n        this.phone = p;\n    }\n\n    public void display() {\n        System.out.printf(\"%-15s %-20s %-10s %-12s\\n\", usn, name, branch, phone);\n    }\n}",
                "doing": "Defines the student record template and constructor, plus a formatted printer.",
                "how": [
                    "`this.usn = u`: Assigns incoming arguments to the instance fields.",
                    "`printf`: Uses format specifiers like `%-20s` (left-align 20 spaces) to print clean, straight columns."
                ],
                "watchout": "Phone numbers and USNs should be Strings, not ints, because they can have letters or leading zeroes!"
            },
            {
                "title": "Part 2: The Two-Phase Object Array Allocation",
                "code": "public class Lab03StudentDemo {\n    public static void main(String[] args) {\n        int n = 3;\n        // PHASE 1: Allocate array of N reference pointers (all currently null!)\n        Student[] students = new Student[n];\n\n        // PHASE 2: Instantiate actual Student objects one-by-one\n        for (int i = 0; i < n; i++) {\n            students[i] = new Student(\"1BI25CS00\" + (i+1), \"Student \" + (i+1), \"CSE\", \"9876543210\");\n        }\n    }\n}",
                "doing": "Demonstrates the two critical steps needed to allocate and populate an array of objects in Java.",
                "how": [
                    "Phase 1 (`new Student[n]`): Creates an array container holding N null references.",
                    "Phase 2 (`students[i] = new Student(...)`): Instantiates actual objects on the Heap and points each slot to them."
                ],
                "watchout": "Biggest beginner trap in Java: Forgetting Phase 2! Trying to use students[0] without `new Student()` triggers instant NullPointerException."
            },
            {
                "title": "Part 3: Printing the Tabular Roster",
                "code": "System.out.println(\"------------------------------------------------------------\");\nSystem.out.printf(\"%-15s %-20s %-10s %-12s\\n\", \"USN\", \"NAME\", \"BRANCH\", \"PHONE\");\nSystem.out.println(\"------------------------------------------------------------\");\nfor (int i = 0; i < n; i++) {\n    students[i].display();\n}\nSystem.out.println(\"------------------------------------------------------------\");",
                "doing": "Prints a header row, loops through the student array calling `display()` on each, and closes the table.",
                "how": [
                    "Header prints column names aligned with the same format string as `display()`.",
                    "Loop walks through index 0 to N - 1, invoking the instance method on each student object."
                ],
                "watchout": "Notice each row is perfectly aligned because both header and data use the exact same width specifiers."
            }
        ],
        "challenge": {
            "prompt": "What does 'Student[] arr = new Student[10];' put into arr[0] before you assign anything?",
            "opts": [
                "A) An empty Student object with blank strings.",
                "B) A random student from memory.",
                "C) null (no Student object has been created yet).",
                "D) A compilation error."
            ],
            "correct_opt": "C",
            "hint": "Arrays of reference types are always initialized to null in Java.",
            "praise": "Bingo! arr[0] is null until you explicitly write 'arr[0] = new Student(...)'.",
            "roast": "Object arrays in Java start filled with null references until you instantiate each one!"
        }
    },

    # ── Experiment 04 ─────────────────────────────────────────────────────────
    {
        "num": 4,
        "title": "Runtime Polymorphism and Method Overriding (Shape)",
        "file": "java-lab/programs/Lab04ShapePolymorphism.java",
        "story": "Polymorphism means 'many forms'! Imagine a universal remote: the button says 'Draw', but when pointed at a Circle, it draws a circle; pointed at a Triangle, it draws a triangle! In Java, a single Superclass variable (`Shape s`) can point to any child object on the Heap. The JVM checks what object is actually there at runtime and calls the right method using Dynamic Method Dispatch (VTable).",
        "problem": "Create a base class Shape with draw() and erase(). Create subclasses Circle, Triangle, Square that override draw() and erase(). Demonstrate polymorphism using a single Shape reference.",
        "concept": "Dynamic Method Dispatch. A superclass reference variable (Shape s) can point to any subclass object (Circle, Triangle) and resolves the overridden method at runtime via the JVM Virtual Method Table (vtable).",
        "blocks": [
            {
                "title": "Part 1: The Base Shape Class",
                "code": "class Shape {\n    public void draw() {\n        System.out.println(\"Drawing generic Shape\");\n    }\n    public void erase() {\n        System.out.println(\"Erasing generic Shape\");\n    }\n}",
                "doing": "Creates the parent class defining the standard contract: all shapes must know how to draw and erase themselves.",
                "how": [
                    "`Shape`: Provides default base implementations that subclasses will override.",
                    "Acts as the common ancestor type for all specific geometric shapes."
                ],
                "watchout": "In real-world Java, Shape could also be abstract, but in this VTU lab, concrete base methods are provided."
            },
            {
                "title": "Part 2: Subclasses Overriding draw() and erase()",
                "code": "class Circle extends Shape {\n    @Override\n    public void draw() { System.out.println(\"Drawing Circle ⭕\"); }\n    @Override\n    public void erase() { System.out.println(\"Erasing Circle\"); }\n}\n\nclass Triangle extends Shape {\n    @Override\n    public void draw() { System.out.println(\"Drawing Triangle 🔺\"); }\n    @Override\n    public void erase() { System.out.println(\"Erasing Triangle\"); }\n}\n\nclass Square extends Shape {\n    @Override\n    public void draw() { System.out.println(\"Drawing Square ⬛\"); }\n    @Override\n    public void erase() { System.out.println(\"Erasing Square\"); }\n}",
                "doing": "Child classes inherit from Shape and provide their own specialized drawing behavior using method overriding.",
                "how": [
                    "`extends Shape`: Establishes the 'IS-A' relationship (Circle IS-A Shape).",
                    "`@Override`: A compiler safety check guaranteeing method names and signatures match the parent."
                ],
                "watchout": "Overriding requires exact same method signature (name + parameters). Changing parameters is Overloading, NOT Overriding!"
            },
            {
                "title": "Part 3: Dynamic Method Dispatch in Action",
                "code": "public class Lab04ShapePolymorphism {\n    public static void main(String[] args) {\n        Shape s; // Single reference variable on the Call Stack\n\n        s = new Circle();   // Points to Circle on Heap\n        s.draw();           // Dynamic dispatch invokes Circle.draw()!\n\n        s = new Triangle(); // Reassigned to Triangle\n        s.draw();           // Dynamic dispatch invokes Triangle.draw()!\n\n        s = new Square();   // Reassigned to Square\n        s.draw();           // Dynamic dispatch invokes Square.draw()!\n    }\n}",
                "doing": "Uses one single Shape reference `s` to trigger completely different behaviors depending on what object is currently attached to it.",
                "how": [
                    "At compile time, compiler only knows `s` is a Shape.",
                    "At runtime, the JVM looks at the heap object header, finds its Virtual Method Table (vtable), and calls the child's overridden method.",
                    "This is the very essence of Runtime Polymorphism."
                ],
                "watchout": "Examiners will ask: 'Does s.draw() decide which method to call at compile-time or runtime?' Answer: RUNTIME!"
            }
        ],
        "challenge": {
            "prompt": "What determines which overridden method gets called when you invoke 's.draw()' on a Shape reference?",
            "opts": [
                "A) The declared type of the reference variable at compile time.",
                "B) The actual object type currently residing on the Heap at runtime (Dynamic Method Dispatch).",
                "C) The order of methods inside the source file.",
                "D) The operating system language setting."
            ],
            "correct_opt": "B",
            "hint": "Dynamic Dispatch resolves method calls at runtime based on the actual object on the heap.",
            "praise": "100% correct! The runtime object type decides the method, not the reference type.",
            "roast": "Dynamic dispatch checks the actual object on the heap at runtime via the vtable!"
        }
    },

    # ── Experiment 05 ─────────────────────────────────────────────────────────
    {
        "num": 5,
        "title": "Resizable Interface Implementation",
        "file": "java-lab/programs/Lab05ResizableInterface.java",
        "story": "Classes can only inherit from ONE parent class in Java, but they can implement as many INTERFACES as they want! An interface is like a legally binding contract: it has no state, only method promises. Here, `Resizable` promises that anything implementing it can be resized in width and height. Our `Rectangle` class signs the contract and provides the code.",
        "problem": "Create an interface Resizable with resizeWidth(int width) and resizeHeight(int height). Implement it in a Rectangle class.",
        "concept": "Interfaces define a 100% abstract behavioral contract. Classes implement interfaces to guarantee specific capabilities, supporting multiple inheritance of type.",
        "blocks": [
            {
                "title": "Part 1: The Resizable Interface Contract",
                "code": "interface Resizable {\n    void resizeWidth(int width);   // Implicitly public and abstract\n    void resizeHeight(int height); // Implicitly public and abstract\n}",
                "doing": "Declares the contract specifying that any resizable entity must provide width and height resizing methods.",
                "how": [
                    "`interface`: Keyword defining a pure contract.",
                    "All methods inside an interface are automatically `public abstract` — you don't even need to type it!"
                ],
                "watchout": "Interfaces cannot have instance variables or normal constructors. They define WHAT to do, not HOW."
            },
            {
                "title": "Part 2: Rectangle Implementing the Contract",
                "code": "class Rectangle implements Resizable {\n    private int width, height;\n\n    public Rectangle(int w, int h) {\n        this.width = w;\n        this.height = h;\n    }\n\n    // Implementing interface methods MUST be declared 'public'\n    @Override\n    public void resizeWidth(int width) {\n        this.width = width;\n    }\n\n    @Override\n    public void resizeHeight(int height) {\n        this.height = height;\n    }\n\n    public void display() {\n        System.out.println(\"Rectangle Dimensions: \" + width + \" x \" + height);\n    }\n}",
                "doing": "Rectangle signs the contract (`implements Resizable`) and provides the concrete method bodies.",
                "how": [
                    "`implements Resizable`: Signals to compiler that Rectangle satisfies the contract.",
                    "`public void resizeWidth()`: MUST be public! In Java, you cannot reduce the visibility of an inherited method."
                ],
                "watchout": "If you forget the 'public' keyword on resizeWidth(), compiler throws: 'Cannot reduce visibility of inherited method'!"
            },
            {
                "title": "Part 3: Testing Resizing in main()",
                "code": "public class Lab05ResizableInterface {\n    public static void main(String[] args) {\n        Rectangle rect = new Rectangle(50, 30);\n        rect.display(); // 50 x 30\n\n        // Resizing dimensions\n        rect.resizeWidth(80);\n        rect.resizeHeight(60);\n        rect.display(); // 80 x 60\n    }\n}",
                "doing": "Instantiates a rectangle, prints initial dimensions, mutates dimensions via the interface methods, and displays the result.",
                "how": [
                    "Calls `resizeWidth(80)` to modify internal width safely.",
                    "Calls `resizeHeight(60)` to modify internal height safely."
                ],
                "watchout": "You can also write `Resizable r = new Rectangle(50, 30); r.resizeWidth(100);` using interface references!"
            }
        ],
        "challenge": {
            "prompt": "What happens if you omit the keyword 'public' when implementing an interface method in a class?",
            "opts": [
                "A) The method becomes private.",
                "B) Compilation error: Cannot reduce the visibility of the inherited method from the interface.",
                "C) It compiles fine with package-private access.",
                "D) The interface is automatically deleted."
            ],
            "correct_opt": "B",
            "hint": "Interface methods are public by default. Overriding methods can never reduce visibility.",
            "praise": "Crucial exam catch! Overridden interface methods MUST always be explicitly declared public.",
            "roast": "Interface methods are public by default; subclasses cannot make them default or private!"
        }
    },

    # ── Experiment 06 ─────────────────────────────────────────────────────────
    {
        "num": 6,
        "title": "User-Defined Packages (mypack)",
        "file": "java-lab/programs/Lab06PackageDemo.java",
        "story": "Imagine two developers writing a class called 'Database': which one does your program use? Packages solve this by creating folder namespaces (like folders on your hard drive). In this experiment, we create our own custom package named `mypack`, compile it with `javac -d .`, and import it from another Java program across folder boundaries!",
        "problem": "Create a user-defined package named 'mypack' containing a class with a public method. Write a driver program in another file to import and invoke it.",
        "concept": "Packages prevent naming collisions and enforce access protection boundaries. Physical directory paths mirror package namespace hierarchies.",
        "blocks": [
            {
                "title": "Part 1: The Packaged Class (mypack/MyClass.java)",
                "code": "// Must be the very first non-comment line in file\npackage mypack;\n\npublic class MyClass {\n    public void displayMessage() {\n        System.out.println(\"Hello from mypack.MyClass! Package working perfectly.\");\n    }\n}",
                "doing": "Declares that this class belongs to the `mypack` namespace and makes both class and method public.",
                "how": [
                    "`package mypack;`: Tells JVM this class resides in directory folder `mypack/`.",
                    "`public class`: Must be public so classes outside the folder can see it.",
                    "`public void displayMessage()`: Must be public so external code can call it."
                ],
                "watchout": "`package` statement MUST be line 1! Putting imports or code before package triggers a compiler error."
            },
            {
                "title": "Part 2: Compiling Packages with javac -d .",
                "code": "# Terminal command to compile package:\njavac -d . MyClass.java\n\n# Flag breakdown:\n# -d . -> Automatically creates folder 'mypack/' and puts MyClass.class inside!",
                "doing": "Uses the compiler's `-d` flag to automatically create the folder structure and place bytecode in it.",
                "how": [
                    "`-d` stands for Destination Directory.",
                    "`.` means the current folder.",
                    "Compiler reads `package mypack;`, generates folder `mypack/`, and outputs `MyClass.class` inside it."
                ],
                "watchout": "If you just run `javac MyClass.java` without `-d`, it won't create the folder structure!"
            },
            {
                "title": "Part 3: Importing and Consuming the Packaged Class",
                "code": "// File: Lab06PackageDemo.java (outside mypack folder)\nimport mypack.MyClass; // Import our custom package!\n\npublic class Lab06PackageDemo {\n    public static void main(String[] args) {\n        MyClass obj = new MyClass();\n        obj.displayMessage();\n    }\n}",
                "doing": "Imports `mypack.MyClass` across directory boundaries, instantiates it, and executes its method.",
                "how": [
                    "`import mypack.MyClass;`: Informs compiler to find MyClass inside the `mypack/` directory on the CLASSPATH.",
                    "`obj.displayMessage()`: Successfully executes the packaged class."
                ],
                "watchout": "Ensure you run the program from the parent directory: `java Lab06PackageDemo`."
            }
        ],
        "challenge": {
            "prompt": "What compiler flag automatically generates the physical directory matching the package statement?",
            "opts": [
                "A) javac -p",
                "B) javac -pkg",
                "C) javac -dir",
                "D) javac -d <directory>"
            ],
            "correct_opt": "D",
            "hint": "-d specifies the destination directory for package output.",
            "praise": "Correct! 'javac -d .' generates the package directory structure automatically.",
            "roast": "The flag is 'javac -d .' where -d stands for destination!"
        }
    },

    # ── Experiment 07 ─────────────────────────────────────────────────────────
    {
        "num": 7,
        "title": "Custom Exception Handling (Division By Zero)",
        "file": "java-lab/programs/Lab07CustomException.java",
        "story": "When things go wrong in a program (like dividing by zero), you don't want your app to crash in front of the user! Java lets you create your own custom Exception classes. We create a `DivisionByZeroException`, explicitly fire it using `throw new`, catch it safely in a `try-catch` block, and prove that the `finally` block ALWAYS runs cleanup code no matter what happens!",
        "problem": "Create a custom exception class DivisionByZeroException. Read two numbers, check if denominator is zero, throw the custom exception, and handle it gracefully with try-catch-finally.",
        "concept": "Robust error management via exception handling. Custom exceptions extend Exception (checked) or RuntimeException (unchecked), separating error-handling code from normal logic.",
        "blocks": [
            {
                "title": "Part 1: Creating the Custom Exception Class",
                "code": "class DivisionByZeroException extends Exception {\n    public DivisionByZeroException(String message) {\n        super(message); // Passes error description to java.lang.Exception\n    }\n}",
                "doing": "Defines our own user-created error type by inheriting from Java's built-in `Exception` class.",
                "how": [
                    "`extends Exception`: Makes this a Checked Exception (must be handled or declared).",
                    "`super(message)`: Stores the custom error string so `e.getMessage()` can retrieve it later."
                ],
                "watchout": "Extending `Exception` makes it checked (strict); extending `RuntimeException` makes it unchecked."
            },
            {
                "title": "Part 2: The divide() Method with Explicit throw",
                "code": "public static double divide(int a, int b) throws DivisionByZeroException {\n    if (b == 0) {\n        // Explicitly instantiate and fire the exception!\n        throw new DivisionByZeroException(\"Denominator cannot be zero!\");\n    }\n    return (double) a / b;\n}",
                "doing": "Checks if the denominator is 0: if so, halts execution and launches our custom exception into the Call Stack.",
                "how": [
                    "`throw new ...`: Explicitly creates and raises the exception object.",
                    "`throws DivisionByZeroException`: Declares in the method signature that callers must be ready to catch this."
                ],
                "watchout": "Notice `throw` (action: fire exception) vs `throws` (declaration: warning in method header)."
            },
            {
                "title": "Part 3: try-catch-finally Call Stack Handling",
                "code": "try {\n    double result = divide(numerator, denominator);\n    System.out.println(\"Result: \" + result);\n} catch (DivisionByZeroException e) {\n    System.out.println(\"Caught Custom Exception: \" + e.getMessage());\n} finally {\n    System.out.println(\"Finally block ALWAYS executes! Closing scanner...\");\n    sc.close();\n}",
                "doing": "Protects dangerous math inside `try`, recovers gracefully in `catch`, and guarantees resource cleanup in `finally`.",
                "how": [
                    "`try`: Runs the division calculation.",
                    "`catch`: Intercepts the exception before the JVM crashes.",
                    "`finally`: The superhero block! ALWAYS runs, whether division succeeded or failed, making it the perfect place to close files and scanners."
                ],
                "watchout": "Even if the catch block returns early, `finally` will STILL execute before returning!"
            }
        ],
        "challenge": {
            "prompt": "What is the key difference between the keywords 'throw' and 'throws' in Java?",
            "opts": [
                "A) 'throw' is used in the method signature; 'throws' triggers the exception.",
                "B) 'throw' is used to explicitly instantiate and raise an exception; 'throws' declares in the method signature that a method may raise an exception.",
                "C) They are completely interchangeable synonyms.",
                "D) 'throw' is for checked exceptions; 'throws' is for unchecked exceptions."
            ],
            "correct_opt": "B",
            "hint": "throw = verb (do it now!); throws = disclaimer (heads up, this might happen).",
            "praise": "Spot on! throw raises the exception object; throws declares it in the method header.",
            "roast": "Remember: `throw` fires the exception; `throws` declares it in the method signature!"
        }
    },

    # ── Experiment 08 ─────────────────────────────────────────────────────────
    {
        "num": 8,
        "title": "Multithreading and Concurrent Execution",
        "file": "java-lab/programs/Lab08ThreadConcurrency.java",
        "story": "Why make your CPU do one thing at a time when your laptop has multiple cores? Multithreading lets your program do multiple tasks simultaneously! In this lab, we build a `ChildThread` that counts numbers in the background with simulated delays (`Thread.sleep()`), while the `MainThread` counts simultaneously in parallel. You will see both threads taking turns on the screen!",
        "problem": "Create multiple threads in Java to demonstrate concurrent execution and context switching using Thread.sleep() and start().",
        "concept": "Concurrency enables simultaneous execution of two or more parts of a program. Creating threads via 'extends Thread' or 'implements Runnable' allows OS time-slicing across cores.",
        "blocks": [
            {
                "title": "Part 1: Thread Constructor & super(name)",
                "code": "class MyThread extends Thread {\n    public MyThread(String name) {\n        super(name); // Names the thread in the OS scheduler\n        start();     // Immediately spawns child thread onto a new OS call stack\n    }\n}",
                "doing": "Inherits from java.lang.Thread and configures thread identity before kicking off execution.",
                "how": [
                    "`super(name)`: Passes the human-readable thread name to the base `Thread` constructor.",
                    "`start()`: Requests a brand-new call stack from the JVM thread scheduler and schedules `run()`."
                ],
                "watchout": "Never call `run()` directly — calling `start()` is the only way to allocate a true separate call stack."
            },
            {
                "title": "Part 2: run() Payload & Thread.sleep() Interleaving",
                "code": "@Override\npublic void run() {\n    for (int i = 1; i <= 5; i++) {\n        System.out.println(\"  [Child Thread] \" + Thread.currentThread().getName() + \" Count: \" + i);\n        try {\n            Thread.sleep(500); // Voluntarily yield CPU for 500ms\n        } catch (InterruptedException e) {\n            System.out.println(\"Child thread interrupted: \" + e.getMessage());\n        }\n    }\n}",
                "doing": "Executes the concurrent worker loop, printing counts and pausing to give other threads access to the CPU.",
                "how": [
                    "`run()`: The entry point for the new thread, executing asynchronously in the background.",
                    "`Thread.sleep(500)`: Suspends execution for half a second, triggering OS context switching.",
                    "`InterruptedException`: Checked exception caught in case another thread interrupts sleep."
                ],
                "watchout": "If you don't handle `InterruptedException` with try-catch, Java will refuse to compile because sleep is checked."
            },
            {
                "title": "Part 3: Main Thread Loop & child.join() Synchronization",
                "code": "public class Lab08ThreadConcurrency {\n    public static void main(String[] args) {\n        MyThread child = new MyThread(\"Worker-Child-Thread\");\n\n        for (int i = 1; i <= 5; i++) {\n            System.out.println(\"[Main Thread] \" + Thread.currentThread().getName() + \" Count: \" + i);\n            try { Thread.sleep(500); } catch (InterruptedException e) {}\n        }\n\n        try {\n            child.join(); // Main thread pauses here until child thread finishes!\n        } catch (InterruptedException e) {}\n        System.out.println(\"Threads completed!\");\n    }\n}",
                "doing": "Runs the main thread loop side-by-side with child thread and synchronizes termination using `join()`.",
                "how": [
                    "Main thread and child thread take turns running and printing counts concurrently.",
                    "`child.join()`: Forces the main thread to wait until the child thread completely terminates before exiting."
                ],
                "watchout": "Without `join()`, main thread could finish and exit early while background worker threads are still computing."
            }
        ],
        "challenge": {
            "prompt": "What happens if you invoke 't.run()' directly instead of 't.start()' on a Thread object?",
            "opts": [
                "A) It spawns a background thread with higher priority.",
                "B) An IllegalThreadStateException is thrown.",
                "C) It does NOT spawn a new thread; it simply executes run() as a normal method call synchronously on the current thread.",
                "D) The operating system crashes."
            ],
            "correct_opt": "C",
            "hint": "Only start() creates a new thread call stack. Calling run() directly is just a plain function call.",
            "praise": "Exactly right! start() spawns a new thread; run() is just a plain synchronous call.",
            "roast": "Calling run() does NOT create a thread — it just runs synchronously on the calling thread!"
        }
    },

    # ── Experiment 09 ─────────────────────────────────────────────────────────
    {
        "num": 9,
        "title": "Java Enumerations and valueOf()",
        "file": "java-lab/programs/Lab09DepartmentEnum.java",
        "story": "Ever had a bug because a user typed 'computer-sci' instead of 'CSE'? Strings are error-prone! Java Enums (Enumerations) solve this by creating a closed, type-safe list of valid choices (like CSE, ISE, ECE). In Java, Enums are full-fledged classes that have positions (`ordinal()`), full iteration lists (`values()`), and can convert user input strings directly into constants using `valueOf()`!",
        "problem": "Create an enum Department (CSE, ISE, ECE, MECH, CIVIL). Demonstrate values(), ordinal(), and converting a user String to enum constant via valueOf().",
        "concept": "Enums are type-safe lists of named constants. In Java, enums are full-featured classes that can contain fields, constructors, and methods, preventing invalid constant assignments.",
        "blocks": [
            {
                "title": "Part 1: The Department Enum Declaration",
                "code": "enum Department {\n    CSE, ISE, ECE, MECH, CIVIL\n}",
                "doing": "Defines the only 5 valid engineering departments permitted by the system.",
                "how": [
                    "`enum`: Defines a type-safe enumeration class inheriting from `java.lang.Enum`.",
                    "Each constant (`CSE`, `ISE`...) is a public static final singleton instance."
                ],
                "watchout": "Enums eliminate magic strings. You can never assign a random string like 'HACKER' to a Department variable."
            },
            {
                "title": "Part 2: values() and ordinal() Iteration",
                "code": "System.out.println(\"Available Departments:\");\nfor (Department d : Department.values()) {\n    System.out.println(\"Dept: \" + d + \" | Ordinal Position: \" + d.ordinal());\n}",
                "doing": "Loops through all valid department choices and prints each choice alongside its zero-based position index.",
                "how": [
                    "`Department.values()`: Built-in static method returning an array of all enum constants.",
                    "`d.ordinal()`: Returns the declaration index (`CSE` is 0, `ISE` is 1, `ECE` is 2...)."
                ],
                "watchout": "`values()` is synthesized automatically by the Java compiler for every enum!"
            },
            {
                "title": "Part 3: String to Enum Parsing via valueOf()",
                "code": "Scanner sc = new Scanner(System.in);\nSystem.out.print(\"Enter your department code: \");\nString input = sc.next().toUpperCase();\n\ntry {\n    Department userDept = Department.valueOf(input);\n    System.out.println(\"Valid Department confirmed: \" + userDept);\n} catch (IllegalArgumentException e) {\n    System.out.println(\"Error: '\" + input + \"' is not a recognized department!\");\n}",
                "doing": "Converts user text into an official enum constant, safely catching invalid department codes.",
                "how": [
                    "`Department.valueOf(input)`: Searches for the exact matching enum constant name.",
                    "If input doesn't match any constant (e.g., 'BIOTECH'), it throws `IllegalArgumentException`.",
                    "The try-catch block intercepts the error and warns the user without crashing."
                ],
                "watchout": "`valueOf()` is case-sensitive! Always call `.toUpperCase()` on user input first."
            }
        ],
        "challenge": {
            "prompt": "What exception is thrown by Department.valueOf() if the input string does not match any enum constant?",
            "opts": [
                "A) NullPointerException",
                "B) ClassCastException",
                "C) NoSuchElementException",
                "D) IllegalArgumentException"
            ],
            "correct_opt": "D",
            "hint": "Passing an unrecognized identifier string throws java.lang.IllegalArgumentException.",
            "praise": "Spot on! Enum.valueOf() throws IllegalArgumentException on invalid strings.",
            "roast": "Enum.valueOf() throws java.lang.IllegalArgumentException when an invalid constant is passed!"
        }
    },

    # ── Experiment 10 ─────────────────────────────────────────────────────────
    {
        "num": 10,
        "title": "Wrapper Classes and Autoboxing / Unboxing",
        "file": "java-lab/programs/Lab10MarksCalculator.java",
        "story": "Java has two worlds: fast primitive types (`int`, `double`) and flexible reference Objects (`Integer`, `Double`). Collections like ArrayList can ONLY store objects! Wrapper Classes bridge this gap by wrapping primitives inside object boxes. Thanks to Autoboxing and Unboxing, the Java compiler boxes and unboxes numbers automatically behind the scenes!",
        "problem": "Develop a Java program using Wrapper classes to read student test scores as Strings, parse them using Integer.parseInt(), calculate totals using autoboxed Integers, and unbox to primitives.",
        "concept": "Wrapper classes (Integer, Double, Character) convert primitive data types into first-class Java objects. Autoboxing (primitive -> object) and Unboxing (object -> primitive) happen automatically.",
        "blocks": [
            {
                "title": "Part 1: Reading Marks as Strings",
                "code": "Scanner scanner = new Scanner(System.in);\nSystem.out.print(\"Enter marks for Subject 1 (as string): \");\nString strMark1 = scanner.next();\nString strMark2 = scanner.next();\nString strMark3 = scanner.next();",
                "doing": "Captures marks from the console as pure character strings rather than numbers.",
                "how": [
                    "`scanner.next()`: Reads user inputs as raw `java.lang.String` text.",
                    "Simulates real-world systems (APIs, forms) where incoming numeric data arrives as plain text."
                ],
                "watchout": "String text cannot be used in arithmetic operations directly without wrapper conversion."
            },
            {
                "title": "Part 2: Double.valueOf() & NumberFormatException",
                "code": "try {\n    // Converting string text directly into Double wrapper objects\n    Double mark1 = Double.valueOf(strMark1);\n    Double mark2 = Double.valueOf(strMark2);\n    Double mark3 = Double.valueOf(strMark3);\n} catch (NumberFormatException e) {\n    System.out.println(\"Error: Please enter valid numeric values!\");\n}",
                "doing": "Converts string digits into Double objects and guards against invalid non-numeric typing.",
                "how": [
                    "`Double.valueOf(s)`: Parses string text and wraps the numeric value into a heap `Double` object.",
                    "`NumberFormatException`: Caught safely if the user types letters or symbols instead of valid numbers."
                ],
                "watchout": "If user types 'eighty', valueOf throws NumberFormatException — catching it prevents application crashes."
            },
            {
                "title": "Part 3: Autoboxing & Unboxing Arithmetic",
                "code": "// 1. UNBOXING: mark1, mark2, mark3 unbox to primitive double for (+)\n// 2. AUTOBOXING: Primitive double sum is re-boxed into Double total\nDouble total = mark1 + mark2 + mark3;\nDouble average = total / 3.0;\n\nSystem.out.printf(\"Total Marks : %.2f%n\", total);\nSystem.out.printf(\"Average Marks : %.2f%n\", average);",
                "doing": "Computes total and average where Java transparently unwraps objects for math and re-boxes the results.",
                "how": [
                    "Unboxing: Java extracts `.doubleValue()` automatically so the CPU can execute `+` and `/` operations.",
                    "Autoboxing: Java takes the calculated double primitive and calls `Double.valueOf()` to store in `Double total`."
                ],
                "watchout": "Autoboxing is convenient, but running billions of boxing operations in tight loops creates heap garbage — use primitives for heavy loops!"
            }
        ],
        "challenge": {
            "prompt": "What method does the Java compiler automatically emit behind the scenes when executing 'Integer x = 42;' (Autoboxing)?",
            "opts": [
                "A) Integer.valueOf(42)",
                "B) Integer.parseInt(42)",
                "C) new int(42)",
                "D) (Integer) 42"
            ],
            "correct_opt": "A",
            "hint": "Autoboxing translates directly to Integer.valueOf() invocations in bytecode.",
            "praise": "Precisely! Autoboxing calls Integer.valueOf(42) behind the scenes.",
            "roast": "Under the hood, Java compiler converts 'Integer x = 42;' into 'Integer.valueOf(42)'!"
        }
    }
]
