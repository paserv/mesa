from mesa import Agent
import numpy as np
from scipy.stats import poisson, beta, expon
from agents.AgentIcon import agent_icon

class Customer(Agent):

    def __init__(self, unique_id, model, max_width, max_height):
        super().__init__(unique_id, model)
        self.icon = agent_icon.customer
        self.max_width = max_width
        self.max_height = max_height
        self.coords = None
        # Time required to process the customer's transaction
        self.service_time = expon.rvs(scale = 2)
        # Time of arrival at queue
        self.entry_time = np.int(beta(3, 3).rvs() * model.ticks) + 1
        self.balk_tolerance = 350000#poisson(35).rvs() + 1
        # Whether or not the customer has arrived at the queue
        self._arrived = False
        self._q_entry = None
        self._q_exit = None
        self._service_entry = None
        self._service_exit = None

    def step(self):
        if self.entry_time == self.model._current_tick:
            self._arrived = True
            #if self.balk_tolerance > len(self._chosen_counter.queue):
            self._q_entry = self.model._current_tick
            if self.balk_tolerance > len(self.model.queue):
                self.model.queue.append(self)
                self.coords = (self.random.randrange(0, self.max_width), self.random.randrange(0, self.max_height) + 3)
                self.model.grid.place_agent(self, self.coords)
            else:
                self._q_exit = self.model._current_tick
            #print('Customer ' + str(self.unique_id) + ' start queue at ' + str(self.model._current_tick) +' with service time of ' + str(self.service_time))
        