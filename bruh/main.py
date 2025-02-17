import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(4, 4))
ax = fig.add_subplot()

vals = [10, 20, 30, 50, 200, 5]
labels = ['Toyota', 'Supra', 'BMW', 'F1', 'Lada', 'Lamborgini']

esp = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0]

ax.plot(vals, labels=labels, autopct='%1.1f%%', explode=esp, shadow=True)

plt.show()
