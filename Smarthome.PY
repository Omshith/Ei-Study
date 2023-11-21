from abc import ABC, abstractmethod
from datetime import datetime
import re

# Define the Device interface using the Factory Method
class Device(ABC):
    def __init__(self, id):
        self.id = id

    @abstractmethod
    def get_status(self):
        pass

# Define concrete Device classes: Light, Thermostat, and DoorLock
class Light(Device):
    def __init__(self, id, status='off'):
        super().__init__(id)
        self.status = status

    def get_status(self):
        return f"Light {self.id} is {self.status}."

class Thermostat(Device):
    def __init__(self, id, temperature=70):
        super().__init__(id)
        self.temperature = temperature

    def get_status(self):
        return f"Thermostat is set to {self.temperature} degrees."

class DoorLock(Device):
    def __init__(self, id, status='locked'):
        super().__init__(id)
        self.status = status

    def get_status(self):
        return f"Door is {self.status}."

# Define the SmartHomeHub to manage devices, scheduling, and triggers using the Observer Pattern
class SmartHomeHub:
    def __init__(self):
        self.devices = {}
        self.scheduled_tasks = []
        self.triggers = []

    def add_device(self, device):
        self.devices[device.id] = device

    def remove_device(self, device_id):
        if device_id in self.devices:
            del self.devices[device_id]

    def turn_on_device(self, device_id):
        if device_id in self.devices:
            device = self.devices[device_id]
            if isinstance(device, Light):
                device.status = 'on'

    def set_schedule(self, device_id, time, action):
        self.scheduled_tasks.append({"device": device_id, "time": time, "action": action})

    def add_trigger(self, condition, action):
        self.triggers.append({"condition": condition, "action": action})

    def update(self, timestamp):
        for task in self.scheduled_tasks:
            task_time = datetime.strptime(task["time"], "%H:%M")
            if timestamp.hour == task_time.hour and timestamp.minute == task_time.minute:
                command = task["action"]
                self.execute_command(command)

    def execute_command(self, command):
        # Split command into function and arguments
        parts = re.split(r'[()]', command)
        if len(parts) >= 2:
            function_name = parts[0]
            args = parts[1].split(',')
            if function_name in dir(self):
                function = getattr(self, function_name)
                function(*args)

    def get_status_report(self):
        status_report = [device.get_status() for device in self.devices.values()]
        return "\n".join(status_report)

    def get_scheduled_tasks(self):
        return self.scheduled_tasks

    def get_automated_triggers(self):
        return self.triggers

# Main function to run the Smart Home System simulation
def main():
    # Create devices
    light1 = Light(1, 'off')
    thermostat1 = Thermostat(2, 70)
    doorlock1 = DoorLock(3, 'locked')

    # Create the Smart Home Hub
    smart_home_hub = SmartHomeHub()

    # Add devices to the hub
    smart_home_hub.add_device(light1)
    smart_home_hub.add_device(thermostat1)
    smart_home_hub.add_device(doorlock1)

    # Define input commands
    commands = ['turn_on_device(1)', 'set_schedule(2, "06:00", "turn_on_device(1)")', 'add_trigger("temperature > 75", "turn_on_device(1)")']

    # Simulate time and update the hub
    current_time = datetime.strptime("06:00", "%H:%M")
    smart_home_hub.update(current_time)

    # Print the status report, scheduled tasks, and automated triggers
    print("Status Report:", smart_home_hub.get_status_report())
    print("Scheduled Tasks:", smart_home_hub.get_scheduled_tasks())
    print("Automated Triggers:", smart_home_hub.get_automated_triggers())

if __name__ == "__main__":
    main()
