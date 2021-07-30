import wx
import math
import matplotlib.backends.backend_wxagg
import matplotlib.pyplot
import matplotlib.figure
import numpy as np
import random
from pylsl import StreamInlet, resolve_stream, local_clock
from datetime import datetime

##example: https://stackoverflow.com/questions/29005931/matplotlib-pyplot-in-a-wx-panel

data = [
    [
        ["20:   ", random.randint(0, 10)],
        ["19:   ", random.randint(0, 10)],
        ["18:   ", random.randint(0, 10)],
        ["17:   ", random.randint(0, 10)],
        ["16:   ", random.randint(0, 10)],
        ["15:   ", random.randint(0, 10)],
        ["14:   ", random.randint(0, 10)],
        ["13:   ", random.randint(0, 10)],
        ["12:   ", random.randint(0, 10)],
        ["11:   ", random.randint(0, 10)],
        ["10:   ", random.randint(0, 10)],
        ["09:   ", random.randint(0, 10)],
        ["08:   ", random.randint(0, 10)],
        ["07:   ", random.randint(0, 10)],
        ["06:   ", random.randint(0, 10)],
        ["05:   ", random.randint(0, 10)],
        ["04:   ", random.randint(0, 10)],
        ["03:   ", random.randint(0, 10)],
        ["02:   ", random.randint(0, 10)],
        ["01:   ", random.randint(0, 10)]
        ],
    [
        ["Alpha1", random.randint(0, 10)],
        ["Alpha2", random.randint(0, 10)],
        ["Alpha3", random.randint(0, 10)],
        ["Alpha4", random.randint(0, 10)]
        ]
    ]

labelOverTimeSession = []
bandpowerOverTimeSession = []
labelOverTime = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
bandpowerOverTime = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
lastBandpowerArray = [1, 1, 1, 1]
currentBandpower = [1, 1, 1, 1]
totalBandpower = []

fileNameSessionResults = datetime.now().strftime('%Y-%m-%d%H%M%S') + "_SessionResults.txt"
fileNameSessionResultsFigure = datetime.now().strftime('%Y-%m-%d%H%M%S') + "_SessionResultsFigure"

class panel_plot(wx.Panel):
    def __init__(self, parent):
        #jg
        stylePanel = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
          wx.NO_BORDER | wx.FRAME_SHAPED | wx.NO_FULL_REPAINT_ON_RESIZE )
        #jg

        wx.Panel.__init__(self, parent, style = stylePanel)        
