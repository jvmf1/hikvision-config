#!/usr/bin/env python3
import json
import os
import sys

try:
    import requests
except ImportError:
    print('pip install requests')
    sys.exit()

import argparse

try:
    import xmltodict
except ImportError:
    print('pip install xmltodict')
    sys.exit()

from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth

parser=argparse.ArgumentParser()
parser.add_argument("-u", "--user", "--username", required=True)
parser.add_argument("-p", "--password", required=True)
parser.add_argument("-i", "--ip", required=True)
parser.add_argument("--id")
parser.add_argument("--auth", default='digest', help='digest | basic', metavar='')
parser.add_argument("--set-time-mode", help='NTP | manual', metavar='')
parser.add_argument("--set-localtime", help='2022-06-29T02:19:39+08:00', metavar='')
parser.add_argument("--set-timezone", help='CST-8:00:00', metavar='')
parser.add_argument("--set-ntp-server", metavar='')
parser.add_argument("--set-ntp-port", metavar='')
parser.add_argument("--set-ntp-interval", metavar='')
parser.add_argument("--set-audio", help='true | false', metavar='')
parser.add_argument("--set-audio-codec", metavar='')
parser.add_argument("--set-fps", metavar='')
parser.add_argument("--set-bitrate", metavar='')
parser.add_argument("--set-codec", metavar='')
parser.add_argument("--set-name", metavar='')
parser.add_argument("--set-device-number", metavar='')
parser.add_argument("--set-smoothing", metavar='')
parser.add_argument("--set-quality", metavar='')
parser.add_argument("--set-resolution", help='1920x1080', metavar='')
parser.add_argument("--set-flashing", help='true | false', metavar='')
parser.add_argument("--set-transparent", help='true | false', metavar='')
parser.add_argument("--set-fontsize", metavar='')
parser.add_argument("--set-font-align", metavar='')
parser.add_argument("--set-overlay-name-enable", help='true | false', metavar='')
parser.add_argument("--set-overlay-name-position", help='x,y', metavar='')
parser.add_argument("--set-overlay-date-enable", help='true | false', metavar='')
parser.add_argument("--set-overlay-date-position", help='x,y', metavar='')
parser.add_argument("--set-overlay-date-week", help='true | false', metavar='')
parser.add_argument("--set-overlay-date-format", help='DD-MM-YYYY', metavar='')
parser.add_argument("--set-overlay-date-style", help='12hour | 24hour', metavar='')
parser.add_argument("--set-overlay-1-text", metavar='')
parser.add_argument("--set-overlay-1-position", help='x,y', metavar='')
parser.add_argument("--set-overlay-1-enable", help='true | false', metavar='')
parser.add_argument("--reboot", action='store_true')

parser.add_argument("--list-time", action='store_true')
parser.add_argument("--list-online-users", action='store_true')
parser.add_argument("--list-users", action='store_true')
parser.add_argument("--list-time-capabilities", action='store_true')
parser.add_argument("--list-channels", action='store_true')
parser.add_argument("--list-capabilities", action='store_true')
parser.add_argument("--list-deviceinfo", action='store_true')
parser.add_argument("--list-overlay", action='store_true')
parser.add_argument("--list-overlay-capabilities", action='store_true')

args = parser.parse_args()


try:
    h = os.get_terminal_size().lines
    w = os.get_terminal_size().columns
except:
    h=0
    w=0

def get_xml_overlay():
    data = session.get(f"http://{args.ip}/ISAPI/System/Video/inputs/channels/1/overlays").content
    data = xmltodict.parse(data)
    data = todict(data)
    return data

def get_xml_channels():
    data = session.get(f"http://{args.ip}/ISAPI/Streaming/channels").content
    data = xmltodict.parse(data)
    data = todict(data)
    return data

def get_xml_deviceinfo():
    data = session.get(f"http://{args.ip}/ISAPI/System/deviceinfo").content
    data = xmltodict.parse(data)
    data = todict(data)
    return data

def get_xml_time():
    data = session.get(f"http://{args.ip}/ISAPI/System/time").content
    data = xmltodict.parse(data)
    data = todict(data)
    return data

