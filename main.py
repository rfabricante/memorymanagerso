import math

NEW = "NEW"
READY = "READY"
FINISHED = "FINISHED"
SUSPENDED = "SUSPENDED"

frame_size = 128
mp_size = 512
ms_size = 32 * 1024
num_pages_per_process = 16 

class Frame:
    def __init__(self, available, info, process_id="", u=1):
        self.available = available
        self.info = info
        self.u = u
        self.process_id = process_id

class RAM:
    def __init__(self, size):
        self.size = size
        self.frames = [None] * int(size/frame_size)
        self.pointer = 0

    def allocate(self, index, process_id, info=0): 
        frame = Frame(False, info, process_id)
        self.frames[index] = frame
        self.pointer = index + 1

    def free(self, index):
        self.frames[index].available = True

    def get_available_frames(self): 
        response = []
        for i in range(len(self.frames)):
            if self.frames[i] == None or self.frames[i].available:
                response.append(i)
        return response

class HD:
    def __init__(self, size):
        self.size = size

class Row:
    def __init__(self, p, m, frame=-1):
        self.p = p
        self.m = m
        self.frame = frame

    def __str__(self):
        return "{} {} {}".format(self.p, self.m, self.frame)

class PageTable:
    def __init__(self, process):
        self.process = process
        self.max_frames = num_pages_per_process
        self.rows = [None] * self.max_frames

    def allocate(self, index, frame):
        if index < self.max_frames:
            row = Row(1, 0, frame)
            self.rows[index] = row
            return

        print("Invalid row {} for process {}. Exiting...".format(index, self.process.id))
        raise SystemExit()

    def get_frames(self):
        frames = {}
        for r in self.rows:
            if r.p == 1:
                frames[r.frame] = r.m
        return frames

    def get_row_by_frame_index(self, index): 
        for row in self.rows:
            if row.frame == index:
                return row

    def is_suspended(self):
        for row in self.rows:
            if row == None:
                continue
            if row.p == 1:
                return False
        return True

    def __str__(self):
        string = "Table for process {}:\n".format(self.process.id)
        for i in range(len(self.rows)):
            string += "{}\n".format(self.rows[i])

        return string 
        

class Process:
    def __init__(self, id, size):
        self.id = id
        self.state = NEW
        self.size = size 
        self.num_frames = math.ceil(size/frame_size)

    def __str__(self): 
        return "Process with id {} and size {} is {}".format(self.id, self.size, self.state)

class SO:
    def __init__(self):
        self.hd = HD(ms_size)
        self.ram = RAM(mp_size)
        self.page_tables = {} # PageTable()
    
    def execute(self, process_id, command, inst=None):
        if command == 'P':
            pass
        elif command == 'I':
            pass
        elif command == 'C':
            self.create_process(process_id, int(*inst))
        elif command == 'R':
            pass
        elif command == 'W':
            pass 
        elif command == 'T':
            self.terminate_process(process_id)
        else:
            print("Invalid command '{}'. Exiting...".format(command))
            raise SystemExit()

        print(self.page_tables[process_id].process)
        print(self.page_tables[process_id])

    def create_process(self, process_id, size):
        print('Creating process {}'.format(process_id))
        process = Process(process_id, size)
        page_table = PageTable(process)  
        self.page_tables[process_id] = page_table
        available_frames = self.ram.get_available_frames()
        if len(available_frames) > 0: 
            for i in range(process.num_frames):
                if len(available_frames) > i:
                    frame = available_frames[i]
                    self.page_tables[process_id].allocate(i, frame)
                    self.ram.allocate(frame, process_id)
        else: 
            print("No available frame")
            self.u_clock(page_table, 0)
        
        self.page_tables[process_id].process.state = READY

    def terminate_process(self, process_id):
        print('Finishing process {}'.format(process_id))
        frames = self.page_tables[process_id].get_frames()    
        for key in frames:
            if frames[key] == 0:
                self.ram.free(key) 
            else: 
                pass
        self.page_tables[process_id].process.state = FINISHED
        

    def u_clock(self, page_table, page_number):
        process_id = "" 
        while True:
            pointer = self.ram.pointer % len(self.ram.frames)
            current_frame = self.ram.frames[pointer]
            if current_frame.u == 0:
                process_id = current_frame.process_id
                row = self.page_tables[process_id].get_row_by_frame_index(pointer)
                if row.m == 0:
                    row.p = 0
                    page_table.allocate(page_number, pointer)
                    self.ram.pointer += 1
                else: 
                    pass
                break
            elif current_frame.u == 1: 
                current_frame.u = 0
                self.ram.pointer += 1
        if self.page_tables[process_id].is_suspended(): 
            print("Suspending process {}".format(process_id))
            self.page_tables[process_id].process.state = SUSPENDED
            


def read_instructions():
    instructions = []
    for i in range(3):
        instructions.append(input())
    return instructions

if __name__ == '__main__':
    so = SO()
    instructions = read_instructions()
    for i in instructions:
        process_id, command, *inst = i.split()
        so.execute(process_id, command, inst)

# 32 bits endereço logico
# 128 kB tamanho do quadro
# 8 GB MP
# 256 GB MS
# 20 quadros por processo

