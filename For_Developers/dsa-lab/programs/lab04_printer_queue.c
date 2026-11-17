/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 04: Printer Queue Simulation Using an Array
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * Simulate a printer queue. Insert print-job IDs, process the next job,
 * display pending jobs, and detect queue overflow and underflow conditions.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - Queue is a FIFO (First-In, First-Out) data structure.
 * - Front pointer: where elements are deleted (served).
 * - Rear pointer: where elements are inserted (enqueued).
 * - Empty state: front == -1.
 * - Full state:  rear == capacity - 1 (in a linear queue).
 * - Single-element reset: When front == rear during dequeue, the queue becomes
 *   empty and both pointers reset back to -1.
 * ==============================================================================
 */

#include <stdio.h>
#define MAX 100

int queue[MAX];
int front = -1;
int rear = -1;
int capacity = 10;

int isQueueEmpty(void) {
    return front == -1;
}

int isQueueFull(void) {
    return rear == capacity - 1;
}

void initializeQueue(void) {
    front = -1;
    rear = -1;
    printf("✔ Printer queue initialized.\n");
}

/*
 * Block 1: addPrintJob() [Enqueue]
 * Adds a new print job to the rear of the queue.
 */
void addPrintJob(int jobID) {
    if (isQueueFull()) {
        printf("🚨 QUEUE OVERFLOW: Printer queue is full (Capacity = %d)!\n", capacity);
        printf("   Job #%d cannot be added. Wait for pending jobs to finish.\n", jobID);
        return;
    }
    if (isQueueEmpty()) {
        front = 0;
    }
    rear = rear + 1;
    queue[rear] = jobID;
    printf("✔ Print job #%d added to queue at position (Rear = %d).\n", jobID, rear);
}

/*
 * Block 2: processPrintJob() [Dequeue]
 * Serves and removes the job at the front of the queue.
 */
void processPrintJob(void) {
    if (isQueueEmpty()) {
        printf("🚨 QUEUE UNDERFLOW: No pending print jobs to process!\n");
        return;
    }
    int processedJob = queue[front];
    printf("🖨️  Processing and printing job #%d from queue...\n", processedJob);

    if (front == rear) {
        // Queue had only 1 item and is now empty: Reset pointers!
        front = -1;
        rear = -1;
        printf("   (All jobs complete! Queue pointers reset to -1).\n");
    } else {
        front = front + 1;
    }
}

/*
 * Block 3: countPendingJobs()
 * Calculates how many jobs are currently queued.
 */
int countPendingJobs(void) {
    if (isQueueEmpty()) {
        return 0;
    }
    return rear - front + 1;
}

/*
 * Block 4: displayPendingJobs()
 * Renders the queue visually from Front to Rear.
 */
void displayPendingJobs(void) {
    if (isQueueEmpty()) {
        printf("Printer queue is currently EMPTY.\n");
        return;
    }
    printf("\n--- PENDING PRINT JOBS IN QUEUE ---\n");
    printf("[FRONT: %d] --> ", front);
    for (int i = front; i <= rear; i++) {
        printf("[Job #%d]", queue[i]);
        if (i < rear) {
            printf(" -> ");
        }
    }
    printf(" <-- [REAR: %d]\n", rear);
}

/*
 * Block 5: displayQueueStatus()
 * Reports diagnostic telemetry on queue capacity.
 */
void displayQueueStatus(void) {
    printf("\n--- PRINTER QUEUE STATUS ---\n");
    printf("Front Position      : %d\n", front);
    printf("Rear Position       : %d\n", rear);
    printf("Maximum Capacity    : %d\n", capacity);
    printf("Pending Jobs Count  : %d\n", countPendingJobs());
    printf("Available Slots     : %d\n", capacity - countPendingJobs());
    if (isQueueEmpty()) {
        printf("Queue Condition     : EMPTY (Idle)\n");
    } else if (isQueueFull()) {
        printf("Queue Condition     : FULL (Cannot accept new jobs)\n");
    } else {
        printf("Queue Condition     : ACTIVE\n");
    }
}

int main(void) {
    int choice, jobID;

    printf("================ PRINTER QUEUE SIMULATION (1BCSL306) ================\n");
    printf("Enter maximum size of printer queue (1 to %d): ", MAX);
    if (scanf("%d", &capacity) != 1 || capacity <= 0 || capacity > MAX) {
        printf("Invalid input. Defaulting capacity to 10.\n");
        capacity = 10;
    }

    initializeQueue();

    do {
        printf("\n========== PRINTER QUEUE MENU (Capacity: %d) ==========\n", capacity);
        printf("1. Add a Print Job (Enqueue)\n");
        printf("2. Process Next Print Job (Dequeue)\n");
        printf("3. Display Pending Print Jobs\n");
        printf("4. Display Count of Waiting Jobs\n");
        printf("5. Display Queue Status & Diagnostics\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Exiting.\n");
            break;
        }

        switch (choice) {
            case 1:
                printf("Enter Print Job ID (integer): ");
                scanf("%d", &jobID);
                addPrintJob(jobID);
                break;
            case 2:
                processPrintJob();
                break;
            case 3:
                displayPendingJobs();
                break;
            case 4:
                printf("Pending jobs in queue: %d\n", countPendingJobs());
                break;
            case 5:
                displayQueueStatus();
                break;
            case 6:
                printf("Exiting Printer Queue simulator.\n");
                break;
            default:
                printf("Invalid choice! Please choose [1 - 6].\n");
        }
    } while (choice != 6);

    return 0;
}

