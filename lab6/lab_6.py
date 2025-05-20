import numpy as np
import matplotlib.pyplot as plt

# 1. Генеруємо дані y = kx + b
np.random.seed(0)
k_true = 2.5
b_true = 1.0
x = np.linspace(0, 10, 50)
rand = np.random.normal(0, 2, size=x.shape)
y = k_true * x + b_true + rand

# 2. Метод найменших квадратів
def least_squares(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)
    k = numerator / denominator
    b = y_mean - k * x_mean
    return k, b

k_custom, b_custom = least_squares(x, y)

# 3. Порівняння з numpy.polyfit
k_np, b_np = np.polyfit(x, y, 1)

print(f"Істинні параметри: k = {k_true}, b = {b_true}")
print(f"Оцінка (власна): k = {k_custom:.3f}, b = {b_custom:.3f}")
print(f"Оцінка (np.polyfit): k = {k_np:.3f}, b = {b_np:.3f}")

# 4.
plt.scatter(x, y, label='Згенеровані дані', color='gray', alpha=0.6)
plt.plot(x, k_true * x + b_true, label='Початкова пряма (y = kx + b)', linestyle='--', color='black')
plt.plot(x, k_custom * x + b_custom, label='Власна реалізація', color='blue')
plt.plot(x, k_np * x + b_np, label='np.polyfit', color='red', linestyle=':')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Завдання 1')
plt.legend()
plt.grid(True)
plt.show()
