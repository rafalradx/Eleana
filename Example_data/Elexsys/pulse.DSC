#DESC	1.2 * DESCRIPTOR INFORMATION ***********************
*
*	Dataset Type and Format:
*
DSRC	EXP
BSEQ	BIG
IKKF	CPLX
XTYP	IDX
YTYP	NODATA
ZTYP	NODATA
*
*	Item Formats:
*
IRFMT	D
IIFMT	D
*
*	Data Ranges and Resolutions:
*
XPTS	1024
XMIN	-0.000000
XWID	8184.000000
*
*	Documentational Text:
*
TITL	'FeS_WT_9K_Tm'
IRNAM	'Intensity'
IINAM	'Intensity'
XNAM	'Time'
IRUNI	''
IIUNI	''
XUNI	'ns'
*
************************************************************
*
#SPL	1.2 * STANDARD PARAMETER LAYER
*
OPER    marcin
DATE    02/20/08
TIME    11:16:26
CMNT    
SAMP    
SFOR    
STAG    C
EXPT    
OXS1    
AXS1    
AXS2    
AXS3    
MWPW    0.01525
A1CT    1.2
B0VL    1.266016
A1SW    0.4
MWFQ    3.36828e+10
AVGS    1
*
************************************************************
*
#DSL	1.0 * DEVICE SPECIFIC LAYER
*

.DVC     acqStart, 1.0


.DVC     cwBridge, 1.0

AcqFineTuning      Never
AcqScanFTuning     No Scan
AcqSliceFTuning    No Slice
Power              15.25 mW
PowerAtten         1 dB

.DVC     fieldCtrl, 1.0

AllegroMode        False
CenterField        12000.00 G
Delay              0.0 s
FieldFlyback       On
FieldResol         0.02441
FieldWait          Wait LED off
GFactor            2.000000
SetToSampleG       False
SweepDirection     Up
SweepWidth         4000.0 G

.DVC     freqCounter, 1.0

FrequencyMon       33.682796 GHz
QMonitBridge       Off

.DVC     ftBridge, 1.0

Attenuation        60.00 dB
ELDORAtt           30 dB
FrequencyA         33.500000 GHz
VideoBW            200 MHz
VideoGain          27 dB

.DVC     ftEpr, 1.0

AutoTimeOut        True
AveragesPerScan    36
FTEzB0SettlDel     0 s
FTEzB0Step         0 G
FTEzCurrELDOR      33.217436 GHz
FTEzD11deer        0 ns
FTEzD20deer        0 ns
FTEzD3deer         300 ns
FTEzDXdeer         0 ns
FTEzDelay0         200 ns
FTEzDelay1         200 ns
FTEzDelay2         300 ns
FTEzDeltaX         4 ns
FTEzDeltaY         4 ns
FTEzELDORStart     33.217436 GHz
FTEzELDORWidth     0.000000 GHz
FTEzENDORDetDel    0 ns
FTEzExtTrgDel      200 ns
FTEzIntgBase       4 ns
FTEzIntgGate       88 ns
FTEzMWPiHalf       20 ns
FTEzP20deer        0 ns
FTEzP3             40 ns
FTEzRF1Pi          0 ns
FTEzRF1PlsSep      4 ns
FTEzRF1Pump        0.500 MHz
FTEzRF1Start       0.500 MHz
FTEzRF1Width       0.000 MHz
FTEzSRELDORExp     False
FTEzSXdeer         1024
FTEzSXdeerExp      False
FTEzSleep          0 s
PPExtTrg           False
PPExtTrgSlope      Rising
PlsSPELEXPSlct     Decay
PlsSPELLISTSlct    2-step
PlsSPELPhPrgEx     Normal
QuadDetect         True
ReplaceMode        Off
ShotRepTime        2499.00 us
ShotsPLoop         36
SptProgress        100 %
SweepsPExp         1
TriggerTimeOut     111 s
XSpecRes           1024
YSpecRes           1

.DVC     recorder, 1.0

BaselineCorr       Off
NbScansAcc         1
NbScansDone        1
NbScansToDo        1
ReplaceMode        Off

.DVC     routeTrg, 1.0


.DVC     sigChanSmall, 1.0


.DVC     transRec, 1.0


*
************************************************************
