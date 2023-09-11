#DESC	1.2 * DESCRIPTOR INFORMATION ***********************
*
*	Dataset Type and Format:
*
DSRC	EXP
BSEQ	BIG
IKKF	REAL
XTYP	IDX
YTYP	NODATA
ZTYP	NODATA
*
*	Item Formats:
*
IRFMT	D
*
*	Data Ranges and Resolutions:
*
XPTS	2048
XMIN	83.900000
XWID	2432.200000
*
*	Documentational Text:
*
TITL	'dolny_B_6K_0,2mW'
IRNAM	'Intensity'
XNAM	'Field'
IRUNI	''
XUNI	'G'
*
************************************************************
*
#SPL	1.2 * STANDARD PARAMETER LAYER
*
OPER    bruker
DATE    03/02/21
TIME    11:50:31
CMNT    
SAMP    
SFOR    
STAG    C
EXPT    CW
OXS1    IADC
AXS1    B0VL
AXS2    NONE
AXS3    
A1CT    0.13
A1SW    0.24322
MWFQ    9.391831e+09
MWPW    0.0002
AVGS    2
RESO    shqe0511
SPTP    0.04096
RCAG    60
RCHM    1
B0MA    0.001
B0MF    100000
RCPH    0.0
RCOF    0.0
A1RS    2048
RCTC    0.01024
*
************************************************************
*
#DSL	1.0 * DEVICE SPECIFIC LAYER
*

.DVC     acqStart, 1.0


.DVC     fieldCtrl, 1.0

CenterField        1300.00 G
Delay              0.0 s
FieldFlyback       On
FieldWait          Wait LED off
GFactor            6.000000
SetToSampleG       False
SweepDirection     Up
SweepWidth         2432.2 G

.DVC     fieldSweep, 1.0


.DVC     freqCounter, 1.0

FrequencyMon       9.391831 GHz
QMonitBridge       On

.DVC     mwBridge, 1.0

AcqFineTuning      Never
Power              0.2000 mW
PowerAtten         30 dB

.DVC     recorder, 1.0

BaselineCorr       Off
NbScansAcc         2
NbScansDone        2
NbScansToDo        2
ReplaceMode        Off

.DVC     scanEnd, 1.0


.DVC     signalChannel, 1.0

AFCTrap            True
Calibrated         True
ConvTime           40.96 ms
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
ModAmp             10.00 G
ModFreq            100.00 kHz
ModInput           Internal
ModOutput          Internal
ModPhase           0.0
Offset             0.0 %
QuadMode           False
QuadPhase          90.0
Resolution         2048
Resonator          1
SctNorm            True
SctRevision        DSC2
SignalInput        Internal
SweepTime          83.89 s
TimeConst          10.24 ms
TuneCaps           36

*
************************************************************
