/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 07: Infix-to-Postfix Conversion with Bracket & Syntax Validation
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * A compiler design team needs a tool to convert arithmetic expressions from
 * infix notation to postfix notation. Expressions contain alphanumeric operands,
 * operators (+, -, *, /, %, ^), and brackets (), {}, []. Read an infix
 * expression, validate correct bracket nesting and syntax, and convert a valid
 * expression to postfix.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - Stack for Bracket Validation:
 *   Push '(', '{', '['. When closing bracket is found, top must match.
 * - Operator Precedence:
 *   ^ : Precedence 3 (Right Associative)
 *   *, /, % : Precedence 2 (Left Associative)
 *   +, - : Precedence 1 (Left Associative)
 * - Conversion Algorithm:
 *   * Operands go directly to the postfix output.
 *   * Opening brackets are pushed to stack.
 *   * Closing bracket pops stack to output until matching opening bracket is popped.
 *   * Operators pop higher-or-equal precedence operators before pushing themselves.
 * ==============================================================================
 */

#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX 300

char opStack[MAX];
int top = -1;

void push(char c) {
    if (top < MAX - 1) {
        opStack[++top] = c;
    }
}

char pop(void) {
    if (top == -1) return '\0';
    return opStack[top--];
}

char peek(void) {
    if (top == -1) return '\0';
    return opStack[top];
}

int isOpeningBracket(char c) {
    return (c == '(' || c == '{' || c == '[');
}

int isClosingBracket(char c) {
    return (c == ')' || c == '}' || c == ']');
}

int isMatchingPair(char open, char close) {
    if (open == '(' && close == ')') return 1;
    if (open == '{' && close == '}') return 1;
    if (open == '[' && close == ']') return 1;
    return 0;
}

int isOperator(char c) {
    return (c == '+' || c == '-' || c == '*' || c == '/' || c == '%' || c == '^');
}

int precedence(char op) {
    switch (op) {
        case '^': return 3;
        case '*':
        case '/':
        case '%': return 2;
        case '+':
        case '-': return 1;
        default : return 0;
    }
}

int isRightAssociative(char op) {
    return (op == '^');
}

/*
 * Block 1: validateBrackets()
 * Checks that (), {}, [] are properly paired and nested.
 */
int validateBrackets(const char expr[]) {
    char bStack[MAX];
    int bTop = -1;

    for (int i = 0; expr[i] != '\0'; i++) {
        char ch = expr[i];
        if (isOpeningBracket(ch)) {
            bStack[++bTop] = ch;
        } else if (isClosingBracket(ch)) {
            if (bTop == -1) return 0; // Closing without opening
            if (!isMatchingPair(bStack[bTop], ch)) return 0; // Type mismatch e.g. ( ]
            bTop--;
        }
    }
    return (bTop == -1); // Must be empty at end
}

/*
 * Block 2: validateSyntax()
 * Verifies alternating operand and operator sequence.
 */
int validateSyntax(const char expr[]) {
    int i = 0;
    int expectingOperand = 1;
    int operandCount = 0;

    while (expr[i] != '\0') {
        char ch = expr[i];
        if (isspace((unsigned char)ch)) {
            i++;
            continue;
        }
        if (isalnum((unsigned char)ch)) {
            if (!expectingOperand) return 0; // Two operands without operator e.g. "A B"
            while (isalnum((unsigned char)expr[i])) i++;
            expectingOperand = 0;
            operandCount++;
            continue;
        }
        if (isOpeningBracket(ch)) {
            if (!expectingOperand) return 0; // e.g. "A("
            i++;
            continue;
        }
        if (isClosingBracket(ch)) {
            if (expectingOperand) return 0; // e.g. "(+)" or "(A+)"
            i++;
            continue;
        }
        if (isOperator(ch)) {
            if (expectingOperand) return 0; // Operator without preceding operand
            expectingOperand = 1;
            i++;
            continue;
        }
        return 0; // Illegal character
    }
    return (operandCount > 0 && !expectingOperand);
}

/*
 * Block 3: convertToPostfix()
 * Transforms valid infix string into spaced postfix notation.
 */
void convertToPostfix(const char infix[], char postfix[]) {
    int i = 0, k = 0;
    top = -1;

    while (infix[i] != '\0') {
        char ch = infix[i];
        if (isspace((unsigned char)ch)) {
            i++;
            continue;
        }

        if (isalnum((unsigned char)ch)) {
            // Read entire operand token
            while (isalnum((unsigned char)infix[i])) {
                postfix[k++] = infix[i++];
            }
            postfix[k++] = ' ';
            continue;
        }

        if (isOpeningBracket(ch)) {
            push(ch);
            i++;
            continue;
        }

        if (isClosingBracket(ch)) {
            while (top != -1 && !isOpeningBracket(peek())) {
                postfix[k++] = pop();
                postfix[k++] = ' ';
            }
            pop(); // Remove matching opening bracket from stack
            i++;
            continue;
        }

        if (isOperator(ch)) {
            while (top != -1 && isOperator(peek())) {
                int topPrec = precedence(peek());
                int curPrec = precedence(ch);

                if (topPrec > curPrec || (topPrec == curPrec && !isRightAssociative(ch))) {
                    postfix[k++] = pop();
                    postfix[k++] = ' ';
                } else {
                    break;
                }
            }
            push(ch);
            i++;
        }
    }

    while (top != -1) {
        postfix[k++] = pop();
        postfix[k++] = ' ';
    }
    if (k > 0 && postfix[k - 1] == ' ') k--; // Trim trailing space
    postfix[k] = '\0';
}

int main(void) {
    char infix[MAX];
    char postfix[MAX * 2];

    printf("================ INFIX TO POSTFIX CONVERTER (1BCSL306) ================\n");
    printf("Supports: Alphanumeric operands, +, -, *, /, %%, ^ and (), {}, []\n");
    printf("Enter Infix Expression (e.g., ((A + B) * C - D) / E): ");

    if (fgets(infix, sizeof(infix), stdin) == NULL) return 1;
    infix[strcspn(infix, "\r\n")] = '\0';

    if (strlen(infix) == 0) {
        printf("Empty input.\n");
        return 1;
    }

    // Step 1: Validate bracket nesting
    if (!validateBrackets(infix)) {
        printf("\n❌ SYNTAX ERROR: Mismatched or unbalanced brackets detected!\n");
        printf("   Check your (), {}, and [] closures.\n");
        return 1;
    }

    // Step 2: Validate arithmetic syntax
    if (!validateSyntax(infix)) {
        printf("\n❌ SYNTAX ERROR: Invalid expression syntax!\n");
        printf("   Check for consecutive operators or missing operands.\n");
        return 1;
    }

    // Step 3: Convert to postfix
    convertToPostfix(infix, postfix);

    printf("\n✔ Expression validated successfully!");
    printf("\nInfix Expression   : %s", infix);
    printf("\nPostfix Expression : %s\n", postfix);

    return 0;
}

