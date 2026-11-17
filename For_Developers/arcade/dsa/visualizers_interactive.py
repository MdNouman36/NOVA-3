# pyright: reportMissingImports=false
"""
arcade.dsa.visualizers_interactive — Interactive ASCII Memory & Data Structure Sandboxes.
Preserves the user-driven, step-by-step learning style of commit 237ae62.
"""
import time
try:
    from arcade.core import Color, clear_screen, prompt_input  # type: ignore
    from arcade.session import _record_visualizer_explored  # type: ignore
except (ImportError, ValueError):
    from ..core import Color, clear_screen, prompt_input  # type: ignore
    from ..session import _record_visualizer_explored  # type: ignore


# ==============================================================================
# 1. INTERACTIVE STACK SANDBOX (Lab 03: Stack Operations)
# ==============================================================================

def visualizer_stack():
    _record_visualizer_explored("DSA-V1")
    stack = [10, 25, 42]
    cap = 5
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║   📦 INTERACTIVE STACK MEMORY SANDBOX (Capacity: {cap} Elements)               ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("  Current Call Stack / Array Memory Container:")
        print("       +------------+")
        for i in range(cap - 1, -1, -1):
            if i < len(stack):
                is_top = (i == len(stack) - 1)
                tag = f" {Color.YELLOW}<-- [TOP = {i}]{Color.RESET}" if is_top else ""
                print(f"    [{i}] |  {Color.GREEN}{stack[i]:6d}{Color.RESET}    |{tag}")
            else:
                print(f"    [{i}] |  {Color.DIM}(empty){Color.RESET}   |")
        print("       +------------+\n")

        print(f"  Status: {Color.BOLD}top = {len(stack)-1}{Color.RESET}  |  Count: {len(stack)}/{cap}")
        print(f"  Actions: {Color.YELLOW}[1] Push{Color.RESET}  {Color.RED}[2] Pop{Color.RESET}  {Color.BLUE}[3] Peek{Color.RESET}  {Color.MAGENTA}[4] Reset{Color.RESET}  {Color.DIM}[0] Return{Color.RESET}")
        cmd = prompt_input(f"\n{Color.BOLD}Choose action [1 - 4, 0=Back]: {Color.RESET}").strip()

        if cmd == "1":
            if len(stack) >= cap:
                print(f"\n{Color.RED}{Color.BOLD}🚨 STACK OVERFLOW! Stack is completely full ({cap}/{cap})!{Color.RESET}")
                print(f"  {Color.DIM}Boundary Condition: top == MAX - 1 ({len(stack)-1} == {cap-1}). Cannot push without corrupting memory.{Color.RESET}")
                prompt_input("\nPress Enter to continue...")
            else:
                val = prompt_input("Enter integer to push: ").strip()
                if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                    int_val = int(val)
                    print(f"\n  {Color.YELLOW}Step 1: Check Boundary Condition{Color.RESET}")
                    print(f"          if (top == MAX - 1) -> ({len(stack)-1} == {cap-1}) is FALSE [Safe to insert]")
                    prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                    print(f"\n  {Color.YELLOW}Step 2: Advance Pointer (Pre-increment){Color.RESET}")
                    print(f"          top = top + 1  -> New top index: {len(stack)}")
                    prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                    print(f"\n  {Color.YELLOW}Step 3: Write Memory at Top Index{Color.RESET}")
                    print(f"          stack[top] = {int_val}  -> Stored {int_val} in slot [{len(stack)}]")
                    stack.append(int_val)
                    time.sleep(0.4)
                else:
                    print(f"{Color.RED}Please enter a valid integer!{Color.RESET}")
                    time.sleep(0.8)
        elif cmd == "2":
            if not stack:
                print(f"\n{Color.RED}{Color.BOLD}🚨 STACK UNDERFLOW! Stack is empty.{Color.RESET}")
                print(f"  {Color.DIM}Boundary Condition: top == -1. There are no elements in memory to pop.{Color.RESET}")
                prompt_input("\nPress Enter to continue...")
            else:
                popped = stack[-1]
                curr_top = len(stack) - 1
                print(f"\n  {Color.YELLOW}Step 1: Check Boundary Condition{Color.RESET}")
                print(f"          if (top == -1) -> ({curr_top} == -1) is FALSE [Stack contains items]")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 2: Retrieve Element at Top{Color.RESET}")
                print(f"          item = stack[top]  -> Retrieved value: {Color.GREEN}{popped}{Color.RESET}")
                prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 3: Decrement Pointer (Post-decrement){Color.RESET}")
                print(f"          top = top - 1  -> New top index: {curr_top - 1} (slot [{curr_top}] freed)")
                stack.pop()
                time.sleep(0.4)
        elif cmd == "3":
            if not stack:
                print(f"\n{Color.YELLOW}Stack is empty (top == -1). Nothing to peek.{Color.RESET}")
            else:
                print(f"\n{Color.GREEN}✔ Top element is: {Color.BOLD}{stack[-1]}{Color.RESET}{Color.GREEN} at index [{len(stack)-1}]{Color.RESET}")
                print(f"  {Color.DIM}Peek does not modify 'top' or alter memory — time complexity O(1).{Color.RESET}")
            prompt_input("\nPress Enter to continue...")
        elif cmd == "4":
            stack = []
            print(f"\n{Color.YELLOW}Stack cleared! top is now -1.{Color.RESET}")
            time.sleep(0.6)
        elif cmd in ("0", "b", "exit", "back"):
            break


