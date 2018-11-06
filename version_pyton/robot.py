#!/usr/bin/env python3

import wpilib


class MyRobot(wpilib.SampleRobot):
    '''Main robot class'''

    def robotInit(self):
        '''Code pour initialiser le robot doit etre mis ici'''

        self.joysyick = wpilib.Joystick(0)  # USB port a utilise. peux etre 0, 1, 2 ou 3
        
        self.moteur_gauche = wpilib.Victor(0)
        self.moteur_droit  = wpilib.Victor(1)
        self.robot_drive = wpilib.RobotDrive(leftMotor = self.moteur_gauche, rightMotor = self.moteur_droit)

        self.moteur_tapis = wpilib.Victor(2)

        self.compresseur = wpilib.Compressor()
        self.compresseur.start()

        self.piston = wpilib.DoubleSolenoid(forwardChannel=0, reverseChannel=1)

        self.pousse_block = wpilib.DoubleSolenoid(forwardChannel=2, reverseChannel=3)

        # gyro calibration constant, may need to be adjusted
        # gyro value of 360 is set to correspond to one full revolution
        self.voltsPerDegreePerSecond = .0128
        self.gyro = wpilib.AnalogGyro(channel=0)

    def disabled(self):
        '''Called when the robot is disabled'''
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def autonomous(self):
        '''Called when autonomous mode is enabled'''
        
        timer = wpilib.Timer()
        timer.start()

        self.gyro.setSensitivity(self.voltsPerDegreePerSecond)  # calibrates gyro values to equal degrees

        while self.isAutonomous() and self.isEnabled():
            
            debut = timer.get()
            if (timer.get()-debut) < 4.0:
                # Avance durant 4 second
                self.robot_drive.arcadeDrive(0.5, 0)
            elif self.gyro.getAngle() < 90 :
                # Tourne jusqu a 90 degree
                self.robot_drive.arcadeDrive(0, 0,5)
                debut = timer.get()
            elif (timer.get() - debut) < 4.0:
                #avance durant 4 seconde
                self.robot_drive.arcadeDrive(0.5, 0)
            elif self.gyro.getAngle() > 5 :
                # Tourne jusqu a 90 degree
                self.robot_drive.arcadeDrive(0, -0.5)
            else:
                # Arrete le robot
                self.robot_drive.arcadeDrive(0, 0)

            wpilib.Timer.delay(0.01)

    def operatorControl(self):
        '''Called when operation control mode is enabled'''

        while self.isOperatorControl() and self.isEnabled():
            
            # Deplacement
            self.robot_drive.arcadeDrive(self.joysyick.getY(), self.joysyick.getX())

            # Tapis roulant
            if self.joysyick.getRawButton(2):
                vitesse = 1  # Avance vite
            elif self.joysyick.getRawButton(3):
                vitesse = -1  # Recule vite
            else:
                vitesse = 0  # Arrete

            self.moteur_tapis.set(.8)

            #Piston
            if self.joysyick.getRawButton(1):
                self.piston.set(wpilib.DoubleSolenoid.Value.kForward)
            else:
                self.piston.set(wpilib.DoubleSolenoid.Value.kReverse)

            # Pousse Block
            if self.joysyick.getRawButton(2):
                self.pousse_block.set(wpilib.DoubleSolenoid.Value.kForward)
            else:
                self.pousse_block.set(wpilib.DoubleSolenoid.Value.kReverse)


            wpilib.Timer.delay(0.04)


if __name__ == '__main__':
    wpilib.run(MyRobot,
               physics_enabled=True)

