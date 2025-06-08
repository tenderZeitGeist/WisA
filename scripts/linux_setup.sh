# !/bin/bash

# Make RAPL temporarily readable for non-sudoers
sudo chmod -R a+r /sys/class/powercap/intel-rapl