# ==============================================================================
# 2. INTERACTIVE LINEAR QUEUE SANDBOX (Lab 04: Linear Queue)
# ==============================================================================

def visualizer_linear_queue():
    _record_visualizer_explored("DSA-V2")
    cap = 5
    items = [None] * cap
    items[0] = 10
    items[1] = 20
    front = 0
    rear = 1

    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║   🖨️  INTERACTIVE LINEAR QUEUE SANDBOX (Array Implementation, Cap: {cap})       ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("  Array Memory Slots [0 .. 4]:")
        slot_str = "    "
        for i in range(cap):
            if items[i] is not None and front <= i <= rear and front != -1:
                slot_str += f"|  {Color.GREEN}{items[i]:3d}{Color.RESET}  "
            else:
                slot_str += f"| {Color.DIM}(emp){Color.RESET} "
        slot_str += "|"
        print("    +" + "-------+" * cap)
        print(slot_str)
        print("    +" + "-------+" * cap)

        # Index labels
        idx_str = "       " + "       ".join([f"[{i}]" for i in range(cap)])
        print(idx_str)

        # Pointer markers
        ptr_line = ["       "] * cap
        if front != -1 and front < cap:
            ptr_line[front] = f"{Color.YELLOW} [FRONT]{Color.RESET}"
        if rear != -1 and rear < cap:
            if front == rear and front != -1:
                ptr_line[rear] = f"{Color.CYAN}[F & R]{Color.RESET}"
            else:
                ptr_line[rear] = f"{Color.MAGENTA} [REAR]{Color.RESET}"
        print("   " + "".join([f"{p:<15}" for p in ptr_line]))

        count = (rear - front + 1) if (front != -1 and front <= rear) else 0
        print(f"\n  Status: {Color.BOLD}front = {front}{Color.RESET}, {Color.BOLD}rear = {rear}{Color.RESET}  |  Count: {count}/{cap}")
        if front > 0 and rear == cap - 1:
            print(f"  {Color.RED}⚠️ FALSE OVERFLOW ALERT:{Color.RESET} {front} slot(s) at front are empty, but rear is at MAX-1!")
            print(f"  {Color.DIM}Linear queue cannot reuse freed slots. This is why Circular Queues are used!{Color.RESET}")

        print(f"\n  Actions: {Color.YELLOW}[1] Enqueue{Color.RESET}  {Color.RED}[2] Dequeue{Color.RESET}  {Color.BLUE}[3] Front Element{Color.RESET}  {Color.MAGENTA}[4] Reset{Color.RESET}  {Color.DIM}[0] Return{Color.RESET}")
        cmd = prompt_input(f"\n{Color.BOLD}Choose action [1 - 4, 0=Back]: {Color.RESET}").strip()

        if cmd == "1":
            if rear == cap - 1:
                print(f"\n{Color.RED}{Color.BOLD}🚨 QUEUE OVERFLOW! (rear == MAX - 1){Color.RESET}")
                if front > 0:
                    print(f"  {Color.YELLOW}Note: Even though slots 0 to {front-1} are empty, linear queue rear cannot wrap around!{Color.RESET}")
                prompt_input("\nPress Enter to continue...")
            else:
                val = prompt_input("Enter integer to enqueue: ").strip()
                if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                    int_val = int(val)
                    print(f"\n  {Color.YELLOW}Step 1: Check Boundary Condition{Color.RESET}")
                    print(f"          if (rear == MAX - 1) -> ({rear} == {cap-1}) is FALSE [Safe to insert]")
                    prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                    print(f"\n  {Color.YELLOW}Step 2: Advance Pointer(s){Color.RESET}")
                    if front == -1:
                        front = 0
                        print("          First element: front set to 0")
                    rear += 1
                    print(f"          rear = rear + 1 -> New rear index: {rear}")
                    prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                    print(f"\n  {Color.YELLOW}Step 3: Write Memory at Rear{Color.RESET}")
                    print(f"          queue[rear] = {int_val} -> Written to slot [{rear}]")
                    items[rear] = int_val
                    time.sleep(0.4)
                else:
                    print(f"{Color.RED}Please enter a valid integer!{Color.RESET}")
                    time.sleep(0.8)
        elif cmd == "2":
            if front == -1 or front > rear:
                print(f"\n{Color.RED}{Color.BOLD}🚨 QUEUE UNDERFLOW! Queue is empty.{Color.RESET}")
                print(f"  {Color.DIM}Boundary Condition: front == -1 or front > rear. No elements to remove.{Color.RESET}")
                prompt_input("\nPress Enter to continue...")
            else:
                removed = items[front]
                print(f"\n  {Color.YELLOW}Step 1: Check Boundary Condition{Color.RESET}")
                print("          if (front == -1 || front > rear) is FALSE [Queue has items]")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 2: Retrieve Element at Front{Color.RESET}")
                print(f"          item = queue[front] -> Retrieved value: {Color.GREEN}{removed}{Color.RESET}")
                prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 3: Advance Front Pointer{Color.RESET}")
                items[front] = None
                front += 1
                if front > rear:
                    print(f"          front ({front}) > rear ({rear}) -> Queue exhausted! Resetting front = rear = -1")
                    front = -1
                    rear = -1
                else:
                    print(f"          front = front + 1 -> New front index: {front}")
                time.sleep(0.4)
        elif cmd == "3":
            if front == -1 or front > rear:
                print(f"\n{Color.YELLOW}Queue is empty. No front element.{Color.RESET}")
            else:
                print(f"\n{Color.GREEN}✔ Front element is: {Color.BOLD}{items[front]}{Color.RESET}{Color.GREEN} at slot [{front}]{Color.RESET}")
            prompt_input("\nPress Enter to continue...")
        elif cmd == "4":
            items = [None] * cap
            front = -1
            rear = -1
            print(f"\n{Color.YELLOW}Linear queue reset to empty!{Color.RESET}")
            time.sleep(0.6)
        elif cmd in ("0", "b", "exit", "back"):
            break


