import xml.etree.ElementTree as ET
import json
import logging
import sys

# Crea il logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Crea il gestore di log per scrivere i messaggi sulla console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Crea il formattatore dei messaggi di log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Aggiungi il gestore di log al logger
logger.addHandler(console_handler)


# Crea una funzione per la conversione del file XML in un dizionario Python
def xml_to_dict(filename):
    # Inizia a processare il file XML
    logger.info(f'Inizio conversione del file {filename}')
    context = ET.iterparse(filename, events=('start', 'end'))
    _, root = next(context)
    stack = [root]
    for event, elem in context:
        if event == 'start':
            stack.append(elem)
        elif event == 'end':
            parent = stack[-2]
            if elem.tag in parent:
                if not isinstance(parent[elem.tag], list):
                    parent[elem.tag] = [parent[elem.tag]]
                parent[elem.tag].append(elem.attrib)
            else:
                parent[elem.tag] = elem.attrib
            stack.pop()
        # Scrivi un messaggio di log ogni 10000 elementi processati
        if len(stack) == 1 and len(stack[0]) % 10000 == 0:
            logger.debug(f'Processati {len(stack[0])} elementi')
    return root.attrib


# Converte il file XML in un dizionario Python
dict_data = xml_to_dict('data/export_cda.xml')

# Scrivi il file JSON
with open('output/cda.json', 'w') as file:
    json.dump(dict_data, file)
