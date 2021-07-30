PYTHON README 6/27/21 JG


===== How to run =====

1. Open the Petal GUI.

2. Turn on your Muse.

3. Start the stream.

4. Run the python script!

5. Run the Unity program!


===== Important Note =====
DON'T edit your metrics call! It is set for all detections by default (necessary for apiPythonToUnity.py and ExampleStringInlet.cs in Unity):
	Line: metricsCall = ['bandpower', 'eye', 'blink', 'artifact_detect']


===== Scripts =====

1. apiHelper.py
	Only helper functions for the other scripts, ignore this one

2. apiPythonToUnity.py
	Run: python apiPythonToUnity.py -k WmPFfy1pAtkX6t_KuSCxOV9xH4TEmp25RK9mWFANkZQ
	Output: sends all api output over a LSL Marker Stream that Unity can pick up
	
3. Unity Demo
	Open the "ExampleScene" in CompiledProjects_June2021\Unity\PetalAPI_ToUnity_Demo\PetalAPI_ToUnity_Demo\Assets\Scenes\
	Click on LabStreamingLayer in the Hierarchy
	Make sure the following options are correct in the Example String Inlet (Script) under inspector view:
		Moment: Fixed Update
		Stream Type: Markers
		Sample From Inlet and Last Sample should be blank
	Now you ready to go!


===== API Output --> Unity Variables =====

API: Artifact_Detect --> Unity: string[] artifactAPI = new string[4];

API: Blink --> Unity: string blinkAPI;

API: Eye --> Unity: string eyeAPI;

API: Bandpower --> Unity: [ch1, ch2, ch3, ch4]
	float[] deltaPowerAPI = new float[4];
	float[] thetaPowerAPI = new float[4];
	float[] alphaPowerAPI = new float[4];
	float[] betaPowerAPI = new float[4];
		NOTE: If "bad_data", will simply display the last value for now
		
Unity Average Bandpower across all channels at each frequency: [delta, theta, alpha, beta]
	float[] bandpowerAverageAPI = new float[4];
		NOTE: If "bad_data", will simply display the last value for now


===== How to use the API output in Unity =====

Example String Inlet (Script) shows all values in real time:

1. lastSample: full API output (unparsed)

2. Blink API: True/False value for blink detection

3. Eye API: True/False value for eye movement detection

4. Artifact API: Artifact label displayed separately for each channel: [ch1, ch2, ch3, ch4]

5. Delta/Theta/Alpha/Beta Power API: Bandpower displayed separately for each channel: [ch1, ch2, ch3, ch4]

6. Bandpower API Average: Average Bandpower across all channels displayed separately for each band: [delta, theta, alpha, beta]



GameObject.Find("LabStreamingLayer").GetComponent<ExampleStringInlet>().blinkAPI




===== How to set up a new Unity project from scratch =====

1. Copy the LSL4Unity folder located in CompiledProjects_June2021\Unity\PetalAPI_ToUnity_Demo\PetalAPI_ToUnity_Demo\Assets\

2. Place copied LSL4Unity folder into your Assets folder

3. Open your project

4. Add LabStreamingLayer prefab to your scene from LSL4Unity/Prefabs

5. Drag ExampleStringInlet.cs onto LabStreamingLayer prefab (located in LSL4Unity\Scripts\Examples\).
	Make sure the ExampleStringInlet.cs script has "6/28/21 JG" commented at the top.
	
6. Make sure the following options are correct in the Example String Inlet (Script) under inspector view:
	Moment: Fixed Update.
	Stream Type: Markers.
	Sample From Inlet and Last Sample should be blank.
	
7. Run the python script, then click play your unity!
	Make sure the API output is printing in the console.


