LSL_API_README 6/27/21 JG


===== How to run =====

1. Open the Petal GUI.

2. Turn on your Muse.

3. Start the stream.

4. Run the python script!


===== Important Note =====
Metrics calls at the top of each script are set for all detections by default. Remove/edit to select only a few instead:
	Line: metricsCall = ['bandpower', 'eye', 'blink', 'artifact_detect']
		Example for blink and bandpower only: metricsCall = ['blink', 'bandpower']


===== Scripts =====

1. apiHelper.py
	Only helper functions for the other scripts, ignore this one

2. apiCall.py
	Run: python apiCall.py -k WmPFfy1pAtkX6t_KuSCxOV9xH4TEmp25RK9mWFANkZQ
	Output: prints API output
	
3. apiCall_Save_API.py
	Run: python apiCall_Save_API.py -k WmPFfy1pAtkX6t_KuSCxOV9xH4TEmp25RK9mWFANkZQ
	Output: prints API output and saves API output to text file with timestamps
	
4. apiCall_Save_API_EEG.py
	Run: python apiCall_Save_API.py -k WmPFfy1pAtkX6t_KuSCxOV9xH4TEmp25RK9mWFANkZQ
	Output: prints API output and saves both API output and raw EEG to text file with timestamps
	
5. apiCall_AverageBandpower.py
	Run: python apiCall_AverageBandpower.py -k WmPFfy1pAtkX6t_KuSCxOV9xH4TEmp25RK9mWFANkZQ
	Output: example to average bandpower across each channel, prints average bandpower
	
6. LSL_Receive_Save_EEGsample.py
	Run: python LSL_Receive_Save_EEGsample.py
	Output: prints and saves the raw EEG data into .txt file by sample (one sample at a time)

7. LSL_Receive_Save_EEGchunk.py
	Run: python LSL_Receive_Save_EEGchunk.py
	Output: prints and saves the raw EEG data into .txt file by chunk (one second of samples at a time)


===== Installation Requirements Python =====
1. pip install numpy
2. pip install lsl


===== API Output =====

Artifact_Detect:
	Output: Array of four labels (strings: one for each channel) detailing type of artifact (if any): [ch1, ch2, ch3, ch4]
	Possible values:
		'good': Channel has good data
		'blink': Channel has a blink artifact (typically shows up on channels 1 and 4 at the same time)
		'eye': Channel has an eye movement artifact (typically shows up on channels 2 and 3 at the same time)
		'artifact': Channel has an unknown artifact
			Note: If all channels have artifacts, the bandpower output will be "bad_data" for each channel and frequency bandpower
				However, if at least one channel is 'good', the other channel data will be interpolated and is still usable
	Example 1: ['blink', 'good', 'good', 'blink'] # Channels 1 and 4 have blink artifacts, Channels 2 and 3 are good
	Example 2: ['artifact', 'eye', 'eye', 'good'] # Channel 1 has an artifact, Channels 2 and 3 are eye movements, channel 4 is good

Blink:
	Output: True or false string that says whether a blink was detected (True) or not (False)
	Possible values: True, False
	Example 1: 'blink': 'True'
	Example 2: 'blink': 'False'
	
Eye:
	Output: True or false string that says whether an eye movement was detected (True) or not (False)
	Possible values: True, False
	Example 1: 'eye': 'True'
	Example 2: 'eye': 'False'
	
Bandpower:
	Output: Bandpower values (floats) for each channel at four frequency bands: [ch1, ch2, ch3, ch4][delta, theta, alpha, beta]
	Possible values: Bandpower values for delta (1-3 Hz), theta (3-8 Hz), alpha (8-13 Hz), and beta (13-30 Hz), 'bad_data' string
		Note: If 1-3 channels contain artifacts, the bandpower for those channels are interpolated
			However, if all four channels contain artifacts, the bandpower values will all contain strings of 'bad_data'
	Example 1:
	Example 2: 
	
	