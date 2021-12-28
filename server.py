from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import QueueModel
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule

no_counters = 5
grid_width = 10
grid_height = grid_width

def agent_portrayal(agent):
    portrayal = {"Layer": 0,
                 "Shape": agent.icon
                 }
    return portrayal

grid = CanvasGrid(agent_portrayal, grid_width, grid_height, 500, 500)
chart = ChartModule([
    {"Label": "Average Queue Size", "Color": "Black"}, 
    {"Label": "Customers Arrived", "Color": "Red"}, 
    {"Label": "Customers Served", "Color": "Green"},
    {"Label": "Average Mobile Queue Size", "Color": "Magenta"}, 
    {"Label": "Mobile Customers Arrived", "Color": "Pink"}, 
    {"Label": "Mobile Customers Served", "Color": "Yellow"}
    ], data_collector_name='datacollector')

model_params = {
    "hours": UserSettableParameter("slider", "Hours", value=2, min_value=1, max_value=10, step=1), 
    "no_customers": UserSettableParameter("slider", "N. Customers", value=100, min_value=10, max_value=10000, step=100), 
    "no_mobile_customers": UserSettableParameter("slider", "N. Mobile Customers", value=10, min_value=1, max_value=60, step=1), 
    "no_counters": no_counters, 
    "grid_width": grid_width, 
    "grid_height": grid_height,
    "closing_at": [
        [[0, 60]], 
        [[60, 120]], 
        [[120, 180]], 
        [[240, 300]], 
        [[0, 60], [300, 400]]
        ]
    }

server = ModularServer(QueueModel,
                       [grid, chart],
                       "Queue Model",
                       model_params
                       )
server.port = 8521 # The default
server.launch()
