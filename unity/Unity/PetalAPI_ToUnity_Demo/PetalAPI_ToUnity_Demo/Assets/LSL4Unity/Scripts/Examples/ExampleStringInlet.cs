//6/28/21 JG
using UnityEngine;
using System;
using System.Linq;
using Assets.LSL4Unity.Scripts.AbstractInlets;

namespace Assets.LSL4Unity.Scripts.Examples
{
    /// <summary>
    /// Just an example implementation for a Inlet recieving float values
    /// </summary>
    public class ExampleStringInlet : AStringInlet
    {
        //public string sampleFromInlet = String.Empty;
        public string lastSample = String.Empty;

        public string blinkAPI = String.Empty;
        public string eyeAPI = String.Empty;
        public string[] artifactAPI = new string[4];
        public float[] deltaPowerAPI = new float[4];
        public float[] thetaPowerAPI = new float[4];
        public float[] alphaPowerAPI = new float[4];
        public float[] betaPowerAPI = new float[4];
        public float[] bandpowerAverageAPI = new float[4];

        protected override void Process(string[] newSample, double timeStamp)
        {
            //print("working now");
            lastSample = string.Join(" ", newSample.Select(c => c.ToString()).ToArray());
            //print(GameObject.Find("LabStreamingLayer").GetComponent<ExampleStringInlet>().lastSample);

            string[] fullArrayParse = lastSample.Split(char.Parse("{"));

            string[] parseArtifact = fullArrayParse[2].Split(char.Parse(","));
            string[] artifactParseCh1 = parseArtifact[0].Split(char.Parse(":"));
            string[] artifactParseCh2 = parseArtifact[1].Split(char.Parse(":"));
            string[] artifactParseCh3 = parseArtifact[2].Split(char.Parse(":"));
            string[] artifactParseCh4_Brack = parseArtifact[3].Split(char.Parse("}"));
            string[] artifactParseCh4 = artifactParseCh4_Brack[0].Split(char.Parse(":"));

            artifactAPI[0] = artifactParseCh1[1];
            artifactAPI[1] = artifactParseCh2[1];
            artifactAPI[2] = artifactParseCh3[1];
            artifactAPI[3] = artifactParseCh4[1];

            string[] parseBlink = fullArrayParse[3].Split(char.Parse(","));
            string[] parseBlink_Brack = parseBlink[0].Split(char.Parse("}"));
            string[] parseBlink_Final = parseBlink_Brack[0].Split(char.Parse(":"));
            blinkAPI = parseBlink_Final[1];

            string[] parseEye = fullArrayParse[4].Split(char.Parse(","));
            string[] parseEye_Brack = parseEye[0].Split(char.Parse("}"));
            string[] parseEye_Final = parseEye_Brack[0].Split(char.Parse(":"));
            eyeAPI = parseEye_Final[1];

            string[] parseBandpowerCh1 = fullArrayParse[6].Split(char.Parse(","));
            string[] parseBandpowerCh1_Delta = parseBandpowerCh1[0].Split(char.Parse(":"));
            string[] parseBandpowerCh1_Theta = parseBandpowerCh1[1].Split(char.Parse(":"));
            string[] parseBandpowerCh1_Alpha = parseBandpowerCh1[2].Split(char.Parse(":"));
            string[] parseBandpowerCh1_Beta_Brack = parseBandpowerCh1[3].Split(char.Parse("}"));
            string[] parseBandpowerCh1_Beta = parseBandpowerCh1_Beta_Brack[0].Split(char.Parse(":"));

            string[] parseBandpowerCh2 = fullArrayParse[7].Split(char.Parse(","));
            string[] parseBandpowerCh2_Delta = parseBandpowerCh2[0].Split(char.Parse(":"));
            string[] parseBandpowerCh2_Theta = parseBandpowerCh2[1].Split(char.Parse(":"));
            string[] parseBandpowerCh2_Alpha = parseBandpowerCh2[2].Split(char.Parse(":"));
            string[] parseBandpowerCh2_Beta_Brack = parseBandpowerCh2[3].Split(char.Parse("}"));
            string[] parseBandpowerCh2_Beta = parseBandpowerCh2_Beta_Brack[0].Split(char.Parse(":"));

            string[] parseBandpowerCh3 = fullArrayParse[8].Split(char.Parse(","));
            string[] parseBandpowerCh3_Delta = parseBandpowerCh3[0].Split(char.Parse(":"));
            string[] parseBandpowerCh3_Theta = parseBandpowerCh3[1].Split(char.Parse(":"));
            string[] parseBandpowerCh3_Alpha = parseBandpowerCh3[2].Split(char.Parse(":"));
            string[] parseBandpowerCh3_Beta_Brack = parseBandpowerCh3[3].Split(char.Parse("}"));
            string[] parseBandpowerCh3_Beta = parseBandpowerCh3_Beta_Brack[0].Split(char.Parse(":"));

            string[] parseBandpowerCh4 = fullArrayParse[9].Split(char.Parse(","));
            string[] parseBandpowerCh4_Delta = parseBandpowerCh4[0].Split(char.Parse(":"));
            string[] parseBandpowerCh4_Theta = parseBandpowerCh4[1].Split(char.Parse(":"));
            string[] parseBandpowerCh4_Alpha = parseBandpowerCh4[2].Split(char.Parse(":"));
            string[] parseBandpowerCh4_Beta_Brack = parseBandpowerCh4[3].Split(char.Parse("}"));
            string[] parseBandpowerCh4_Beta = parseBandpowerCh4_Beta_Brack[0].Split(char.Parse(":"));

            //// if there is bad data, we currently use the previous average: use this code to set them all to 0
            //if (parseBandpowerCh1_Delta[1] == parseBandpowerCh2_Delta[1])
            //{
            //    print("BAD DATA");
            //    for (int i = 0; i < 4; i++)
            //    {
            //        deltaPower[i] = 0f;
            //        thetaPower[i] = 0f;
            //        alphaPower[i] = 0f;
            //        betaPower[i] = 0f;
            //    }
            //    //bandpowerAverageAPI[0] = 0f;
            //    //bandpowerAverageAPI[1] = 0f;
            //    //bandpowerAverageAPI[2] = 0f;
            //    //bandpowerAverageAPI[3] = 0f;
            //}

            if (parseBandpowerCh1_Delta[1] != parseBandpowerCh2_Delta[1])
            {
                deltaPowerAPI[0] = float.Parse(parseBandpowerCh1_Delta[1]);
                deltaPowerAPI[1] = float.Parse(parseBandpowerCh2_Delta[1]);
                deltaPowerAPI[2] = float.Parse(parseBandpowerCh3_Delta[1]);
                deltaPowerAPI[3] = float.Parse(parseBandpowerCh4_Delta[1]);
                thetaPowerAPI[0] = float.Parse(parseBandpowerCh1_Theta[1]);
                thetaPowerAPI[1] = float.Parse(parseBandpowerCh2_Theta[1]);
                thetaPowerAPI[2] = float.Parse(parseBandpowerCh3_Theta[1]);
                thetaPowerAPI[3] = float.Parse(parseBandpowerCh4_Theta[1]);
                alphaPowerAPI[0] = float.Parse(parseBandpowerCh1_Alpha[1]);
                alphaPowerAPI[1] = float.Parse(parseBandpowerCh2_Alpha[1]);
                alphaPowerAPI[2] = float.Parse(parseBandpowerCh3_Alpha[1]);
                alphaPowerAPI[3] = float.Parse(parseBandpowerCh4_Alpha[1]);
                betaPowerAPI[0] = float.Parse(parseBandpowerCh1_Beta[1]);
                betaPowerAPI[1] = float.Parse(parseBandpowerCh2_Beta[1]);
                betaPowerAPI[2] = float.Parse(parseBandpowerCh3_Beta[1]);
                betaPowerAPI[3] = float.Parse(parseBandpowerCh4_Beta[1]);
            }

            bandpowerAverageAPI[0] = (deltaPowerAPI[0] + deltaPowerAPI[1] + deltaPowerAPI[2] + deltaPowerAPI[3]) / 4;
            bandpowerAverageAPI[1] = (thetaPowerAPI[0] + thetaPowerAPI[1] + thetaPowerAPI[2] + thetaPowerAPI[3]) / 4;
            bandpowerAverageAPI[2] = (alphaPowerAPI[0] + alphaPowerAPI[1] + alphaPowerAPI[2] + alphaPowerAPI[3]) / 4;
            bandpowerAverageAPI[3] = (betaPowerAPI[0] + betaPowerAPI[1] + betaPowerAPI[2] + betaPowerAPI[3]) / 4;

            //// for printing into console
            //print(blinkAPI);                                                             //true or false
            //print(eyeAPI);                                                               //true or false
            //foreach (var x in artifactAPI) Debug.Log(x.ToString());                      //four values, one for each channel in order
            //foreach (var x in deltaPowerAPI) Debug.Log(x.ToString());                    //four delta values, one for each channel in order
            //foreach (var x in thetaPowerAPI) Debug.Log(x.ToString());                    //four theta values, one for each channel in order
            //foreach (var x in alphaPowerAPI) Debug.Log(x.ToString());                    //four alpha values, one for each channel in order
            //foreach (var x in betaPowerAPI) Debug.Log(x.ToString());                     //four beta values, one for each channel in order
            //foreach (var x in bandpowerAverageAPI) Debug.Log(x.ToString());              //four average bandpower values, on for each band in order: delta, theta, alpha, beta

        }
    }
}