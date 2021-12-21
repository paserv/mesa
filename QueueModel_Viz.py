from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from QueueModel import QueueModel
from Sportello import Sportello

ticks = 3600 # 3600 ticks = 3600 seconds = 1 hour
no_customers = 60
no_counters = 5
grid_width = 10
grid_height = grid_width

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.3}
    if type(agent) is Sportello:
        portrayal["Sportello"] = agent.unique_id + 1
        portrayal["Color"] = "blue"
        portrayal["r"] = 0.5
    else:
        portrayal["Service time"] = int(agent.service_time)
        portrayal["Customer Behind"] = agent.customer_behind
    return portrayal

grid = CanvasGrid(agent_portrayal, grid_width, grid_height, 500, 500)

server = ModularServer(QueueModel,
                       [grid],
                       "Queue Model",
                       {"no_customers":no_customers, "no_counters":no_counters, "ticks":ticks, "grid_width": grid_width, "grid_height": grid_height})
server.port = 8522 # The default
server.launch()
