#!/bin/bash

while true ; do
        if ifconfig wlan0 | grep -q "inet" ; then
                echo "Reconnect"
                break
        else
                echo "Network connection down! Attempting reconnection."
                sudo  wpa_supplicant -Dnl80211 -iwlan0 -c/etc/wpa_supplicant.con                                                                                        f
        fi
done