# ==============================================================================
# 3. INTERACTIVE CIRCULAR QUEUE SANDBOX (Lab 04: Modulo Ring Buffer)
# ==============================================================================

def visualizer_circular_queue():
    _record_visualizer_explored("DSA-V3")
    cap = 5
    items = [None] * cap
    items[3] = 10
    items[4] = 20
    items[0] = 30
    front = 3
    rear = 0

    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║   🔄 INTERACTIVE CIRCULAR QUEUE (Ring Buffer with Modulo Arithmetic, Cap: {cap})║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")

        print("  Physical Array Slots [0 .. 4]:")
        slot_str = "    "
        for i in range(cap):
            val = items[i]
            if val is not None:
                slot_str += f"|  {Color.GREEN}{val:3d}{Color.RESET}  "
            else:
                slot_str += f"| {Color.DIM}(emp){Color.RESET} "
        slot_str += "|"
        print("    +" + "-------+" * cap)
        print(slot_str)
        print("    +" + "-------+" * cap)

        # Index labels & tags
        idx_labels = []
        for i in range(cap):
            tags = []
            if i == front and front != -1:
                tags.append("F")
            if i == rear and rear != -1:
                tags.append("R")
            tag_str = f"[{','.join(tags)}]" if tags else f"[{i}]"
            idx_labels.append(f"{tag_str:^7}")
        print("    " + "".join(idx_labels))

        print(f"\n  State: {Color.BOLD}front = {front}{Color.RESET}, {Color.BOLD}rear = {rear}{Color.RESET}  |  Next rear would be: {Color.YELLOW}(rear + 1) % {cap} = {(rear + 1) % cap if rear != -1 else 0}{Color.RESET}")
        print(f"  {Color.CYAN}💡 Ring Rule: Modulo (%) wraps indices cleanly: Slot 4 -> Slot 0 seamlessly!{Color.RESET}")

        print(f"\n  Actions: {Color.YELLOW}[1] Enqueue{Color.RESET}  {Color.RED}[2] Dequeue{Color.RESET}  {Color.MAGENTA}[3] Reset{Color.RESET}  {Color.DIM}[0] Return{Color.RESET}")
        cmd = prompt_input(f"\n{Color.BOLD}Choose action [1 - 3, 0=Back]: {Color.RESET}").strip()

        if cmd == "1":
            next_rear = (rear + 1) % cap if rear != -1 else 0
            if front != -1 and next_rear == front:
                print(f"\n{Color.RED}{Color.BOLD}🚨 CIRCULAR QUEUE OVERFLOW! (rear wraps to front){Color.RESET}")
                print(f"  {Color.DIM}Check: (rear + 1) % MAX == front -> ({rear} + 1) % {cap} == {front} is TRUE. Queue is full!{Color.RESET}")
                prompt_input("\nPress Enter to continue...")
            else:
                val = prompt_input("Enter integer to enqueue: ").strip()
                if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                    int_val = int(val)
                    print(f"\n  {Color.YELLOW}Step 1: Calculate Next Position with Modulo{Color.RESET}")
                    print(f"          next_rear = (rear + 1) % MAX -> ({rear} + 1) % {cap} = {next_rear}")
                    prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                    print(f"\n  {Color.YELLOW}Step 2: Update Pointers{Color.RESET}")
                    if front == -1:
                        front = 0
                        rear = 0
                        print("          Queue was empty -> front = 0, rear = 0")
                    else:
                        rear = next_rear
                        print(f"          rear updated to index [{rear}]")
                    prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                    print(f"\n  {Color.YELLOW}Step 3: Write Memory at Wrapped Rear{Color.RESET}")
                    print(f"          queue[rear] = {int_val} -> Stored in slot [{rear}]")
                    items[rear] = int_val
                    time.sleep(0.4)
                else:
                    print(f"{Color.RED}Please enter a valid integer!{Color.RESET}")
                    time.sleep(0.8)
        elif cmd == "2":
            if front == -1:
                print(f"\n{Color.RED}{Color.BOLD}🚨 CIRCULAR QUEUE UNDERFLOW! (front == -1){Color.RESET}")
                print(f"  {Color.DIM}The queue contains no elements.{Color.RESET}")
                prompt_input("\nPress Enter to continue...")
            else:
                removed = items[front]
                print(f"\n  {Color.YELLOW}Step 1: Retrieve Data at Front{Color.RESET}")
                print(f"          item = queue[front] -> Retrieved: {Color.GREEN}{removed}{Color.RESET} from slot [{front}]")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 2: Advance Front with Modulo Arithmetic{Color.RESET}")
                items[front] = None
                if front == rear:
                    print(f"          front == rear ({front} == {rear}) -> Last element consumed! Resetting front = rear = -1")
                    front = -1
                    rear = -1
                else:
                    new_front = (front + 1) % cap
                    print(f"          front = (front + 1) % MAX -> ({front} + 1) % {cap} = {new_front}")
                    front = new_front
                time.sleep(0.4)
        elif cmd == "3":
            items = [None] * cap
            front = -1
            rear = -1
            print(f"\n{Color.YELLOW}Circular queue reset to empty!{Color.RESET}")
            time.sleep(0.6)
        elif cmd in ("0", "b", "exit", "back"):
            break


