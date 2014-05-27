import sys
import gtk
import gtk.glade
import pygtk
import glob
from hv_switching_board_rpc import HVSwitchingBoard
from dmf_control_board.dmf_control_board import DmfControlBoard
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

node = HVSwitchingBoard(glob.glob('/dev/ttyUSB*')[0])
control = DmfControlBoard()
control.connect()

builder = gtk.Builder()


class SwitchingBoardTest(object):

	def __init__(self):
		builder.add_from_file('switching_board_test.glade')
		builder.connect_signals(self)
		self.window = builder.get_object('window1')
		if (self.window):
			self.window.connect('destroy', gtk.main_quit)
		self.window.show()
		dic = {"on_button1_clicked" : gtk.main_quit}
		self.window.set_icon_from_file('switch-icon.png')

	def on_button2_clicked(self, widget):
		button1 = builder.get_object('button1')
		button1.set_label("Close")
		radiobutton1 = builder.get_object('radiobutton1')
		if radiobutton1.get_active():
			voltage = False
		else:
			voltage = True
		self.all_channel_feedback(voltage)

	def all_channel_feedback(self, voltage):
		if voltage:
			progressbar = builder.get_object('progressbar1')
			spacer = builder.get_object('label1')
			results_bool = builder.get_object('label3')
			results_bool.set_visible(False)
			self.window.resize(1,1)
			spacer.set_visible(False)
			progressbar.set_visible(True)
			control.amplifier_gain = 1
			control.set_waveform_frequency(10e3)
			control.set_waveform_voltage(1)
			feedback = []
			progressbar.set_fraction(0.0)
			for i in range(0, 40):
        			node.turn_on_channel(i)
        			results = control.measure_impedance(10, 5, 0, [])
        			results_frame = pd.DataFrame(list(results)).T
        			max_voltage = (6*results_frame[results_frame[3] >= 0][2].describe()['mean'] + (2 * results_frame[results_frame[3] >= 0][2].describe()['std']))
        			feedback_bool = 'Fail'
        			if int(max_voltage) >= 1:
           				if int(max_voltage) <= 2:
                				feedback_bool = 'Pass'
        			feedback.append(feedback_bool)
    			channel_response = pd.DataFrame(list(feedback), index=list(range(1, 41)))
			channel_bool = channel_response.to_string(header=False)
			spacer.set_visible(True)
			progressbar.set_visible(False)
			results_bool.set_text(channel_bool)
			results_bool.set_visible(True)
		else:
			progressbar = builder.get_object('progressbar1')
			spacer = builder.get_object('label1')
			results_bool = builder.get_object('label3')
			results_bool.set_visible(False)
			self.window.resize(1,1)
			spacer.set_visible(False)
			progressbar.set_visible(True)
			control.amplifier_gain = 1
			control.set_waveform_frequency(10e3)
			control.set_waveform_voltage(1)
			feedback = []
			progressbar.set_fraction(0.0)
			for i in range(0, 40):
				node.turn_on_channel(i)
				results = control.measure_impedance(10, 50, 0, [])
				results_frame = pd.DataFrame(list(results)).T
				max_voltage = (15*results_frame[results_frame[3] >= 0][2].describe()['mean'])
				feedback_bool = 'Fail'
				if int(max_voltage) >= 1:
					if int(max_voltage) <=2:
						feedback_bool = 'Pass'
				feedback.append(feedback_bool)
				while gtk.events_pending():
					gtk.main_iteration()
				new_value = progressbar.get_fraction() + 0.024
				progressbar.set_fraction(new_value)
			channel_response = pd.DataFrame(list(feedback), index=list(range(1, 41)))
			channel_bool = channel_response.to_string(header=False)
			spacer.set_visible(True)
			progressbar.set_visible(False)
			results_bool.set_text(channel_bool)
			results_bool.set_visible(True)

	def on_button1_clicked(self, button):
		gtk.main_quit()

if __name__ == "__main__":
	hwg = SwitchingBoardTest()
	gtk.main()
