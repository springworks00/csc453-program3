from collections import namedtuple

class VirtualAddr:
    def __init__(self, vaddr, loc):
        self.val = vaddr
        self.num = (vaddr >> 8) & 0xFF
        self.offset = vaddr & 0xFF
        self.addr_list_loc = loc

    def from_file(path):
        xs = []
        for i, addr in enumerate(open(path, "r").readlines()):
            xs.append(VirtualAddr(int(addr), i))
        return xs 
        #return list(map(lambda x: VirtualAddr(int(x)), open(path, 'r').readlines()))

    def __eq__(self, other):
        return self.num == other.num

    def __hash__(self):
        return hash(self.num)

    def __repr__(self):
        return f"VA(num={self.num})"

class Input:
    def __init__(self, argv):
        # ADDRESSES
        self.vaddrs = VirtualAddr.from_file(argv[1])

        # FRAMES
        if len(argv) >= 3:
            self.frames = int(argv[2])
        else:
            self.frames = 256

        # ALGORITHM
        if len(argv) >= 4 and argv[3] in ["FIFO", "LRU", "OPT", "BAD"]:
            self.algorithm = argv[3]
        else:
            self.algorithm = "FIFO"


class Output:
    def __init__(self, addr_count):
        self.addr_count = addr_count
        self.hits = 0
        self.misses = 0
        self.faults = 0

    def __eq__(self, other):
        return self.hits == other.hits and self.misses == other.misses and self.faults == other.faults

    def __repr__(self):
        fault_rate = self.faults / self.addr_count
        hit_rate = self.hits / (self.hits + self.misses)
        s = ""
        s += f"Number of Translated Addresses = {self.addr_count}\n"
        s += f"Page Faults = {self.faults}\n"
        s += "Page Fault Rate = {0:.3f}\n".format(fault_rate)
        s += f"TLB Hits = {self.hits}\n"
        s += f"TLB Misses = {self.misses}\n"
        s += "TLB Hit Rate = {0:.3f}".format(hit_rate)
        return s
