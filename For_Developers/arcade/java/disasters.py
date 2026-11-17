JAVA_DISASTER_SCENARIOS = [
    {
        "title": "🚨 DISASTER 1: The Infamous NullPointerException in Object Array",
        "story": "In Experiment 03 (Student Class), you wrote:\n  Student[] s = new Student[5];\n  s[0].display();\n\nYour JVM immediately crashes in flames with:\n\033[91mjava.lang.NullPointerException: Cannot invoke Student.display() because s[0] is null\033[0m!",
        "prompt": "Why was s[0] null when you just declared 'new Student[5]'?",
        "choices": [
            "'new Student[5]' allocates an array of 5 NULL references; you must instantiate each element with 's[0] = new Student(...)'.",
            "Java does not support arrays of custom classes.",
            "Student class must be declared 'static'.",
            "You must reboot the JVM to register new classes."
        ],
        "ans_idx": 1,
        "reaction": "EXACTLY! In Java, arrays of objects are arrays of references. All slots start as null until explicitly instantiated with 'new'!"
    },
    {
        "title": "🚨 DISASTER 2: The Fake-Out Synchronous Thread",
        "story": "In Experiment 08 (Multithreading), you created a worker thread:\n  MyThread t = new MyThread(\"Worker\");\n  t.run();\n\nThe examiner looks at your terminal and points out that the main thread waited for the worker to finish before continuing. Why did concurrency fail?",
        "prompt": "What was the mistake in starting the thread?",
        "choices": [
            "You called 't.run()' directly instead of 't.start()'. Calling run() executes sequentially on the caller thread without creating a new OS thread!",
            "Thread class only works on Linux operating systems.",
            "You forgot to extend Runnable instead of Thread.",
            "Java requires root privileges to execute concurrent threads."
        ],
        "ans_idx": 1,
        "reaction": "CORRECT! Calling run() is just a standard method call. Calling start() registers with the JVM scheduler and allocates a new thread stack!"
    },
    {
        "title": "🚨 DISASTER 3: The Case-Sensitive Enum Crash",
        "story": "In Experiment 09 (Department Enum), the user typed 'cse' in lowercase. Your program crashed with:\n\033[91mjava.lang.IllegalArgumentException: No enum constant Department.cse\033[0m!",
        "prompt": "Why did Enum.valueOf() reject the input?",
        "choices": [
            "Enum constants are strictly CASE-SENSITIVE in Java. You must convert user input using '.toUpperCase()' before calling valueOf()!",
            "Enums cannot store words shorter than 4 letters.",
            "Enums only accept integer inputs.",
            "valueOf() is deprecated in Java 21."
        ],
        "ans_idx": 1,
        "reaction": "NAILED IT! Department.valueOf(\"cse\") fails because the constant is named CSE. Always sanitize with input.trim().toUpperCase()!"
    },
    {
        "title": "🚨 DISASTER 4: The Unhandled Checked Exception Compiler Strike",
        "story": "In Experiment 07 (Custom Exceptions), you wrote a helper that calls 'divide(10, 0)'. The Java compiler refuses to build your code:\n\033[91munreported exception DivisionByZeroException; must be caught or declared to be thrown\033[0m!",
        "prompt": "Why is the compiler forcing you to handle DivisionByZeroException?",
        "choices": [
            "Because DivisionByZeroException extends 'Exception' (Checked Exception). The compiler enforces handling via try-catch or 'throws' in the signature!",
            "Because division by zero is illegal under federal copyright laws.",
            "Because custom exceptions must extend RuntimeException instead.",
            "You forgot to import java.lang.Throwable."
        ],
        "ans_idx": 1,
        "reaction": "SPOT ON! Checked exceptions (inheriting from Exception but not RuntimeException) are verified at compile-time by the javac compiler!"
    },
    {
        "title": "🚨 DISASTER 5: The Autoboxing NullPointerException Trap",
        "story": "In Experiment 10 (Wrapper Classes), you wrote:\n  Double mark = null;\n  double total = mark + 10.0;\n\nSuddenly, your program crashes with NullPointerException on an arithmetic line!",
        "prompt": "Why did an addition operation throw NullPointerException?",
        "choices": [
            "Unboxing invokes 'mark.doubleValue()'. Since mark is null, invoking a method on it triggers NullPointerException during automatic unboxing!",
            "Java does not support adding primitives to wrapper classes.",
            "The double literal 10.0 must be cast to (Double).",
            "Wrapper classes cannot be used in arithmetic operations."
        ],
        "ans_idx": 1,
        "reaction": "ARCHITECTURAL MASTERY! When unboxing occurs behind the scenes, Java calls .doubleValue(). If the object reference is null, it immediately throws NPE!"
    },
    {
        "title": "🚨 DISASTER 6: The Package Directory Hierarchy Mismatch",
        "story": "In Experiment 06 (Packages), you put 'package mypack;' at the top of 'MyClass.java', but you saved the file directly in the root project folder instead of a subfolder named 'mypack/'.\njavac gives an error when importing!",
        "prompt": "What fundamental rule of Java packages was violated?",
        "choices": [
            "The directory structure MUST mirror the package hierarchy. Classes in 'package mypack;' must reside in a physical folder named 'mypack'.",
            "Package names cannot start with the letter 'm'.",
            "Java packages require a package.json file.",
            "Packages can only be created inside the JDK bin directory."
        ],
        "ans_idx": 1,
        "reaction": "EXACTLY! In Java, package namespaces are directly tied to filesystem directory paths."
    },
    {
        "title": "🚨 DISASTER 7: The Missing @Override Spelling Blunder",
        "story": "In Experiment 04 (Shape Polymorphism), you wanted to override 'void draw()', but accidentally typed 'void Draw()' with a capital D. You ran 'Shape s = new Circle(); s.draw();' and it printed 'Drawing a generic Shape' instead of Circle!",
        "prompt": "Why didn't runtime polymorphism call Circle's method?",
        "choices": [
            "Java is case-sensitive! 'Draw()' is a completely new method, NOT an override of 'draw()'. Using '@Override' would have caught this at compile time!",
            "Dynamic method dispatch only works with abstract classes.",
            "Shape references cannot access subclass methods.",
            "Circle must implement the Drawable interface."
        ],
        "ans_idx": 1,
        "reaction": "BINGO! Without @Override, the compiler thought you were creating a new method Draw(), silently leaving the original draw() un-overridden!"
    },
    {
        "title": "🚨 DISASTER 8: The Forgotten public Modifier in Interface Methods",
        "story": "In Experiment 05 (Resizable), you implemented 'void resizeWidth(int w)' inside class Rectangle without writing 'public'. The compiler shouts:\n\033[91mresizeWidth() in Rectangle cannot implement resizeWidth() in Resizable; attempting to assign weaker access privileges; was public\033[0m!",
        "prompt": "Why must interface methods ALWAYS be declared 'public' when implemented in a class?",
        "choices": [
            "All interface methods are implicitly 'public abstract'. A class cannot reduce the visibility of an inherited interface method (package-private is weaker than public)!",
            "Classes can only have public methods in Java.",
            "Interfaces cannot be implemented by concrete classes.",
            "You must use the 'protected' keyword instead."
        ],
        "ans_idx": 1,
        "reaction": "GOLDEN JAVA CONTRACT RULE! Interface methods are implicitly public. A subclass cannot reduce visibility to default package-private!"
    }
]


# Extract Java experiments & visualizers from java_engine

# ==============================================================================