#!/usr/bin/python

# does not do both yet.
## work on me tomorrow

import plistlib
import subprocess

rights = {
    'change':{
        ## just use right name and then add plist or commands around as needed
        ## system.device.dvd.setregion.change
        'cmd_prefix': '/usr/bin/security authorizationdb write system.device.dvd.setregion.change <',
        'comment': 'blah',
        'tmp': '/tmp/system.device.dvd.setregion.change.plist',
        },
    'initial':{
        'comment': 'blahblah',
        'tmp': '/tmp/bar',
        },
    }

def get_initial_settings():
    proc = subprocess.Popen(['/usr/bin/security',
            'authorizationdb',
            'read',
            'system.device.dvd.setregion.initial'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return stdout
    
def modify_plist(new_comment='Custom'):
    settings = plistlib.readPlistFromString(get_initial_settings())
    settings['class'] = 'allow'
    settings['comment'] = new_comment
    settings['group'] = 'user'
    return settings

def write_sec_settings():
    tmp_file = '/tmp/system.device.dvd.setregion.change.plist'
    cmd = '/usr/bin/security authorizationdb write system.device.dvd.setregion.change <' + tmp_file
    plistlib.writePlist(modify_plist(), tmp_file)
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as error:
        if error.returncode == 255:
            print 'Failed to write plist to authdb!'
            print 'You must provide valid credentials!'
        exit(error.returncode)

write_sec_settings()