# ==============================================================================
# 4. INTERACTIVE SINGLY LINKED LIST SANDBOX (Lab 08: Student SLL)
# ==============================================================================

def visualizer_singly_linked_list():
    _record_visualizer_explored("DSA-V4")
    nodes = [10, 25, 42]
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║   🔗 INTERACTIVE SINGLY LINKED LIST SANDBOX (Dynamic Heap Node Pointers)     ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print("  Memory Pointer Chain (Heap Nodes):")
        if not nodes:
            print(f"    {Color.YELLOW}[HEAD]{Color.RESET} ───> {Color.RED}NULL{Color.RESET}  (Empty List)\n")
        else:
            chain = f"    {Color.YELLOW}[HEAD]{Color.RESET} ───> "
            for idx, val in enumerate(nodes):
                chain += f"[{Color.GREEN}{val:2d}{Color.RESET} | •] ───> "
            chain += f"{Color.RED}NULL{Color.RESET}"
            print(chain)
            sub_labels = "            " + "         ".join([f"Node #{i+1}" for i in range(len(nodes))])
            print(f"{Color.DIM}{sub_labels}{Color.RESET}\n")

        print(f"  List Length: {Color.BOLD}{len(nodes)} Node(s){Color.RESET}")
        print(f"  Actions: {Color.YELLOW}[1] Insert Front{Color.RESET}  {Color.GREEN}[2] Insert End{Color.RESET}  {Color.RED}[3] Delete Front{Color.RESET}  {Color.RED}[4] Delete End{Color.RESET}  {Color.BLUE}[5] Search{Color.RESET}  {Color.DIM}[0] Return{Color.RESET}")
        cmd = prompt_input(f"\n{Color.BOLD}Choose action [1 - 5, 0=Back]: {Color.RESET}").strip()

        if cmd == "1":
            val = prompt_input("Enter integer for new node: ").strip()
            if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                int_val = int(val)
                print(f"\n  {Color.YELLOW}Step 1: Allocate Node on Heap & Set Data{Color.RESET}")
                print("          new_node = (Node *)malloc(sizeof(Node));")
                print(f"          new_node->data = {int_val};")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 2: Connect New Node's Next Pointer to Current Head{Color.RESET}")
                print("          new_node->next = HEAD;  (links new node to previous first node)")
                prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 3: Update HEAD Pointer to New Node{Color.RESET}")
                print("          HEAD = new_node;        (new node is now the list starting point)")
                nodes.insert(0, int_val)
                time.sleep(0.4)
            else:
                print(f"{Color.RED}Please enter a valid integer!{Color.RESET}")
                time.sleep(0.8)
        elif cmd == "2":
            val = prompt_input("Enter integer for new node: ").strip()
            if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                int_val = int(val)
                print(f"\n  {Color.YELLOW}Step 1: Allocate Heap Node & Set Tail Next to NULL{Color.RESET}")
                print("          new_node = (Node *)malloc(sizeof(Node));")
                print(f"          new_node->data = {int_val}; new_node->next = NULL;")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                if not nodes:
                    print(f"\n  {Color.YELLOW}Step 2: List was empty -> Set HEAD = new_node{Color.RESET}")
                else:
                    print(f"\n  {Color.YELLOW}Step 2: Traverse from HEAD until Last Node{Color.RESET}")
                    print("          temp = HEAD; while (temp->next != NULL) temp = temp->next;")
                    prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                    print(f"\n  {Color.YELLOW}Step 3: Attach New Node to Tail{Color.RESET}")
                    print("          temp->next = new_node; (previous tail now points to new node)")
                nodes.append(int_val)
                time.sleep(0.4)
            else:
                print(f"{Color.RED}Please enter a valid integer!{Color.RESET}")
                time.sleep(0.8)
        elif cmd == "3":
            if not nodes:
                print(f"\n{Color.RED}List is empty. Nothing to delete!{Color.RESET}")
                time.sleep(0.8)
            else:
                removed = nodes[0]
                print(f"\n  {Color.YELLOW}Step 1: Save Target Pointer to Free Later{Color.RESET}")
                print(f"          temp = HEAD;  (holds memory address of node with data {removed})")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 2: Advance HEAD Pointer{Color.RESET}")
                print("          HEAD = HEAD->next;  (second node becomes the new HEAD)")
                prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 3: Reclaim Heap Memory{Color.RESET}")
                print("          free(temp);  (releases heap memory to prevent memory leaks!)")
                nodes.pop(0)
                time.sleep(0.4)
        elif cmd == "4":
            if not nodes:
                print(f"\n{Color.RED}List is empty. Nothing to delete!{Color.RESET}")
                time.sleep(0.8)
            elif len(nodes) == 1:
                removed = nodes.pop(0)
                print(f"\n  {Color.YELLOW}Single node list:{Color.RESET} free(HEAD); HEAD = NULL; (deleted {removed})")
                time.sleep(0.4)
            else:
                removed = nodes[-1]
                print(f"\n  {Color.YELLOW}Step 1: Traverse to Second-to-Last Node{Color.RESET}")
                print("          temp = HEAD; while (temp->next->next != NULL) temp = temp->next;")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 2: Free Last Node Memory{Color.RESET}")
                print(f"          free(temp->next);  (deallocated tail node holding {removed})")
                prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 3: Terminate List with NULL{Color.RESET}")
                print("          temp->next = NULL; (new tail now properly points to NULL)")
                nodes.pop()
                time.sleep(0.4)
        elif cmd == "5":
            if not nodes:
                print(f"\n{Color.YELLOW}List is empty.{Color.RESET}")
                prompt_input("Press Enter to continue...")
            else:
                key = prompt_input("Enter value to search for: ").strip()
                if key.isdigit() or (key.startswith("-") and key[1:].isdigit()):
                    k_val = int(key)
                    print(f"\n  {Color.CYAN}Traversing list pointer by pointer from HEAD...{Color.RESET}")
                    found = False
                    for idx, val in enumerate(nodes):
                        print(f"    Inspecting Node #{idx+1}: value is {val} ... {'MATCH! ✔' if val == k_val else 'No match'}")
                        time.sleep(0.3)
                        if val == k_val:
                            found = True
                            print(f"\n  {Color.GREEN}✔ Found key {k_val} at position {idx+1} (index {idx})!{Color.RESET}")
                            break
                    if not found:
                        print(f"\n  {Color.RED}Reached NULL without finding key {k_val}.{Color.RESET}")
                    prompt_input("\nPress Enter to continue...")
        elif cmd in ("0", "b", "exit", "back"):
            break


