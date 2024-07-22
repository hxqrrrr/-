import numpy as np
import matplotlib.pyplot as plt


# 目标函数（要最大化的函数）
def objective_function(x):
    return -(x ** 2) + 5 * x + 10


# 遗传算法类
class GeneticAlgorithm:
    def __init__(self, pop_size, gene_length, bounds, generations, mutation_rate):
        self.pop_size = pop_size
        self.gene_length = gene_length
        self.bounds = bounds
        self.generations = generations
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        return np.random.randint(2, size=(self.pop_size, self.gene_length))

    def decode(self, chromosome):
        decimal = int(''.join(map(str, chromosome)), 2)
        return self.bounds[0] + (decimal / (2 ** self.gene_length - 1)) * (self.bounds[1] - self.bounds[0])

    def calculate_fitness(self, population):
        fitness = np.array([objective_function(self.decode(ind)) for ind in population])
        return fitness - fitness.min() + 1e-6  # 确保所有值都是正的

    def select_parents(self, population, fitness):
        probs = fitness / fitness.sum()
        return population[np.random.choice(len(population), size=2, p=probs)]

    def crossover(self, parents):
        crossover_point = np.random.randint(1, self.gene_length)
        child1 = np.concatenate([parents[0][:crossover_point], parents[1][crossover_point:]])
        child2 = np.concatenate([parents[1][:crossover_point], parents[0][crossover_point:]])
        return child1, child2

    def mutate(self, individual):
        for i in range(len(individual)):
            if np.random.random() < self.mutation_rate:
                individual[i] = 1 - individual[i]
        return individual

    def evolve(self):
        population = self.initialize_population()
        best_solutions = []

        for _ in range(self.generations):
            fitness = self.calculate_fitness(population)
            best_solutions.append(self.decode(population[np.argmax(fitness)]))

            new_population = []
            for _ in range(self.pop_size // 2):
                parents = self.select_parents(population, fitness)
                child1, child2 = self.crossover(parents)
                new_population.extend([self.mutate(child1), self.mutate(child2)])

            population = np.array(new_population)

        return best_solutions


# 设置参数
pop_size = 50
gene_length = 16
bounds = (-5, 5)
generations = 100
mutation_rate = 0.01

# 创建并运行遗传算法
ga = GeneticAlgorithm(pop_size, gene_length, bounds, generations, mutation_rate)
best_solutions = ga.evolve()

# 打印结果
print(f"最优解: {best_solutions[-1]}")
print(f"最优适应度值: {objective_function(best_solutions[-1])}")

# 可视化结果
plt.figure(figsize=(10, 6))
x = np.linspace(-5, 5, 1000)
y = objective_function(x)
plt.plot(x, y, label='Objective Function')
plt.plot(best_solutions, [objective_function(x) for x in best_solutions], 'ro-', label='Best Solution')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Genetic Algorithm Optimization')
plt.legend()
plt.grid(True)
plt.show()

# 绘制收敛曲线
plt.figure(figsize=(10, 6))
plt.plot(range(generations), [objective_function(x) for x in best_solutions])
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title('Convergence Curve')
plt.grid(True)
plt.show()
