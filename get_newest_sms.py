import os

p = os.popen('get_sms').read()
p2 = p.split(">")
p3 = p2[13].split("<")
p3[0]
print("Neuste Empfangene Nachricht ist: ",p3[0])