# ==============================================================================
# 5. INTERACTIVE CIRCULAR LINKED LIST SANDBOX (Lab 05: Polynomial Addition)
# ==============================================================================

def visualizer_circular_linked_list():
    _record_visualizer_explored("DSA-V5")
    terms = [(8, 3), (4, 2), (2, 0)]  # (coeff, exp)
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║   ⭕ CIRCULAR LINKED LIST WITH HEADER NODE (Lab 05: Polynomial Addition)     ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")

        print("  Polynomial Expression:  " + " + ".join([f"{c}x^{e}" for c, e in terms]))
        print("\n  Circular Pointer Architecture:")
        print("    [HEADER (exp: -1)] ──> ", end="")
        for c, e in terms:
            print(f"[{c}x^{e} | •] ──> ", end="")
        print("\n    ▲                                                        │")
        print("    └────────────────── (Loops Back to Header) ──────────────┘\n")

        print(f"  {Color.CYAN}💡 Examiner Secret:{Color.RESET} The header node has a dummy exponent (-1).")
        print("     This eliminates NULL pointer checks! Traversal simply continues `while (p != header)`.\n")

        print(f"  Actions: {Color.YELLOW}[1] Insert Term{Color.RESET}  {Color.GREEN}[2] Step-by-Step Poly Addition Algorithm{Color.RESET}  {Color.DIM}[0] Return{Color.RESET}")
        cmd = prompt_input(f"\n{Color.BOLD}Choose action [1 - 2, 0=Back]: {Color.RESET}").strip()

        if cmd == "1":
            c_str = prompt_input("Enter coefficient: ").strip()
            e_str = prompt_input("Enter exponent (>= 0): ").strip()
            if (c_str.isdigit() or (c_str.startswith("-") and c_str[1:].isdigit())) and e_str.isdigit():
                c_val = int(c_str)
                e_val = int(e_str)
                print(f"\n  {Color.YELLOW}Step 1: Allocate Term Node{Color.RESET}")
                print(f"          new_node->coeff = {c_val}; new_node->exp = {e_val};")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 2: Traverse while p->next != header && p->next->exp > {e_val}{Color.RESET}")
                prompt_input(f"  {Color.DIM}Press Enter for Step 3...{Color.RESET}")
                print(f"\n  {Color.YELLOW}Step 3: Wire Circular Pointers In-Place{Color.RESET}")
                print("          new_node->next = p->next; p->next = new_node;")
                terms.append((c_val, e_val))
                terms.sort(key=lambda t: t[1], reverse=True)
                time.sleep(0.4)
        elif cmd == "2":
            clear_screen()
            print(f"\n{Color.CYAN}{Color.BOLD}🎓 3-CASE POLYNOMIAL ADDITION ALGORITHM TRACE:{Color.RESET}\n")
            print("  Poly 1 (P1):  5x^3 + 4x^2 + 2x^0")
            print("  Poly 2 (P2):  3x^3 + 6x^1 + 1x^0\n")
            print("  Pointer traversal comparison loop:\n")
            print(f"  {Color.YELLOW}Case 1: P1->exp == P2->exp  (both exponents are 3){Color.RESET}")
            print("          Add coefficients: 5 + 3 = 8 -> Store term 8x^3 in Result List.")
            print("          Advance BOTH P1 and P2 pointers!\n")
            prompt_input(f"  {Color.DIM}Press Enter for next step...{Color.RESET}\n")

            print(f"  {Color.GREEN}Case 2: P1->exp > P2->exp   (P1 has exp 2, P2 has exp 1){Color.RESET}")
            print("          P1 term has higher degree -> Copy term 4x^2 into Result List.")
            print("          Advance ONLY P1 pointer!\n")
            prompt_input(f"  {Color.DIM}Press Enter for next step...{Color.RESET}\n")

            print(f"  {Color.MAGENTA}Case 3: P1->exp < P2->exp   (P1 has exp 0, P2 has exp 1){Color.RESET}")
            print("          P2 term has higher degree -> Copy term 6x^1 into Result List.")
            print("          Advance ONLY P2 pointer!\n")
            prompt_input(f"  {Color.DIM}Press Enter for final conclusion...{Color.RESET}\n")

            print(f"  {Color.CYAN}Terminating Condition:{Color.RESET}")
            print("  Loop terminates when BOTH P1 reaches header1 AND P2 reaches header2!")
            print(f"  Final Sum: {Color.BOLD}8x^3 + 4x^2 + 6x^1 + 3x^0{Color.RESET}\n")
            prompt_input("Press Enter to return...")
        elif cmd in ("0", "b", "exit", "back"):
            break


