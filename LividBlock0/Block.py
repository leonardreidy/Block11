#Ohm64.py 
#This is a midi remote script for the Ohm64 by Michael Chenetz
#updated for Live9 by amounra

import Live # This allows us (and the Framework methods) to use the Live API on occasion

from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, EncoderElement
from ableton.v2.control_surface.components import ClipSlotComponent, MixerComponent, SceneComponent, SessionComponent, TransportComponent # Class attaching to the mixer of a given track
from ableton.v2.control_surface import ControlSurface, ControlElement # Central base class for scripts based on the new Framework
# from .device import DeviceComponent



# Globals
CHANNEL = 0 # Channels are numbered 0 through 15, this script only makes use of one MIDI Channel (Channel 1)
session = None #Global session object - global so that we can manipulate the same session object from within our methods 
mixer = None #Global mixer object - global so that we can manipulate the same mixer object from within our methods

class Block(ControlSurface):
	
	def __init__(self, c_instance):
		super(Block, self).__init__(c_instance)
		with self.component_guard():
			# self._setup_transport_control()
			# self._setup_mixer_control() # Setup the mixer object
			self._setup_session_control()  # Setup the session object
		
	
	def _setup_transport_control(self):
		self

	def _setup_mixer_control(self):
		self

	def _setup_session_control(self):
		True
