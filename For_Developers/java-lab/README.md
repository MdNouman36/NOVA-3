# ☕ Object-Oriented Programming with Java Lab — 1BCS302 (3rd Sem)

Welcome to the **Java Lab** module of **OILS-3** (*Oops, I Learnt Something!*), fully aligned with the **VTU 2025 Scheme**.

> **Status:** ✅ All 10 Lab Experiments Verified, Standards-Compliant, and Ready to Compile!

---

## 📌 Experiment Directory

All verified programs are located in [`programs/`](programs/):

1. **[Lab 01: Matrix Addition](programs/Lab01MatrixAddition.java)**
   * *Concepts:* 2D arrays, nested loops, `Scanner` class, order N matrix addition.
2. **[Lab 02: Stack Operations](programs/Lab02StackOperations.java)**
   * *Concepts:* Encapsulation, private data members, `push()`, `pop()`, `display()`, `isEmpty()`, `isFull()`.
3. **[Lab 03: Student Objects Array](programs/Lab03StudentDemo.java)**
   * *Concepts:* Constructors, `this` reference, arrays of object references, formatted tabular display with `printf`.
4. **[Lab 04: Shape Polymorphism](programs/Lab04ShapePolymorphism.java)**
   * *Concepts:* Inheritance (`Circle`, `Triangle`, `Square` extending `Shape`), `@Override`, Dynamic Method Dispatch (Runtime Polymorphism).
5. **[Lab 05: Resizable Interface](programs/Lab05ResizableInterface.java)**
   * *Concepts:* Interface contracts (`resizeWidth`, `resizeHeight`), `implements` keyword, `Rectangle` class.
6. **[Lab 06: User-Defined Packages](programs/Lab06PackageDemo.java)**
   * *Concepts:* Custom package declaration (`mypack/MyPackageClass.java`), folder mapping, `import`, compiling across directories.
7. **[Lab 07: Custom Exception Handling](programs/Lab07CustomException.java)**
   * *Concepts:* User-defined `DivisionByZeroException extends Exception`, `throw`, `throws`, `try-catch-finally`.
8. **[Lab 08: Multithreading Concurrency](programs/Lab08ThreadConcurrency.java)**
   * *Concepts:* `MyThread extends Thread`, calling `super(name)` in constructor, starting thread with `start()`, concurrent interleaved execution with main thread.
9. **[Lab 09: Enumeration with `valueOf()`](programs/Lab09DepartmentEnum.java)**
   * *Concepts:* `enum Department { CSE, ISE, ECE, MECH }`, parsing input string to enum with `valueOf()`, catching `IllegalArgumentException`.
10. **[Lab 10: Wrapper Classes & Autoboxing](programs/Lab10MarksCalculator.java)**
    * *Concepts:* `Double.valueOf()`, automatic unboxing in `+` operator, autoboxing result, `NumberFormatException` safety.

---

## 🛠️ How to Compile & Run Any Program:

```bash
# Standard compilation:
cd programs
javac Lab01MatrixAddition.java
java Lab01MatrixAddition

# For Package Demo (Lab 06):
javac mypack/MyPackageClass.java
javac Lab06PackageDemo.java
java Lab06PackageDemo
```

Or just launch the interactive arcade:
```bash
python play.py
```
*(Choose Option `[3] ☕ Java OOP Lab Studio`)*
