import math
import random
import multiprocessing
from functools import lru_cache

# 定义城市及其坐标（经度，纬度）
cities = {
    "北京": (116.4074, 39.9042),
    "上海": (121.4737, 31.2304),
    "广州": (113.2644, 23.1291),
    "深圳": (114.0579, 22.5431),
    "成都": (104.0665, 30.5723),
    "重庆": (106.5516, 29.5630),
    "西安": (108.9402, 34.3416),
    "武汉": (114.3054, 30.5928),
    "南京": (118.7969, 32.0603),
    "杭州": (120.1551, 30.2741)
}


@lru_cache(maxsize=None)
def distance(city1, city2):
    """计算两个城市之间的距离（使用简化的球面距离公式）"""
    lat1, lon1 = math.radians(cities[city1][1]), math.radians(cities[city1][0])
    lat2, lon2 = math.radians(cities[city2][1]), math.radians(cities[city2][0])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # 地球平均半径（单位：公里）
    return c * r


def total_distance(tour):
    """计算整个路径的总距离"""
    return sum(distance(tour[i], tour[i - 1]) for i in range(len(tour)))


def generate_initial_tour():
    """使用贪心算法生成初始解"""
    unvisited = list(cities.keys())[1:]  # 除北京外的所有城市
    tour = ["北京"]
    while unvisited:
        last = tour[-1]
        next_city = min(unvisited, key=lambda x: distance(last, x))
        tour.append(next_city)
        unvisited.remove(next_city)
    tour.append("北京")
    return tour


def two_opt(tour):
    """实现2-opt邻域结构"""
    i, j = sorted(random.sample(range(1, len(tour) - 1), 2))
    return tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]


def adaptive_markov_chain_length(temp, initial_temp, initial_length):
    """动态调整马尔可夫链长度"""
    return int(initial_length * (initial_temp / temp))


def adaptive_cooling(temp, initial_temp, current_iteration, total_iterations):
    """自适应冷却策略"""
    progress = current_iteration / total_iterations
    if progress < 0.3:
        return temp * 0.99  # 快速冷却
    elif progress < 0.6:
        return temp * 0.999  # 中等冷却
    else:
        return temp * 0.9999  # 慢速冷却


def adaptive_simulated_annealing(initial_temp, final_temp, initial_markov_length, max_iterations):
    current_tour = generate_initial_tour()
    current_distance = total_distance(current_tour)
    best_tour = current_tour
    best_distance = current_distance
    temp = initial_temp

    iteration = 0
    iterations_without_improvement = 0

    while iteration < max_iterations and temp > final_temp:
        markov_chain_length = adaptive_markov_chain_length(temp, initial_temp, initial_markov_length)

        for _ in range(markov_chain_length):
            new_tour = two_opt(current_tour)
            new_distance = total_distance(new_tour)
            delta = new_distance - current_distance

            if delta < 0 or random.random() < math.exp(-delta / temp):
                current_tour = new_tour
                current_distance = new_distance

                if current_distance < best_distance:
                    best_tour = current_tour
                    best_distance = current_distance
                    iterations_without_improvement = 0
                else:
                    iterations_without_improvement += 1

        temp = adaptive_cooling(temp, initial_temp, iteration, max_iterations)
        iteration += 1

        if iterations_without_improvement >= max_iterations // 10:
            # 重启策略
            current_tour = generate_initial_tour()
            current_distance = total_distance(current_tour)
            temp = initial_temp * 0.5  # 降低重启温度以加快收敛
            iterations_without_improvement = 0

        if iteration % 100 == 0:
            print(f"迭代 {iteration}: 温度 = {temp:.2f}, 最佳距离 = {best_distance:.2f}")

    return best_tour, best_distance


def run_annealing(args):
    return adaptive_simulated_annealing(*args)


if __name__ == "__main__":
    initial_temp = 1000
    final_temp = 0.1
    initial_markov_length = len(cities) * 100
    max_iterations = 10000

    num_runs = multiprocessing.cpu_count()  # 使用可用的CPU核心数

    pool = multiprocessing.Pool()
    results = pool.map(run_annealing, [(initial_temp, final_temp, initial_markov_length, max_iterations)] * num_runs)

    best_overall_tour, best_overall_distance = min(results, key=lambda x: x[1])

    print(f"\n最终最佳路线: {' -> '.join(best_overall_tour)}")
    print(f"总距离: {best_overall_distance:.2f} 公里")
