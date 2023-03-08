from util import *

class OPTCache:
    def __init__(self, capacity, all_vaddrs): #, reference_string):
        self.capacity = capacity
        #self.reference_string = reference_string
        self.cache = []
        self.all_vaddrs = all_vaddrs
        self.pnum_assigner = 0

    def register_get(self, vaddr):
        pass

    def put(self, new_vaddr, page_table, tlb_evict):
        new_vnum = new_vaddr.num
        if len(self.cache) >= self.capacity:
            #print("too large")
            # collect future_access metrics
            future_accesses = {}
            i = new_vaddr.addr_list_loc
            for other_vnum in self.cache:
                future_accesses[other_vnum] = float('inf')
                tmp = VirtualAddr(other_vnum, 0)

                for j in range(i, len(self.all_vaddrs)):
                    if self.all_vaddrs[j].num == other_vnum:
                        break
                # DOES NOT ACCOUNT FOR NOT-FOUND (no infs make it through)
                distance = j - new_vaddr.addr_list_loc
                future_accesses[other_vnum] = distance

            #print("\n", future_accesses, "->", self.all_vaddrs[i:], "\n")
            
            
            # evict the farthest in the future
            evict_vnum = max(future_accesses, key=future_accesses.get)
            evict_pnum = page_table[evict_vnum]
            page_table[evict_vnum] = None
            self.cache.remove(evict_vnum)

            tlb_evict(evict_vnum)
            new_pnum = evict_pnum
        else:
            new_pnum = self.pnum_assigner
            self.pnum_assigner += 1

        self.cache.append(new_vnum)
        page_table[new_vnum] = new_pnum


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []
        self.pnum_assigner = 0

    def register_get(self, vaddr):
        vnum = vaddr.num
        try: 
            self.cache.remove(vnum)
            self.cache.append(vnum)
        except ValueError:
            pass

    def put(self, new_vaddr, page_table, tlb_evict):
        new_vnum = new_vaddr.num
        if len(self.cache) >= self.capacity:
            evict_vnum = self.cache.pop(0)
            evict_pnum = page_table[evict_vnum]
            page_table[evict_vnum] = None
            tlb_evict(evict_vnum)
            new_pnum = evict_pnum
        else:
            new_pnum = self.pnum_assigner
            self.pnum_assigner += 1
        self.cache.append(new_vnum)
        page_table[new_vnum] = new_pnum


class FIFOCache:
    def __init__(self, capacity):
        self.cache = []
        self.capacity = capacity
        self.pnum_assigner = 0

    def register_get(self, vaddr):
        pass

    def put(self, new_vaddr, page_table, tlb_evict):
        new_pnum = None
        new_vnum = new_vaddr.num
        
        if len(self.cache) >= self.capacity:
            evict_vnum = self.cache.pop()
            evict_pnum = page_table[evict_vnum]
            page_table[evict_vnum] = None
            tlb_evict(evict_vnum)
            new_pnum = evict_pnum
        else:
            new_pnum = self.pnum_assigner
            self.pnum_assigner += 1

        self.cache.insert(0, new_vnum)
        page_table[new_vnum] = new_pnum
        return new_pnum

# Not Recently Used
# -> evicts the most recently used page
# not particularly creative 
class BADCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []
        self.pnum_assigner = 0

    def register_get(self, vaddr):
        vnum = vaddr.num
        try: 
            self.cache.remove(vnum)
            self.cache.append(vnum)
        except ValueError:
            pass

    def put(self, new_vaddr, page_table, tlb_evict):
        new_vnum = new_vaddr.num

        if len(self.cache) >= self.capacity:
            evict_vnum = self.cache.pop()
            evict_pnum = page_table[evict_vnum]
            page_table[evict_vnum] = None
            tlb_evict(evict_vnum)
            new_pnum = evict_pnum
        else:
            new_pnum = self.pnum_assigner
            self.pnum_assigner += 1
        self.cache.append(new_vnum)
        page_table[new_vnum] = new_pnum
