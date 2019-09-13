class Menu():  # TODO add starting index 
    def __init__(self, initial_options, header="", index=0):
        self.options = initial_options
        self.header = header
        self.index = index

    def add_option(self, new_option):
        self.options.append(new_option)

    def remove_option(self, old_option):
        try:
            self.options.remove(old_option)
        except:
            pass

    def print_options(self):
        for option in self.options:
            print(option)

    def print_ioptions(self):
        for i in range(len(self.options)):
            print(f"[{i + self.index}] " + self.options[i])

    def select_option(self, acceptable_values=[]):
        self.print_ioptions()
        choice = "\n"
        while (choice not in range(index, len(self.options) + index)) and (choice not in acceptable_values):
            choice = input("Please select an option: ")
            if choice in acceptable_values:
                return choice
            elif not choice.isnumeric():
                print("Please enter a number! ")
            else:
                choice = int(choice)
                if choice not in range(index, len(self.options + index)):
                    print("That option is not in the list! Please try again")
        return choice

    def get_option(self, item):
        if item in range(len(self.options)):
            return self.options[item]
        else:
            raise Exception("Item not in list")

    def get_ioption(self, item):
        if item - self.index in range(len(self.options)):
            return self.options[item - self.index]

    def get_length(self):
        return len(self.options)

    def get_header():
        return self.header

    def set_header(new_header):
        self.header = new_header
