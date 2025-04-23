import matplotlib.pyplot as plt
import numpy as np


def plot_progress(progress, avg_fitness):
    """Enhanced progress plot with best distance and average fitness"""
    plt.figure(figsize=(14, 10))
    
    # Create subplots
    ax1 = plt.subplot(2, 1, 1)  # Best distance
    ax2 = plt.subplot(2, 1, 2)  # Average fitness

    # ===== 1. Best Distance Plot =====
    ax1.plot(progress, 'b-', linewidth=2, label='Best Distance')
    ax1.set_title('Genetic Algorithm Optimization Progress', fontsize=14, pad=20)
    ax1.set_ylabel('Distance (km)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Highlight specific generations with clear labels
    highlight_gens = [10, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450]
    for gen in highlight_gens:
        if gen < len(progress):
            # Plot marker
            ax1.scatter(gen, progress[gen], c='red', s=80, edgecolors='black', zorder=5)
            
            # Add generation label
            ax1.text(gen, progress[gen]*0.98, f'G{gen}', 
                    ha='center', va='top', fontsize=10,
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.8))
    
    ax1.legend(loc='upper right')
    
    # ===== 2. Average Fitness Plot =====
    ax2.plot(avg_fitness, 'g-', linewidth=1.5, label='Average Fitness')
    ax2.set_ylabel('Fitness Score', fontsize=12)
    ax2.set_xlabel('Generation', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Set appropriate y-limits based on data
    y_min = min(avg_fitness) * 0.98
    y_max = max(avg_fitness) * 1.02
    ax2.set_ylim(y_min, y_max)
    
    # Highlight same generations
    for gen in highlight_gens:
        if gen < len(avg_fitness):
            ax2.scatter(gen, avg_fitness[gen], c='orange', s=60, edgecolors='black', zorder=5)
    
    ax2.legend(loc='lower right')
    
    plt.tight_layout()
    plt.savefig("genetic_algorithm_progress.png", format="png", dpi=300)
    plt.show()


def plot_fitness_distribution(ga):
    """Improved fitness distribution visualization"""
    plt.figure(figsize=(12, 7))
    
    # Select key generations to plot
    generations_to_plot = [0, 10, 25, 50, 100, -1]  # First, middle, last
    
    # Create violin plots instead of KDE for better comparison
    all_data = []
    labels = []
    
    for gen in generations_to_plot:
        if gen >= len(ga.avg_fitness):
            continue
        
        if gen == 0:
            label = 'Initial Population'
        elif gen == len(ga.avg_fitness)-1:
            label = f'Final Generation (G{gen})'
        else:
            label = f'Generation {gen}'
        
        distances = [ga.calculate_distance(route) for route in ga.population]
        all_data.append(distances)
        labels.append(label)
    
    # Create violin plot
    parts = plt.violinplot(all_data, showmeans=True, showmedians=True)
    
    # Customize colors
    for pc in parts['bodies']:
        pc.set_facecolor('#1f77b4')
        pc.set_edgecolor('black')
        pc.set_alpha(0.7)
    
    # Customize labels and ticks
    plt.xticks(range(1, len(labels)+1), labels)
    plt.title('Population Fitness Distribution Evolution', fontsize=14, pad=20)
    plt.xlabel('Generation', fontsize=12)
    plt.ylabel('Route Distance (km)', fontsize=12)
    plt.grid(True, axis='y', alpha=0.3)
    
    # Add some statistical annotations
    for i, data in enumerate(all_data):
        mean = np.mean(data)
        median = np.median(data)
        plt.text(i+1.2, mean, f'μ={mean:.1f}', va='center', fontsize=10)
        plt.text(i+1.2, median, f'med={median:.1f}', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig("fitness_distribution.png", format="png", dpi=300)
    plt.show()


def plot_convergence_analysis(generation_stats):
    """Plot convergence metrics (best, average, worst)"""
    best = [gen['best'] for gen in generation_stats]
    avg = [gen['average'] for gen in generation_stats]
    worst = [gen['worst'] for gen in generation_stats]
    
    plt.figure(figsize=(12, 6))
    plt.plot(best, label='Best', linewidth=2)
    plt.plot(avg, label='Average', linewidth=2)
    plt.plot(worst, label='Worst', linewidth=2)
    
    plt.title('Convergence Analysis')
    plt.xlabel('Generation')
    plt.ylabel('Distance (km)')
    plt.legend()
    plt.grid(True)
    plt.savefig("convergence_analysis.png", format="png", dpi=300)
    plt.show()
