EESchema Schematic File Version 2
LIBS:conn
LIBS:ClassD_Audio
LIBS:device
LIBS:power
LIBS:PMIC
LIBS:linear
LIBS:74xx
LIBS:uSD-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "2 jun 2017"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONN_01X08 J1
U 1 1 59A61204
P 1650 1750
F 0 "J1" H 1650 2200 50  0000 C CNN
F 1 "CONN_01X08" V 1750 1750 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Angled_1x08_Pitch1.27mm" H 1650 1750 50  0001 C CNN
F 3 "" H 1650 1750 50  0001 C CNN
	1    1650 1750
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1850 1400 3000 1400
Wire Wire Line
	1850 1500 3000 1500
Wire Wire Line
	1850 1600 3000 1600
Wire Wire Line
	1850 1700 3000 1700
Wire Wire Line
	1850 1800 3000 1800
Wire Wire Line
	1850 1900 3000 1900
Wire Wire Line
	1850 2000 3000 2000
Wire Wire Line
	1850 2100 3000 2100
Text Label 2100 1400 0    60   ~ 0
NC
Wire Notes Line
	2050 1100 2050 2300
Wire Notes Line
	2400 1100 2400 2300
Text Notes 2100 1200 0    60   ~ 0
SPI
Text Label 2100 1500 0    60   ~ 0
/CS
Text Label 2100 1600 0    60   ~ 0
DI
Text Label 2100 1700 0    60   ~ 0
Vdd
Text Label 2100 1800 0    60   ~ 0
CLK
Text Label 2100 1900 0    60   ~ 0
Vss
Text Label 2100 2000 0    60   ~ 0
DO
Text Label 2100 2100 0    60   ~ 0
RSV
Wire Notes Line
	2750 1100 2750 2300
Text Notes 2450 1200 0    60   ~ 0
SD
Text Notes 2450 1400 0    60   ~ 0
DAT2
Text Notes 2450 1500 0    60   ~ 0
DAT3
Text Notes 2450 1600 0    60   ~ 0
CMD
Text Notes 2450 1700 0    60   ~ 0
Vdd
Text Notes 2450 1800 0    60   ~ 0
CLK
Text Notes 2450 1900 0    60   ~ 0
Vss
Text Notes 2450 2000 0    60   ~ 0
DAT0
Text Notes 2450 2100 0    60   ~ 0
DAT1
Text Label 4000 1500 0    60   ~ 0
Vdd
Text Label 4000 2050 0    60   ~ 0
Vss
$Comp
L VDD #PWR01
U 1 1 59A615B3
P 3600 1450
F 0 "#PWR01" H 3600 1300 50  0001 C CNN
F 1 "VDD" H 3600 1600 50  0000 C CNN
F 2 "" H 3600 1450 50  0001 C CNN
F 3 "" H 3600 1450 50  0001 C CNN
	1    3600 1450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR02
U 1 1 59A615C9
P 3600 2100
F 0 "#PWR02" H 3600 1850 50  0001 C CNN
F 1 "GND" H 3600 1950 50  0000 C CNN
F 2 "" H 3600 2100 50  0001 C CNN
F 3 "" H 3600 2100 50  0001 C CNN
	1    3600 2100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3600 1450 3600 1600
Wire Wire Line
	3600 1500 4000 1500
Wire Wire Line
	3600 1900 3600 2100
Wire Wire Line
	3600 2050 4000 2050
$Comp
L C C1
U 1 1 59A6164E
P 3600 1750
F 0 "C1" H 3625 1850 50  0000 L CNN
F 1 "100nF" H 3625 1650 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 3638 1600 50  0001 C CNN
F 3 "" H 3600 1750 50  0001 C CNN
	1    3600 1750
	1    0    0    -1  
$EndComp
$Comp
L C C2
U 1 1 59A6168B
P 3950 1750
F 0 "C2" H 3975 1850 50  0000 L CNN
F 1 "1uF" H 3975 1650 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 3988 1600 50  0001 C CNN
F 3 "" H 3950 1750 50  0001 C CNN
	1    3950 1750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 1900 3950 2050
Connection ~ 3600 2050
Connection ~ 3600 1500
Connection ~ 3950 1500
Wire Wire Line
	3950 1600 3950 1500
Connection ~ 3950 2050
$Comp
L 74HC165 U2
U 1 1 59A61903
P 5150 3750
F 0 "U2" H 5150 3250 60  0000 C CNN
F 1 "74HC165" H 5150 4250 60  0000 C CNN
F 2 "Housings_SSOP.pretty:SSOP-16_4.4x5.2mm_Pitch0.65mm" H 5150 3750 60  0001 C CNN
F 3 "" H 5150 3750 60  0000 C CNN
	1    5150 3750
	1    0    0    -1  
$EndComp
$Comp
L 74HC595 U1
U 1 1 59A619F4
P 5100 5300
F 0 "U1" H 5250 5900 50  0000 C CNN
F 1 "74HC595" H 5100 4700 50  0000 C CNN
F 2 "Housings_SSOP.pretty:SSOP-16_4.4x5.2mm_Pitch0.65mm" H 5100 5300 50  0001 C CNN
F 3 "" H 5100 5300 50  0001 C CNN
	1    5100 5300
	1    0    0    -1  
$EndComp
$EndSCHEMATC
