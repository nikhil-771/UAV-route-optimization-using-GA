from genetic_algorithm import GeneticAlgorithm
from visualization import (plot_progress,  
                          plot_fitness_distribution,
                          
                          plot_convergence_analysis)
import time
import map
from variables import waypoints




def main():
    map.plot_initial_waypoints(waypoints, "Initial Map")

    print("Starting route optimization...")
    start_time = time.time()
    
    ga = GeneticAlgorithm()
    best_route, best_distance, progress = ga.run()
    
    print(f"\nOptimization completed in {time.time()-start_time:.2f} seconds")
    print(f"Best route distance: {best_distance:.2f} km")
    
    
    # Visualizations
    print("\nGenerating visualizations...")
    
    plot_progress(progress, ga.avg_fitness)
    plot_fitness_distribution(ga)
    plot_convergence_analysis(ga.generation_stats)
    print("Visualizations generated and saved")

    map.plot_final_waypoints(best_route, "Final Map")

    print("Completed")
    
if __name__ == "__main__":
    main()

