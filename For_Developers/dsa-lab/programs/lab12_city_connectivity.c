/*
 * ==============================================================================
 * OILS-3: DATA STRUCTURES LABORATORY (VTU 2025 Scheme - 1BCSL306)
 * Experiment 12: City Connectivity Using Graphs and Depth-First Search (DFS)
 * ==============================================================================
 *
 * 🎯 PROBLEM STATEMENT:
 * A transportation department wants to analyse connectivity between cities.
 * Each city has a City Name and cities are interconnected with roads.
 * Develop a menu-driven C program to create a graph representing N cities
 * and roads, display the graph representation, print all cities reachable by
 * road from a given city, and check whether any two given cities are connected.
 *
 * 🧠 KEY CONCEPT & MEMORY LOGIC:
 * - Graph Representation: N x N Adjacency Matrix where adj[u][v] = 1 represents
 *   an undirected road between city u and city v.
 * - Depth-First Search (DFS): Recursive graph traversal using visited array
 *   to explore down each branch before backtracking.
 * - Reachability: If visited[v] == 1 after DFS(u), city v is reachable from u.
 * ==============================================================================
 */

#include <stdio.h>
#include <string.h>

#define MAX_CITIES 50
#define NAME_LEN 50

char cityNames[MAX_CITIES][NAME_LEN];
int adjMatrix[MAX_CITIES][MAX_CITIES];
int visited[MAX_CITIES];
int numCities = 0;

int findCity(const char name[]) {
    for (int i = 0; i < numCities; i++) {
        if (strcmp(cityNames[i], name) == 0) {
            return i;
        }
    }
    return -1;
}

void resetVisited(void) {
    for (int i = 0; i < numCities; i++) {
        visited[i] = 0;
    }
}

/*
 * Block 1: createGraph()
 * Reads city names and roads to construct adjacency matrix.
 */
void createGraph(void) {
    int numRoads;
    char src[NAME_LEN], dest[NAME_LEN];

    printf("\nEnter total number of cities (1 to %d): ", MAX_CITIES);
    if (scanf("%d", &numCities) != 1 || numCities <= 0 || numCities > MAX_CITIES) {
        printf("Invalid number of cities.\n");
        numCities = 0;
        return;
    }

    for (int i = 0; i < numCities; i++) {
        printf("  Enter name of city %d: ", i + 1);
        scanf(" %49[^\n]", cityNames[i]);
    }

    // Initialize adjacency matrix to 0
    for (int i = 0; i < numCities; i++) {
        for (int j = 0; j < numCities; j++) {
            adjMatrix[i][j] = 0;
        }
    }

    printf("\nEnter number of interconnected roads: ");
    scanf("%d", &numRoads);

    for (int i = 0; i < numRoads; i++) {
        printf("  Road %d (Enter starting city): ", i + 1);
        scanf(" %49[^\n]", src);
        printf("  Road %d (Enter destination city): ", i + 1);
        scanf(" %49[^\n]", dest);

        int u = findCity(src);
        int v = findCity(dest);

        if (u == -1 || v == -1) {
            printf("  ❌ Error: One or both city names invalid ('%s' or '%s'). Road skipped!\n", src, dest);
        } else {
            adjMatrix[u][v] = 1;
            adjMatrix[v][u] = 1; // Undirected road
            printf("  ✔ Road between '%s' and '%s' added.\n", src, dest);
        }
    }
    printf("\n✔ Graph created successfully with %d cities and %d roads.\n", numCities, numRoads);
}

/*
 * Block 2: displayGraph()
 * Prints adjacency matrix table.
 */
void displayGraph(void) {
    if (numCities == 0) {
        printf("Graph is empty. Create graph first.\n");
        return;
    }
    printf("\n--- GRAPH ADJACENCY MATRIX ---\n");
    printf("%-15s", "City");
    for (int i = 0; i < numCities; i++) {
        printf("%-12.10s", cityNames[i]);
    }
    printf("\n--------------------------------------------------------------------\n");
    for (int i = 0; i < numCities; i++) {
        printf("%-15.14s", cityNames[i]);
        for (int j = 0; j < numCities; j++) {
            printf("%-12d", adjMatrix[i][j]);
        }
        printf("\n");
    }
}

/*
 * Block 3: dfs()
 * Recursive DFS traversal.
 */
void dfs(int u, int printOutput) {
    visited[u] = 1;
    if (printOutput) {
        printf("  • %s\n", cityNames[u]);
    }
    for (int v = 0; v < numCities; v++) {
        if (adjMatrix[u][v] == 1 && !visited[v]) {
            dfs(v, printOutput);
        }
    }
}

/*
 * Block 4: displayReachableCities()
 */
void displayReachableCities(void) {
    if (numCities == 0) {
        printf("Graph is empty.\n");
        return;
    }
    char startName[NAME_LEN];
    printf("Enter source city name: ");
    scanf(" %49[^\n]", startName);

    int start = findCity(startName);
    if (start == -1) {
        printf("City '%s' not found.\n", startName);
        return;
    }

    resetVisited();
    printf("\nCities reachable by road from '%s':\n", startName);
    dfs(start, 1);
}

/*
 * Block 5: checkConnectivity()
 */
void checkConnectivity(void) {
    if (numCities == 0) {
        printf("Graph is empty.\n");
        return;
    }
    char c1[NAME_LEN], c2[NAME_LEN];
    printf("Enter First City: ");
    scanf(" %49[^\n]", c1);
    printf("Enter Second City: ");
    scanf(" %49[^\n]", c2);

    int u = findCity(c1);
    int v = findCity(c2);

    if (u == -1 || v == -1) {
        printf("❌ Invalid city name entered.\n");
        return;
    }

    resetVisited();
    dfs(u, 0); // Traversal without printing

    if (visited[v]) {
        printf("\n✔ CONNECTED: Road path EXISTS between '%s' and '%s'!\n", c1, c2);
    } else {
        printf("\n❌ DISCONNECTED: NO road path exists between '%s' and '%s'.\n", c1, c2);
    }
}

int main(void) {
    int choice;

    do {
        printf("\n========== CITY CONNECTIVITY GRAPH (1BCSL306) ==========\n");
        printf("1. Create / Recreate Graph (Cities & Roads)\n");
        printf("2. Display Graph Representation (Adjacency Matrix)\n");
        printf("3. Display All Cities Reachable from a Given City (DFS)\n");
        printf("4. Check Connectivity Between Two Cities\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1) break;

        switch (choice) {
            case 1:
                createGraph();
                break;
            case 2:
                displayGraph();
                break;
            case 3:
                displayReachableCities();
                break;
            case 4:
                checkConnectivity();
                break;
            case 5:
                printf("Exiting City Connectivity graph system.\n");
                break;
            default:
                printf("Invalid choice! Choose [1 - 5].\n");
        }
    } while (choice != 5);

    return 0;
}

