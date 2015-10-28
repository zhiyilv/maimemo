# coding=utf-8
import urllib2
import socket

# load proxies today and previous data
with open('all-proxies-hide-my-ip.txt') as proxy_today:
    proxies = proxy_today.readlines()
with open('bad.txt') as bad:
    bad_proxies = bad.readlines()
with open('success.txt') as success:
    success_proxies = success.readlines()

# define the visiting page
# user_id = int(raw_input('input your maimemo id:'))
user_id = 34154
url = 'http://www.maimemo.com/share/page/?uid=%d&pid=194' % user_id

# refine proxies for today
proxies = [i for i in proxies if (i not in success_proxies) and (i not in bad_proxies)]
# consider all those not succeeded before
# proxies = [i for i in proxies if (i not in success_proxies)]
total = len(proxies)
print 'There are totally %d new proxies today' % total

# get current visit num
response = urllib2.urlopen(url)
temp = response.read()
visit = int(temp[temp.find('感谢')+6:temp.find('位')])
print 'Currently, there are %d visits already' % visit
original_visit = visit

# main
num = 0
potential = []  # store the potential proxies
bad_proxies = []
success_proxies = []

for i in proxies:
    # delete the '\n'
    i = i[:len(i)-1]

    proxy_handler = urllib2.ProxyHandler({'http': i})
    opener = urllib2.build_opener(proxy_handler)
    try:
        total -= 1
        num += 1
        response = opener.open(url, timeout=15)
        temp = response.read()
    except Exception, e:
        print type(e)
        print '#%d fails, %d left' % (num, total)
        if i not in bad_proxies:
            bad_proxies.append(i)
    else:
        # guarantee the succeeded proxies generate a new visit
        try:
            new_visit = int(temp[temp.find('感谢')+6:temp.find('位')])
        except:
            print 'WTF! CANNOT GET THE VISIT NUM!'
        else:
            if new_visit == visit:
                if i not in potential:
                    potential.append(i)
                print '# %d is stored for later test, %d left' % (num, total)
            elif new_visit > visit:
                print '#%d proxy ' % num + i + ' is valid, and generated a new visit'
                visit = new_visit
                print "currently there are %d visits already" % visit
                # this proxy is used up and stored into success.txt
                if i not in success_proxies:
                    success_proxies.append(i)
            else:
                print 'WTF! The visit number is WRONG!'
# the writing
with open('success.txt', 'a') as s:
    for i in success_proxies:
        s.write(i+'\n')
with open('bad.txt', 'a') as b:
    for i in bad_proxies:
        b.write(i+'\n')

# test for potentials
success_proxies = []
bad_proxies = []
print '**********************************'
print 'Finished the easy ones, now for these potentials'
print 'There are %d potential ones for further test' % len(potential)

# loop at most 5 times
count = 0
while count < 5 and len(potential) > 0:
    count += 1
    for i in potential:
        proxy_handler = urllib2.ProxyHandler({'http': i})
        opener = urllib2.build_opener(proxy_handler)
        try:
            response = opener.open(url, timeout=15)
            temp = response.read()
        except:
            print 'proxy ' + i + ' is not stable'
            potential.remove(i)
            if i not in bad_proxies:
                bad_proxies.append(i)
        else:

            try:
                new_visit = int(temp[temp.find('感谢')+6:temp.find('位')])
            except:
                print 'WTF! CANNOT GET THE VISIT NUM!'
            else:
                if new_visit > visit:
                    print 'proxy ' + i + ' passed the test'
                    potential.remove(i)
                    if i not in success_proxies:
                        success_proxies.append(i)
            print 'There are %d potentials left' % len(potential)
    print 'Finished the %d loop' % count
# the writing
with open('success.txt', 'a') as s:
    for i in success_proxies:
        s.write(i+'\n')
with open('bad.txt', 'a') as b:
    for i in bad_proxies:
        b.write(i+'\n')

print '**********************'
print 'Finished potential test'
if len(potential) > 0:
    print 'storing the blimps...'
    with open('success.txt', 'a') as s:
        for i in potential:
            s.write(i+'\n')

response = urllib2.urlopen(url)
temp = response.read()
final_visit = int(temp[temp.find('感谢')+6:temp.find('位')])
print 'Eventually, generated %d visits' % (final_visit - original_visit)
