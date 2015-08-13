#!/usr/bin/python
# This quick script will monitor a riak cluster for a given set of metrics
# and output those metrics onscreen as well as to a CSV file for quick graphing

import time, urllib, json, os, datetime, sys

# -- CONFIG -- #
# This is just a simple testing script, so all config is internal to the script.

parent_node = 'dev-riak-01'     # Initial node to connect to
node_port   = 8098              # Port to use for node connections
sleep_time  = 60                # Time between API calls
out_csv     = r'riak_perf.csv'  # Output file

# Category of metric, followed by a list of metric names, metric names must
# match the name of the metric returned by the API
metrics = {
    'Node Stats (Last Minute)':('node_puts','node_gets'),
    'Node Stats (Total)':('node_puts_total','node_gets_total')
}

# Make a call to the initial node we specified and get the rest of the nodes in the cluster
result = json.load(urllib.urlopen('http://{}:{}}/stats'.format(parent_node,node_port)))
nodes = result['ring_members']

# Function that does all the work. Called in a loop.
def getStats(o):
    out_file = open(o,"a")
    current_time = str(datetime.datetime.now())
    os.system('cls')
    print "Riak stats as of: {}".format(current_time)
    print "-----------------------------------------------------------"
    for node in sorted(list(nodes)):
        print "\n============================================"
        print "Node: {}".format(node)
        print "============================================"
        result = json.load(urllib.urlopen('http://{}:{}/stats'.format(node,node_port)))
        for stat_cat in sorted(list(metrics)):
            print "--------------------------"
            print "{}:".format(stat_cat)
            print "--------------------------"
            for metric in metrics[stat_cat]:
                print "{}: {}".format(metric,result[metric])

                # Write out to CSV file
                out_file.write("{}\t{}\t{}\t{}\n".format(current_time,node,metric,result[metric]))
        print "============================================"
    out_file.close()

# Enter a loop and get the node stats, then pause for the specified amount of time
while True:
    try:
        getStats(out_csv)
        time.sleep(sleep_time)
    except:
        print "Error: {}".format(sys.exc_info()[0])
        exit()
