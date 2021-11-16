# L3n 2021
# Ableton Live v11.5.0

from YaeltexUniversal.Map import PAN_CHANNEL, SESSION_BOX_SIZE, TRACK_PARAMETER_CCS, VU_METER_ENABLED, VU_METER_LOG_SCALING
from ableton.v2.control_surface.elements.color import Color
from .colors import *

VU_METER_LOG_SCALING = False
VU_METER_ENABLED = True

SESSION_BOX_SIZE = (8, 8) # maximum: 8 tracks x 8 scenes

MUTE_NOTES = list(range(8))
MUTE_CHANNEL = 0

SOLO_NOTES = list(range(8, 16))
SOLO_CHANNEL = 0

ARM_NOTES = list(range(16, 24))
ARM_CHANNEL = 0

SELECT_NOTES = list(range(24, 40))
SELECT_CHANNEL = 0

CROSSFADE_ASSIGN_NOTES = list(range(40, 48))
CROSSFADE_ASSIGN_CHANNEL = 0

VOLUME_CCS = list(range(8))
VOLUME_CHANNEL = 0

PAN_CCS = list(range(8, 16))
PAN_CHANNEL = 0

PARAMETER_ON_OFF_NOTE = 127
PARAMETER_CCS = list(range(16, 24))
PARAMETER_CHANNEL = 0

# TRACK_PARAMETER_ON_OFF_NOTES = list(range(72))
# TRACK_PARAMETER_ON_OFF_CHANNEL = 3

TRAC