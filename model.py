from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents.Customer import Customer
from agents.MobileCustomer import MobileCustomer
from agents.Sportello import Sportello
import numpy as np
from mesa.datacollection import DataCollector

class QueueModel(Model):
    """Queueing model with customers and counters as two
    types of agents that interact with each other
    """

    def __init__(self, no_customers, no_mobile_customers, no_counters, closing_at, hours=60, grid_width=100, grid_height=100):
        self.ticks = hours * 60
        self._current_tick = 1
        self.closing_at = closing_at
        self.queue = []
        self.queue_mobile = []
        self.no_customers = no_customers
        self.no_mobile_customers = no_mobile_customers
        self.no_counters = no_counters
        self.schedule = RandomActivation(self)
        # Create agents
        self.customers = []
        self.mobile_customers = []
        self.counters = []
        self.grid = MultiGrid(grid_width, grid_height, torus=True)
        for i in range(self.no_counters):
            sportello = Sportello(i, self, i * 2, closing_at[i] if i < len(closing_at) else [])
            self.schedule.add(sportello)
            self.counters.append(sportello)
        for i in range(self.no_customers):
            customer = Customer(i + no_counters, self, grid_width, grid_height - 3)
            self.schedule.add(customer)
            self.customers.append(customer)
        for i in range(self.no_mobile_customers):
            customer = MobileCustomer(i + no_counters + no_customers, self, grid_width, grid_height - 3)
            self.schedule.add(customer)
            self.mobile_customers.append(customer)
        self.datacollector = DataCollector(
            model_reporters={
                'Customers Arrived': self.get_customers_arrived,
                'Customers Served': self.get_customers_served,
                'Mobile Customers Arrived': self.get_mobile_customers_arrived,
                'Mobile Customers Served': self.get_mobile_customers_served,
                'Customers Balked': self.get_customers_balked,
                'Average Waiting Time': self.get_avg_waiting_time,
                'Average Queue Size': self.get_avg_queue_size,
                'Average Mobile Queue Size': self.get_avg_mobile_queue_size
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
        return int(no_customers_arrived)
    
    def get_mobile_customers_arrived(model):
        customers_arrived = [customer._arrived for customer in model.mobile_customers]
        no_customers_arrived = np.sum(customers_arrived)
        return int(no_customers_arrived)

    def get_customers_served(model):
        customers_served = [not(customer._service_exit is None)
                            for customer in model.customers]
        no_customers_served = np.sum(customers_served)
        return int(no_customers_served)

    def get_mobile_customers_served(model):
        customers_served = [not(customer._service_exit is None)
                            for customer in model.mobile_customers]
        no_customers_served = np.sum(customers_served)
        return int(no_customers_served)

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
    
    def get_avg_mobile_queue_size(model):
        return len(model.queue_mobile)

    def get_avg_waiting_time(model):
        customers_wait = [np.nan if customer._q_exit is None else customer._q_exit -
                          customer._q_entry for customer in model.customers]
        avg_customer_wait = np.nanmean(customers_wait)
        return avg_customer_wait
