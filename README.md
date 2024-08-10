### anaesthesiaSystem-eeg

# Real time EEG signal processing and visualization system for patients during general anaesthesia

The EEG signal is useful in surgical interventions for monitoring the anaesthesia depth of patients. The wave form has more sensitive to fisiological changes and stimulus like a skin incision than the BIS index. Furthere more, it is possible to extract other index from the EEG signal as the permutation entropy, also know the electrical activity of both hemispheres and the changes in time and frequency of the signal.

Unlike the commercial equipment used nowadays for anesthesia monitoring, this work proposes a low-cost, real-time EEG signal processing and visualization system, made with open-source technologies and with a user-centered design.

**This project aims to support the monitoring of anesthetic depth.**


# Requirements
- [🔗](https://shop.openbci.com/products/cyton-biosensing-board-8-channel?variant=38958638542)OpenBCI Cyton Biosensing Board (8-channels).

- OpenBCI programmable dongle (for bluetooth communication).

- AA batteries.

- Gold Cup Electrodes.

- Conductive Paste.

- Python 3.9



# Installation
1. Install Python 3.9
```javascript
sudo apt-get update
sudo apt-get install python3.9 python3.9-venv python3.9-dev
```
2. Create and activate a virtual environment:
```javascript
python3.9 -m venv anaesthesia-env
source anaesthesia-env/bin/activate
```
3. Install required libraries:
```javascript
pip install pyOpenBCI scipy numpy matplotlib pyserial bitstring xmltodict requests pylsl pyqtgraph==0.10.0 PyWavelets
```
4. Install CYTON DONGLE DRIVERS
- [🔗](https://openbci.com/downloads) Download link
5. Modify ptime.py in pyqtgraph:  
- Locate the file ptime.py in the folder anaconda3/lib/site-packages/pyqtgraph
- Change line 24 to:
```javascript
cstart = systime.time()
```

# Running the Project
1. Run the OpenBCI server:
```javascript
py server_openbci.py
```
2. Run the OpenBCI simulator (optional):
```javascript
py SimOpenBCI.py
```
3. Run the main application:
```javascript
py main.py
```

## Signal filtering
- Linear filters:

    Low-pass: cut off frequency at 28Hz.

    High-pass: cut off frecuency at 3Hz.

- Wavelet filtering:

    Universal threshold.
    
    Hard thresholding.

    Multiple weighting.


## Signal processing
 - Continuous wavelet transform to plotted the scalogram as a function of time and frequency.
  
 - Welch's method for estimating power spectra.
  
 - Permutation Entropy to describes complexity of the signal measured.
  
Data is recording and processing in windows of 5 seconds with 1 second overlap
  
  
## User interface
- Model-View-Controller (MVC) as the architectural pattern.
- It is used object-oriented programming.
- Qt Creator is used for the graphic components.


## Location of scalp electrodes
The electrodes are placed using the 10-20 international system, but it is only used the F3, F4 and Fz positions or the Fp1, Fp2 and Fpz positions.

![Image](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/EEG_10-10_system_with_additional_information.svg/512px-EEG_10-10_system_with_additional_information.svg.png)



## Authors

[@yeimmygit11](https://github.com/yeimmygit11)

[@mariacvilla](https://github.com/mariacvilla)

## Reviewer
[@NicolasUdea](https://github.com/NicolasUdea)
