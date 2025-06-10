#DESC	1.2 * DESCRIPTOR INFORMATION ***********************
*
*	Dataset Type and Format:
*
DSRC	EXP
BSEQ	BIG
IKKF	CPLX
XTYP	IDX
YTYP	IDX
ZTYP	NODATA
*
*	Item Formats:
*
IRFMT	D
IIFMT	D
*
*	Data Ranges and Resolutions:
*
XPTS	160
XMIN	-0.000000
XWID	2544.000000
YPTS	20
YMIN	-0.000000
YWID	152.000000
*
*	Documentational Text:
*
TITL	'3P_ESEEM_FNR_szpinak_120K_tau_sweep'
IRNAM	'Intensity'
IINAM	'Intensity'
XNAM	'Time'
YNAM	'Time'
IRUNI	''
IIUNI	''
XUNI	'ns'
YUNI	'ns'
*
************************************************************
*
#SPL	1.2 * STANDARD PARAMETER LAYER
*
OPER    bruker
DATE    05/23/25
TIME    16:12:34
CMNT    
SAMP    
SFOR    
STAG    C
EXPT    
OXS1    
AXS1    
AXS2    
AXS3    
MWPW    2.049e-07
A1CT    0.3464
B0VL    0.3452008
A1SW    0.008
MWFQ    9.683969e+09
AVGS    2
*
************************************************************
*
#DSL	1.0 * DEVICE SPECIFIC LAYER
*

.DVC     acqStart, 1.0


.DVC     cwBridge, 1.0

AcqFineTuning      Never
Power              0.0002049 mW
PowerAtten         60 dB

.DVC     fieldCtrl, 1.0

CenterField        3464.00 G
Delay              0.0 s
FieldFlyback       On
FieldWait          Wait LED off
GFactor            2.000000
SetToSampleG       False
SweepDirection     Up
SweepWidth         80.0 G

.DVC     freqCounter, 1.0

FrequencyMon       9.683969 GHz
QMonitBridge       On

.DVC     ftBridge, 1.0

Attenuation        6.50 dB
ELDORAtt           30 dB
FrequencyA         9.500000 GHz
VideoBW            200 MHz
VideoGain          39 dB

.DVC     ftEpr, 1.0

AveragesPerScan    100
FTEzB0SettlDel     0 s
FTEzB0Step         0 G
FTEzCurrELDOR      9.170000 GHz
FTEzD11deer        0 ns
FTEzD20deer        0 ns
FTEzD3deer         300 ns
FTEzDXdeer         0 ns
FTEzDelay0         428 ns
FTEzDelay1         104 ns
FTEzDelay2         40 ns
FTEzDeltaX         16 ns
FTEzDeltaY         8 ns
FTEzELDORStart     9.170000 GHz
FTEzELDORWidth     0.000000 GHz
FTEzENDORDetDel    0 ns
FTEzExtTrgDel      200 ns
FTEzIntgBase       4 ns
FTEzIntgGate       36 ns
FTEzMWPiHalf       12 ns
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
PlsSPELEXPSlct     3-Pls vs 2-Pls
PlsSPELLISTSlct    4-step
PlsSPELPhPrgEx     Normal
QuadDetect         True
ReplaceMode        Off
ShotRepTime        3999.42 us
ShotsPLoop         100
SweepsPExp         2
TriggerTimeOut     10 s
XSpecRes           160
YSpecRes           20

.DVC     recorder, 1.0

BaselineCorr       Off
NbScansAcc         2
NbScansDone        2
NbScansToDo        2
ReplaceMode        Off

.DVC     routeTrg, 1.0


.DVC     sigChanSmall, 1.0


.DVC     transRec, 1.0


*
************************************************************
