class RAM:
    def __init__(self, size):
        self.size = size
        self.frames = []

class HD:
    def __init__(self, size):
        self.size = size

class PageTable:
    def __init__(self):
        self.p = 0
        self.m = 0
        self.frames = []

class Process:
    def __init__(self, id):
        self.id = id
        self.page_table = PageTable()

class SO:
    def __init__(self):
        self.hd = HD(1)
        self.ram = RAM(1)
        self.processes = []
    
    def execute(self, process_id, command, end=None):
        if command == 'P':
            pass
        elif command == 'I':
            pass
        elif command == 'C':
            pass
        elif command == 'R':
            pass
        elif command == 'W':
            pass 
        elif command == 'T':
            pass
        else:
            print("Invalid command '{}'. Exiting...".format(command))
            raise SystemExit()

    def read_instructions(self):
        instructions = []
        for i in range(1):
            instructions.append(input())
        return instructions

if __name__ == '__main__':
    so = SO()
    instructions = so.read_instructions()
    for i in instructions:
        process_id, command, *end = i.split()
        so.execute(process_id, command, end)
