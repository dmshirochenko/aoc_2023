import math
from collections import deque

class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def gen_file_reader(file_name):
        with open(file_name, "r") as file:
            for line in file:
                yield line.strip()

class Module:
    def __init__(self, module_id, connections, enabled):
        self.module_id = module_id
        self.connections = connections
        self.enabled = enabled
        self.inputs = {}

    def __repr__(self):
        return f'Module id {self.module_id}'

class BroadCaster(Module):
    def __init__(self, connections):
        super().__init__('broadcaster', connections, True)
    
    def updateState(self, input_signal, input_id):
        return input_signal

class FlipFlop(Module):
    def __init__(self, module_id, connections):
        super().__init__(module_id, connections, False)

    def updateState(self, input_signal, input_id):
        if input_signal == True:
            return None
        self.enabled = not self.enabled
        return self.enabled

class Conjunction(Module):
    def __init__(self, module_id, connections):
        super().__init__(module_id, connections, True)

    def updateState(self, input_signal, input_id):
        self.inputs[input_id] = input_signal
        return not all(value == True for key, value in self.inputs.items())

class ModuleConfig:
    def __init__(self):
        self.modules = {}

    def initModules(self, module_type, module_id, connections):
        if '%' in module_type:
            module = FlipFlop(module_id, connections)
        elif '&' in module_type:
            module = Conjunction(module_id, connections)
        else:
            module = BroadCaster(connections)
        self.modules[module_id] = module

    def initInputs(self, module_type, module_id, connections):
        for connection in connections:
            if self.modules.get(connection):
                self.modules[connection].inputs[module_id] = False

    def input_parse(self, line):
        module_type, connections = line.split(' -> ')
        connections = connections.split(', ')
        module_id = module_type.strip('&%')
        return module_type, module_id, connections

    def get_multiplication_of_low_and_high_pulses(self, file_name, part=None):
        for line in FileReader().gen_file_reader(file_name):
            module_type, module_id, connections = self.input_parse(line)
            self.initModules(module_type, module_id, connections)
        
        # Initialize inputs
        for line in FileReader().gen_file_reader(file_name):
            module_type, module_id, connections = self.input_parse(line)
            self.initInputs(module_type, module_id, connections)

        print('Total number of modules:', len(self.modules))
        high_pulse_count = 0
        low_pulse_count = 0
        module_rx_times = {}

        for cycle in range(5000):
            if cycle == 1000:
                task1_result = high_pulse_count * low_pulse_count
            low_pulse_count += 1
            current_module = self.modules['broadcaster']
            signal = current_module.updateState(0, None)
            queue = deque([(current_module, signal)])

            while queue:
                current_module, signal = queue.popleft()
                for connection in current_module.connections:
                    if signal:
                        high_pulse_count += 1
                    else:
                        low_pulse_count += 1

                    if self.modules.get(connection):
                        if signal and self.modules[connection].module_id == 'lx':
                            if current_module.module_id not in module_rx_times:
                                module_rx_times[current_module.module_id] = cycle + 1
                            if set(module_rx_times) == set(self.modules[connection].inputs):
                                return task1_result, math.lcm(*module_rx_times.values())

                        new_signal = self.modules[connection].updateState(signal, current_module.module_id)
                        if new_signal is not None:
                            queue.append((self.modules[connection], new_signal))

        return high_pulse_count * low_pulse_count

if __name__ == '__main__':
    print('Day 20')
    module_config = ModuleConfig()
    low_high_pulse_product, button_press_count = module_config.get_multiplication_of_low_and_high_pulses(file_name='day_20.txt')
    print('Task 1 result:', low_high_pulse_product)
    print('Task 2 result:', button_press_count)
