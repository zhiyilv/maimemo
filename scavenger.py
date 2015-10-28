# coding=utf-8
import os
import urllib2

# load proxies
# with open('bad.txt') as bad:
#    bad_proxies = bad.readlines()
# with open('success.txt') as success:
#    success_proxies = success.readlines()
with open('temp.txt') as t:
    proxies = t.readlines()

# define the visiting page
# user_id = int(raw_input('input your maimemo id:'))
user_id = 34154
url = 'http://www.maimemo.com/share/page/?uid=%d&pid=185' % user_id

# show info
# print "There are %d succeeded proxies and %d failed ones." % (len(success_proxies), len(bad_proxies))
print "Scavenger is working..."

# refine proxies
# proxies = success_proxies + bad_proxies
proxies = list(set(proxies))
total = len(proxies)
print 'Merging them together, there are %d proxies in total' % total

# delete existing files
# os.remove('bad.txt')
# os.remove('success.txt')

# visit the url
bad = []
suc = []
for i in proxies:
    # delete the '\n'
    i = i[:len(i)-1]

    proxy_handler = urllib2.ProxyHandler({'http': i})
    opener = urllib2.build_opener(proxy_handler)
    try:
        total -= 1
        response = opener.open(url, timeout=10)
    except:
        print 'confirmed a broken proxy, %d left to check.' % total
        if i not in bad:
            bad.append(i)
    else:
        print 'Cong! 1 good proxy! %d good ones now, %d left to check' % (len(suc), total)
        if i not in suc:
            suc.append(i)

# writing
with open('bad.txt', 'a') as b:
    for i in bad:
        b.write(i+'\n')

with open('success.txt', 'a') as s:
    for i in suc:
        s.write(i+'\n')
