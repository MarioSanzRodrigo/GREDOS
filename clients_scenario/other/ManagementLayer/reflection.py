#!/flask/bin/python 
from importlib import import_module

parental = 'ManagementLayer.RenemaApps.ParentalControl.ParentalControl'
status = 'ManagementLayer.RenemaApps.NetworkStatus.NetworkStatus'
method = 'get_ReneseMessage()'

renese_message = {
    'SenderId': 'sdnal-renese-01',               # RENEMA App Id
    'ReceiverId': 'ml-app-02',       # RENESE Id
    'Service': 'new_connection',
    'Arguments': {
        'device_mac': '68:eb:ae:68:eb:ff', #  14:fe:b5:14:fe:b5, 68:eb:ae:68:eb:ae
        'device_port': 1,
        'port_queue': 3
    }
}

package, module = status.rsplit('.', 1)
print package
print module
generic_module = import_module(package)
generic_instance = getattr(generic_module, module)
generic_instance().get_ReneseMessage(renese_message)
