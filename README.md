# CloudBridge Cluster Builder
Cli programe to assist with determining the number of cloudbridges and the mask to apply for a Wccp cluster when using Citrix Cloudbridges(Sd-Wan) appliances

# Instructions

From terminal, run citrixWccpMaskCalculator -h to view the available flags.  All flags are optional so can be left out if you do not have the information at hand.  However, all options are based on hardware limits for a citrix cloudbridge so if left out could cause you undersize your deployment.

The hardware limits we are looking at are:
maximum TCP connection
maximum ICA connections
maximum bandwdith

So for example, if you were looking at a CB2000-010 its max citrix connections are 100 and max TCP connections is 20K.  But, if you did not know your TCP connections across the wan yet you can run just based on citrix connections as follows:

    'citrixWccpMaskCalculator.py -icaPerApp 100 -maxIca 250'

Number of appliances require for N + 1 in the cluster is: 4
The recommend number of bits to set in order to provide 16 buckets on 4 devices for proper wccp load balancing is: 4.0
