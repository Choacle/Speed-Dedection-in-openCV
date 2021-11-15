import pyads

plc = pyads.Connection('127.0.0.1.1.1', pyads.PORT_TC3PLC1)
plc.open()

i = 1
plc.write_by_name("variableOne", i)
plc.close()