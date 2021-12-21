from mesa import Agent

class Sportello(Agent):

    def __init__(self, unique_id, model, x_pos):
        super().__init__(unique_id, model)
        self.active_customer = None
        self.x_pos = x_pos
        model.grid.place_agent(self, (x_pos, 0))

    def dequeue(self):
        try:
            self.active_customer = self.model.queue.pop(0)
            self.active_customer._q_exit = self.model._current_tick
            self.active_customer._service_entry = self.model._current_tick
            self.active_customer.coords = (self.x_pos, 1)
            self.model.grid.move_agent(self.active_customer, self.active_customer.coords)
            #print('Sportello ' + str(self.unique_id) + " now serving Customer " + str(self.active_customer.unique_id) + ' at ' + str(self.model._current_tick))
        except:
            pass

    def step(self):
        if self.active_customer is None:
            self.dequeue()
        elif self.active_customer._service_entry + self.active_customer.service_time < self.model._current_tick:
            self.active_customer._service_exit = self.model._current_tick
            self.model.grid.remove_agent(self.active_customer)
            #print('Sportello ' + str(self.unique_id) + " has served Customer " + str(self.active_customer.unique_id) + ' at ' + str(self.model._current_tick))
            self.active_customer = None

