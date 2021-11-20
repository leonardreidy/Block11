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
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
SHOW_PLAYING_CLIP_DELAY = 5
class blockGlobal(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Global control for Block Script '

    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
        self._play_btn = None
        self._unall_btn = None
        self._cursor_btn = None
        self._gqntz_btn = None
        self._rqntz_btn = None
        self._bpm_btn = None
        self._clip_rec_btn = None
        self._device_nav_button = None
        self._view_control = None
        
        self._last_gqntz = 4
        self._last_rqntz = 5
        self._clip_flag = -1
        self._rqs = ['None', '1/4', '1/8', '1/8T', '1/8 + 1/8T', '1/16', '1/16T', '1/16 + 1/16T', '1/32']        
        
        self._register_timer_callback(self._on_timer)
              

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        if (self._clip_rec_btn != None):
            self._clip_rec_btn.remove_value_listener(self._clip_rec)
            self._clip_rec_btn = None
        if (self._play_btn != None):
            self._play_btn.remove_value_listener(self._play)
            self._play_btn = None
        if (self._unall_btn != None):
            self._unall_btn.remove_value_listener(self._unall)
            self._unall_btn = None
        if (self._cursor_btn != None):
            self._cursor_btn.remove_value_listener(self._cursor)
            self._cursor_btn = None
        if (self._bpm_btn != None):
            self._bpm_btn.remove_value_listener(self._bpm)
            self._bpm_btn = None
        if (self._gqntz_btn != None):
            self._gqntz_btn.remove_value_listener(self._gqntz)
            self._gqntz_btn = None
        if (self._rqntz_btn != None):
            self._rqntz_btn.remove_value_listener(self._rqntz)
            self._rqntz_btn = None
        if (self._device_nav_button != None):
            self._device_nav_button.remove_value_listener(self._nav_value)
            self._device_nav_button = None
        if (self._view_control != None):
            self._view_control.remove_value_listener(self._view)
            self._view_control = None
            

    def set_play_btn(self, button):
        if (self._play_btn != None):
            self._play_btn.remove_value_listener(self._play)
        self._play_btn = button
        if (self._play_btn != None):
            self._play_btn.add_value_listener(self._play)
            
        
    def _play(self, value):
        assert (self._play_btn != None)
        assert (value in range(16))
        if self.song().is_playing == False:
            self.song().is_playing = True
        elif self.song().is_playing == True:
            self.song().is_playing = False
                    
                    
    def set_unall_btn(self, button):
        if (self._unall_btn != None):
            self._unall_btn.remove_value_listener(self._unall)
        self._unall_btn = button
        if (self._unall_btn != None):
            self._unall_btn.add_value_listener(self._unall)
            
        
    def _unall(self, value):
        assert (self._unall_btn != None)
        assert (value in range(16))
        if value == 1:
            for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
                if track.mute:
                    track.mute = False
        if value == 2:
            for track in tuple(self.song().tracks) + tuple(self.song().return_tracks):
                if track.solo:
                    track.solo = False
        if value == 3:
            for track in tuple(self.song().tracks):
                if (track.can_be_armed and track.arm):
                    track.arm = False
                    
                    
    def set_cursor_btn(self, button):
        if (self._cursor_btn != None):
            self._cursor_btn.remove_value_listener(self._cursor)
        self._cursor_btn = button
        if (self._cursor_btn != None):
            self._cursor_btn.add_value_listener(self._cursor) 
            
            
    def _cursor(self, value):
        assert (self._cursor_btn != None)
        assert (value in range(128))
        modifier_pressed = True
        if (value == 1):
            if self.application().view.is_view_visible('Session'):
                self.application().view.scroll_view(Live.Application.Application.View.NavDirection.up, '', (not modifier_pressed))
            else:
                self.application().view.zoom_view(Live.Application.Application.View.NavDirection.up, '', (not modifier_pressed))
        if (value == 2):
            if self.application().view.is_view_visible('Session'):
                self.application().view.scroll_view(Live.Application.Application.View.NavDirection.down, '', (not modifier_pressed))
            else:
                self.application().view.zoom_view(Live.Application.Application.View.NavDirection.down, '', (not modifier_pressed))
        if (value == 3):
            if self.application().view.is_view_visible('Session'):
                self.application().view.scroll_view(Live.Application.Application.View.NavDirection.left, '', (not modifier_pressed))
            else:
                self.application().view.scroll_view(Live.Application.Application.View.NavDirection.up, '', (not modifier_pressed))
        if (value == 4):
            if self.application().view.is_view_visible('Session'):
                self.application().view.scroll_view(Live.Application.Application.View.NavDirection.right, '', (not modifier_pressed))
            else:
                self.application().view.scroll_view(Live.Application.Application.View.NavDirection.down, '', (not modifier_pressed))
                
                
    def set_bpm_btn(self, button):
        if (self._bpm_btn != None):
            self._bpm_btn.remove_value_listener(self._bpm)
        self._bpm_btn = button
        if (self._bpm_btn != None):
            self._bpm_btn.add_value_listener(self._bpm)   
            
        
    def _bpm(self, value):
        assert (self._bpm_btn != None)
        assert (value in range(128))
        if (value == 1):
            step = 1
        if (value == 2):
            step = -1
        tempo = max(20, min(999, (self.song().tempo + step)))
        self.song().tempo = tempo
 
        
    def set_gqntz_btn(self, button):
        if (self._gqntz_btn != None):
            self._gqntz_btn.remove_value_listener(self._gqntz)
        self._gqntz_btn = button
        if (self._gqntz_btn != None):
            self._gqntz_btn.add_value_listener(self._gqntz)
            
            
    def _gqntz(self, value):
        assert (self._gqntz_btn != None)
        assert (value in range(14))
        q = self.song().clip_trigger_quantization
        if (value == 1):
            q = q + 1
        if (value == 2):
            q = q - 1
        if (value == 3):
            if q == 0:
                q = self._last_gqntz
            elif q != 0:
                self._last_gqntz = q
                q = 0
        if q >= 0 and q <= 13:
            self.song().clip_trigger_quantization = q  
            self._gqntz_btn.send_value(self.song().clip_trigger_quantization)
            
            
    def set_rqntz_btn(self, button):
        if (self._rqntz_btn != None):
            self._rqntz_btn.remove_value_listener(self._rqntz)
        self._rqntz_btn = button
        if (self._rqntz_btn != None):
            self._rqntz_btn.add_value_listener(self._rqntz)
            
            
    def _rqntz(self, value):
        assert (self._rqntz_btn != None)
        assert (value in range(14))
        q = self.song().midi_recording_quantization
        if (value == 1):
            q = q + 1
        if (value == 2):
            q = q - 1
        if (value == 3):
            if q == 0:
                q = self._last_rqntz
            elif q != 0:
                self._last_rqntz = q
                q = 0
        if q >= 0 and q <= 8:
            self.song().midi_recording_quantization = q  
            self._rqntz_btn.send_value(self.song().midi_recording_quantization)
            newq = self._rqs[q]
            self._parent.show_message("Record Quantization value is " + str(newq))
            
            
    def set_device_nav_button(self, button):
        if (self._device_nav_button != None):
            self._device_nav_button.remove_value_listener(self._nav_value)
        self._device_nav_button = button
        if (self._device_nav_button != None):
            self._device_nav_button.add_value_listener(self._nav_value) 
            
    
    def _nav_value(self, value):
        assert (self._device_nav_button != None)
        assert (value in range(128))
        modifier_pressed = True
        if ((not self.application().view.is_view_visible('Detail')) or (not self.application().view.is_view_visible('Detail/DeviceChain'))):
            self.application().view.show_view('Detail')
            self.application().view.show_view('Detail/DeviceChain')
        else:
            d = Live.Application.Application.View.NavDirection
            if value == 1:
                self.application().view.scroll_view(d.right, 'Detail/DeviceChain', (not modifier_pressed))
            if value == 2:
                self.application().view.scroll_view(d.left, 'Detail/DeviceChain', (not modifier_pressed))
         
                
    def set_view_control(self, button):
        if (self._view_control != None):
            self._view_control.remove_value_listener(self._view)
        self._view_control = button
        if (self._view_control != None):
            self._view_control.add_value_listener(self._view) 
            
    
    def _view(self, value):
        assert (self._view_control != None)
        assert (value in range(128))
        if value == 1:
            if self.application().view.is_view_visible('Browser'):
                self.application().view.hide_view('Browser')
                self.application().view.focus_view('')
            else:
                self.application().view.show_view('Browser')
                if self.application().view.is_view_visible('Browser'):
                    self.application().view.focus_view('Browser')
        if value == 2:
            if self.application().view.is_view_visible('Session'):
                self.application().view.hide_view('Session')
            else:
                assert self.application().view.is_view_visible('Arranger')
                self.application().view.hide_view('Arranger')
        if value == 3:
            if (not self.application().view.is_view_visible('Detail')):
                self.application().view.show_view('Detail')
            if (not self.application().view.is_view_visible('Detail/DeviceChain')):
                self.application().view.show_view('Detail/DeviceChain')
            else:
                self.application().view.show_view('Detail/Clip')
        if value == 4:
            if (self.application().view.is_view_visible('Detail')):
                self.application().view.hide_view('Detail')
            else:
                self.application().view.show_view('Detail')      
 
            
    def set_clip_rec_btn(self, button):
        if (self._clip_rec_btn != None):
            self._clip_rec_btn.remove_value_listener(self._clip_rec)
        self._clip_rec_btn = button
        if (self._clip_rec_btn != None):
            self._clip_rec_btn.add_value_listener(self._clip_rec)
                    
            
    def _clip_rec(self, value):
        assert (value in range(128))
        assert (self._clip_rec_btn != None)
        clip_slot = self.song().view.highlighted_clip_slot
        track = self.song().view.selected_track
        if track in self.song().tracks and track.is_foldable == 0:
            self._clip_flag = -1
            if clip_slot.clip:
                self.song().view.highlighted_clip_slot.fire()
            else:
                self.song().view.highlighted_clip_slot.fire()
                if (track.arm == 1 and (self.song().clip_trigger_quantization != 0)):
                    self._clip_flag = 1
            
            
    def _on_timer(self):
        clip_slot = self.song().view.highlighted_clip_slot
        clip_val = 0
        if (clip_slot and clip_slot.clip):
            if (self._clip_flag == 1):
                if clip_slot.clip.is_playing:
                    od = self.song().overdub
                    if (od == 1):
                        self.song().overdub = 0
                        self.song().view.highlighted_clip_slot.fire()
                        self.song().overdub = 1
                    else:
                        self.song().view.highlighted_clip_slot.fire()
                    self._clip_flag = -1
            if clip_slot.clip.is_playing or clip_slot.clip.is_recording or clip_slot.clip.is_triggered:
                clip_val = 1
        self._clip_rec_btn.send_value(clip_val)
        self._gqntz_btn.send_value(self.song().clip_trigger_quantization)
        self._rqntz_btn.send_value(self.song().midi_recording_quantization)
                    
                    
    def on_enabled_changed(self):
        pass


    def update(self):    
        pass     
                    
