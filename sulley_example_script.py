from sulley import *
import sys
import time
import os

#------------------------------------------------------------------------------
TARGET_IP="10.1.1.41"
TARGET_PORT=12345
SESSON_FILE_NAME="example_script.sess"

# Time to wait between mutations
SLEEP_TIME=0.5
# Time to wait before claiming a host is unresponsive
TIMEOUT=3
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
try:
	os.remove("SESSION_FILE_NAME")
except:
	pass
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Initialize a request
s_initialize("request1")
#s_byte("\x41")
#s_string("asdf")
s_static("A")
#s_random("\x65",min_length=1, max_length=1, num_mutations=2)

# Initialize another request
s_initialize("request2")
#s_byte("\x41")
#s_string("asdf")
s_static("B")
#s_random("\x66",min_length=1, max_length=1, num_mutations=2)

# Initialize the Sulley mutation descriptor
s_initialize("request3")
#s_byte("\x41")
#s_random(1,min_length=1, max_length=1, num_mutations=3)
s_static("C")
#s_random("\x67",min_length=1, max_length=1, num_mutations=2)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
print "Total mutations: " + str(s_num_mutations()) + "\n"
print "Minimum time for execution: " + str(round(((s_num_mutations() * (SLEEP_TIME))/3600),2)) + " hours."

print "Press CTRL/C to cancel"
sys.stdout.flush()
time.sleep(3)


# For debugging purposes, uncomment these lines to see Sulley's mutations
# in hex dump format (no data is sent over the network)
#print "Hex dump mutation output:"
#while s_mutate():
#	print s_hex_dump(s_render())

sess = sessions.session(session_filename=SESSON_FILE_NAME, sleep_time=SLEEP_TIME, timeout=TIMEOUT, proto="udp")

# Create a sessioin (graph) connecting the requests
sess.connect(s_get("request1"))
sess.connect(s_get("request1"), s_get("request2"))
sess.connect(s_get("request2"), s_get("request3"))

target = sessions.target(TARGET_IP, TARGET_PORT)

# Add the target to the session (can be repeated for multiple targets)
sess.add_target(target)

# Kick off the fuzzer, monitoring with WebUI on localhost:26000
sess.fuzz()
