from QueueModel import QueueModel
import matplotlib.pyplot as plt

# Config
ticks = 200 # 3600 ticks = 3600 seconds = 1 hour
no_customers = 10
no_counters = 10
grid_width = no_counters
grid_height = grid_width

model = QueueModel(ticks=ticks, no_customers=no_customers,
                   no_counters=no_counters)
for i in range(ticks):
    model.step()

run_stats = model.datacollector.get_model_vars_dataframe()
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
fig.figure.set_figwidth(12)
fig.figure.set_figheight(16)
fig.suptitle(f'Simulations stats using {no_counters} counters', fontsize=20)
ax1.plot(run_stats[['Customers Arrived',
                'Customers Served',
                'Customers Balked',
               ]])
ax1.legend(['Customers Arrived',
            'Customers Served',
            'Customers Balked',
            ])
ax1.set_ylabel('Customers')
ax1.set_xlim(0)
ax1.set_ylim(0)
ax2.plot(run_stats['Average Queue Size'], color='red')
ax2.legend(['Average Queue Size'])
ax2.set_ylabel('Customers')
ax2.set_xlim(0)
ax2.set_ylim(0)
ax3.plot(run_stats['Average Waiting Time'], color='grey')
ax3.legend(['Average Waiting Time (across full hour)'])
ax3.set_ylabel('Seconds')
ax3.set_xlim(0)
ax3.set_ylim(0)
fig.show()
input("Press Enter to continue...")