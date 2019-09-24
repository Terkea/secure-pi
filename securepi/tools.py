import os
import time
import sys

# Check if os is linux
def linux_interaction():
    if (sys.platform.startswith('linux')):
        return True
    else:
        return False

# returns CPU temp
def measure_temp():
    try:
        if linux_interaction() == True:
            temp = os.popen("vcgencmd measure_temp").readline()
            return (temp.replace("temp=", "")).strip()
        else:
            return ('n\\a')
    except:
        return ('n\\a')

# returns Storage available
def get_machine_storage():
    try:
        if linux_interaction() == True:
            result = os.statvfs('/')
            block_size = result.f_frsize
            total_blocks = result.f_blocks
            free_blocks = result.f_bfree
            # giga=1024*1024*1024
            giga = 1000 * 1000 * 1000
            total_size = total_blocks * block_size / giga
            free_size = free_blocks * block_size / giga
            return ('%s GB' % free_size)
        else:
            return ('n\\a')
    except:
        return ('n\\a')