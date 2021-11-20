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
class blockClip(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Clip Control for Block Script '

    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
        self.song().add_current_song_time_listener(self._on_time_changed)
        self._loop_btn = None
        self._chop_btn = None
        self._chrom_btn = None
        self._mode_select_btn = None
        self._mode = 'Off'
        self._last_loop = None
        self._length = None
        self._last_time = 0
        self._chop_factor = None
        self._register_timer_callback(self._on_timer)
        
               
    def disconnect(self):
        self.song().remove_current_song_time_listener(self._on_time_changed)
        self._unregister_timer_callback(self._on_timer)
        if (self._chop_btn != None):
            self._chop_btn.remove_value_listener(self._chop_val)
            self._chop_btn = None
        if (self._loop_btn != None):
            self._loop_btn.remove_value_listener(self._loop_value)
            self._loop_btn = None 
        if (self._chrom_btn != None):
            self._chrom_btn.remove_value_listener(self._chrom_val)
            self._chrom_btn = None 
        if (self._mode_select_btn != None):
            self._mode_select_btn.remove_value_listener(self._mode_select)
            self._mode_select_btn = None
                
                
    def set_mode_select_btn(self, button):
        if (self._mode_select_btn != None):
            self._mode_select_btn.remove_value_listener(self._mode_select)
        self._mode_select_btn = button
        if (self._mode_select_btn != None):
            self._mode_select_btn.add_value_listener(self._mode_select)
            
        
    def _mode_select(self, value):
        assert (self._mode_select_btn != None)
        assert (value in range(16))
        if value == 0:
            self._mode = 'Off'
            self._length = None
        if value == 1:
            self._chop_factor = 16
        if value == 2:
            self._chop_factor = 32
        if value == 3:
            self._chop_factor = None
        if value > 0:
            self._last_loop = None
            self._mode = 'Play'
            self._get_length()
            self._on_timer()
            
            
    def set_loop_btn(self, button):
        if (self._loop_btn != None):
            self._loop_btn.remove_value_listener(self._loop_value)
        self._loop_btn = button
        if (self._loop_btn != None):
            self._loop_btn.add_value_listener(self._loop_value)
            
        
    def _loop_value(self, value):
        assert (self._loop_btn != None)
        assert (value in range(128))
        clip = self.song().view.detail_clip
        if (clip):
            val = 0
            if (clip.looping==1):
                clip.looping = 0
            else:
                clip.looping = 1
                val = 32
            self._loop_btn.send_value(val)
            self._get_length()
       
    
    def set_chop_btn(self, button):
        if (self._chop_btn != None):
            self._chop_btn.remove_value_listener(self._chop_val)
        self._chop_btn = button
        if (self._chop_btn != None):
            self._chop_btn.add_value_listener(self._chop_val)
            
        
    def _chop_val(self, value):
        assert (self._chop_btn != None)
        assert (value in range(32))
        clip = self.song().view.detail_clip
        self._length = None
        if (clip):
            if ((clip.is_midi_clip) or ((clip.is_audio_clip) and (clip.warping==1))):
                chop = clip.length + clip.loop_start                
                if (clip.looping==True):
                    clip.looping = False
                    l = clip.length + clip.loop_start  
                    clip.looping = True
                    if (l < chop):
                        chop = l
                self._length = chop
                clip.loop_start = (chop/32) * value
                if (clip.looping==True):
                    clip.looping = False
                    clip.loop_start = (chop/32) * value
                    clip.looping = True
                clip.fire()
        
        
    def _get_length(self):
        clip = self.song().view.detail_clip
        if (clip):
            if ((clip.is_midi_clip) or ((clip.is_audio_clip) and (clip.warping==1))):
                chop = clip.length + clip.loop_start                
                if (clip.looping==True):
                    clip.looping = False
                    l = clip.length + clip.loop_start  
                    clip.looping = True
                    if (l < chop):
                        chop = l
                self._length = chop
      
                
                
    def set_chrom_btn(self, button):
        if (self._chrom_btn != None):
            self._chrom_btn.remove_value_listener(self._chrom_val)
        self._chrom_btn = button
        if (self._chrom_btn != None):
            self._chrom_btn.add_value_listener(self._chrom_val)
            
        
    def _chrom_val(self, value):
        assert (self._chrom_btn != None)
        assert (value in range(32))
        clip = self.song().view.detail_clip
        if (clip):
            if (clip.is_audio_clip):
                clip.pitch_coarse = value - 15
                clip.fire()
  
          
    def on_selected_track_changed(self):
        ControlSurfaceComponent.on_selected_track_changed(self)
        self.on_selected_scene_changed()
        
    
    def on_selected_scene_changed(self):
        self._length = None
        self._on_timer()
        
        
    def on_enabled_changed(self):
        pass

    
    def update(self):    
        pass     
    

    def _on_timer(self):
        force_send = True
        if (self._mode == 'Play'):
            slot = self.song().view.highlighted_clip_slot
            loop_val = 0
            if (slot and slot.clip):
                clip = slot.clip
                if (self._loop_btn != None):
                    if (clip.looping==1):
                        loop_val = 32
            if self._last_loop != loop_val:
                self._last_loop = loop_val
                self._loop_btn.send_value(loop_val, force_send)
                
                
    def _on_time_changed(self):   
        if (self._mode == 'Play'):
            if (self._length != None):
                slot = self.song().view.highlighted_clip_slot
                if (slot and slot.clip):
                    clip = slot.clip
                    if self._chop_factor != None and clip.is_playing == True:
                        p = clip.playing_position
                        l = self._length/self._chop_factor
                        n = int(p/l)
                        if ((n >= 0) and (n < self._chop_factor)):
                            if (n != self._last_time):
                                self._parent._send_midi((240, 0, 0, self._last_time, 1, 247))
                                self._last_time = n
                                self._parent._send_midi((240, 0, 0, n, 0, 247))
                                self._parent.schedule_message(5, self._clear) 
            else:
                self._clear()
                            
                            
    def _clear(self):
        slot = self.song().view.highlighted_clip_slot
        if (slot and slot.clip):
            clip = slot.clip
        if self.song().is_playing == False or self._length == None or (clip and clip.is_playing == False):
            if self._last_time:
                self._parent._send_midi((240, 0, 0, self._last_time, 1, 247))
      