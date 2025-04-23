import random
import numpy as np
from variables import waypoints, gen_num, pop_size, mutation_rate, elitism_ratio, crossover_rate, max_stall
from helper_functions import haversine

class GeneticAlgorithm:
    def __init__(self):
        self.start_point = waypoints[0]
        self.end_point = waypoints[-1]
        self.mid_points = waypoints[1:-1]
        self.population = []
        self.best_distance = float('inf')
        self.best_route = []
        self.final_best_route = []
        self.progress = []
        self.avg_fitness = []
        self.population_diversity = []
        self.generation_stats = []
        self.stall_counter = 0  # Track generations without improvement

    def initialize_population(self):
        """Create initial population of routes"""
        self.population = []
        for _ in range(pop_size):
            individual = self.mid_points.copy()
            random.shuffle(individual)
            self.population.append(individual)

    def calculate_distance(self, route):
        """Calculate total distance of a route including fixed start and end"""
        full_route = [self.start_point] + route + [self.end_point]
        total_distance = 0
        for i in range(len(full_route)-1):
            total_distance += haversine(full_route[i], full_route[i+1])
        return total_distance

    def fitness(self, route):
        """Fitness is inverse of distance (we want to minimize distance)"""
        return 1 / (self.calculate_distance(route) + 1e-6)

    def rank_routes(self):
        """Rank routes based on fitness"""
        fitness_results = {}
        for i in range(len(self.population)):
            fitness_results[i] = self.fitness(self.population[i])
        return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)

    def selection(self, ranked_routes):
        """Select parents using tournament selection"""
        selection_results = []
        
        # Elitism
        elitism_num = int(elitism_ratio * pop_size)
        for i in range(elitism_num):
            selection_results.append(ranked_routes[i][0])
        
        # Tournament selection
        for _ in range(pop_size - elitism_num):
            tournament = random.sample(ranked_routes, min(5, len(ranked_routes)))
            winner = max(tournament, key=lambda x: x[1])
            selection_results.append(winner[0])
        
        return selection_results

    def crossover(self, parent1, parent2):
        """Ordered crossover (OX)"""
        if random.random() > crossover_rate:
            return parent1.copy()
        
        size = len(parent1)
        child = [None] * size
        
        # Create crossover points
        start, end = sorted(random.sample(range(size), 2))
        child[start:end] = parent1[start:end]
        
        # Fill remaining genes
        current_pos = end % size
        parent_pos = end % size
        
        while None in child:
            if parent2[parent_pos] not in child:
                child[current_pos] = parent2[parent_pos]
                current_pos = (current_pos + 1) % size
            parent_pos = (parent_pos + 1) % size
        
        return child

    def mutate(self, individual):
        """Swap mutation"""
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(individual)), 2)
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
        return individual

    def calculate_population_diversity(self):
        """Calculate population diversity"""
        unique_routes = set(tuple(route) for route in self.population)
        return len(unique_routes) / pop_size

    def evolve_population(self):
        """Create next generation"""
        ranked_routes = self.rank_routes()
        selection_indices = self.selection(ranked_routes)
        
        # Track best individual
        best_idx = ranked_routes[0][0]
        current_best_distance = self.calculate_distance(self.population[best_idx])
        
        # Update best solution if improved
        if current_best_distance < self.best_distance:
            self.best_distance = current_best_distance
            self.best_route = self.population[best_idx].copy()
            self.stall_counter = 0  # Reset counter on improvement
        else:
            self.stall_counter += 1  # Increment counter if no improvement
        
        # Store statistics
        self.progress.append(self.best_distance)
        self.avg_fitness.append(np.mean([self.fitness(route) for route in self.population]))
        self.population_diversity.append(self.calculate_population_diversity())
        self.generation_stats.append({
            'best': self.best_distance,
            'worst': max(self.calculate_distance(route) for route in self.population),
            'average': np.mean([self.calculate_distance(route) for route in self.population])
        })
        
        # Create new population
        new_population = []
        
        # Preserve elites
        for i in range(int(elitism_ratio * pop_size)):
            new_population.append(self.population[selection_indices[i]].copy())
        
        # Generate offspring
        while len(new_population) < pop_size:
            parent1 = self.population[random.choice(selection_indices)]
            parent2 = self.population[random.choice(selection_indices)]
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)
        
        self.population = new_population

    def run(self):
        """Run the algorithm with early stopping"""
        self.initialize_population()
        
        for gen in range(gen_num):
            self.evolve_population()
            
            # Early stopping check
            if self.stall_counter >= max_stall:
                print(f"\nEarly stopping at generation {gen} - No improvement for {max_stall} generations")
                break
            
            # Progress reporting
            if gen % 10 == 0:
                print(f"Generation {gen}: Best Distance = {self.best_distance:.2f} km")
        
        # Store final best route
        self.final_best_route = [self.start_point] + self.best_route + [self.end_point]
        
        print(f"\nOptimization complete after {len(self.progress)} generations")
        print(f"Final Best Distance: {self.best_distance:.2f} km")
        print("Optimized Route:")
        for i, point in enumerate(self.final_best_route):
            print(f"{i+1}. {point}")
        
        return self.final_best_route, self.best_distance, self.progress

# Usage example
if __name__ == "__main__":
    ga = GeneticAlgorithm()
    best_route, distance, progress = ga.run(max_stall=30)  # Stop if no improvement for 30 generations
    print("\nStored final best route:", best_route)