# https://africa.prdf.mpf.mp.br/rrd_updates?start=1&host=true&cf=ave&interval=10s%27

# import urllib2
import urllib.request as request
import xml.dom.minidom
import sys
import time
import itertools
import re
import shutil
import ssl
import getopt
import os
# import fcntl
import logging
import logging.handlers
import credentials
from api import xenapi as XenAPI

maxage = 60
# arq_cred = /location/ofthe/archive/credentials.txt

# ssl._create_default_https_context = ssl._create_unverified_context

# sys.path.append('/usr/local/lib/python')

ssl._create_default_https_context = ssl._create_unverified_context

sx = object

xenmaster, username, password = "africa", "root", "t1hu4n4123"


def get_session(xenmaster, username, password):
    url = "https://{}".format(xenmaster)
    session = XenAPI.Session(url, ignore_ssl=True)
    try:
        session.login_with_password(username, password, "1.0", "citrix.py")
    except (XenAPI.Failure, e):
        if (e.details[0] == 'HOST_IS_SLAVE'):
            session = XenAPI.Session("https://{}".format(e.details[1]))
            session.login_with_password(username, password)
        else:
            raise
    sx = session.xenapi
    return sx


def close_session():
    return sx.logout()


def get_hosts_vms(session, xenhosts, xenvms, xensrs):

    # session = get_session(xenmaster,username, password)
    retval = False

    all_hosts = session.host.get_all()

    for host in all_hosts:
        xenhosts[session.host.get_uuid(host)] = session.host.get_hostname(host)
        all_pbds = session.host_get_PBDs(host)
        for pbd in all_pbds:
            sr = session.PBD.get_SR(pbd)
            srname = session.SR.get_name_label(sr).replace(" ", "_")
            if (re.match(r"(DVD_drives|Removable_storage|XenServer_Tools)", srname)):
                continue
            xensrs[session.SR.get_uuid(sr)] = srname

        for vm in session.host.get_resident_VMs(host):
            xenvms[session.VM.get_uuid(vm)] = session.VM.get_name_label(vm)

        retval = True

    print("===All Hosts===\n\n{}".format(all_hosts))

    return retval


"""
Gather
"""


def getStatsXML(hostname, username, password, delay):
    start = int(time.time()) - 2 * int(delay)
    url = "https://{}/rrd_updates?start={}&host=true&cf=ave&interval={}".format(
        hostname, start, delay)
    default_realm = request.HTTPPasswordMgrWithDefaultRealm()
    default_realm.add_password(None, url, username, password)
    auth_handler = request.HTTPBasicAuthHandler(default_realm)
    opener = request.build_opener(auth_handler)
    request.install_opener(opener)
    page_handle = request.urlopen(url)
    return page_handle.read()


def getStats(xenhosts, username, password, delay):
    legends_array = []
    values_array = []

    for hostname in xenhosts.values():
        page = getStatsXML(hostname, username, password, delay)
        # print ("\n== Page {} == \n".format(hostname), (page))
        dom = xml.dom.minidom.parseString(page)    
        legends = dom.getElementsByTagName("legend")[0]
        # print (legends) 
        for legend in legends.getElementsByTagName("entry"):
            legends_array.append(legend.childNodes[0].data)
        # print (legends_array)

        data = dom.getElementsByTagName("data")[0]

        print (data)

        for row in data.getElementsByTagName("row"):
            for value in row.getElementsByTagName("v"):
                print(value.childNodes[0].data)

        # values = dom.getElementsByTagName("row")[0]
        # print (values) 
        # for value in values.getElementsByTagName("v"):
        #     values_array.append(value.childNodes[0].data)
        # print (values_array)


if __name__ == "__main__":

    session = get_session(xenmaster, username, password)

    xenhosts = dict()
    xenvms = dict()
    xensrs = dict()

    delay = 60

    get_hosts_vms(session, xenhosts, xenvms, xensrs)
    session.logout()
    print("===Xen hosts====\n\n{}".format(xenhosts))
    # print("===Xen VMs===\n\n{}".format(xenvms))
    # print("===Xen SRs===\n\n{}".format(xensrs))
    # xml = getStatsXML(xenmaster, username, password, delay)
    values = getStats(xenhosts, username, password, maxage)
    print (xml)
    # print (session)
