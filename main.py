import itertools
import tkinter as tk
from tkinter import Canvas

def calculate_total_distance(path, distances):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distances[path[i]][path[i + 1]]
    total_distance += distances[path[-1]][path[0]]
    return total_distance

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

def draw_direction_canvas(direction_canvas, best_path):
    num_cities = len(best_path)

    for i in range(num_cities - 1):
        direction_canvas.create_text(10, 20 * i + 10, anchor=tk.W, text=f"{best_path[i]} to {best_path[i + 1]}", font=("Helvetica", 10), fill='black')

    direction_canvas.create_text(10, 20 * (num_cities - 1) + 10, anchor=tk.W, text=f"{best_path[-1]} to {best_path[0]}", font=("Helvetica", 10), fill='black')

def solve_tsp_step_by_step(distances, all_paths, index, canvas, coordinates, direction_canvas):
    if index < len(all_paths):
        path = all_paths[index]
        draw_tsp_solution(distances, path, canvas, coordinates, direction_canvas)
        draw_direction_canvas(direction_canvas, path)
        canvas.update()

def solve_tsp_animation(distances, all_paths, index, canvas, coordinates, direction_canvas):
    if index < len(all_paths):
        path = all_paths[index]
        draw_tsp_solution(distances, path, canvas, coordinates, direction_canvas)
        draw_direction_canvas(direction_canvas, path)
        canvas.update()
        canvas.after(1000, solve_tsp_animation, distances, all_paths, index + 1, canvas, coordinates, direction_canvas)

def solve_tsp_step(distances, all_paths, index, canvas, coordinates, direction_canvas):
    if index < len(all_paths):
        path = all_paths[index]
        draw_tsp_solution(distances, path, canvas, coordinates, direction_canvas)
        draw_direction_canvas(direction_canvas, path)
        return index + 1
    return index

def next_step_callback(distances, all_paths, index_var, canvas, coordinates, direction_canvas):
    index_var.set(solve_tsp_step(distances, all_paths, index_var.get(), canvas, coordinates, direction_canvas))

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

num_cities = len(distances)
cities = list(range(num_cities))
all_paths = list(itertools.permutations(cities))

best_path, _ = tsp_bruteforce(distances)

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