# ==============================================================================
# 6. INTERACTIVE BINARY SEARCH TREE SANDBOX (Lab 10: Numeric BST)
# ==============================================================================

def visualizer_bst():
    _record_visualizer_explored("DSA-V6")
    keys = [50, 30, 70, 20, 40]
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║   🌳 INTERACTIVE BINARY SEARCH TREE SANDBOX (Lab 10: Numeric BST)            ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")

        print("  Current Keys in Tree: " + ", ".join(map(str, keys)))
        print("\n  ASCII Tree Structure:")
        print("              [50] <--- (Root)")
        print("             /    \\")
        print("          [30]    [70]")
        print("          /  \\")
        print("       [20]  [40]\n")
        print(f"  {Color.CYAN}BST Invariant: Left Subtree < Root < Right Subtree{Color.RESET}\n")

        print(f"  Actions: {Color.YELLOW}[1] Trace Insertion of New Key{Color.RESET}  {Color.GREEN}[2] Inorder Traversal (Sorted Output){Color.RESET}  {Color.BLUE}[3] Search Key{Color.RESET}  {Color.DIM}[0] Return{Color.RESET}")
        cmd = prompt_input(f"\n{Color.BOLD}Choose action [1 - 3, 0=Back]: {Color.RESET}").strip()

        if cmd == "1":
            val = prompt_input("Enter integer key to insert into BST: ").strip()
            if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                k_val = int(val)
                print(f"\n  {Color.YELLOW}Trace: Inserting key {k_val} starting at Root (50):{Color.RESET}")
                if k_val < 50:
                    print(f"    • {k_val} < 50  ──> Move LEFT to Node (30)")
                    if k_val < 30:
                        print(f"    • {k_val} < 30  ──> Move LEFT to Node (20)")
                        if k_val < 20:
                            print(f"    • {k_val} < 20  ──> Left child is NULL -> Attach {k_val} as Left Child of 20!")
                        elif k_val > 20:
                            print(f"    • {k_val} > 20  ──> Right child is NULL -> Attach {k_val} as Right Child of 20!")
                        else:
                            print(f"    • {k_val} == 20 ──> Duplicate key! BST ignores duplicates.")
                    elif k_val > 30:
                        print(f"    • {k_val} > 30  ──> Move RIGHT to Node (40)")
                        if k_val < 40:
                            print(f"    • {k_val} < 40  ──> Attach {k_val} as Left Child of 40!")
                        elif k_val > 40:
                            print(f"    • {k_val} > 40  ──> Attach {k_val} as Right Child of 40!")
                        else:
                            print(f"    • {k_val} == 40 ──> Duplicate key!")
                    else:
                        print(f"    • {k_val} == 30 ──> Duplicate key!")
                elif k_val > 50:
                    print(f"    • {k_val} > 50  ──> Move RIGHT to Node (70)")
                    if k_val < 70:
                        print(f"    • {k_val} < 70  ──> Left child is NULL -> Attach {k_val} as Left Child of 70!")
                    elif k_val > 70:
                        print(f"    • {k_val} > 70  ──> Right child is NULL -> Attach {k_val} as Right Child of 70!")
                    else:
                        print(f"    • {k_val} == 70 ──> Duplicate key!")
                else:
                    print(f"    • {k_val} == 50 ──> Root duplicate!")

                if k_val not in keys:
                    keys.append(k_val)
                prompt_input("\nPress Enter to continue...")
        elif cmd == "2":
            sorted_k = sorted(keys)
            print(f"\n  {Color.GREEN}{Color.BOLD}Inorder Traversal Algorithm: (Left -> Root -> Right){Color.RESET}")
            print("  Trace: Recursively visit Left Subtree, print Root Data, recursively visit Right Subtree.")
            print(f"  Sorted Sequence: {Color.BOLD}{Color.YELLOW}{' -> '.join(map(str, sorted_k))}{Color.RESET}")
            print(f"  {Color.DIM}Notice: Inorder traversal of a BST ALWAYS yields sorted ascending output!{Color.RESET}")
            prompt_input("\nPress Enter to continue...")
        elif cmd == "3":
            val = prompt_input("Enter key to search: ").strip()
            if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                k_val = int(val)
                print(f"\n  {Color.CYAN}Binary Search trace for key {k_val}:{Color.RESET}")
                curr = 50
                steps = 1
                while True:
                    print(f"    Step {steps}: Compare {k_val} with Node ({curr})")
                    if k_val == curr:
                        print(f"    {Color.GREEN}✔ FOUND key {k_val} in {steps} step(s)! Complexity: O(log N){Color.RESET}")
                        break
                    elif k_val < curr:
                        print(f"      {k_val} < {curr} -> Branching LEFT")
                        if curr == 50:
                            curr = 30
                        elif curr == 30:
                            curr = 20
                        else:
                            print(f"    {Color.RED}Reached leaf/NULL. Key {k_val} NOT FOUND in tree.{Color.RESET}")
                            break
                    else:
                        print(f"      {k_val} > {curr} -> Branching RIGHT")
                        if curr == 50:
                            curr = 70
                        elif curr == 30:
                            curr = 40
                        else:
                            print(f"    {Color.RED}Reached leaf/NULL. Key {k_val} NOT FOUND in tree.{Color.RESET}")
                            break
                    steps += 1
                prompt_input("\nPress Enter to continue...")
        elif cmd in ("0", "b", "exit", "back"):
            break


