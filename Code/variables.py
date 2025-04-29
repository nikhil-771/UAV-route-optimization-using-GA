import os
import csv

waypoints = []

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'waypoints.csv')

with open(file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        lat, lon = map(float, row)
        waypoints.append((lat, lon))
        

gen_num = 500
pop_size = 100
mutation_rate = 0.1
elitism_ratio = 0.2
crossover_rate = 0.9
max_stall = 50
