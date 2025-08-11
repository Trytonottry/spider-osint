# integrations/misp.py
import pymisp

# integrations/misp.py
def send_iocs_to_misp(iocs: dict, event_title: str = "Auto-Extracted IOCs"):
    # Создаём событие и добавляем атрибуты
    for ioc_type, values in iocs.items():
        for value in values:
            add_attribute(event.uuid, {"type": ioc_type, "value": value})

def send_to_misp(event_title: str,  dict, misp_url: str, api_key: str):
    misp = pymisp.PyMISP(misp_url, api_key, ssl=False)
    event = pymisp.MISPEvent()
    event.info = event_title
    event = misp.add_event(event, pythonify=True)

    for key, value in data.items():
        attr = pymisp.MISPAttribute()
        attr.type = "text"
        attr.value = str(value)
        attr.category = "External analysis"
        misp.add_attribute(event.uuid, attr)