def get_xml_ntp():
    data = session.get(f"http://{args.ip}/ISAPI/System/time/ntpServers/1").content
    data = xmltodict.parse(data)
    data = todict(data)
    return data

def todict(input_ordered_dict):
    return json.loads(json.dumps(input_ordered_dict))


def pprint(data, i=0, ignoreat=True):
    if type(data) == str:
        print('\t'*i, end='')
        print(data)
    elif type(data) == dict:
        for k, v in data.items():
            if '@xmlns' in k or '@version' in k:
                continue
            if ignoreat and '@' in k:
                continue
            print('\t'*i,end='')
            if type(v) == dict:
                print(k)
            elif type(v) == list:
                print(k)
            else:
                print(k,v)
            if not type(v) == str:
                pprint(v, i+1, ignoreat)
    elif type(data) == list:
        for v in data:
            pprint(v,i, ignoreat)


session = requests.Session()

if args.auth == 'digest':
    session.auth = HTTPDigestAuth(args.user, args.password)

if args.auth == 'basic':
    session.auth = HTTPBasicAuth(args.user, args.password)

if args.reboot:
    session.put(f'http://{args.ip}/ISAPI/System/reboot')

if args.list_time or args.list_channels or args.list_capabilities or args.list_deviceinfo or args.list_overlay or args.list_overlay_capabilities or args.list_time_capabilities or args.list_online_users or args.list_users:
    print('-'*w)

if args.list_online_users:
    data = session.get(f'http://{args.ip}/ISAPI/Security/onlineUser').content
    data = xmltodict.parse(data)
    data = todict(data)
    if type(data['OnlineUserList']['OnlineUser']) == list:
        for user in data['OnlineUserList']['OnlineUser']:
            pprint(user)
            print('-'*w)
    else:
        pprint(data['OnlineUserList']['UserList'])
        print('-'*w)
    sys.exit()

if args.list_users:
    data = session.get(f'http://{args.ip}/ISAPI/Security/users').content
    data = xmltodict.parse(data)
    data = todict(data)
    if type(data['UserList']['User']) == list:
        for user in data['UserList']['User']:
            pprint(user)
            print('-'*w)
    else:
        pprint(data['UserList']['User'])
        print('-'*w)
    sys.exit()

if args.list_overlay_capabilities:
    data = session.get(f"http://{args.ip}/ISAPI/System/Video/inputs/channels/1/overlays/capabilities").content
    data = xmltodict.parse(data)
    data = todict(data)
    pprint(data['VideoOverlay'], ignoreat=False)
    print('-'*w)
    sys.exit()

if args.list_overlay:
    data = session.get(f"http://{args.ip}/ISAPI/System/Video/inputs/channels/1/overlays").content
    data = xmltodict.parse(data)
    data = todict(data)
    pprint(data['VideoOverlay'], ignoreat=False)
    print('-'*w)
    sys.exit()


if args.list_time:
    data = session.get(f"http://{args.ip}/ISAPI/System/time").content
    data = xmltodict.parse(data)
    data = todict(data)
    pprint(data['Time'], ignoreat=False)
    print('-'*w)
    data = session.get(f"http://{args.ip}/ISAPI/System/time/ntpServers/1").content
    data = xmltodict.parse(data)
    data = todict(data)
    pprint(data, ignoreat=False)
    print('-'*w)
    sys.exit()

if args.list_time_capabilities:
    data = session.get(f"http://{args.ip}/ISAPI/System/time/capabilities").content
    data = xmltodict.parse(data)
    data = todict(data)
    pprint(data['Time'], ignoreat=False)
    print('-'*w)
    sys.exit()

if args.list_channels:
    streaming_data = session.get(f"http://{args.ip}/ISAPI/Streaming/channels").content
    streaming_data = xmltodict.parse(streaming_data)
    streaming_data = todict(streaming_data)
    for i in streaming_data['StreamingChannelList']['StreamingChannel']:
        pprint(i)
        print('-'*w)
    sys.exit()

if args.list_deviceinfo:
    data = session.get(f"http://{args.ip}/ISAPI/System/deviceinfo").content
    data = xmltodict.parse(data)
    data = todict(data)
    pprint(data['DeviceInfo'], ignoreat=False)
    print('-'*w)
    sys.exit()

