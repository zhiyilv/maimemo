# coding=utf-8
import urllib2

# load proxies today and previous data
with open('all-proxies-hide-my-ip.txt') as proxy_today:
    proxies = proxy_today.readlines()
total = len(proxies)
print 'There are totally %d new proxies today' % total

# define the visiting page
user_id = int(raw_input('input your maimemo id:'))
url = 'http://www.maimemo.com/share/page/?uid=%d&pid=185' % user_id

# get current visit num
response = urllib2.urlopen(url)
temp = response.read()
visit = int(temp[temp.find('感谢')+6:temp.find('位')])
print 'Currently, there are %d visits already' % visit

# main
num = 0
for i in proxies:
    # delete the '\n'
    i = i[:len(i)-1]

    proxy_handler = urllib2.ProxyHandler({'http': i})
    opener = urllib2.build_opener(proxy_handler)
    try:
        total -= 1
        num += 1
        response = opener.open(url, timeout=5)
    except:
        print '#%d proxy ' % num + i + ' fails, try the next one, %d proxies left' % total
        with open('bad.txt', 'a') as bad:
            bad.write(i+'\n')
    else:
        # guarantee the succeeded proxies generate a new visit
        temp = response.read()
        new_visit = int(temp[temp.find('感谢')+6:temp.find('位')])
        count = 1
        while new_visit == visit and count < 11:
            try:
                response = opener.open(url)
            except:
                print '#%d is unstable' % num
                break
            else:
                count += 1
                temp = response.read()
                new_visit = int(temp[temp.find('感谢')+6:temp.find('位')])

        if new_visit > visit:
            print '#%d proxy ' % num + i + ' is valid, and generated a new visit'
            visit = new_visit
            print "currently there are %d visits already" % visit
        else:
            print '#%d proxy ' % num + i + ' is valid, but is not useful'
        # whether or not the proxy generated a new visit, it will be added to succeeded list
        with open('success.txt', 'a') as success:
            success.write(i+'\n')
