import glob
from hv_switching_board_rpc import HVSwitchingBoard
from dmf_control_board.dmf_control_board import DmfControlBoard
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

node = HVSwitchingBoard(glob.glob('/dev/ttyUSB*')[0])
control = DmfControlBoard()
control.connect()
