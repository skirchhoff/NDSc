'''
    device vendor scanner for local area networks 1.0
'''

import sched, time, os, json



class NTDevice:

    def __init__(self,name,ip,mac,interface):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.interface = interface


class PyOne:

    def __init__(self):
        self.i = 0
        self.devs = {}
        self.oui_by_id = {}
        self.oui_by_name = {}
        self.device_stack = {}

        self.read_OUI_file()

        p = os.popen('arp -a')

        while 1:
            line = p.readline()
            if not line:
                #print(self.devs)
                self.write_report()
                #print(self.oui_by_id)
                break

            #print(line)
            self.add_device(line)


    def add_device (self, dl):

        da = dl.replace("(", "").replace(")", "").split( " " )

        if self.mac_report(da[3]) in self.oui_by_id:
            self.devs[da[1]] = {"name":da[0],
                                "ip":da[1],
                                "mac":da[3],
                                "interface":da[5],
                                "manufacturer":self.oui_by_id[self.mac_report(da[3])]}
        else:
            self.devs[da[1]] = {"name": da[0],
                                "ip": da[1],
                                "mac": da[3],
                                "interface": da[5],
                                "manufacturer": "unkown"}

        #NTDevice(da[0],da[1],da[3],da[5])

    def mac_report (self, m):

        ma = m.split(":")
        tx = ""
        for x in ma[0:3] :
            if len(x)==1:
                tx = tx+"0"+x
            else:
                tx = tx+x
        return tx.upper()


    def device_mac (self, m):

        ma = m.split(":")
        tx = ""
        for x in ma:
            if len(x) == 1:
                tx = tx + "0" + x
            else:
                tx = tx + x
        return tx.upper()

    '''
        {vendor} - {short_mac} - {device info}
    '''


    def read_OUI_file (self):

        if os.path.isfile("/Users/stephan/PycharmProjects/PyOne/vendor_mac_stack"):
            f1 = open("vendor_mac_stack")
            self.oui_by_id = json.loads(f1.read())
        else:
            print("vendor_mac_stack not found")

    def write_report (self):

        print("nds - Network Device Scanner 1.0\n\n")

        for x in self.devs:

            print("device name:         " + self.devs[x]["name"])
            print("device ip-address:   " + self.devs[x]["ip"])
            print("device mac-address:  " + self.devs[x]["mac"])
            print("device manufacturer: " + self.devs[x]["manufacturer"])
            print("")
            print("")






# periodic calls test functions
scheduler = sched.scheduler(time.time, time.sleep)
def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, periodic,(scheduler, interval, action, actionargs))
    action(actionargs)
    scheduler.run()

def query_rate_limit (p01):
    p01.i+=1
    print("count {}".format(p01.i))


if __name__ == '__main__':

    o1 = PyOne()
    print("out")

    # test for periodic calls
    # periodic(scheduler, 0.01, query_rate_limit,(PyOne()))



