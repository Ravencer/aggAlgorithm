import re

def read_net_file(file_path):
    nets = {}
    nodes = []
    elements = []
    data = ''
    reading_nets = False
    current_node = None
    with open(file_path, 'r') as file:
        data = file.read()

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith('$NETS'):
                reading_nets = True
                continue
            elif reading_nets and line.startswith('$END'):
                break
            
            
            if reading_nets:
                match = re.match(r'^([A-Za-z\d]+);(.+)$', line)
                if match:
                    current_node = match.group(1)
                    connected_elements = match.group(2).split()
                    nets[current_node] = {}
                    for element in connected_elements:
                        element_name, _, pin = element.partition('.')
                        pin = pin.replace(',', '').replace('.', '')
                        if element_name:
                            nets[current_node][element_name] = {'pin': pin}
                            elements.append(element_name)
                            nodes.append(current_node)
                elif current_node is not None:
                    connected_elements = line.split()
                    for element in connected_elements:
                        element_name, _, pin = element.partition('.')
                        pin = pin.replace(',', '').replace('.', '')
                        if element_name:
                            nets[current_node][element_name] = {'pin': pin}
                            elements.append(element_name)
                            nodes.append(current_node)

    return nets, list(set(nodes)), list(set(elements)), data