import urllib
import requests
import json
import os
import re
import pyquery

all_posts = []
post_cnt=0

def get_web_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:    
            print('Wrong：', response.status_code)        
    except Exception as e:
        print(e)
        return None

#only able to query 12 post of one iteration
def get_twelve_post(edges):   
    global all_posts
    global post_cnt
    
    #12 post of this for loop
    for edge in edges:
        shortcode = edge['node']['shortcode']
        url_shortcode = 'https://www.instagram.com/p/'+shortcode+'/?__a=1'
        with urllib.request.urlopen(url_shortcode) as temp_u:
            js_data = json.loads(temp_u.read().decode())
        photo_in_post_cnt=0
        post = []
        if 'edge_sidecar_to_children' in js_data['graphql']['shortcode_media']:
            edges_shortcode = js_data['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
            #num of pic in single post of this for loop            
            for edge_s in edges_shortcode:
                if edge_s['node']['is_video'] and edge_s['node']['video_url'] != 'https://static.cdninstagram.com/rsrc.php/null.jpg':
                    display_url = edge_s['node']['video_url']
                elif edge_s['node']['display_url']:
                    display_url = edge_s['node']['display_url']
                post.append(display_url)
                photo_in_post_cnt=photo_in_post_cnt+1  
        else:            
            if js_data['graphql']['shortcode_media']['is_video'] and js_data['graphql']['shortcode_media']['video_url'] != 'https://static.cdninstagram.com/rsrc.php/null.jpg':
                display_url = js_data['graphql']['shortcode_media']['video_url']
            elif js_data['graphql']['shortcode_media']['display_url']:
                display_url = js_data['graphql']['shortcode_media']['display_url']
            post.append(display_url)
        all_posts.append(post)
        post_cnt=post_cnt+1

#download all the images to local
def save_from_url_to_local(dname):
    for i in range(0,len(all_posts)):
        for j in range(0,len(all_posts[i])):
            if re.search('\.mp4\?', all_posts[i][j]):
                file_name = dname+str(len(all_posts)-1-i)+'_'+str(j)+'.mp4'
            else:
                file_name = dname+str(len(all_posts)-1-i)+'_'+str(j)+'.png'
            if os.path.isfile(file_name):
                print(file_name," already exist.  No need to download for remaining post.")
                return False
            else:                
                #print("saving ",all_posts[i][j]," to ", file_name)
                #urllib.request.urlretrieve(all_posts[i][j], file_name)
                try:
                    urllib.request.urlretrieve(all_posts[i][j], file_name)
                except urllib.error.HTTPError as err:
                    if err.code == 410:
                        print(all_posts[i][j]," is gone. Skip downloading... Error code: ",err.code)
                    else:
                        print(all_posts[i][j]," downloading fail... Error code: ",err.code)
                else:
                    #download success
                    print("saving ",all_posts[i][j]," to ", file_name)
    print("First time to query this account.  Download all finished.")
    return True
    
#user to download
user_name = 'emmawatson'
#download path
dname = 'C:\\Users\\Download\\' + user_name + '\\'
#total query post = 12*(max_post_iter+1)
max_post_iter=1000

if not os.path.exists(dname):
    os.makedirs(dname)
else:
    print(dname," already exist")


url = 'https://www.instagram.com/' + user_name
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}
html = get_web_html(url)
user_id = re.findall('profilePage_([0-9]+)', html, re.S)[0]
doc = pyquery.PyQuery(html)
items = doc('script[type="text/javascript"]').items()

print("user_id:",user_id)
print("url:",url)

#query latest 12 post
for item in items:
    if item.text().strip().startswith('window._sharedData'):
        js_data = json.loads(item.text()[21:-1], encoding='utf-8')
        edges = js_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        cursor = js_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        flag = js_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        get_twelve_post(edges)
            
#query remaining posts other than latest 12  #total query post = 12*(max_post_iter+1)
for index in range(0,max_post_iter):  
    if (flag):
        url_next = 'https://instagram.com/graphql/query/?query_id=17888483320059182&id='+user_id+'&first=12&after='+cursor
        print('next url:',url_next)
        with urllib.request.urlopen(url_next) as temp_u:
            js_data = json.loads(temp_u.read().decode())
        edges = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        get_twelve_post(edges)
    else:
        break
      
save_from_url_to_local(dname)