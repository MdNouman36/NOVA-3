JAVA_VIVA_GAUNTLET = [
    {
        "q": "Why does Java NOT support multiple inheritance through classes?",
        "options": [
            "A) Because JVM bytecodes only support one class file at a time.",
            "B) To avoid the Diamond Problem (ambiguity when two parent classes define the same method).",
            "C) Because multiple inheritance was patented by C++.",
            "D) Because Java classes cannot have more than 10 methods."
        ],
        "ans": "B",
        "tip": "The Diamond Problem happens when class D extends B and C, which both extend A. If B and C override a method, D does not know which one to inherit! Interfaces solve this because they contain no state.",
        "praise": "Spot on! The Diamond Problem is the classic reason Java uses interfaces instead.",
        "roast": "Multiple inheritance of classes leads to ambiguity (the Diamond Problem)."
    },
    {
        "q": "What is the difference between final, finally, and finalize in Java?",
        "options": [
            "A) They are identical keywords used for backward compatibility.",
            "B) final is a modifier (constant/cannot override/cannot inherit); finally is a block in exception handling; finalize is a method called by the Garbage Collector.",
            "C) final is for loops; finally is for classes; finalize is for interfaces.",
            "D) final is deprecated; finally and finalize are active."
        ],
        "ans": "B",
        "tip": "final variable = constant; final method = cannot override; final class = cannot extend. finally = block after try/catch. finalize() = called before GC destroys object.",
        "praise": "Examiner favorite! You nailed the distinction between all three.",
        "roast": "Don't confuse them: final = modifier; finally = block; finalize = GC cleanup method."
    },
    {
        "q": "Why must super() or this() always be the very FIRST statement in a constructor?",
        "options": [
            "A) Because Java syntax rules say all method calls must be capitalized first.",
            "B) Because the superclass state must be fully initialized before the subclass can configure its own state.",
            "C) To prevent the garbage collector from running during object allocation.",
            "D) It is an optional recommendation that does not affect compilation."
        ],
        "ans": "B",
        "tip": "Object construction proceeds from superclass down to subclass. The child relies on parent fields being ready.",
        "praise": "Architectural mastery! Subclass fields depend on parent initialization completing first.",
        "roast": "The parent object must exist before the child can add its own state to it."
    },
    {
        "q": "What happens if you invoke thread.run() instead of thread.start() in Java?",
        "options": [
            "A) It throws an IllegalThreadStateException.",
            "B) It runs the run() code synchronously on the CURRENT thread without creating a new separate thread.",
            "C) It starts two threads at the same time.",
            "D) The JVM immediately crashes with an OutOfMemoryError."
        ],
        "ans": "B",
        "tip": "start() allocates a new call stack and requests OS scheduling. run() is just a normal method call executed on the current caller's thread!",
        "praise": "Brilliant! Calling run() directly bypasses all concurrency.",
        "roast": "Calling run() does NOT create a thread; it just executes sequentially on the current thread."
    },
    {
        "q": "What is the difference between String, StringBuilder, and StringBuffer in Java?",
        "options": [
            "A) String is mutable; StringBuilder and StringBuffer are immutable.",
            "B) String is immutable; StringBuilder is mutable and not synchronized (fast); StringBuffer is mutable and thread-safe (synchronized).",
            "C) StringBuffer is for numbers; StringBuilder is for text.",
            "D) They have identical performance characteristics."
        ],
        "ans": "B",
        "tip": "Strings cannot be modified after creation. For heavy concatenation, use StringBuilder (single-threaded) or StringBuffer (multi-threaded).",
        "praise": "Precise and complete! Immutability vs Thread-safety.",
        "roast": "String is immutable. StringBuilder is fast/unsynchronized. StringBuffer is thread-safe."
    }
]

# ==============================================================================
# INTERACTIVE OOP VISUALIZERS
# ==============================================================================