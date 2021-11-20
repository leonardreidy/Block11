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

from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.ButtonElement import ButtonElement

class blockFaders(ModeSelectorComponent):
    __module__ = __name__
    __doc__ = ' Block Fader Mode Assignments '

    def __init__(self, parent, mixer, transport):
        assert isinstance(mixer, MixerComponent)
        ModeSelectorComponent.__init__(self)
        self._parent = parent
        self._controls = None
        self._mixer = mixer
        self._transport = transport
        self._fader_mode_names = ['MASTER VOL / CUE', 'MASTER PAN / XFADE', 'TEMPO / TEMPO FINE']
        self._last_fader_mode = 'MASTER VOL / CUE'


    def disconnect(self):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._controls = None
        self._mixer = None
        self._transport = None

        ModeSelectorComponent.disconnect(self)
        
        
    
    def set_modes_buttons(self, buttons):
        assert ((buttons == None) or (isinstance(buttons, tuple) or (len(buttons) == self.number_of_modes())))
        identify_sender = True
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if (buttons != None):
            for button in buttons:
                assert isinstance(button, ButtonElement)
                self._modes_buttons.append(button)
                button.add_value_listener(self._mode_value, identify_sender)

        self.set_mode(0)
        self.update()



    def set_controls(self, controls):
        assert ((controls == None) or (isinstance(controls, tuple) and (len(controls) == 2)))
        self._controls = controls
        self.set_mode(0)
        self.update()



    def number_of_modes(self):
        return 3



    def on_enabled_changed(self):
        self.update()
     
        
    def update(self):
        assert (self._modes_buttons != None)
        if self.is_enabled():
            if (self._controls != None):
                if (self._mode_index == 0):
                    self._mixer.master_strip().set_pan_control(None)
                    self._mixer.set_crossfader_control(None)
                    self._transport.set_tempo_control(None, None) 
                    self._mixer.master_strip().set_volume_control(self._controls[0])
                    self._mixer.set_prehear_volume_control(self._controls[1])
                elif (self._mode_index == 1):
                    self._mixer.master_strip().set_volume_control(None)
                    self._mixer.set_prehear_volume_control(None)
                    self._transport.set_tempo_control(None, None) 
                    self._mixer.master_strip().set_pan_control(self._controls[0])
                    self._mixer.set_crossfader_control(self._controls[1])
                elif (self._mode_index == 2):
                    self._controls[0].release_parameter()
                    self._transport.set_tempo_control(self._controls[0], self._controls[1])
                    self._mixer.master_strip().set_volume_control(None)
                    self._mixer.set_prehear_volume_control(None)
                    self._mixer.master_strip().set_pan_control(None)
                    self._mixer.set_crossfader_control(None)
                    
                else:
                    print 'Invalid mode index'
                    assert False
                mode = self._fader_mode_names[self._mode_index]
                if (mode != self._last_fader_mode):
                    self._parent.show_message("FADER MODE = " + str(mode))
                    self._last_fader_mode = mode
                        
                #self._rebuild_callback()
 