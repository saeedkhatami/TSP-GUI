# TSP

## explaination

### Line 1-3: Importing Libraries

```python
import itertools
import tkinter as tk
from tkinter import Canvas
```

**Explanation:**
- These lines import necessary libraries:
  - `itertools`: Provides functions for working with iterators, used for generating permutations of cities.
  - `tkinter`: The standard GUI (Graphical User Interface) toolkit in Python.
  - `Canvas`: A class in Tkinter for drawing and displaying graphics.

### Line 5-16: `calculate_total_distance` Function

```python
def calculate_total_distance(path, distances):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distances[path[i]][path[i + 1]]
    total_distance += distances[path[-1]][path[0]]
    return total_distance
```

**Explanation:**
- Defines a function `calculate_total_distance` that computes the total distance of a given path based on a distances matrix.
- `path`: The order of cities to visit.
- `distances`: A matrix representing distances between cities.
- The function iterates through the cities in the path, summing up the distances between consecutive cities, and adding the distance from the last city back to the starting city.
- Returns the total distance.

### Line 18-29: `tsp_bruteforce` Function

```python
def tsp_bruteforce(distances):
    num_cities = len(distances)
    cities = list(range(num_cities))
    all_paths = list(itertools.permutations(cities))

    min_distance = float('inf')
    best_path = None

    for path in all_paths:
        total_distance = calculate_total_distance(path, distances)
        if total_distance < min_distance:
            min_distance = total_distance
            best_path = path

    return best_path, min_distance
```

**Explanation:**
- Defines a function `tsp_bruteforce` that solves the Traveling Salesman Problem using a brute-force approach.
- Generates all possible permutations of cities using `itertools.permutations`.
- Iterates through each permutation, calculates the total distance using `calculate_total_distance`, and updates `min_distance` and `best_path` if a shorter path is found.
- Returns the best path and its corresponding minimum distance.

### Line 31-52: `draw_tsp_solution` Function

```python
def draw_tsp_solution(distances, best_path, canvas, coordinates, direction_canvas):
    canvas.delete("all")
    direction_canvas.delete("all")

    num_cities = len(distances)

    for i in range(num_cities):
        x, y = coordinates[i]
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='blue')
        canvas.create_text(x, y - 10, text=str(i), font=("Helvetica", 10), fill='black')

    for i in range(num_cities - 1):
        canvas.create_line(coordinates[best_path[i]][0], coordinates[best_path[i]][1],
                           coordinates[best_path[i + 1]][0], coordinates[best_path[i + 1]][1], fill='red')

    canvas.create_line(coordinates[best_path[-1]][0], coordinates[best_path[-1]][1],
                       coordinates[best_path[0]][0], coordinates[best_path[0]][1], fill='red')

    canvas.create_text(200, 20, text=f"Total Distance: {calculate_total_distance(best_path, distances)}", font=("Helvetica", 12), fill='black')
```

**Explanation:**
- Defines a function `draw_tsp_solution` to visualize the TSP solution on the canvas.
- Clears the canvas and direction_canvas.
- Draws city circles and labels on the canvas.
- Connects cities in the best path with red lines.
- Displays the total distance at the top of the canvas.

### Line 54-65: `draw_direction_canvas` Function

```python
def draw_direction_canvas(direction_canvas, best_path):
    num_cities = len(best_path)

    for i in range(num_cities - 1):
        direction_canvas.create_text(10, 20 * i + 10, anchor=tk.W, text=f"{best_path[i]} to {best_path[i + 1]}", font=("Helvetica", 10), fill='black')

    direction_canvas.create_text(10, 20 * (num_cities - 1) + 10, anchor=tk.W, text=f"{best_path[-1]} to {best_path[0]}", font=("Helvetica", 10), fill='black')
```

**Explanation:**
- Defines a function `draw_direction_canvas` to visualize the direction of the TSP solution on a separate canvas.
- Creates text on direction_canvas indicating the order of cities in the best path.

### Line 67-77: `solve_tsp_step_by_step` Function

```python
def solve_tsp_step_by_step(distances, all_paths, index, canvas, coordinates, direction_canvas):
    if index < len(all_paths):
        path = all_paths[index]
        draw_tsp_solution(distances, path, canvas, coordinates, direction_canvas)
        draw_direction_canvas(direction_canvas, path)
        canvas.update()
```