##        wx.Panel.__init__(self, parent, style = wx.NO_FULL_REPAINT_ON_RESIZE)

        self.figure = matplotlib.figure.Figure()
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self, -1, self.figure)

        self.set_size()
        self.draw()

        self._resize_flag = False

        self.Bind(wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_idle(self, event):
        if self._resize_flag:
            self._resize_flag = False
            self.set_size()

    def on_size(self, event):
        self._resize_flag = True

    def set_size(self):
        pixels = tuple(self.GetSize())
        self.SetSize(pixels)
        self.canvas.SetSize(pixels)
        self.figure.set_size_inches([float(x) / self.figure.get_dpi() for x in pixels])

    def draw(self):
        self.canvas.draw()

class frame_main ( wx.Frame ):
    def __init__( self, parent ):
        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.NO_BORDER | wx.FRAME_SHAPED  )
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = style )
##        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        sizer_bg = wx.BoxSizer( wx.HORIZONTAL )

        self.panel_bg = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer_main = wx.BoxSizer( wx.VERTICAL )

        self.button_change = wx.Button( self.panel_bg, wx.ID_ANY, u"Change data", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_main.Add( self.button_change, 0, wx.ALL, 5 )
        
        self.panel_matplotlib = panel_plot(self.panel_bg)
        sizer_main.Add( self.panel_matplotlib, 1, wx.EXPAND |wx.ALL, 5 )


        self.panel_bg.SetSizer( sizer_main )
        self.panel_bg.Layout()
        sizer_main.Fit( self.panel_bg )
        sizer_bg.Add( self.panel_bg, 1, wx.EXPAND, 5 )


        self.SetSizer( sizer_bg )
        self.Layout()

        self.i = 0

        self.on_change()

        self.setbinds()

        self.SetTransparent( 220 )

        self.on_timer()

    def setbinds(self):
        self.button_change.Bind(wx.EVT_BUTTON, self.on_change)

    def on_change(self, event = None):
        self.panel_matplotlib.figure.clf()
        axes = self.panel_matplotlib.figure.gca()

        self.i += 1
        _data = np.array(data[self.i%2])
        
##        for i in range(0, len(_data)):
##            _data[i][1] = random.randint(0, 10)
        
        datapoints = np.array(range(len(_data)))
        values = np.array([int(x[1]) for x in _data])
        labelpositions = np.array([x + 0.4 for x in range(len(_data))])
        labeltext = np.array([x[0] for x in _data])

        axes.barh(datapoints, values)
        axes.set_yticks(labelpositions)
        axes.set_yticklabels(labeltext)

        self.panel_matplotlib.draw()

#on click, also save the session figure
#NOTE: This lags things a lot, if you call too much like every 10 ms putting it in the timer function below it will get the script behind
#However, if you only call on button click like here, it will slow things down but then catch back up, can check with local_clock()
#Even so, with this code when you click it lags, which is annoying, even if it catches back up
        x = labelOverTimeSession
        y = bandpowerOverTimeSession
        fig2, ax2 = matplotlib.pyplot.subplots()
##        ax2.set_yscale('log')

        for i in range(0, len(labelOverTimeSession)):
            if labelOverTimeSession[i] == 'Blink':
                ax2.bar(i, bandpowerOverTimeSession[i], color='MAGENTA')
            if labelOverTimeSession[i] == 'Interp':
                ax2.bar(i, bandpowerOverTimeSession[i], color='y')
            if labelOverTimeSession[i] == 'bad':
                ax2.bar(i, bandpowerOverTimeSession[i], color='r')
            if labelOverTimeSession[i] == 'Alpha':
                ax2.bar(i, bandpowerOverTimeSession[i], color='b')

        ax2.set_xticks([idx+0.5 for idx in range(len(x))])
        ax2.set_xticklabels(x, rotation=35, ha='right', size=10)
        fig2.tight_layout()
##        plt.show()
#NOTE: Only save as one file type, multiple will lags things considerably
        fig2.savefig(fileNameSessionResultsFigure + '.png')
##        fig2.savefig(fileNameSessionResultsFigure + '.pdf')
        matplotlib.pyplot.close(fig2)

    def on_timer(self):
        #NOTE: Sample here is the alpha bandpower values (len=4) THEN NEXT ARE artifact values for each channel (len=4), comma separated
        sample, timestamp = inlet.pull_sample()
        if sample:
##            print(local_clock())
            bandArray = []
            artifactArray = []
            cleanDataArray = []
            labelChannel = []
            bandpowerSample = sample[0]
            bandpowerSplit = bandpowerSample.split(',')
            for channelPower in range(0, 4):
                bandArray.append(round(float(bandpowerSplit[channelPower]), 5))
            for artifactCount in range(4, 8):
                artifactArray.append(bandpowerSplit[artifactCount])
            heogArtifact = int(bandpowerSplit[len(bandpowerSplit)-1])
            print(artifactArray)
            print(heogArtifact)

            self.panel_matplotlib.figure.clf()
            axes = self.panel_matplotlib.figure.gca()

            _data = np.array(data[self.i%2])

    #average clean channels
            
    #variables
            logScale = 1            #change display to log scale, 1=on
            cleanTotal = 0          #total clean channels, used for dividing good channel averages when interpolating bad channels
            cleanSum = 0            #sum of clean channels, cleanSum/cleanTotal = interpolated average

    #basically np.roll bandpowerOverTime and associated interp/artifact over time to add newest value and drop oldest value
            for i in range(0, len(bandpowerOverTime)-1):
                bandpowerOverTime[i] = bandpowerOverTime[i+1]
                labelOverTime[i] = labelOverTime[i+1]

    #catch artifacts
            for i in range(0, len(bandArray)):
##                if int(float(artifactArray[i])) > 0:                                            #if artifact channel, mark as 0 in cleanDataArray
                if int(float(artifactArray[i])) > 0 or bandArray[i] > 40:
                    cleanDataArray.append(0)
                else:                                                                           #if clean channel, add value to cleanDataArray and add 1 to cleanSum and cleanTotal
                    cleanSum += bandArray[i]
                    cleanTotal += 1
                    cleanDataArray.append(bandArray[i])

    #if all channels are bad, we want to take the last average
            if sum(cleanDataArray) == 0:
                bandpowerOverTime[len(bandpowerOverTime)-1] = bandpowerOverTime[len(bandpowerOverTime)-2]   #duplicate most recent bandpower
                labelOverTime[len(labelOverTime)-1] = 'bad'                                                 #populate labelOverTime with 'bad' indicating all channels contain artifact
                for i in range(0, len(bandArray)):
                    labelChannel.append('bad')
            elif heogArtifact > 0:
                bandpowerOverTime[len(bandpowerOverTime)-1] = bandpowerOverTime[len(bandpowerOverTime)-2]   #duplicate most recent bandpower
                labelOverTime[len(labelOverTime)-1] = 'HEOG'                                                 #populate labelOverTime with 'bad' indicating all channels contain artifact
                for i in range(0, len(bandArray)):
                    labelChannel.append('HEOG')

    #if we have at least one good channel, we can interpolate others and add new values
            else:
                #populate labelOverTime with labels over time
                if 0 in cleanDataArray:
                    if cleanDataArray[0] == 0 and cleanDataArray[3] == 0 and cleanDataArray[1] > 0 and cleanDataArray[2] > 0:
                        print('blink')
                        labelOverTime[len(labelOverTime)-1] = 'Blink'
                    else:
                        labelOverTime[len(labelOverTime)-1] = 'Interp'                                          #populate labelOverTime with 'interp' indicating 1-3 channels interpolated
                if 0 not in cleanDataArray:
                    labelOverTime[len(labelOverTime)-1] = 'Alpha'                                           #populate labelOverTime with 'Alpha' indicating all channels are good

                # populate labelChannel labels for individual channels
                for i in range(0, len(bandArray)):
                    if cleanDataArray[i] == 0:
                        labelChannel.append('Interp')
                        currentBandpower[i] = (cleanSum/cleanTotal)                             #interpolate bad channels with clean channels
                    else:
                        labelChannel.append('Alpha')
                        currentBandpower[i] = cleanDataArray[i]                                 #if clean, add channel value normally
                    lastBandpowerArray[i] = currentBandpower[i]                                 #fill lastBandpowerArray with final channel values, used to duplicate if next sample is all bad
                lastAverageBandpower = np.mean(currentBandpower)                             #update lastBandpower with current value
                bandpowerOverTime[len(bandpowerOverTime)-1] = np.mean(currentBandpower)      #add new channel average to most recent bandpowerOverTime position

    #now we populate display data
            if len(_data) == 20:                                                                #if overTime is displayed
                for i in range(0, len(_data)):
                    _data[i][1] = int(bandpowerOverTime[i]*100)                                 #populate display values from bandpowerOverTime, already interpolated
                    _data[i][0] = str(labelOverTime[i]) + str(i)                                #populate display labels from labelsOverTime
            bandpowerOverTimeSession.append(bandpowerOverTime[len(bandpowerOverTime)-1])    #populate running log of display values for entire session
            labelOverTimeSession.append(labelOverTime[len(labelOverTime)-1])                #populate running log of display labels for entire session
            if len(_data) == 4:                                                                 #if by channel is displayed
                for i in range(0, len(_data)):
                    _data[i][0] = labelChannel[i]
                    if labelChannel[i] == 'bad':                                                #show last average if bad
                        _data[i][1] = int(lastBandpowerArray[i]*100)
                    else:
                        _data[i][1] = int(currentBandpower[i]*100)                              #show new data if good, already interpolated
                        lastBandpowerArray[i] = currentBandpower[i]

##            if len(_data) == 20 and logScale == 1:
##                for i in range(0, len(bandpowerOverTime)):
##                    _data[i][1] = int(math.log10(bandpowerOverTime[i])*100)
####                    print(_data[i][1])

    #average clean channels

    ##        print(_data)
            
            datapoints = np.array(range(len(_data)))
            values = np.array([int(x[1]) for x in _data])
            labelpositions = np.array([x + 0.4 for x in range(len(_data))])
            labeltext = np.array([x[0] for x in _data])

            #colors: https://wxpython.org/Phoenix/docs/html/wx.ColourDatabase.html
    ##        axes.barh(datapoints[0], values[0], color='b')
    ##        axes.barh(datapoints[1:4], values[1:4], color='r')

            #Color the bars overTime
            if len(_data) == 20:
                for i in range(0, len(labelOverTime)):
                    if labelOverTime[i] == 'Blink':
                        axes.barh(datapoints[i], values[i], color='MAGENTA')
                    if labelOverTime[i] == 'Interp':
                        axes.barh(datapoints[i], values[i], color='y')
                    if labelOverTime[i] == 'bad':
                        axes.barh(datapoints[i], values[i], color='r')
                    if labelOverTime[i] == 'Alpha':
                        axes.barh(datapoints[i], values[i], color='b')
                    if labelOverTime[i] == 'HEOG':
                        axes.barh(datapoints[i], values[i], color='g')

    #save session log with bandpowerOverTimeSession values and labelOverTimeSession labels, continually overwrite file
            f=open(fileNameSessionResults,"w")
    ##        f.write('MetaData: totalSamples = ' + str(totalSamples) + ', chunkLength = ' + str(chunkLength) + ', nperseg = ' + str(nperseg) + 'nfft = ' + str(nfft)
    ##        + ', device = ' + str(device) + ', numSensors = ' + str(numSensors) + ', channelArray = ' + str(channelArray))
    ##        f.write(", ")
    ##        f.write('\n')
            f.write(str(labelOverTimeSession))
            f.write(", ")
            f.write('\n')
            f.write(str(bandpowerOverTimeSession))
            f.write(", ")
            f.write('\n')
            f.close()

    #Color the bars individual channels
            if len(_data) == 4:
                if labelOverTime[len(labelOverTime)-1] == 'Blink':
                    for i in range(0, len(labelChannel)):
                        axes.barh(datapoints[i], values[i], color='MAGENTA')
                if labelOverTime[len(labelOverTime)-1] == 'bad':
                    for i in range(0, len(labelChannel)):
                        axes.barh(datapoints[i], values[i], color='r')
                if labelOverTime[len(labelOverTime)-1] == 'HEOG':
                    for i in range(0, len(labelChannel)):
                        axes.barh(datapoints[i], values[i], color='g')
                else:
                    for i in range(0, len(labelChannel)):
                        if labelChannel[i] == 'Interp':
                            axes.barh(datapoints[i], values[i], color='y')
                        else:
                            axes.barh(datapoints[i], values[i], color='b')

    ##        axes.barh(datapoints, values)
            axes.set_yticks(labelpositions)
            axes.set_yticklabels(labeltext)

##            axes.set_xscale('log')
##            print(max(bandpowerOverTimeSession))
##            print(max(bandpowerOverTime))
            print('average alpha' + str(np.mean(bandpowerOverTime)))
##            print(bandpowerOverTime[len(bandpowerOverTime)-1])
##            axes.set_xlim(0, 20*20)

    ##        axes.set_xlim(0, 500)

            self.panel_matplotlib.draw()

        wx.CallLater(10, self.on_timer)

class App(wx.App):
    def __init__(self):
        super(App, self).__init__()
        self.mainframe = frame_main(None)
        self.mainframe.Show()
        self.MainLoop()

print("looking for a marker stream...")
streams = resolve_stream('type', 'Markers')
inlet = StreamInlet(streams[0])

App()
