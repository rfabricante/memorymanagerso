import math

NEW = "NEW"
READY = "READY"
FINISHED = "FINISHED"

frame_size = 128
mp_size = 8 * 1024
ms_size = 32 * 1024
num_frames_per_page = 20 

class Frame:
    def __init__(self, available, info, process_id="", u=1):
        self.available = available
        self.info = info
        self.u = u
        self.process_id = process_id

class RAM:
    def __init__(self, size):
        self.size = size
        self.frames = [Frame(True, 0)] * (size/frame_size)
        self.pointer = 0

    def allocate(self, index, info=0): 
        self.frames[index].available = False
        self.frames[index].info = info
        self.pointer = index

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

    def get_row_by_frame_index(self, index): 
        for row in self.rows:
            if row.frame == index:
                return row

    def set_row(self, page_number, frame):
        if self.rows >= page_number:
            self.rows[page_number].frame = frame
            self.rows[page_number].p = 1
            return

        print("Invalid row {} for process {}. Exiting...".format(page_number, self.process))
        raise SystemExit()

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
            self.terminate_process(process_id)
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
            return
        


    def terminate_process(self, process_id):
        frames = self.page_tables[process_id].getFrames()    
        for key in frames:
            if frames[key] == 0:
                self.ram.free(key) 
            else: 
                pass

        self.page_tables[process_id].state = FINISHED
        

    def u_clock(self, page_table, page_number):
        for f in self.ram.frames:
            pointer = self.ram.pointer % len(self.ram.frames)
            current_frame = self.ram.frames[pointer]
            if current_frame.u == 0:
                process_id = current_frame.process_id
                row = self.page_tables[process_id].get_row_by_frame_index(pointer)
                if row.m == 0:
                    row.p = 0
                    page_table.set_row(page_number, pointer)
                    self.ram.pointer += 1
                else: 
                    pass
            elif current_frame.u == 1: 
                current_frame.u = 0
                self.ram.pointer += 1


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

