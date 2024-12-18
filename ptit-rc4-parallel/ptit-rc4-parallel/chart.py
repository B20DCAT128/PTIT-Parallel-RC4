import matplotlib.pyplot as plt
import pandas as pd
import subprocess

file_path="rc4_results.csv"
data = pd.read_csv(file_path)

file_sizes= data["File Size (MB)"]
columns= data.columns[1:]

x = range(len(file_sizes))
width = 0.15
fig, ax = plt.subplots(figsize=(10,6))

for i, col in enumerate(columns):
    ax.bar([pos + i * width for pos in x],data[col],width=width, label=col)
ax.set_xlabel("File Size (MB)", fontsize=12)
ax.set_ylabel("Time (s)", fontsize=12)
ax.set_xticks([pos + width *(len(columns)-1)/2 for pos in x])
ax.set_xticklabels(file_sizes)
ax.legend(title="Execution Mode")
plt.tight_layout()
plt.savefig("rc4_chart.png")
subprocess.run(["cat", "/home/check.txt"])
subprocess.run(["feh", "rc4_chart.png"])
