from json import JSONEncoder

class agent_icon(JSONEncoder):
   sportello_aperto = 'img/sportello_aperto.png'
   sportello_chiuso = 'img/sportello_chiuso.png'
   customer = 'img/customer.png'
   mobile_customer = 'img/mobile_customer.png'

   def default(self, o):
      return o.__dict__
