#Ohm64.py 
#This is a midi remote script for the Ohm64 by Michael Chenetz
#updated for Live9 by amounra

from __future__ import with_statement
import Live # This allows us (and the Framework methods) to use the Live API on occasion
import time # We will be using time functions for time-stamping our log file outputs

""" We are only using using some of the Framework classes them in this script (the rest are not listed here) """
from _Framework.ButtonElement import ButtonElement # Class representing a button a the controller
from _Framework.ButtonMatrixElement import ButtonMatrixElement 
from _Framework.ChannelStripComponent import ChannelStripComponent # Class attaching to the mixer of a given track
from _Framework.ClipSlotComponent import ClipSlotComponent # Class representing a ClipSlot within Live
from _Framework.CompoundComponent import CompoundComponent # Base class for classes encompasing other components to form complex components
from _Framework.ControlElement import ControlElement # Base class for all classes representing control elements on a controller
from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # Base class for all classes encapsulating functions in Live
from _Framework.InputControlElement import * # Base class for all classes representing control elements on a controller
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.SceneComponent import SceneComponent # Class representing a scene in Live
from _Framework.SessionComponent import SessionComponent # Class encompassing several scene to cover a defined section of Live's session
from _Framework.SessionZoomingComponent import DeprecatedSessionZoomingComponent as SessionZoomingComponent
from _Framework.SliderElement import SliderElement # Class representing a slider on the controller
from _Framework.TransportComponent import TransportComponent # Class encapsulating all functions in Live's transport section
from _Framework.EncoderElement import EncoderElement
from _Framework.DeviceComponent import DeviceComponent 



""" Here we define some global variables """
CHANNEL = 0 # Channels are numbered 0 through 15, this script only makes use of one MIDI Channel (Channel 1)
session = None #Global session object - global so that we can manipulate the same session object from within our methods 
mixer = None #Global mixer object - global so that we can manipulate the same mixer object from within our methods
# switchxfader = (240, 0, 1, 97, 2, 15, 1, 247)

class Block(ControlSurface):
	__module__ = __name__
	__doc__ = " Ohm64 controller script "
	
	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		with self.component_guard():
			# self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= Block opened =--------------") # Writes message into Live's main log file. This is a ControlSurface method.	   
			# self._send_midi(switchxfader)
			self._setup_transport_control()
			self._setup_mixer_control() # Setup the mixer object
			self._setup_session_control()  # Setup the session object
		

	def handle_sysex(self, midi_bytes):
		self._send_midi(240, 00, 1, 97, 2, 15, 1, 247)
		response = [int(0),int(0)]
		self.log_message(response)
	
	def _setup_transport_control(self):
		return

	def _setup_mixer_control(self):
		return

	def _setup_session_control(self):
		return
