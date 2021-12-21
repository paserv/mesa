from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from Customer import Customer
from Sportello import Sportello
import numpy as np
from mesa.datacollection import DataCollector


class QueueModel(Model):
    """Queueing model with customers and counters as two
    types of agents that interact with each other
    """

    def __init__(self, no_customers, no_counters, ticks, grid_width=100, grid_height=100):
        self.ticks = ticks
        self._current_tick = 1
        self.queue = []
        self.no_customers = no_customers
        self.no_counters = no_counters
        self.schedule = RandomActivation(self)
        # Create agents
        self.customers = []
        self.counters = []
        self.grid = MultiGrid(grid_width, grid_height, torus=True)
        for i in range(self.no_counters):
            sportello = Sportello(i, self, i * 2)
            self.schedule.add(sportello)
            self.counters.append(sportello)
        for i in range(self.no_customers):
            customer = Customer(i + no_counters, self, grid_width, grid_height - 3)
            self.schedule.add(customer)
            self.customers.append(customer)
        self.datacollector = DataCollector(
            model_reporters={
                'Customers Arrived': self.get_customers_arrived,
                'Customers Served': self.get_customers_served,
                'Customers Balked': self.get_customers_balked,
                'Average Waiting Time': self.get_avg_waiting_time,
                'Average Queue Size': self.get_avg_queue_size
            })
        self.running = True

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self._current_tick += 1
        if self.ticks <= self._current_tick:
            self.running = False

    def get_customers_arrived(model):
        customers_arrived = [customer._arrived for customer in model.customers]
        no_customers_arrived = np.sum(customers_arrived)
        return no_customers_arrived

    def get_customers_served(model):
        customers_served = [not(customer._service_exit is None)
                            for customer in model.customers]
        no_customers_served = np.sum(customers_served)
        return no_customers_served

    def get_customers_balked(model):
        customers_arrived = [customer._arrived for customer in model.customers]
        # Customers who never joined a queue
        customers_no_q = np.array(
            [customer._q_entry is None for customer in model.customers])
        no_customers_balked = np.sum(customers_arrived * customers_no_q)
        return no_customers_balked

    def get_avg_queue_size(model):
        #queue_size = [len(counter.queue) for counter in model.counters]
        #avg_queue_size = np.mean(queue_size)
        #return avg_queue_size
        return len(model.queue)

    def get_avg_waiting_time(model):
        customers_wait = [np.nan if customer._q_exit is None else customer._q_exit -
                          customer._q_entry for customer in model.customers]
        avg_customer_wait = np.nanmean(customers_wait)
        return avg_customer_wait