# ==============================================================================
# 7. INTERACTIVE HASH TABLE SANDBOX (Lab 09 & 11: Linear Probing)
# ==============================================================================

def visualizer_hash_table():
    _record_visualizer_explored("DSA-V7")
    size = 7
    table = [None] * size
    # initial sample items
    table[0] = 14  # 14 % 7 = 0
    table[1] = 21  # 21 % 7 = 0 -> Collided at [0], probed to [1]
    table[3] = 10  # 10 % 7 = 3

    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║   🗄️  INTERACTIVE HASH TABLE (Size: {size}, Hash Function: key % {size}, Probing) ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")

        print(f"  Bucket Array [0 .. {size-1}]:")
        for i in range(size):
            if table[i] is not None:
                orig = table[i] % size
                coll = f" {Color.YELLOW}(Collided from [{orig}])" if orig != i else ""
                print(f"    [{i}] |  {Color.GREEN}{table[i]:4d}{Color.RESET}  |{coll}")
            else:
                print(f"    [{i}] |  {Color.DIM}(empty){Color.RESET} |")

        print(f"\n  Actions: {Color.YELLOW}[1] Insert Key{Color.RESET}  {Color.BLUE}[2] Search Key{Color.RESET}  {Color.MAGENTA}[3] Reset{Color.RESET}  {Color.DIM}[0] Return{Color.RESET}")
        cmd = prompt_input(f"\n{Color.BOLD}Choose action [1 - 3, 0=Back]: {Color.RESET}").strip()

        if cmd == "1":
            val = prompt_input("Enter integer key to insert: ").strip()
            if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                k_val = int(val)
                h = k_val % size
                print(f"\n  {Color.YELLOW}Step 1: Compute Home Bucket Index{Color.RESET}")
                print(f"          hash_index = key % SIZE -> {k_val} % {size} = [{h}]")
                prompt_input(f"  {Color.DIM}Press Enter for Step 2 (Collision Resolution)...{Color.RESET}")

                curr = h
                probes = 0
                inserted = False
                while probes < size:
                    if table[curr] is None:
                        print(f"    Slot [{curr}] is EMPTY! Writing key {k_val} here.")
                        table[curr] = k_val
                        inserted = True
                        break
                    else:
                        print(f"    {Color.RED}Collision at slot [{curr}]! (Occupied by {table[curr]}){Color.RESET}")
                        curr = (curr + 1) % size
                        print(f"    Probing next slot: ({curr-1 if curr>0 else size-1} + 1) % {size} = [{curr}]")
                        probes += 1
                        time.sleep(0.3)

                if not inserted:
                    print(f"\n  {Color.RED}🚨 HASH TABLE FULL! Cannot insert key {k_val}.{Color.RESET}")
                prompt_input("\nPress Enter to continue...")
        elif cmd == "2":
            val = prompt_input("Enter key to search: ").strip()
            if val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                k_val = int(val)
                h = k_val % size
                print(f"\n  {Color.CYAN}Searching for key {k_val} (Start at home bucket [{h}]):{Color.RESET}")
                curr = h
                probes = 0
                found = False
                while probes < size:
                    print(f"    Probing slot [{curr}]: contains {table[curr] if table[curr] is not None else 'EMPTY'}")
                    time.sleep(0.3)
                    if table[curr] == k_val:
                        found = True
                        print(f"\n  {Color.GREEN}✔ Found key {k_val} at slot [{curr}] after {probes+1} probe(s)!{Color.RESET}")
                        break
                    elif table[curr] is None:
                        print(f"    Hit EMPTY slot. By linear probing rules, key {k_val} is NOT in table.")
                        break
                    curr = (curr + 1) % size
                    probes += 1

                if not found and table[curr] is not None and probes == size:
                    print(f"    Searched entire table. Key {k_val} NOT FOUND.")
                prompt_input("\nPress Enter to continue...")
        elif cmd == "3":
            table = [None] * size
            print(f"\n{Color.YELLOW}Hash table cleared!{Color.RESET}")
            time.sleep(0.6)
        elif cmd in ("0", "b", "exit", "back"):
            break


