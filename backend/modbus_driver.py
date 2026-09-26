"""
Industrial Modbus-TCP Hardware Ingestion Driver
Connects to Schneider Electric Energy Meters (EasyLogic PM5000/PM1000, EM6400, PowerLogic ION)
and Industrial IoT Gateways (EcoStruxure Edge Box / Moxa / Advantech).
"""

import time
import math
import struct
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from pymodbus.client import ModbusTcpClient
except ImportError:
    ModbusTcpClient = None

class SchneiderModbusDriver:
    def __init__(self):
        self.mode = "SIMULATION"  # "SIMULATION" or "LIVE_MODBUS"
        self.host = "127.0.0.1"
        self.port = 502
        self.slave_id = 1
        self.meter_model = "Schneider Electric EasyLogic™ PM5350"
        self.client = None
        self.is_connected = False
        self.last_poll_time = None
        self.last_error = None
        
        # Standard Schneider Register Offsets (0-indexed or 1-indexed depending on gateway)
        # PowerLogic / EasyLogic standard mapping:
        self.reg_active_power = 3059     # Total Active Power (kW) - Float32 (2 registers)
        self.reg_reactive_power = 3067   # Total Reactive Power (kVAR) - Float32
        self.reg_power_factor = 3083     # Total Power Factor - Float32
        self.reg_frequency = 3109        # Frequency (Hz) - Float32
        self.reg_active_energy = 3203    # Total Active Energy Import (kWh) - Float32 / Int64

    def configure(self, host: str, port: int = 502, slave_id: int = 1, meter_model: str = None, mode: str = "SIMULATION") -> Dict[str, Any]:
        """Updates connection parameters."""
        self.host = host
        self.port = port
        self.slave_id = slave_id
        if meter_model:
            self.meter_model = meter_model
        self.mode = mode
        
        if self.mode == "LIVE_MODBUS":
            return self.connect()
        else:
            self.disconnect()
            return {"status": "ok", "mode": "SIMULATION", "message": "Operating in Physics Digital Twin Simulation mode."}

    def connect(self) -> Dict[str, Any]:
        """Attempts connection to the physical Modbus-TCP gateway."""
        if ModbusTcpClient is None:
            self.last_error = "pymodbus library not available"
            return {"status": "error", "message": self.last_error}
            
        try:
            if self.client:
                self.client.close()
            self.client = ModbusTcpClient(self.host, port=self.port, timeout=3.0)
            self.is_connected = self.client.connect()
            if self.is_connected:
                self.last_error = None
                return {"status": "ok", "mode": "LIVE_MODBUS", "connected": True, "host": self.host, "port": self.port}
            else:
                self.last_error = f"Could not establish TCP connection to {self.host}:{self.port}"
                self.is_connected = False
                return {"status": "error", "message": self.last_error}
        except Exception as e:
            self.last_error = str(e)
            self.is_connected = False
            return {"status": "error", "message": self.last_error}

    def disconnect(self):
        """Disconnects Modbus client."""
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
        self.is_connected = False

    def read_telemetry(self) -> Optional[Dict[str, Any]]:
        """Reads live registers from Schneider energy meter."""
        if not self.is_connected or not self.client:
            return None
            
        try:
            # Read 30 registers starting at 3059 for electrical parameters
            rr = self.client.read_holding_registers(address=self.reg_active_power, count=30, slave=self.slave_id)
            if rr.isError():
                self.last_error = f"Modbus Read Error: {rr}"
                return None
                
            # Helper to unpack IEEE-754 32-bit float from 2 big-endian registers
            def decode_float(reg1, reg2):
                packed = struct.pack('>HH', reg1, reg2)
                return struct.unpack('>f', packed)[0]

            regs = rr.registers
            active_power_kw = round(decode_float(regs[0], regs[1]), 2)
            reactive_power_kvar = round(decode_float(regs[8], regs[9]), 2)
            power_factor = round(decode_float(regs[24], regs[25]), 3)

            self.last_poll_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {
                "active_power_kw": active_power_kw,
                "reactive_power_kvar": reactive_power_kvar,
                "power_factor": power_factor,
                "meter_model": self.meter_model,
                "timestamp": self.last_poll_time
            }
        except Exception as e:
            self.last_error = str(e)
            return None

    def get_status(self) -> Dict[str, Any]:
        """Returns driver status."""
        return {
            "mode": self.mode,
            "host": self.host,
            "port": self.port,
            "slave_id": self.slave_id,
            "meter_model": self.meter_model,
            "is_connected": self.is_connected,
            "last_poll_time": self.last_poll_time,
            "last_error": self.last_error
        }
