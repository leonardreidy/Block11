# L3n 2021
# Ableton Live 11 Remote Script for Stazma's
# Livid Block

from .StazmaBlock import StazmaBlock
from _Framework.Capabilities import controller_id, inport, outport, CONTROLLER_ID_KEY, PORTS_KEY, HIDDEN, NOTES_CC, SCRIPT, REMOTE, SYNC, TYPE_KEY, FIRMWARE_KEY, AUTO_LOAD_KEY

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id="04D8", product_ids=["fd33"], model_name="Livid Block"),
        PORTS_KEY: [inport(props=[HIDDEN, NOTES_CC, SCRIPT, REMOTE]),
                    inport(props = []),
                    outport(props=[HIDDEN, NOTES_CC, SCRIPT, REMOTE]),
                    outport(props=[])],
        TYPE_KEY: 'push',
        AUTO_LOAD_KEY: False}

def create_instance(c_instance):
    """ Creates and returns the StazmaBlock script """
    return StazmaBlock(c_instance)