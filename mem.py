from util import *

TLB_MAX_SIZE = 16
tlb = []
# index=<queue>, val=vaddr.num

PAGE_TABLE_SIZE = 2**8
page_table = [None]*PAGE_TABLE_SIZE
# index=vaddr.num, val=(paddr | None)
fifo = []
# index=<queue>, val=vaddr.num

PHYSICAL_FRAME_COUNT = None # assigned by command line
#backing_store = []

# ---- TLB --------------------------------------------------------------
def check_tlb(vaddr):
    if type(vaddr) is not VirtualAddr:
        raise Exception(f"not a VirtualAddr: {vaddr}")

    # case: vaddr not in cache
    if vaddr.num not in tlb:
        return None

    return check_page_table(vaddr)

def tlb_evict_vnum(vnum):
    if type(vnum) is not int:
        raise Exception(f"not an int (vnum): {vnum}")
    try:
        tlb.remove(vnum) 
    except ValueError:
        pass

def cache(vaddr):
    tlb_evict_vnum(vaddr.num)

    if type(vaddr) is not VirtualAddr:
        raise Exception(f"not a VirtualAddr: {vaddr}")
    tlb.insert(0, vaddr.num)

    if len(tlb) > TLB_MAX_SIZE:
        tlb.pop()


# -----------------------------------------------------------------------


# ---- PAGE TABLE -------------------------------------------------------

def check_page_table(vaddr):
    if type(vaddr) is not VirtualAddr:
        raise Exception(f"not a VirtualAddr: {vaddr}")

    return page_table[vaddr.num]

# FIFO implementation
def assign_paddr(vaddr, algorithm):
    if type(vaddr) is not VirtualAddr:
        raise Exception(f"not a VirtualAddr: {vaddr}")
  
    return algorithm.put(vaddr.num, page_table, tlb_evict_vnum)
    #page_table[vaddr.num] = 1

    # XXX: entries are not getting removed from the TLB

    # case: evict a page
    # if len(fifo) == PHYSICAL_FRAME_COUNT:
    #     evict_vnum = fifo.pop()
    #     if type(evict_vnum) is not int:
    #         raise Exception(f"not an int (vnum): {evict_vnum}")
    #     page_table[evict_vnum] = None
    #     tlb_evict_vnum(evict_vnum)
    # 
    # fifo.insert(0, vaddr.num)
    # page_table[vaddr.num] = 1
    
    pass


# -----------------------------------------------------------------------
