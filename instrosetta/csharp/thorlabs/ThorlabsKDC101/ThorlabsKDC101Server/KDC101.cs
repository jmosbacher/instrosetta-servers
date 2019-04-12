using System;
using System.Collections.Generic;
using Thorlabs.MotionControl.Tools;
using Thorlabs.MotionControl.DeviceManagerCLI;
using Thorlabs.MotionControl.GenericMotorCLI;
using Thorlabs.MotionControl.GenericMotorCLI.ControlParameters;
using Thorlabs.MotionControl.KCube.DCServoCLI;


namespace ThorlabsKDC101Server
{
    public enum MotorState { UNKNOWN, IDLE, MOVING };

    public class KDC101
    {
        private KCubeDCServo _kCubeDCServoMotor = null;

        private static MotorState _state = MotorState.UNKNOWN;

        private static ulong _taskID;


        public KDC101()
        {
        }

        public bool Connected
        {
            get
            {
                if (_kCubeDCServoMotor == null)
                {
                    return false;
                }
                else
                {
                    return true;
                }
            }
        }

        public MotorState State { get { return _state; } }

        public decimal Resolution { get { return _kCubeDCServoMotor.UnitConverter.DeviceUnitToReal(1, DeviceUnitConverter.UnitType.Length); } }

        public decimal Position
        {
            get
            {
                int iPos = _kCubeDCServoMotor.Position_DeviceUnit;
                return _kCubeDCServoMotor.UnitConverter.DeviceUnitToReal(iPos, DeviceUnitConverter.UnitType.Length);
            }
        }


        public string SerialNo
        {
            get
            {
                if (_kCubeDCServoMotor == null)
                {
                    return "0";
                }
                else
                {
                    return _kCubeDCServoMotor.SerialNo;
                }
            }
        }

        public List<string> GetAvailableDevices(bool includeSimulated=true)
        {
            if (includeSimulated)
            {
                SimulationManager.Instance.InitializeSimulations();
            }
            
            List<string> serialNumbers = DeviceManagerCLI.GetDeviceList(KCubeDCServo.DevicePrefix);
            return serialNumbers;
        }

        public void Connect(string serialNo, int timeout, int interval)
        {
            if (_kCubeDCServoMotor != null)
            {
                if (_kCubeDCServoMotor.SerialNo == serialNo)
                {
                    return;
                }
                else
                {
                    Disconnect();

                }

            }



            DeviceManagerCLI.BuildDeviceList();

            _kCubeDCServoMotor = KCubeDCServo.CreateKCubeDCServo(serialNo);

            // Establish a connection with the device.
            _kCubeDCServoMotor.Connect(serialNo);

            // Wait for the device settings to initialize. We ask the device to
            // throw an exception if this takes more than 5000ms (5s) to complete.
            _kCubeDCServoMotor.WaitForSettingsInitialized(timeout);

            //MotorConfiguration motorSettings = _kCubeDCServoMotor.GetMotorConfiguration(serialNo, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings);
            //motorSettings.DeviceSettingsName = "Z825B";
            //motorSettings.UpdateCurrentConfiguration();
            // Initialize the DeviceUnitConverter object required for real world
            // unit parameters.
            _kCubeDCServoMotor.LoadMotorConfiguration(_kCubeDCServoMotor.DeviceID, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings);

            // This starts polling the device at intervals of 250ms (0.25s).
            _kCubeDCServoMotor.StartPolling(interval);

            // We are now able to enable the device for commands.
            _kCubeDCServoMotor.EnableDevice();

            return;

        }

        public void Disconnect()
        {
            if (!(_kCubeDCServoMotor == null))
            {

                _kCubeDCServoMotor.StopPolling();
                _kCubeDCServoMotor.ShutDown();
                _kCubeDCServoMotor = null;

            }

            return;




        }
        public void Home()
        {
            _state = MotorState.MOVING;
            _kCubeDCServoMotor.ClearDeviceExceptions();
            _taskID = _kCubeDCServoMotor.Home(MoveCompleteFunction);
        
        }

        public Tuple<decimal, decimal> GetRange()
        {

            LimitSwitchParameters realLP = _kCubeDCServoMotor.GetLimitSwitchParams();
            return Tuple.Create((decimal)realLP.AnticlockwiseHardwareLimit, (decimal)realLP.ClockwiseHardwareLimit);

        }

        public static void MoveCompleteFunction(ulong taskID)
        {
            if ((_taskID > 0) && (_taskID == taskID))
            {
                _state = MotorState.IDLE;

                Console.WriteLine("Stopped...");
            }
        }


        public void MoveAbsolute(decimal position)
        {

            int iPos = _kCubeDCServoMotor.UnitConverter.RealToDeviceUnit(position, DeviceUnitConverter.UnitType.Length);
            Console.WriteLine("Requested: " + position.ToString() + " " + _kCubeDCServoMotor.UnitConverter.RealUnits + " " + iPos.ToString() + " device steps.");

            _state = MotorState.MOVING;
            _kCubeDCServoMotor.ClearDeviceExceptions();
            _taskID = _kCubeDCServoMotor.MoveTo_DeviceUnit(iPos, MoveCompleteFunction);
            Console.WriteLine("Moving...");

        }

        public void MoveRelative(MotorDirection direction, decimal distance, int timeout)
        {

            uint iDist = (uint)_kCubeDCServoMotor.UnitConverter.RealToDeviceUnit(distance, DeviceUnitConverter.UnitType.Length);
            _state = MotorState.MOVING;
            _kCubeDCServoMotor.ClearDeviceExceptions();
            _taskID = _kCubeDCServoMotor.MoveRelative_DeviceUnit(direction, iDist, MoveCompleteFunction);
            Console.WriteLine("Moving...");
        }

        public void ThrowLastDeviceException()
        {
            _kCubeDCServoMotor.ThrowLastDeviceException();
        }
    }

}
