import matplotlib.pyplot as plt

# Define the blocks and connections
blocks = ['Initialize', 'Search Loop', 'Check if Goal', 'Move to Close', 'Generate Successors', 'Check in Open', 'Update Costs', 'Add to Open', 'Check in Close', 'Update Costs', 'Add to Open', 'Goal Not Found']
connections = [('Initialize', 'Search Loop'), ('Search Loop', 'Check if Goal'), ('Check if Goal', 'Move to Close'),
               ('Move to Close', 'Generate Successors'), ('Generate Successors', 'Check in Open'),
               ('Check in Open', 'Update Costs'), ('Update Costs', 'Add to Open'),
               ('Check in Open', 'Check in Close'), ('Check in Close', 'Update Costs'), ('Update Costs', 'Add to Open'),
               ('Check if Goal', 'Goal Not Found')]

# Create a directed graph
graph = plt.figure(figsize=(8, 6))
ax = graph.add_subplot(111)

# Draw blocks
for i, block in enumerate(blocks):
    ax.text(0.5, i, block, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

# Draw connections
for connection in connections:
    start, end = connection
    start_index = blocks.index(start)
    end_index = blocks.index(end)
    ax.annotate('', xy=(0.5, start_index), xytext=(0.5, end_index), arrowprops=dict(arrowstyle='->'))

# Set axis properties
ax.set_xlim(0, 1)
ax.set_ylim(len(blocks)-1, 0)
ax.axis('off')

# Show the block diagram
plt.show()
