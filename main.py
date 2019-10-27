import math

NEW = "NEW"
READY = "READY"

frame_size = 128
mp_size = 8 * 1024
ms_size = 32 * 1024
num_frames_per_page = 20 

class Frame:
    def __init__(self, available, info):
        self.available = available
        self.info = info

class RAM:
    def __init__(self, size):
        self.size = size
        self.frames = [Frame(True, 0)] * (size/frame_size)

    def allocate(self, index, info=0): 
        self.frames[index].available = False
        self.frames[index].info = info

    def free(self, index):
        self.frames[index].available = True

    def getAvailablesFrames(self): 
        response = []
        for i in range(frames):
            if frames[i].available:
                response.append(i)
        return response

class HD:
    def __init__(self, size):
        self.size = size

class Row:
    def __init__(self, p, m, framse):
        self.p = 0
        self.m = 0
        self.frame = -1

class PageTable:
    def __init__(self, process):
        self.process = process
        self.max_frames = num_frames_per_page
        self.rows = []

    def allocate(self, frame):
        if len(self.rows) < self.max_frames: 
            self.rows.append(Row(1, 0, frame))

    def getFrames(self):
        frames = {}
        for r in rows:
            if r.p == 1:
                frames[r.frame] = r.m
        return frames

class Process:
    def __init__(self, id, size):
        self.id = id
        self.state = NEW
        self.size = size 
        self.num_frames = math.ceil(size/frame_size)

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
            self.create_process(process_id, inst)
        elif command == 'R':
            pass
        elif command == 'W':
            pass 
        elif command == 'T':
            pass
        else:
            print("Invalid command '{}'. Exiting...".format(command))
            raise SystemExit()

    def create_process(self, process_id, size):
        process = Process(process_id, size)
        page_table = PageTable(process)  
        self.page_tables[process_id] = page_table
        available_frames = self.ram.getAvailablesFrames()
        if len(available_frames) > 0: 
            for i in range(process.num_frames):
                if len(available_frames) > i:
                    frame = available_frames[i]
                    self.page_tables[process_id].allocate(frame)
                    self.ram.allocate(frame)

            self.page_tables[process_id].process.state = READY

    def terminate_process(self, process_id):
        frames = self.page_tables[process_id].getFrames()    
        for key in frames:
            if frames[key] == 0:
                self.ram.free(key) 
            else: 
                pass
            

            

def read_instructions():
    instructions = []
    for i in range(1):
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