if args.list_capabilities:
    if args.id == None:
        print('missing --id')
        sys.exit()
    capabilities_data = session.get(f"http://{args.ip}/ISAPI/Streaming/channels/{args.id}/capabilities").content 
    capabilities_data = xmltodict.parse(capabilities_data)
    capabilities_data = todict(capabilities_data)
    pprint(capabilities_data['StreamingChannel'],ignoreat=False)
    print('-'*w)
    sys.exit()

###########################333

if args.set_audio != None or args.set_fps != None or args.set_resolution != None or args.set_quality != None or args.set_smoothing != None or args.set_codec != None or args.set_bitrate != None or args.set_audio_codec != None:
    if args.id == None:
        print('missing --id')
        sys.exit()
    channel_data = get_xml_channels()

if args.set_name != None or args.set_device_number != None:
    deviceinfo_data = get_xml_deviceinfo()

if args.set_time_mode != None or args.set_localtime != None or args.set_timezone != None:
    time_data = get_xml_time()

if args.set_ntp_server != None or args.set_ntp_port != None or args.set_ntp_interval != None:
    ntp_data = get_xml_ntp()

if args.set_flashing != None or args.set_transparent != None or args.set_fontsize != None or args.set_font_align or args.set_overlay_name_enable != None or args.set_overlay_name_position != None or args.set_overlay_date_enable != None or args.set_overlay_date_position != None or args.set_overlay_date_week != None or args.set_overlay_date_format != None or args.set_overlay_date_style != None or args.set_overlay_1_text != None or args.set_overlay_1_enable != None or args.set_overlay_1_position != None:
    overlay_data = get_xml_overlay()

if args.set_audio != None:
    for v in channel_data['StreamingChannelList']['StreamingChannel']:
        if v['id'] == args.id:
            v['Audio']['enabled'] = args.set_audio

if args.set_fps != None:
    for v in channel_data['StreamingChannelList']['StreamingChannel']:
        if v['id'] == args.id:
            v['Video']['maxFrameRate'] = args.set_fps

if args.set_resolution != None:
    width, height = args.set_resolution.split('x')
    for v in channel_data['StreamingChannelList']['StreamingChannel']:
        if v['id'] == args.id:
            v['Video']['videoResolutionWidth'] = width
            v['Video']['videoResolutionHeight'] = height

if args.set_quality != None:
    for v in channel_data['StreamingChannelList']['StreamingChannel']:
        if v['id'] == args.id:
            v['Video']['fixedQuality'] = args.set_quality

if args.set_smoothing != None:
    for v in channel_data['StreamingChannelList']['StreamingChannel']:
        if v['id'] == args.id:
            v['Video']['smoothing'] = args.set_smoothing

if args.set_codec != None:
    for v in channel_data['StreamingChannelList']['StreamingChannel']:
        if v['id'] == args.id:
            v['Video']['videoCodecType'] = args.set_codec

if args.set_bitrate != None:
    for v in channel_data['StreamingChannelList']['StreamingChannel']:
        if v['id'] == args.id:
            v['Video']['vbrUpperCap'] = args.set_bitrate

if args.set_audio_codec != None:
    for v in channel_data['StreamingChannelList']['StreamingChannel']:
        if v['id'] == args.id:
            v['Audio']['audioCompressionType'] = args.set_audio_codec

if args.set_name != None:
    deviceinfo_data['DeviceInfo']['deviceName'] = args.set_name

if args.set_device_number != None:
    deviceinfo_data['DeviceInfo']['telecontrolID'] = args.set_device_number

if args.set_time_mode != None:
    time_data['Time']['timeMode'] = args.set_time_mode

if args.set_localtime != None:
    time_data['Time']['localTime'] = args.set_localtime

if args.set_timezone != None:
    time_data['Time']['timeZone'] = args.set_timezone

if args.set_ntp_server != None:
    ntp_data['NTPServer']['hostName'] = args.set_ntp_server

if args.set_ntp_port != None:
    ntp_data['NTPServer']['portNo'] = args.set_ntp_port

if args.set_ntp_interval != None:
    ntp_data['NTPServer']['synchronizeInterval'] = args.set_ntp_interval

if args.set_flashing != None:
    overlay_data['VideoOverlay']['attribute']['flashing'] = args.set_flashing

