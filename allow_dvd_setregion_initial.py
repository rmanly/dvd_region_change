#!/usr/bin/python

import plistlib
import subprocess

def get_initial_settings():
    proc = subprocess.Popen(['/usr/bin/security',
            'authorizationdb',
            'read',
            'system.device.dvd.setregion.initial'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return stdout
    
def modify_plist():
    settings = plistlib.readPlistFromString(get_initial_settings())
    settings['class'] = 'allow'
    settings['comment'] = 'Allows any user to change the DVD region code.'
    settings['group'] = 'user'
    return settings

def write_sec_settings():
    tmp_file = '/tmp/system.device.dvd.setregion.initial.plist'
    cmd = '/usr/bin/security authorizationdb write system.device.dvd.setregion.initial <' + tmp_file
    plistlib.writePlist(modify_plist(), tmp_file)
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as error:
        if error.returncode == 255:
            print 'Failed to write plist to authdb!'
            print 'You must provide valid credentials!'
        exit(error.returncode)

write_sec_settings()
