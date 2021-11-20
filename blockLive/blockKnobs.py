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
from _Framework.ButtonElement import ButtonElement
from _Framework.DeviceComponent import DeviceComponent
from _Framework.MixerComponent import MixerComponent

class blockKnobs(ModeSelectorComponent):
    __module__ = __name__
    __doc__ = ' Block Knob Mode Assignments '

    def __init__(self, parent, mixer, device):
        assert isinstance(mixer, MixerComponent)
        ModeSelectorComponent.__init__(self)
        self._parent = parent
        self._controls = None
        self._mixer = mixer
        self._device = device
        self._btn_mode = None 
        self._btn_mode_names = ['LAUNCH', 'TRACK', 'CLIP', 'DRUM', 'CHROMATIC', 'LEARN', 'USER 1', 'USER 2']
        self._knob_mode_names = ['VOLUME', 'PAN', 'DEVICE', 'SEND A', 'SEND B', 'SEND C', 'SEND D', 'SEND E', 'SEND F', 'SEND G', 'SEND H']
        self._last_knob_mode = 'VOLUME'
        self._last_btn_mode = 'LAUNCH'


    def disconnect(self):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._controls = None
        self._mixer = None
        self._device = None
        
        if (self._btn_mode != None):
            self._btn_mode.remove_value_listener(self._btn_mode_show)
            self._btn_mode = None  
       
        ModeSelectorComponent.disconnect(self)
        
        
    def set_btn_mode(self, button):
        if (self._btn_mode != None):
            self._btn_mode.remove_value_listener(self._btn_mode_show)
        self._btn_mode = button
        if (self._btn_mode != None):
            self._btn_mode.add_value_listener(self._btn_mode_show)   
            
        
    def _btn_mode_show(self, value):
        assert (self._btn_mode != None)
        assert (value in range(128))
        mode = self._btn_mode_names[value]
        if (mode != self._last_btn_mode):
            self._parent.show_message("BUTTON MODE = " + str(mode))
            self._last_btn_mode = mode


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
        assert ((controls == None) or (isinstance(controls, tuple) and (len(controls) == 8)))
        self._controls = controls
        self.set_mode(0)
        self.update()



    def number_of_modes(self):
        return 11



    def on_enabled_changed(self):
        self.update()
     
        
    def update(self):
        assert (self._modes_buttons != None)
        if self.is_enabled():
            if (self._controls != None):
                for track in range(len(self._controls)):
                    if (self._mode_index == 0):
                        self._mixer.channel_strip(track).set_volume_control(self._controls[track])
                        self._mixer.channel_strip(track).set_pan_control(None)
                        self._mixer.channel_strip(track).set_send_controls((None, None, None, None, None, None, None, None))
                        self._device.set_parameter_controls(tuple())
                    elif (self._mode_index == 1):
                        self._mixer.channel_strip(track).set_volume_control(None)
                        self._mixer.channel_strip(track).set_pan_control(self._controls[track])
                        self._mixer.channel_strip(track).set_send_controls((None, None, None, None, None, None, None, None))
                        self._device.set_parameter_controls(tuple())
                    elif (self._mode_index == 2):
                        self._mixer.channel_strip(track).set_volume_control(None)
                        self._mixer.channel_strip(track).set_pan_control(None)
                        self._mixer.channel_strip(track).set_send_controls((None, None, None, None, None, None, None, None))
                        self._device.set_parameter_controls(tuple(self._controls))
                    elif (self._mode_index == 3):
                        self._mixer.channel_strip(track).set_volume_control(None)
                        self._mixer.channel_strip(track).set_pan_control(None)
                        self._mixer.channel_strip(track).set_send_controls((self._controls[track], None, None, None, None, None, None, None))
                        self._device.set_parameter_controls(tuple())
                    elif (self._mode_index == 4):
                        self._mixer.channel_strip(track).set_volume_control(None)
                        self._mixer.channel_strip(track).set_pan_control(None)
                        self._mixer.channel_strip(track).set_send_controls((None, self._controls[track], None, None, None, None, None, None))
                        self._device.set_parameter_controls(tuple())
                    elif (self._mode_index == 5):
                        self._mixer.channel_strip(track).set_volume_control(None)
                        self._mixer.channel_strip(track).set_pan_control(None)
                        self._mixer.channel_strip(track).set_send_controls((None, None, self._controls[track], None, None, None, None, None))
                        self._device.set_parameter_controls(tuple())
                    elif (self._mode_index == 6):
                        self._mixer.channel_strip(track).set_volume_control(None)
                        self._mixer.channel_strip(track).set_pan_control(None)
                        self._mixer.channel_strip(track).set_send_controls((None, None, None, self._controls[track], None, None, None, None))
                        self._device.set_parameter_controls(tuple())
                    elif (self._mode_index == 7):
                        self._mixer.channel_strip(track).set_volume_control(None)
                        self._mixer.channel_strip(track).set_pan_control(None)
                        self._mixer.channel_strip(track).set_send_controls((None, None, None, None, self._controls[track], None, None, None))
                    elif (self._mode_index == 8):
                        self._mixer.channel_strip(track).set_volume_control(None)
                        self._mixer.channel_strip(track).set_pan_control(None)
                        self._mixer.channel_strip(track).set_send_controls((None, None, None, None, None, self._controls[track], None, None))
                        self._device.set_parameter_controls(tuple())
                    elif (self._mode_index == 9):
                        self._mixer.channel_strip(track).set_volume_control(None)
                        self._mixer.channel_strip(track).set_pan_control(None)
                        self._mixer.channel_strip(track).set_send_controls((None, None, None, None, None, None, self._controls[track], None))
                        self._device.set_parameter_controls(tuple())
                    elif (self._mode_index == 10):
                        self._mixer.channel_strip(track).set_volume_control(None)
                        self._mixer.channel_strip(track).set_pan_control(None)
                        self._mixer.channel_strip(track).set_send_controls((None, None, None, None, None, None, None, self._controls[track]))
                        self._device.set_parameter_controls(tuple())
                    else:
                        print('Invalid mode index')
                        assert False
                mode = self._knob_mode_names[self._mode_index]
                if (mode != self._last_knob_mode):
                    self._parent.show_message("KNOB MODE = " + str(mode))
                    self._last_knob_mode = mode
                        
                #self._rebuild_callback()

