# README

## Description

This document describes the Block11 Python Remote Script for use with the Livid Block in Ableton Live 11. 

## Introduction

The Block11 script is based on an older general purpose remote script by software developer and artist J74. The original (Generic Python Remote Script) may be found [here](https://github.com/j74/Generic-Python-Remote-Script). It is more than 6 years old and incompatible with current versions of Ableton Live because Ableton moved away from Python 2.x to Python 3.x with the release of Live 11. However, it is relatively straightforward to refactor the code to use Python 3.x syntax and the old `_Framework` classes appear to be still supported. 

### Refactoring the Generic Script

The Python interpreter installs in the OS bundled with various tools, among them, a script for porting Python 2.x code to Python 3.x code (`2to3.py`) and more information about that may be found [here](https://docs.python.org/3/library/2to3.html).

### Rationale for Building on the Generic Script

Writing third-party remote scripts for MIDI controller integration with Ableton Live 11 presents challenges that were not present in the landscape before its release. Ableton Live 10 and below supported Python 2.x and the community had built a substantial body of documentation, tutorials, example scripts, and various proprietary and non-proprietary Python 2.x scripts for various controllers that were otherwise unsupported in Ableton's official collection of control surfaces. So, a sufficiently committed individual could source many third-party scripts for a reasonable selection of the most popular controllers or reasonably good information about how to write a custom script or adapt an existing script to integrate such controllers with Live 10. With Live 11, the Python interpreter changed, but so too did the API, which has undergone a version upgrade, although the evidence from working with older scripts suggests that the old API is still supported for the moment. 

The team at Ableton are aware of the community's efforts to write/hack remote scripts for Live, and do not appear to actively prohibit it. But neither do they support it in the ways that really matter, for example by providing official API documentation, test/debug utilities for developing scripts, and resources for learning about third-party remote script development. So as a script developer, the resources available are exclusively the product of a dedicated community of volunteers who are not compensated for their work and are working with precisely the same limitations. Some notable contributors have taken the trouble to reverse engineer API documentation (including Live 11), and others have taken considerable pains to create tutorial and other learning content, and a few have even built out repositories of remote scripts for otherwise unsupported controllers. Unfortunately, much of the learning content that is available is very dated, many of the scripts are now incompatible in one way or another with Live 11, and it is difficult to source a script that can serve as a good starting point for the novice developer. 

J74's Generic Remote script, by contrast, is a good starting point. It is easily upgraded to Python 3.x, and it is exceptionally well-annotated making it much easier to adapt to a given controller, and, finally, it is a _generic_ script. It was built as a template so that, in principle, any developer could come along and use it as a starting point with a sufficient feature-set that could be easily configured to serve an otherwise unserved MIDI controller. The only disadvantage to J74's Generic Script is that it uses the old `_Framework` classes (instead of the newer `ableton.v2` classes) and it is difficult at this time to determine whether they will continue to be supported in the future, or, if it can be ascertained, for how long. 

In any case, it seems that they are supported for the present and I have made the working assumption that by the time they are finally aged out a new generation of community resources for Live 11 will replace them and I will be able to write a new Block11 script at that time that will be more durable.


## Building on the Generic Script

J74's Generic Script contains most of the essential feature set that a MIDI controller would need to control Live 11, including redbox and other session controls, clip and scene launching, mixer and device controls, and so on. To adapt the script to a specific controller, J74 has designed the script to ensure that customisation is, for the most part, a matter of configuration, i.e., MIDI mapping by code. The file `MIDI_Map.py` contains a collection of variables that represent the mappings that are unique to an individual controller and each variable is annotated to guide the developer's attempts at customisations. The Block11 Script departs from this approach and is developed in a few key phases. 

In phase 0, substantial time was spent doing research and experimenting with the existing resources for remote script development. That phase drew to a close a couple of days ago when I finally found just the right combination of resources (documentation and the J74 Generic Script) to begin working effectively with remote scripts. 

In phase 1, the current phase, the basic configurations or mappings will be assigned. This version will be available within the next week or two and it should cover the bases, assuming that there are no surprises with API deprecations. The goal at this stage will be to restore basic functionality to the Livid Block in Live 11. 

In phase 2, the next phase, some more advanced customisations will be attempted with the remote script and additional features will be implemented, either with the remote scripts, or with a combination of the Block11 script and a Max Device rack to implement those features. 

