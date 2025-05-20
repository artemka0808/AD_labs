import numpy as np
import matplotlib.pyplot as plt

# як у Завданні 1
np.random.seed(0)
k = 2.5
b = 1.0
x = np.linspace(0, 10, 50)
rand = np.random.normal(0, 2, size=x.shape)
y = k * x + b + rand

# Функція градієнтного спуску
def gradient_descent(x, y, learning_rate=0.01, n_iter=10000):
    n = len(x)
    k_gd = 0.0
    b_gd = 0.0
    errors = []

    for i in range(n_iter):
        y_pred = k_gd * x + b_gd
        error = y - y_pred
        loss = np.mean(error ** 2)
        errors.append(loss)

        # Градієнти
        grad_k = (-2 / n) * np.sum(x * error)
        grad_b = (-2 / n) * np.sum(error)

        # Оновлення параметрів
        k_gd -= learning_rate * grad_k
        b_gd -= learning_rate * grad_b

    return k_gd, b_gd, errors

# Налаштування параметрів
learning_rate = 0.01
n_iter = 1000

# Виклик функції
k_gd, b_gd, errors = gradient_descent(x, y, learning_rate, n_iter)

# Порівняння з попередніми оцінками
k_ls, b_ls = np.polyfit(x, y, 1)

print(f"Істинні параметри: k = {k}, b = {b}")
print(f"Градієнтний спуск: k = {k_gd:.3f}, b = {b_gd:.3f}")
print(f"np.polyfit (для порівн.): k = {k_ls:.3f}, b = {b_ls:.3f}")

# Побудова лінії регресії
plt.figure(figsize=(8, 5))
plt.scatter(x, y, label='Згенеровані дані', color='gray', alpha=0.6)
plt.plot(x, k * x + b, label='Початкова пряма (y = kx + b)', linestyle='--', color='black')
plt.plot(x, k_gd * x + b_gd, label='Градієнтний спуск', color='green')
plt.plot(x, k_ls * x + b_ls, label='np.polyfit', color='red', linestyle=':')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Завдання 2')
plt.legend()
plt.grid(True)
plt.show()

# Побудова графіка похибки
plt.figure(figsize=(8, 4))
plt.plot(errors, label='MSE', color='purple')
plt.xlabel('Ітерації')
plt.ylabel('Похибка ')
plt.title('Зміна похибки під час градієнтного спуску')
plt.legend()
plt.grid(True)
plt.show()
