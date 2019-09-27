# ***************************************************************
# Classes
# ****************************************************************

class Round:
    def __init__(self, brew_maker, round_id = "", orders = {}):
        self.round_id = round_id
        self.brew_maker = brew_maker
        self.orders = orders

    def add_person(self, name, favourite):
        is_in = False
        for i in range(len(self.orders)):
            if name in list(self.orders.keys()):
                is_in = True
        if not is_in:
            self.orders[name] = favourite

    def update_drink(self, new_drink, name):
        self.orders[name] = new_drink

    def end_round(self):
        orders = self.get_orders()
        self.clear_orders()
        self.brew_maker = ""
        return orders

    def get_orders(self):
        return self.orders

    def get_brew_maker(self):
        return self.brew_maker

    def new_brew_maker(self, name):
        self.brew_maker = name

    def clear_orders(self):
        self.orders = {}

    def class_dict_to_save(self):
        return {self.brew_maker: self.orders}

    def remove_person_from_round(self, name):
        if name in self.orders.keys():
            self.orders.pop(name)

    def get_round_id(self):
        return self.round_id

    def set_round_id(self, new_round_id):
        self.round_id = new_round_id

    def is_person_in_round(self, name):
        is_in = False
        for i in range(len(self.orders)):
            if name in list(self.orders.keys()):
                is_in = True
        return is_in