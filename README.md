# README

## Description

This document describes the Block11 Python Remote Script for use with the Livid Block in Ableton Live 11. 

## Introduction

The Block11 script is based on an older general purpose remote script by software developer and artist J74. The original (Generic Python Remote Script) may be found [here](https://github.com/j74/Generic-Python-Remote-Script). It is more than 6 years old and incompatible with current versions of Ableton Live because Ableton's Python interpreter experienced a major version upgrade from Python 2.x to Python 3.x with the release of Live 11. 

The Block11 remote script ports J74's Generic script to Python 3.x and uses this as a base for the relevant customisations to provide a configuration more suitable to the Livid Block controller. If you have used NativeKontrol's blockLive script in the past, the current implementation of Block11 provides the features of blockLive's _Launch Mode_. It is hoped that in the near future, some additional improvements will be made to the script to support extended modes similar in form if not in all details to the NativeKontrol script. 

## How to Use

0. Download the zip file 
1. Unzip the downloaded file (in any location on your system)
2. Note that after unzipping, you will see a directory called `Block11` which contains a collection of Python (`.py`) files; this is the directory you will need to move/copy in order to install
3. Navigate to the `Remote Scripts` directory and place a copy of the Block11 directory in it. The path to the default location should look like this:

```sh
Windows: \Users\[username]\Documents\Ableton\User Library\Remote Scripts
Mac: Macintosh HD/Users/[username]/Music/Ableton/User Library/Remote Scripts
```

So, on my system, for example, the path to the Remote Scripts diretcory looks like this:

```sh
\Users\Leo\Documents\Ableton\User Library\Remote Scripts
```

Once you have copied or moved the Block11 script directory to the User Library Remote Scripts directory, you are essentially done. 

4. Start up Ableton Live 11 and verify the script installed without incident, before proceeding to use the controller. 

## How to verify the script installed
Once Ableton Live 11 is up and running, take the following steps: 

* open the Preferences dialog;
* navigate to the 'Link Tempo Midi' tab;
* find the new control surface (Block11) in the 'Control Surface' dropdown;
* find the 'block' controller in the Input and Output dropdowns. 
* make sure 'track' and 'remote' are checked for all block entries

If the script compiled without error, and it should, you will experience no difficulty performing the previous steps. If anything goes wrong you can check Ableton's error logs. These are typically found at the following location:

```sh
C:\Users\[username]\AppData\Roaming\Ableton\Live 11.0.12\Preferences
```

So on my system, the log file is found here:

```sh
C:\Users\Leo\AppData\Roaming\Ableton\Live 11.0.12\Preferences
```

If there are errors in the log, please forward it to me at leonardmreidy@gmail.com and I will help you to troubleshoot it. 

## Features currently supported
All pertinent `Launch Mode` features are currently supported alongside a handful of `Global Controls`, primarily those that are relevant to the kind of work you will typically do in Launch Mode. Work is underway to capture a greater feature set, ideally as similar as possible to the blockLive script which it hopes to replace in some cases. 

## Description of Mappings

- Grid is mapped to tracks, clipslots, and scene launchers (see blockLive manual for more details on the relevant features)
- Function buttons are partially mapped to Global Controls
- Sliders are mapped to the Cue Volume, and Master Volume controls respectively
- The first seven encoders (from left to right) are mapped to track volumes
- The eighth encoder is mapped to the Mixer X-Fader
