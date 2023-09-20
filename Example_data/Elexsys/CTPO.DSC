#DESC	1.2 * DESCRIPTOR INFORMATION ***********************
*
*	Dataset Type and Format:
*
DSRC	EXP
BSEQ	BIG
IKKF	REAL
XTYP	IDX
YTYP	IGD
ZTYP	NODATA
*
*	Item Formats:
*
IRFMT	D
YFMT	D
*
*	Data Ranges and Resolutions:
*
XPTS	1024
XMIN	3482.000000
XWID	4.000000
YPTS	40
YMIN	0.000000
YWID	1688.569000
*
*	Documentational Text:
*
TITL	'CTPO_WT-bur2'
IRNAM	'Intensity'
XNAM	'Field'
YNAM	'Time'
IRUNI	''
XUNI	'G'
YUNI	's'
*
************************************************************
*
#SPL	1.2 * STANDARD PARAMETER LAYER
*
OPER    marcin
DATE    02/13/19
TIME    14:12:53
CMNT    
SAMP    
SFOR    
STAG    C
EXPT    CW
OXS1    IADC
AXS1    B0VL
AXS2    ETIM
AXS3    
A2RS    40
A1CT    0.3484
A1SW    0.0004
MWFQ    9.782011e+09
MWPW    0.00202
AVGS    2
RESO    tm9103
SPTP    0.01024
RCAG    60
RCHM    1
B0MA    8e-06
B0MF    100000
RCPH    0.0
RCOF    0.0
A1RS    1024
RCTC    0.02048
*
************************************************************
*
#DSL	1.0 * DEVICE SPECIFIC LAYER
*

.DVC     acqStart, 1.0


.DVC     delay, 1.0

Delay              20000 ms
NbPoints           40

.DVC     fieldCtrl, 1.0

CenterField        3484.00 G
Delay              0.0 s
FieldFlyback       On
FieldWait          Wait LED off
GFactor            2.005490
SetToSampleG       False
SweepDirection     Up
SweepWidth         4.0 G

.DVC     fieldSweep, 1.0


.DVC     freqCounter, 1.0

FrequencyMon       9.782011 GHz
QMonitBridge       On

.DVC     mwBridge, 1.0

AcqFineTuning      Never
Power              2.020 mW
PowerAtten         20 dB

.DVC     recorder, 1.0

BaselineCorr       On
NbScansAcc         2
NbScansDone        2
NbScansToDo        2
ReplaceMode        Off

.DVC     scanEnd, 1.0


.DVC     signalChannel, 1.0

AFCTrap            True
Calibrated         True
ConvTime           10.24 ms
DModAFCTrap        True
DModAmp            1.00 G
DModCalibrated     True
DModDetectSCT      First
DModEliDelay       1.0 us
DModExtLockIn      False
DModExtTrigger     False
DModFieldMod       First
DModGain           60 dB
DModHighPass       True
DModIntegrator     True
DModModOutput      Internal
DModSignalInput    Internal
DModTimeConst      1.28 ms
DoubleModFreq      5.00 kHz
DoubleModPhase     0.0
DoubleMode         False
EliDelay           1.0 us
ExtLockIn          False
ExtTrigger         False
Gain               60 dB
Harmonic           1
HighPass           True
Integrator         False
ModAmp             0.08 G
ModFreq            100.00 kHz
ModInput           Internal
ModOutput          Internal
ModPhase           0.0
Offset             0.0 %
QuadMode           False
QuadPhase          90.0
Resolution         1024
Resonator          1
SctNorm            True
SctRevision        DSC2
SignalInput        Internal
SweepTime          10.49 s
TimeConst          20.48 ms
TuneCaps           32

*
************************************************************
