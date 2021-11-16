# L3n 2021
# Ableton Live v11.5.0

import Live
import math
import sys
import logging
from re import *
from itertools import chain, starmap

from ableton.v2.base import inject, listens, listens_group, nop
from ableton.v2.control_surface import ControlSurface, ControlElement, Layer, Skin, PrioritizedResource, Component, ClipCreator, DeviceBankRegistry
from ableton.v2.control_surface.elements import EncoderElement, ComboElement, ButtonMatrixElement, DoublePressElement, MultiElement, DisplayDataSource, SysexElement
from ableton.v2.control_surface.components import ClipSlotComponent, SceneComponent, SessionComponent, TransportComponent, BackgroundComponent, ViewControlComponent, SessionRingComponent, SessionRecordingComponent, SessionNavigationComponent, MixerComponent, PlayableComponent
from ableton.v2.control_surface.components.mixer import SimpleTrackAssigner
from ableton.v2.control_surface.control import control_color
from ableton.v2.control_surface.mode import AddLayerMode, ModesComponent, DelayMode
from ableton.v2.control_surface.elements.physical_display import PhysicalDisplayElement
from ableton.v2.control_surface.components.session_recording import *
from ableton.v2.control_surface.control import PlayableControl, ButtonControl, control_matrix

from .Map import *
from .debug import initialize_debug
logger = logging.getLogger(__name__)
debug = initialize_debug()

# Pasted en masse; review!
MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
MIDI_PB_TYPE = 2
MIDI_MSG_TYPES = (MIDI_NOTE_TYPE, MIDI_CC_TYPE, MIDI_PB_TYPE)
MIDI_NOTE_ON_STATUS = 144
MIDI_NOTE_OFF_STATUS = 128
MIDI_CC_STATUS = 176
MIDI_PB_STATUS = 224

def is_device(device):
	return (not device is None and isinstance(device, Live.Device.Device) and hasattr(device, 'name'))


def make_pad_translations(chan):
	return tuple((x%4, int(x/4), x+8, chan) for x in range(8))

def return_empty():
	return []

if initialize_debug:
	debug = initialize_debug()

class SpecialSessionRingComponent(SessionRingComponent):

    _linked_session_ring = None

    @listens('offset')
    def _on_linked_offset_changed(self, track_offset, scene_offset):
        debug('new linked offset: ', track_offset, scene_offset)
        self.set_offsets(track_offset, scene_offset)

    def set_linked_session_ring(self, session_ring):
        self._linked_session_ring = session_ring
        self._on_linked_offset_changed.subject = self._linked_session_ring

        