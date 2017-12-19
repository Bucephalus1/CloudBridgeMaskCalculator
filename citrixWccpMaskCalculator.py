import sys
import math
import argparse


def calculateCitrixWccpMask(args):

    maskCalculationHelp = r'https://docs.citrix.com/en-us/cloudbridge/7-4/brsdx-wrapper-con/brsdx-deployment-wrapper-con/br-adv-wccp-mode-con/cb-wccp-cluster-wrapper-con/cb-wccp-cluster-limitations-planning-con/cb-wccp-cluster-limitations-lb-con.html'
    Uspec = args.icaConnPerAppliance #Desired Number of xenapp/xendesktop users per appliance
    Uwan = args.maxIcaConn #Max number of xenapp/xendesktop users
    BWspec = args.applianceBw #Supported bandwidth per appliance
    BWwan = args.wanBw #Wan link Bandwidth
    Connspec = args.tcpConnPerAppliance #Support TCP connections per appliance
    Connwan = args.maxTcpConn #Max number of TCP connections on Wan
	
    #Calculations
	
    if Uwan is not 0 or Uspec is not 0:
        Uoverload = Uwan/Uspec  #Appliances per xen users
    else:
        Uoverload = 0

    if BWwan is not 0 or BWspec is not 0:
        BWoverload = BWwan/BWspec #Appliance needed to support bandwidth
    else:
        BWoverload = 0
    if Connspec is not 0 or Connwan is not 0:
        Connoverload = Connwan / Connspec
    else:
        Connoverload = 0
	
    #import pdb;pdb.set_trace()
    N = math.ceil(max(Uoverload,BWoverload,Connoverload) + 1) # Number of appliances for N + 1
    Bmin = 2**(math.ceil(math.log(N, 2)))  #Minimum number of buckets
    if Bmin * 4 <= 16:
        B = Bmin * 4
    else:
        B = Bmin * 2
    
    #B is recommended buckets
    
    bits = math.log2(B) #mask is the number of bits to set but not what you put in for the mask
    print("\nNumber of appliances require for N + 1 in the cluster is: {}".format(N))
    print("The recommend number of bits to set in order to provide {} buckets on {} devices \
for proper wccp load balancing is: {}".format(B,N,bits))
    print("""\nPlease make note that the number of bits is the number of \'on\' bits set in the mask.
You don't actually put {} in for the mask.  Refer to {} to learn about the binary operations.
You need to take your remote networks and find a mask that should keep one site going to the same Cb in the cluster""".format(bits,maskCalculationHelp))
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="""Calculates the recommended number of cloudBridges needed in a environment
type citrixWccpMaskCalculator -h to see options.  All options are optional and can be filled out based on what you know regarding
the environment.  All options are either limits that are available via the datasheet of the cloudbridge you are looking at or
are parameters that are specific to your network.
""")
    parser.add_argument('-icaPerApp',"--icaConnPerAppliance",help="The supported number of HDX/ICA connections supported by appliance",type=int,default=0)
    parser.add_argument('-maxIca',"--maxIcaConn",help="The total number of citrix users that could be online at a given time",type=int,default=0)
    parser.add_argument('-appBw',"--applianceBw",help="Supported bandwidth of a single appliance in mbits/sec",type=int,default=0)
    parser.add_argument("-wanBw",help="The WAN bandwidth of the circuit in mbits/sec",type=int,default=0)
    parser.add_argument('-tcpPerApp',"--tcpConnPerAppliance",help="The max number of TCP connections supported by the hardware",type=int,default=0)
    parser.add_argument("-maxTcpConn",help="The estimated number of TCP connections that will be crossing the Wan",type=int,default=0)
    args = parser.parse_args()
	
    if (args.icaConnPerAppliance and not args.maxIcaConn) or (args.maxIcaConn and not args.icaConnPerAppliance):
        parser.error("icaConnPerAppliance and maxIcaConn are required when one of them is used")

    if (args.applianceBw and not args.wanBw) or (args.wanBw and not args.applianceBw):
        parser.error("applianceBw and wanBw are required when one of them is used")
    if (args.tcpConnPerAppliance and not args.maxTcpConn) or (args.maxTcpConn and not args.tcpConnPerAppliance):
        parser.error("tcpConnPerAppliance and maxTcpConn are required when one of them is used")
    if (len(sys.argv) == 1):
	    parser.error("Please enter at least one argument")
	
    calculateCitrixWccpMask(args)

    


    
   
