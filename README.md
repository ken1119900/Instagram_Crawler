# Instagram Crawler
This is a very simple crawler and downloader of Instagram.  It can download all the posts (including photo and video) of the specified public user account.  It also supports to dowanload multiple photos and videos in single post.  The naming rule of the downloaded photos and videos are *i_j.png* or *i_j.mp4* where *i* represent *i-th* post and *j* represent *j-th* photo or video in this post (both *i* and *j* start from 0).  

User can specify below 3 variables in the program to control:

+ **user_name:**     the user account you want this program to download posts from

+ **dname:**         download path of your local PC

+ **max_post_iter:** decide how many posts you want to download.  total_download_post = 12*(max_post_iter+1).  Ex: max_post_iter=99.  It will download latest 1200 posts of the user account

(Instagram has some limitation so we can only download 12 post in an iteration)

# Usage 
1. Download or clone the test_ig.py file

2. Setting below variables: "user_name" "dname" "max_post_iter" in the test_ig.py

*Example:*
+ *user_name = 'emmawatson'*
+ *dname = 'C:\\Users\\Download\\' + user_name + '\\'*
+ *max_post_iter=99*

With above setting, this program will download latest 1200 posts of user account "emmawatson" into "C:\\Users\\Download\\emmawatson\\" of your PC.

3. Execute the test_ig.py
```
python test_ig.py
```