if args.set_transparent != None:
    overlay_data['VideoOverlay']['attribute']['transparent'] = args.set_transparent

if args.set_fontsize != None:
    overlay_data['VideoOverlay']['fontSize'] = args.set_fontsize

if args.set_font_align != None:
    overlay_data['VideoOverlay']['alignment'] = args.set_font_align

if args.set_overlay_name_enable != None:
    overlay_data['VideoOverlay']['channelNameOverlay']['enabled'] = args.set_overlay_name_enable

if args.set_overlay_name_position != None:
    x,y = args.set_overlay_name_position.split(',')
    overlay_data['VideoOverlay']['channelNameOverlay']['positionX'] = x
    overlay_data['VideoOverlay']['channelNameOverlay']['positionY'] = y

if args.set_overlay_date_enable != None:
    overlay_data['VideoOverlay']['DateTimeOverlay']['enabled'] = args.set_overlay_date_enable

if args.set_overlay_date_position != None:
    x,y = args.set_overlay_date_position.split(',')
    overlay_data['VideoOverlay']['DateTimeOverlay']['positionX'] = x
    overlay_data['VideoOverlay']['DateTimeOverlay']['positionY'] = y

if args.set_overlay_date_week != None:
    overlay_data['VideoOverlay']['DateTimeOverlay']['displayWeek'] = args.set_overlay_date_week

if args.set_overlay_date_format != None:
    overlay_data['VideoOverlay']['DateTimeOverlay']['dateStyle'] = args.set_overlay_date_format

if args.set_overlay_date_style != None:
    overlay_data['VideoOverlay']['DateTimeOverlay']['timeStyle'] = args.set_overlay_date_style

if args.set_overlay_1_enable != None:
    try:
        for item in overlay_data['VideoOverlay']['TextOverlayList']['TextOverlay']:
            if item['id'] == '1':
                item['enabled'] = args.set_overlay_1_enable
    except:
        overlay_data['VideoOverlay']['TextOverlayList']['TextOverlay'] = []
        overlay_data['VideoOverlay']['TextOverlayList']['TextOverlay'].append({'id': '1', 'enabled': args.set_overlay_1_enable})

if args.set_overlay_1_position != None:
    x,y = args.set_overlay_1_position.split(',')
    for item in overlay_data['VideoOverlay']['TextOverlayList']['TextOverlay']:
        if item['id'] == '1':
            item['positionX'] = x
            item['positionY'] = y


if args.set_overlay_1_text != None:
    for item in overlay_data['VideoOverlay']['TextOverlayList']['TextOverlay']:
        if item['id'] == '1':
            item['displayText'] = args.set_overlay_1_text

if args.set_audio != None or args.set_fps != None or args.set_resolution != None or args.set_quality != None or args.set_smoothing != None or args.set_codec != None or args.set_bitrate != None or args.set_audio_codec != None:
    session.put(f"http://{args.ip}/ISAPI/Streaming/channels", data=xmltodict.unparse(channel_data))

if args.set_name != None or args.set_device_number != None:
    session.put(f"http://{args.ip}/ISAPI/System/deviceinfo", data=xmltodict.unparse(deviceinfo_data))

if args.set_time_mode != None or args.set_localtime != None or args.set_timezone != None:
    session.put(f"http://{args.ip}/ISAPI/System/time", data=xmltodict.unparse(time_data))

if args.set_ntp_server != None or args.set_ntp_port != None or args.set_ntp_interval != None:
    session.put(f"http://{args.ip}/ISAPI/System/time/ntpServers/1", data=xmltodict.unparse(ntp_data))

if args.set_flashing != None or args.set_transparent != None or args.set_fontsize != None or args.set_font_align != None or args.set_overlay_name_enable != None or args.set_overlay_name_position != None or args.set_overlay_date_enable != None or args.set_overlay_date_position != None or args.set_overlay_date_week != None or args.set_overlay_date_format != None or args.set_overlay_date_style != None or args.set_overlay_1_text != None or args.set_overlay_1_enable != None or args.set_overlay_1_position != None:
    session.put(f"http://{args.ip}/ISAPI/System/Video/inputs/channels/1/overlays", data=xmltodict.unparse(overlay_data))
