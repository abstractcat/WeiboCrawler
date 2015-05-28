#!/usr/bin/env python
#coding=utf8

import os
import sys
import urllib
import urllib2
import cookielib
import base64
import re
import hashlib
import json
import rsa
import binascii
import time
import random
import cStringIO
import numpy
import matplotlib.pyplot as plt
from PIL import Image

def get_prelogin_status(username):
    """
    Perform prelogin action, get prelogin status, including servertime, nonce, rsakv, etc.
    """
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=' + get_user(username) + \
     '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_='+str(time.time()).replace('.', '')
    print('prelogin.php:'+prelogin_url)
    data = urllib2.urlopen(prelogin_url).read()
    print('data received:'+data)
    p = re.compile('\((.*)\)')

    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        rsakv = data['rsakv']
        showpin = data['showpin']
        pcid = data['pcid']
        return servertime, nonce, rsakv, showpin, pcid
    except:
        print 'Getting prelogin status met error!'
        return None


def login(username, pwd, cookie_file):
    """"
        Login with use name, password and cookies.
        (1) If cookie file exists then try to load cookies;
        (2) If no cookies found then do login
    """
    #If cookie file exists then try to load cookies
    if os.path.exists(cookie_file):
        try:
            cookie_jar  = cookielib.LWPCookieJar(cookie_file)
            cookie_jar.load(ignore_discard=True, ignore_expires=True)
            loaded = 1
        except cookielib.LoadError:
            loaded = 0
            print 'Loading cookies error'

        #install loaded cookies for urllib2
        if loaded:
            cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
            opener         = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            print 'Loading cookies success'
            return 1
        else:
            return do_login(username, pwd, cookie_file)

    else:   #If no cookies found
        return do_login(username, pwd, cookie_file)


def do_login(username,pwd,cookie_file):
    """"
    Perform login action with use name, password and saving cookies.
    @param username: login user name
    @param pwd: login password
    @param cookie_file: file name where to save cookies when login succeeded
    """
    #POST data per LOGIN WEIBO, these fields can be captured using httpfox extension in FIrefox
    login_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'pagerefer':'',
        'vsnf': '1',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'rsa2',
        'rsakv': '',
        'sp': '',
        'encoding': 'UTF-8',
        'prelt': '45',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META',
        'pcid':'',
        'door':''
        }
    cookie_jar2     = cookielib.LWPCookieJar()
    cookie_support2 = urllib2.HTTPCookieProcessor(cookie_jar2)
    opener2         = urllib2.build_opener(cookie_support2, urllib2.HTTPHandler)
    urllib2.install_opener(opener2)
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'

    try:
        servertime, nonce, rsakv, showpin, pcid = get_prelogin_status(username)
    except:
        return

    #Fill POST data
    login_data['servertime'] = servertime
    login_data['nonce'] = nonce
    login_data['su'] = get_user(username)
    login_data['sp'] = get_pwd_rsa(pwd, servertime, nonce)
    login_data['rsakv'] = rsakv
    #use a manually identified pin code
    if showpin==1:
        login_data['pcid'] = pcid
        s=random_number()
        pin_url='http://login.sina.com.cn/cgi/pin.php?s=%s&p=%s'%(s,pcid)
        print('pin_url:'+pin_url)
        #download the pin image
        file = cStringIO.StringIO(urllib2.urlopen(pin_url).read())
        img = Image.open(file)

        #show image
        img.show()

        #input pin
        login_data['door']  = raw_input("input pin:")

    login_data = urllib.urlencode(login_data)
    http_headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req_login  = urllib2.Request(
        url = login_url,
        data = login_data,
        headers = http_headers
    )
    print('login.php:'+login_url)
    print('post data:'+'\n'.join(login_data.split('&')))
    result = urllib2.urlopen(req_login)
    text = result.read().decode('gbk')
    print('data received:'+text)
    p = re.compile('\'login\',function\(\)\{location\.replace\(\'(.*?)\'\)')
    try:
        #Search login redirection URL
        login_url = p.search(text).group(1)

        print('login_url:'+login_url)
        data = urllib2.urlopen(login_url).read()
        print('received data:'+data)
        #Verify login feedback, check whether result is TRUE
        patt_feedback = 'feedBackUrlCallBack\((.*)\)'
        p = re.compile(patt_feedback, re.MULTILINE)

        feedback = p.search(data).group(1)
        feedback_json = json.loads(feedback)
        if feedback_json['result']:
            cookie_jar2.save(cookie_file,ignore_discard=True, ignore_expires=True)
            return 1
        else:
            return 0
    except:
        return 0


def get_pwd_wsse(pwd, servertime, nonce):
    """
        Get wsse encrypted password
    """
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd3_ = pwd2 + servertime + nonce
    pwd3 = hashlib.sha1(pwd3_).hexdigest()
    return pwd3

def get_pwd_rsa(pwd, servertime, nonce):
    """
        Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1, documents can be accessed at
        http://stuvel.eu/files/python-rsa-doc/index.html
    """
    #n, n parameter of RSA public key, which is published by WEIBO.COM
    #hardcoded here but you can also find it from values return from prelogin status above
    weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'

    #e, exponent parameter of RSA public key, WEIBO uses 0x10001, which is 65537 in Decimal
    weibo_rsa_e = 65537
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)

    #construct WEIBO RSA Publickey using n and e above, note that n is a hex string
    key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)

    #get encrypted password
    encropy_pwd = rsa.encrypt(message, key)
    #trun back encrypted password binaries to hex string
    return binascii.b2a_hex(encropy_pwd)


def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username

def random_number(randomlength=8):
    rn = ''
    for i in range(0,randomlength):
        rn+=str(random.randint(0, 9))
    return rn


if __name__ == '__main__':

    username = 'mcnbtoses0@chacuo.net'
    pwd = 'gtxmxmz65194'
    cookie_file = 'cookies/test_cookie.dat'
    if login(username, pwd, cookie_file):
        print 'Login WEIBO succeeded'
        #if you see the above message, then do whatever you want with urllib2, following is a example for fetch Kaifu's Weibo Home Page
        #Trying to fetch Kaifu Lee's Weibo home page
        kaifu_page = urllib2.urlopen('http://weibo.com/u/2891529877?from=feed&loc=nickname').read()
        #kaifu_page=codecs.decode(kaifu_page,encoding='gbk')
        print kaifu_page

    else:
        print 'Login WEIBO failed'
