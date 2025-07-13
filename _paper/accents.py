import matplotlib.pyplot as plt
import numpy as np
import os
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

x = [0, 0.4, 1]
y = [0, 1, 1]
# Target point
x1, y1 = 0, 0
x2, y2 = 0.4, 1

# Choose b (growth rate)
b = 5

# Compute a using the second point
a = y2 / (np.exp(b * x2) - 1)

# Define the function
def shifted_exp(x):
    return a * (np.exp(b * x) - 1)

# Plot
x_vals = np.linspace(0, 0.4, 100)
y_vals = shifted_exp(x_vals)

plt.figure(figsize = (10,5))
plt.plot([0, 1],[0, 0], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[0.5, 0.5], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[1.0, 1.0], color = 'gray', linewidth = 0.01)

plt.scatter(x, y, color = 'k', s = 400)
plt.plot(x_vals, y_vals, color = 'k')
plt.plot([0.4, 1],[1, 1], color = 'k', linestyle = '--')
plt.axis('off')
plt.tight_layout()
plt.savefig(current_dir + '/bend_1_chart.pdf', dpi = 200)

plt.close()

x = [0, 1]
y = [0, 1]
# Target point
x1, y1 = 0, 0
x2, y2 = 1, 1

# Choose b (growth rate)
b = 5

# Compute a using the second point
a = y2 / (np.exp(b * x2) - 1)

# Define the function
def shifted_exp(x):
    return a * (np.exp(b * x) - 1)

# Plot
x_vals = np.linspace(0, 1.0, 100)
y_vals = shifted_exp(x_vals)

plt.figure(figsize = (10,5))
plt.scatter(x, y, color = 'k', s = 400)
plt.plot([0, 1],[0, 0], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[0.5, 0.5], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[1.0, 1.0], color = 'gray', linewidth = 0.01)

plt.scatter(x, y, color = 'k')
plt.plot(x_vals, y_vals, color = 'k')
plt.axis('off')
plt.tight_layout()
plt.savefig(current_dir + '/bend_2_chart.pdf', dpi = 200)

plt.close()

x = [0, 0.4, 0.6, 0.8, 1]
y = [0, 1, 1, 0, 0]

# Target point
x1, y1 = 0, 0
x2, y2 = 0.4, 1

# Choose b (growth rate)
b = 5

# Compute a using the second point
a = y2 / (np.exp(b * x2) - 1)

# Define the function
def shifted_exp(x):
    return a * (np.exp(b * x) - 1)

# Plot
x_vals = np.linspace(0, 0.4, 100)
y_vals = shifted_exp(x_vals)

x3 = np.linspace(0.6, 0.8, 100)
n = 2  # you can change this for different curve shapes
y3 = 1 - ((x3 - 0.6) / 0.2) ** n


plt.figure(figsize = (10,5))
plt.plot([0, 1],[0, 0], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[0.5, 0.5], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[1.0, 1.0], color = 'gray', linewidth = 0.01)

plt.plot(x3, y3, color = 'k')
plt.scatter(x, y, color = 'k', s = 400)
plt.plot(x_vals, y_vals, color = 'k')
plt.plot([0.4, 0.6],[1, 1], color = 'k', linestyle = '--')
plt.plot([0.8, 1.0],[0, 0], color = 'k', linestyle = '--')
plt.axis('off')
plt.tight_layout()
plt.savefig(current_dir + '/bend_3_chart.pdf', dpi = 200)

plt.close()

# Target point
x = [0, 1]
y = [1.0, 1.0]
plt.figure(figsize = (10,5))
plt.scatter(x, y, color = 'k', s = 400)
plt.plot([0, 1],[0, 0], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[0.5, 0.5], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[1.0, 1.0], color = 'gray', linewidth = 0.01)

plt.plot([0.0, 1.],[1.0, 1.0], color = 'k', linestyle = '--')
plt.axis('off')
plt.tight_layout()
plt.savefig(current_dir + '/bend_4_chart.pdf', dpi = 200)

plt.close()

# Target point
x = [0,0, 1]
y = [0,1.0, 1.0]
plt.figure(figsize = (10,5))
plt.scatter(x, y, color = 'k', s = 400)
plt.plot([0, 1],[0, 0], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[0.5, 0.5], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[1.0, 1.0], color = 'gray', linewidth = 0.01)


plt.plot([0.0, 0.0],[0.0, 1.0], color = 'k')
plt.plot([0.0, 1.],[1.0, 1.0], color = 'k', linestyle = '--')
plt.axis('off')
plt.tight_layout()
plt.savefig(current_dir + '/bend_5_chart.pdf', dpi = 200)

plt.close()



x = [0, 0, 1.0]
y = [0, 1, 1.5]
# Target point
# Define points
P0 = np.array([0.0, 1.0])  # Start point
P1 = np.array([0.7, 1.0])    # Control point (adjust for slope)
P2 = np.array([1.0, 1.5])    # End point

# Quadratic Bézier formula
def bezier(t):
    return (1-t)**2 * P0 + 2*(1-t)*t * P1 + t**2 * P2

# Generate curve
t_vals = np.linspace(0, 1, 100)
curve = np.array([bezier(t) for t in t_vals])

# Plot
plt.figure(figsize = (10,5))
plt.plot(curve[:, 0], curve[:, 1], color = 'k')
plt.scatter(x, y, color = 'k', s = 400)
plt.plot([0, 1],[0, 0], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[0.5, 0.5], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[1.0, 1.0], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[1.5, 1.5], color = 'gray', linewidth = 0.01)

plt.scatter(x, y, color = 'k')
plt.plot([0.0, 0.0],[0.0, 1.0], color = 'k')
plt.axis('off')
plt.tight_layout()
plt.savefig(current_dir + '/bend_6_chart.pdf', dpi = 200)

plt.close()



x = [0, 0, 0.6, 1]
y = [0, 1, 0, 0]


x3 = np.linspace(0.0, 0.6, 100)
n = 2  # you can change this for different curve shapes
y3 = 1 - ((x3) / 0.6) ** n


plt.figure(figsize = (10,5))
plt.plot([0, 1],[0, 0], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[0.5, 0.5], color = 'gray', linewidth = 0.01)
plt.plot([0, 1],[1.0, 1.0], color = 'gray', linewidth = 0.01)

plt.plot(x3, y3, color = 'k')
plt.scatter(x, y, color = 'k', s = 400)
plt.plot([0.0, 0.0],[0, 1], color = 'k')
plt.plot([0.6, 1.0],[0, 0], color = 'k', linestyle = '--')
plt.axis('off')
plt.tight_layout()
plt.savefig(current_dir + '/bend_7_chart.pdf', dpi = 200)

plt.close()