"""
class Oscillator
{
  public:
    Oscillator(int trim=0) {_trim=trim;};
    void attach(int pin, bool rev =false);
    void detach();
    
    void SetA(unsigned int A) {_A=A;};
    void SetO(unsigned int O) {_O=O;};
    void SetPh(double Ph) {_phase0=Ph;};
    void SetT(unsigned int T);
    void SetTrim(int trim){_trim=trim;};
    int getTrim() {return _trim;};
    void SetPosition(int position); 
    void Stop() {_stop=true;};
    void Play() {_stop=false;};
    void Reset() {_phase=0;};
    void refresh();
    
  private:
    bool next_sample();  
    
  private:
    //-- Servo that is attached to the oscillator
    Servo _servo;
    
    //-- Oscillators parameters
    unsigned int _A;  //-- Amplitude (degrees)
    unsigned int _O;  //-- Offset (degrees)
    unsigned int _T;  //-- Period (miliseconds)
    double _phase0;   //-- Phase (radians)
    
    //-- Internal variables
    int _pos;         //-- Current servo pos
    int _trim;        //-- Calibration offset
    double _phase;    //-- Current phase
    double _inc;      //-- Increment of phase
    double _N;        //-- Number of samples
    unsigned int _TS; //-- sampling period (ms)
    
    long _previousMillis; 
    long _currentMillis;
    
    //-- Oscillation mode. If true, the servo is stopped
    bool _stop;

    //-- Reverse mode
    bool _rev;
};

MicroPython driver to Generate sinusoidal oscillations in the servos
Requires a Pulse width modulation (PWM) pin. On the ESP8266 the 
pins 0, 2, 4, 5, 12, 13, 14 and 15 all support PWM. 
The limitation is that they must all be at the same frequency, 
and the frequency must be between 1Hz and 1kHz.
Oscillator.pde: GPL license (c) Juan Gonzalez-Gomez (Obijuan), 2011
"""
import math, time, servo

Class Oscillator:
	def __init__(self, trim = 0):
		self._trim = trim
		FIXME
		
	#-- Attach an oscillator to a servo
	#-- Input: pin is the arduino pin were the servo is connected
	def attach(self, pin, rev): 
		if not self._servo.attached():	#-- If the oscillator is detached,
			self._servo.attach(pin)	#-- Attach the servo and move it to the home position
			self._servo.write(90)

		#-- Initialization of oscilaltor parameters
		self._TS = 30
		self._T = 2000
		self._N = self._T / self._TS
		self._inc = 2 * math.pi / self._N
		self._previousMillis = 0

		#-- Default parameters
		self._A = 45
		self._phase = 0
		self._phase0 = 0
		self._O = 0
		self._stop = False

		#-- Reverse mode
		self._rev = rev

	#-- Detach an oscillator from his servo
	def detach(self):
		if self._servo.attached(): #-- If the oscillator is attached,
		self._servo.detach()

	#--  Set the oscillator Phase (radians)
	def SetA(self, int A):
		self._A = A

	#-- Set the oscillator Phase (radians)
	def SetO(self, int O):
		self._O = O

	#-- Set the oscillator Phase (radians)
	def SetPh(self, Ph):
		self._phase0 = Ph

	#-- Set the oscillator period, ms
	def SetT(self, int T):
		self._T = T #-- Assign the period
		self._N = self._T / self._TS #-- Recalculate the parameters
		self._inc = 2 * math.pi / self._N

	#-- Manual set of the position
	def SetPosition(self, position):
		self._servo.write(position + self._trim)

	#-- SetTrim
	def SetTrim(self, trim):
		self._trim = trim

	#-- getTrim
	def getTrim(self):
		return self._trim

	#-- Stop
	def Stop(self):
		self._stop = True

	#-- Play
	def Play(self):
		self._stop = False

	#-- Reset
	def Reset(self):
		self._phase = 0

	"""
	This function should be periodically called
	in order to maintain the oscillations. It calculates
	if another sample should be taken and position the servo if so
	"""
	def refresh(self):
		if next_sample(): #-- Only When TS milliseconds have passed, sample is obtained
			if not self._stop: #-- If the oscillator is not stopped, the servo position
				self._pos = math.round(self._A * math.sin(self._phase + self._phase0) + self._O) #-- Sample the sine function and set the servo pos
			if self._rev: 
				self._pos = -self._pos FIXME
			self._servo.write(self._pos + 90 + self._trim)

			#-- Increment the phase
			#-- It is always increased, when the oscillator is stop
			#-- so that the coordination is always kept
			self._phase = self._phase + self._inc

#-- should be taken (i.e. the TS time has passed since
#-- the last sample was taken
def next_sample(self):
	self._currentMillis = time.ticks_ms() #-- Read current time
	if self._currentMillis - self._previousMillis > self._TS:		
		self._previousMillis = self._currentMillis;   
		return True
	return False