# ==============================================================================
# MASTER VISUALIZER MENU FOR DSA STUDIO
# ==============================================================================

def mode_dsa_visualizers_menu():
    """Menu presenting all interactive ASCII data structure sandboxes."""
    while True:
        clear_screen()
        print(f"\n{Color.CYAN}{Color.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║   📦 INTERACTIVE DATA STRUCTURE SANDBOX SUITE (VTU Lab Experiments)          ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Color.RESET}\n")
        print(f"  {Color.YELLOW}[1]{Color.RESET} 📦  Stack Memory Sandbox (Push, Pop, Peek, Overflow & Underflow Traces)")
        print(f"  {Color.YELLOW}[2]{Color.RESET} 🖨️   Linear Queue Sandbox (Front/Rear Pointers, False Overflow Demonstration)")
        print(f"  {Color.YELLOW}[3]{Color.RESET} 🔄  Circular Queue Ring Buffer Sandbox (Modulo Wrap-Around & Bounds)")
        print(f"  {Color.YELLOW}[4]{Color.RESET} 🔗  Singly Linked List Sandbox (Heap Nodes, Insert/Delete Front & End)")
        print(f"  {Color.YELLOW}[5]{Color.RESET} ⭕  Circular Linked List with Header Node Sandbox (Polynomial Addition Trace)")
        print(f"  {Color.YELLOW}[6]{Color.RESET} 🌳  Binary Search Tree Sandbox (Insertion, Left/Right Branches, Inorder Sort)")
        print(f"  {Color.YELLOW}[7]{Color.RESET} 🗄️   Hash Table & Linear Probing Sandbox (Modulo Hashing & Collision Trace)")
        print(f"\n  {Color.DIM}[0]   ⬅️  Back to DSA Lab Studio{Color.RESET}\n")

        ch = prompt_input(f"{Color.BOLD}Choose Sandbox [1 - 7, 0=Back]: {Color.RESET}").strip()
        if ch in ("0", "B", "BACK", "EXIT"):
            return
        elif ch == "1":
            visualizer_stack()
        elif ch == "2":
            visualizer_linear_queue()
        elif ch == "3":
            visualizer_circular_queue()
        elif ch == "4":
            visualizer_singly_linked_list()
        elif ch == "5":
            visualizer_circular_linked_list()
        elif ch == "6":
            visualizer_bst()
        elif ch == "7":
            visualizer_hash_table()

