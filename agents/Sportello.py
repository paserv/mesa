from mesa import Agent
from agents.AgentIcon import agent_icon

class Sportello(Agent):

    def __init__(self, unique_id, model, x_pos, closed_at):
        super().__init__(unique_id, model)
        self.icon = agent_icon.sportello_aperto
        self.active_customer = None
        self.x_pos = x_pos
        self.closed_at = closed_at
        self.closing = False
        model.grid.place_agent(self, (x_pos, 0))

    def dequeue(self):
        try:
            if len(self.model.queue_mobile) > 0:
                self.active_customer = self.model.queue_mobile.pop(0)
            else:
                self.active_customer = self.model.queue.pop(0)
            self.active_customer._q_exit = self.model._current_tick
            self.active_customer._service_entry = self.model._current_tick
            self.active_customer.coords = (self.x_pos, 1)
            self.model.grid.move_agent(self.active_customer, self.active_customer.coords)
            #print('Sportello ' + str(self.unique_id) + " now serving Customer " + str(self.active_customer.unique_id) + ' at ' + str(self.model._current_tick))
        except:
            pass

    def step(self):
        self.check_closed()
        if self.active_customer is None:
            if not self.closing:
                self.dequeue()
        elif self.active_customer._service_entry + self.active_customer.service_time < self.model._current_tick:
            self.active_customer._service_exit = self.model._current_tick
            self.active_customer._arrived = False
            self.model.grid.remove_agent(self.active_customer)
            #print('Sportello ' + str(self.unique_id) + " has served Customer " + str(self.active_customer.unique_id) + ' at ' + str(self.model._current_tick))
            self.active_customer = None

    def check_closed(self):
        for interval in self.closed_at:
            if self.model._current_tick >= interval[0] and self.model._current_tick <= interval[1]:
                self.closing = True
                self.icon = agent_icon.sportello_chiuso
                return
        self.closing = False
        self.icon = agent_icon.sportello_aperto
