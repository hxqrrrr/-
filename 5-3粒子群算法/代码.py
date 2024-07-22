import numpy as np
import matplotlib.pyplot as plt


# 目标函数
def objective_function(x, y):
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


# PSO 算法
def pso(objective_func, bounds, num_particles, max_iterations):
    # 问题维度
    dim = len(bounds)

    # 设置算法参数
    w = 0.5  # 惯性权重
    c1 = 1  # 个体学习因子
    c2 = 2  # 社会学习因子

    # 初始化粒子群
    particles = np.random.rand(num_particles, dim) * (bounds[:, 1] - bounds[:, 0]) + bounds[:, 0]
    velocities = np.zeros((num_particles, dim))

    # 初始化个体最优和全局最优
    pbest = particles.copy()
    pbest_fitness = np.apply_along_axis(lambda x: objective_func(*x), 1, pbest)
    gbest = pbest[pbest_fitness.argmin()]
    gbest_fitness = pbest_fitness.min()

    # 迭代优化
    for _ in range(max_iterations):
        # 评估适应度
        fitness = np.apply_along_axis(lambda x: objective_func(*x), 1, particles)

        # 更新个体最优和全局最优
        improved = fitness < pbest_fitness
        pbest[improved] = particles[improved]
        pbest_fitness[improved] = fitness[improved]

        if fitness.min() < gbest_fitness:
            gbest = particles[fitness.argmin()]
            gbest_fitness = fitness.min()

        # 更新速度和位置
        r1, r2 = np.random.rand(2)
        velocities = (w * velocities +
                      c1 * r1 * (pbest - particles) +
                      c2 * r2 * (gbest - particles))
        particles += velocities

        # 边界处理
        particles = np.clip(particles, bounds[:, 0], bounds[:, 1])

    return gbest, gbest_fitness


# 设置参数
bounds = np.array([[-5, 5], [-5, 5]])
num_particles = 30
max_iterations = 100

# 运行PSO算法
best_solution, best_fitness = pso(objective_function, bounds, num_particles, max_iterations)

print(f"最优解: {best_solution}")
print(f"最优适应度值: {best_fitness}")

# 可视化结果
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = objective_function(X, Y)

plt.figure(figsize=(10, 8))
plt.contour(X, Y, Z, levels=50)
plt.colorbar(label='Objective Function Value')
plt.plot(best_solution[0], best_solution[1], 'r*', markersize=15)
plt.title('PSO Optimization Result')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