**Explanation:**
- Defines a function `solve_tsp_step_by_step` to solve TSP step by step, updating the canvas at each step.
- Checks if there are more paths to explore.
- Draws the current solution and updates the canvas.

### Line 79-89: `solve_tsp_animation` Function

```python
def solve_tsp_animation(distances, all_paths, index, canvas, coordinates, direction_canvas):
    if index < len(all_paths):
        path = all_paths[index]
        draw_tsp_solution(distances, path, canvas, coordinates, direction_canvas)
        draw_direction_canvas(direction_canvas, path)
        canvas.update()
        canvas.after(1000, solve_tsp_animation, distances, all_paths, index + 1, canvas, coordinates, direction_canvas)
```

**Explanation:**
- Defines a function `solve_tsp_animation` to solve TSP with animation, updating the canvas with a delay.
- Checks if there are more paths to explore.
- Draws the current solution and updates the canvas.
- Uses `canvas.after` to schedule the next iteration after a 1000 ms (1 second) delay.

### Line 91-98: `solve_tsp_step` Function

```python
def solve_tsp_step(distances, all_paths, index, canvas, coordinates, direction_canvas):
    if index < len(all_paths):
        path = all_paths[index]
        draw_tsp_solution(distances, path, canvas, coordinates, direction_canvas)
        draw_direction_canvas(direction_canvas, path)
        return index + 1
    return index
```

**Explanation:**
- Defines a function `solve_tsp_step` to solve TSP one step at a time.
- Checks if there are more paths to explore.
- Draws the current solution and updates the canvas.
- Returns the next index.

### Line 100-107: `next_step_callback` Function

```python
def next_step_callback(distances, all_paths, index_var, canvas, coordinates, direction

_canvas):
    index_var.set(solve_tsp_step(distances, all_paths, index_var.get(), canvas, coordinates, direction_canvas))
```

**Explanation:**
- Defines a callback function `next_step_callback` for the "Next Step" button.
- Uses `index_var` to keep track of the current step.
- Calls `solve_tsp_step` to solve the TSP for the next step and updates the index.

### Line 109-115: Data Initialization

```python
coordinates = [
    (50, 50),
    (100, 150),
    (200, 100),
    (150, 200),
    (300, 50),
]

distances = [
    [0, 10, 15, 20, 25],
    [10, 0, 12, 18, 24],
    [15, 12, 0, 8, 16],
    [20, 18, 8, 0, 10],
    [25, 24, 16, 10, 0]
]
```

**Explanation:**
- Initializes data:
  - `coordinates`: The (x, y) coordinates of cities.
  - `distances`: A matrix representing distances between cities.

### Line 117-118: Path Generation and Initial Solution

```python
num_cities = len(distances)
cities = list(range(num_cities))
all_paths = list(itertools.permutations(cities))

best_path, _ = tsp_bruteforce(distances)
```

**Explanation:**
- Computes the number of cities and generates all possible permutations of cities.
- Finds the best path and minimum distance using the `tsp_bruteforce` function.

### Line 120-131: GUI Setup

```python
root = tk.Tk()
root.title("TSP Solver")

canvas = Canvas(root, width=400, height=300)
canvas.pack(side=tk.LEFT)

direction_canvas = Canvas(root, width=50, height=100)
direction_canvas.place(x=320, y=10)

index_var = tk.IntVar(value=1)

solve_button = tk.Button(root, text="Solve TSP", command=lambda: solve_tsp_step(distances, all_paths, 0, canvas, coordinates, direction_canvas))
solve_button.pack()

next_step_button = tk.Button(root, text="Next Step", command=lambda: next_step_callback(distances, all_paths, index_var, canvas, coordinates, direction_canvas))
next_step_button.pack()

root.mainloop()
```

**Explanation:**
- Sets up the Tkinter GUI:
  - Creates the main window (`root`).
  - Creates a canvas for drawing the TSP solution.
  - Creates a separate canvas for displaying the direction.
  - Initializes an index variable (`index_var`) to keep track of the current step.
  - Creates "Solve TSP" and "Next Step" buttons with associated commands.
  - Starts the Tkinter main loop to display the GUI.
