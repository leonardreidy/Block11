"""
# Copyright (C) 2013-2014 Stray <stray411@hotmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Stray <stray411@hotmail.com>
"""

import Live 
from _Framework.ButtonElement import ButtonElement  
from _Framework.ButtonMatrixElement import ButtonMatrixElement  
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ChannelTranslationSelector import ChannelTranslationSelector
from _Framework.ClipSlotComponent import ClipSlotComponent  
from _Framework.CompoundComponent import CompoundComponent  
from _Framework.ControlElement import ControlElement  
from _Framework.ControlSurface import ControlSurface  
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent  
from _Framework.DeviceComponent import DeviceComponent
from _Framework.InputControlElement import *  
from _Framework.SceneComponent import SceneComponent  
from _Framework.SessionComponent import SessionComponent  
from _Framework.SessionZoomingComponent import SessionZoomingComponent  
from _Framework.SliderElement import SliderElement  
from _Framework.TransportComponent import TransportComponent  
from .blockGlobal import blockGlobal
from .blockKnobs import blockKnobs
from .blockFaders import blockFaders
from .blockMixer import blockMixer
from .blockClip import blockClip

session = None  
mixer = None

class blockLive(ControlSurface):
    __module__ = __name__
    __doc__ = " blockLive script for Live 8 "
    
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.set_suppress_rebuild_requests(True) 
        is_momentary = True  
        self._refresh_button = None
        self._set_refresh_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 127)) 
        self._undo_button = None
        self._set_undo_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 126)) 
        mixer = self._setup_mixer_control()
        transport = self._setup_transport_control()
        device = self._setup_device_control()
        session = self._setup_session_control() 
        self._setup_global_control()
        self._setup_clip_control()
        self._setup_knobs(mixer, device)
        self._setup_faders(mixer, transport)
        self._send_midi((240, 127, 127, 127, 0, 247))
        self._suggested_input_port = 'From MT Player 1'
        self._suggested_output_port = 'To MT Player 1'
        preset = 'blockLive v1.0.6 for Live 8'
        live = Live.Application.get_application()
        major = live.get_major_version()
	if major == 9:
	    self.set_highlighting_session_component(session)
        minor = live.get_minor_version()
        fix = live.get_bugfix_version()
        self.log_message('NK LOG ------- Preset Version: ' + str(preset) + ' ------- Live Version: ' + str(major) + '.' + str(minor) + '.' + str(fix) + ' ------- END LOG')
        self.show_message(str(preset))
        self.set_suppress_rebuild_requests(False)  
        

    def disconnect(self):
        if (self._refresh_button != None):
            self._refresh_button.remove_value_listener(self._a_refresh)
            self._refresh_button = None
        if (self._undo_button != None):
            self._undo_button.remove_value_listener(self._a_undo)
            self._undo_button = None
            
            
    def _setup_knobs(self, mixer, device):
        is_momentary = True
        global_bank_buttons = []
        global_param_controls = []
        for index in range(8):
            global_param_controls.append(SliderElement(MIDI_CC_TYPE, 0, (115 + index)))
        global_bank_buttons = tuple([ ButtonElement((not is_momentary), MIDI_CC_TYPE, 15, (2 + index)) for index in range(11) ])
        encoder_modes = blockKnobs(self, mixer, device)
        encoder_modes.set_modes_buttons(global_bank_buttons)
        encoder_modes.set_btn_mode(SliderElement(MIDI_CC_TYPE, 15, 32))
        encoder_modes.set_controls(tuple(global_param_controls))
        global_translation_selector = ChannelTranslationSelector()
        global_translation_selector.set_controls_to_translate(tuple(global_param_controls))
        global_translation_selector.set_mode_buttons(global_bank_buttons)
        
        
    def _setup_faders(self, mixer, transport):
        is_momentary = True
        global_bank_buttons = []
        global_param_controls = []
        for index in range(2):
            global_param_controls.append(SliderElement(MIDI_CC_TYPE, 0, (113 + index)))
        global_bank_buttons = tuple([ ButtonElement((not is_momentary), MIDI_CC_TYPE, 15, (33 + index)) for index in range(3) ])
        encoder_modes = blockFaders(self, mixer, transport)
        encoder_modes.set_modes_buttons(global_bank_buttons)
        encoder_modes.set_controls(tuple(global_param_controls))
        global_translation_selector = ChannelTranslationSelector()
        global_translation_selector.set_controls_to_translate(tuple(global_param_controls))
        global_translation_selector.set_mode_buttons(global_bank_buttons)
     

    def _setup_session_control(self):
        is_momentary = True
        num_tracks = 8  
        num_scenes = 7  
        global session  
        session = SessionComponent(num_tracks, num_scenes)  
        session.set_offsets(0, 0)  
        session.selected_scene().set_launch_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 125))
        up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 120)
        down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 121)
        left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 122)
        right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 123)
        session.set_track_bank_buttons(right_button, left_button)
        session.set_scene_bank_buttons(down_button, up_button)  
        matrix = ButtonMatrixElement()   
        scene_launch_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, (index + 72)) for index in range(7) ]
        track_stop_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE,  15, (index + 64)) for index in range(8) ]
        session.set_stop_all_clips_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 79))
        session.set_stop_track_clip_buttons(tuple(track_stop_buttons))
        session.set_stop_track_clip_value(127)
        session.set_mixer(mixer)
        for scene_index in range(7):
            scene = session.scene(scene_index)
            button_row = []
            scene.set_launch_button(scene_launch_buttons[scene_index])
            scene.set_triggered_value(127)
            for track_index in range(8):
                session.selected_scene().clip_slot(track_index).set_launch_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, (80 + track_index)))
                button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, ((track_index * 8) + (scene_index)))
                button_row.append(button)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_triggered_to_play_value(2)
                clip_slot.set_triggered_to_record_value(2)
                clip_slot.set_stopped_value(1)
                clip_slot.set_started_value(3)
                clip_slot.set_recording_value(3)
                clip_slot.set_launch_button(button)
            matrix.add_row(tuple(button_row))
	ControlSurface._set_session_highlight(self, 0, 0, 8, 7, True)
        return session
 
            
    def _setup_mixer_control(self):
        is_momentary = True  
        global mixer
        mixer = blockMixer(8) 
        mixer.set_track_offset(0)  
        self.song().view.selected_track = mixer.channel_strip(0)._track 
	mixer.selected_strip().set_track(self.song().view.selected_track) 
        mixer.selected_strip().set_arm_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 19))
        mixer.master_strip().set_select_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 124))
        for track in range(8):
            strip = mixer.channel_strip(track)
            strip.set_select_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, (88 + track)))
            strip.set_mute_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, (96 + track)))
            strip.set_solo_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, (104 + track)))
            strip.set_arm_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, (112 + track)))
            strip.set_invert_mute_feedback(True)
        return mixer
    
    
    def _setup_device_control(self):
        is_momentary = True
        device = DeviceComponent()
        self.set_device_component(device)
        device.set_on_off_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 27))
        device.set_bank_nav_buttons(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 25), ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 26)) 
        return device 
    
            
    def _setup_global_control(self):
        is_momentary = True
        global_script = blockGlobal(self) 
        global_script.set_play_btn(SliderElement(MIDI_CC_TYPE, 15, 0))
        global_script.set_unall_btn(SliderElement(MIDI_CC_TYPE, 15, 1))
        global_script.set_cursor_btn(SliderElement(MIDI_CC_TYPE, 15, 15))
        global_script.set_clip_rec_btn(SliderElement(MIDI_CC_TYPE, 15, 20))
        global_script.set_bpm_btn(SliderElement(MIDI_CC_TYPE, 15, 23))
        global_script.set_gqntz_btn(SliderElement(MIDI_CC_TYPE, 15, 21))
        global_script.set_rqntz_btn(SliderElement(MIDI_CC_TYPE, 15, 22))
        global_script.set_device_nav_button(SliderElement(MIDI_CC_TYPE, 15, 24))
        global_script.set_view_control(SliderElement(MIDI_CC_TYPE, 15, 13))
        
        
    def _setup_transport_control(self):
        is_momentary = True  
        transport = TransportComponent()  
        transport.set_record_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 18))
        transport.set_overdub_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 17))
        transport.set_metronome_button(ButtonElement(is_momentary, MIDI_CC_TYPE, 15, 16))
        return transport
        
    def _setup_clip_control(self):
        clip_ctrl = blockClip(self)
        clip_ctrl.set_chop_btn(SliderElement(MIDI_CC_TYPE, 15, 28))
        clip_ctrl.set_chrom_btn(SliderElement(MIDI_CC_TYPE, 15, 29))
        clip_ctrl.set_loop_btn(SliderElement(MIDI_CC_TYPE, 15, 30))
        clip_ctrl.set_mode_select_btn(SliderElement(MIDI_CC_TYPE, 15, 31))

        
    def _set_refresh_button(self, button): 
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._refresh_button != None):
            self._refresh_button.remove_value_listener(self._a_refresh)
        self._refresh_button = button
        if (self._refresh_button != None):
            self._refresh_button.add_value_listener(self._a_refresh)
            
            
    def _a_refresh(self, value): 
        assert (self._refresh_button != None)
        assert (value in range(128))
        if ((value != 0) or (not self._refresh_button.is_momentary())):
            ControlSurface.refresh_state(self)
            
            
    def _set_undo_button(self, button): 
        assert ((button == None) or isinstance(button, ButtonElement))
        if (self._undo_button != None):
            self._undo_button.remove_value_listener(self._a_undo)
        self._undo_button = button
        if (self._undo_button != None):
            self._undo_button.add_value_listener(self._a_undo)
            
            
    def _a_undo(self, value): 
        assert (self._undo_button != None)
        assert (value in range(128))
        if ((value != 0) or (not self._undo_button.is_momentary())):
            self.song().undo()
            
            
    def _on_selected_track_changed(self):
        ControlSurface._on_selected_track_changed(self)
        track = self.song().view.selected_track
        device_to_select = track.view.selected_device
        if ((device_to_select == None) and (len(track.devices) > 0)):
            device_to_select = track.devices[0]
        if (device_to_select != None):
            self.song().view.select_device(device_to_select)
        self._device_component.set_device(device_to_select)
        
                
    def disconnect(self):
        ControlSurface.disconnect(self)
        return None