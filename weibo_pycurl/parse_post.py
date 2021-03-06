#coding=utf-8
import re
import chardet
import MySQLdb as mdb
import time
import setting


def parse(html):
    block_pattern=re.compile(r'<div mid="\d+".*?class="WB_feed_repeat S_bg1"',re.S)
    post_id_pattern=re.compile(r'mid="(\d+)"')
    post_time_pattern=re.compile(r'"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})" date=',re.S)
    poster_pattern=re.compile(r'title="(.*?)"')
    poster_image_pa=re.compile(r'<img .*?src="(http://tp.*?)"',re.S)
    poster_id_pattern=re.compile(r'value=wb_nologin_name:(\d+)"')
    post_pattern=re.compile(r'class="feed_content wbcon">(.*?)<div class="feed_from W_textb',re.S) 
    post_in_pattern=re.compile(r'class="feed_content wbcon">(.*?)<div class="comment"',re.S)
    repost_nump_pattern=re.compile('转发<em>(\d*)</em>')
    comment_num_pattern=re.compile('评论<em>(\d*)</em>')
    media_pattern=re.compile(r'class="WB_media_wrap clearfix(.*?)</ul>',re.S)    
    pic_pattern=re.compile(r'<img class=".*?bigcursor" src="(.*?)"',re.S)
    
    inner_allcontent_pa=re.compile(r'class="comment_info(.*?)nofollow"',re.S)
    inner_username_pa=re.compile(r'nick-name="(.*?)"',re.S)
    inner_post_id_pa=re.compile(r'mid=(\d+)')
    inner_posterid_pa=re.compile(r'http://weibo.com/(\d+)/\w+',re.S)
    inner_posttime_pa=re.compile(r'date="(\d+)"')
    inner_content_pa=re.compile(r'class="comme_txt">(.*?)</p>',re.S)
    inner_message_content_pa=re.compile(r'class="feed_action_info">(.*?)</ul>',re.S)
    inner_message_pa=re.compile(r'<em>(\d*)</em></span>',re.S)
    inner_pics_pa=re.compile(r'class="WB_media_a(.*?)</ul>',re.S)
   
    sub_p_1 = re.compile('<[^<>]*?>|\r', re.S)
    def parse_html_content(str):
        '''return a unicode string'''
        str = re.sub(sub_p_1, '', str)    
        str = str.replace('&nbsp;', ' ')
        str = str.replace('&amp;', '')
        str = str.replace('#039;', '')
        str = str.replace('#', '')
        str = str.replace('&#160;', ' ')
        str = str.replace('&lt;', '<')
        str = str.replace('&gt;', '>')
        str = str.replace('&amp;', '&')
        str = str.replace('&quot;', '"')
        str = str.replace(' ','')
        str = str.replace('\n','')
        ustr = str
        return ustr
    
    blocks=re.findall(block_pattern,html)
    print len(blocks)
    
    for b in blocks:
        
        
        #########################################3
        scratch_time = time.strftime('%Y-%m-%d %H:%M:%S')
        #####################################
        post_id=re.findall(post_id_pattern,b)[0]
        print post_id
        #####################################
        post_time=re.findall(post_time_pattern,b)[0]
        #print post_time
        ########################################
        poster=re.findall(poster_pattern,b)[0]
        #print poster
        ##########################################
        poster_image=re.findall(poster_image_pa,b)[0]
        print poster_image
        ###########################################
        poster_id=re.findall(poster_id_pattern,b)[0]
        #print poster_id
        ###########################################
        inner_flag=0
        
        if '<div class="comment_info"' not in b:           #有内贴
            post=re.findall(post_pattern,b)
            #print post
            post=map(lambda x:parse_html_content(x),post)[0]
            post=post.decode('utf-8','ignore').encode('utf-8','ignore')
            #post=post[3:]
        else:
            inner_flag=1
            print '_______'
            post=re.findall(post_in_pattern,b)
            #print post
            post=map(lambda x:parse_html_content(x),post)[0]
            post=post.decode('utf-8','ignore').encode('utf-8','ignore')
            #post=post[3:]
        print post
        #print  post.encode('gbk','ignore')
        
        ##############################################
        b_gbk=b.decode('utf-8').encode('gbk','ignore')
        try:
            repost_num=re.findall(repost_nump_pattern,b_gbk)
            repost_num=repost_num[len(repost_num)-1]
        except: 
            repost_num=0
        if repost_num=='':
            repost_num=0
        print repost_num
        ###################################################
        try:
            comment_num=re.findall(comment_num_pattern,b_gbk)
            comment_num=re.comment_num[len(comment_num)-1]
        except:
            comment_num=0
        if comment_num=='':
            comment_num=0
        print comment_num
        ######################################################
        aa='&url=(http://weibo.com/.*?)&mid='+post_id
        aa1='&url=(http://weibo.com/.*?)&mid='
        #print aa
        post_url_pattern=re.compile(aa,re.S)
        post_url_pattern1=re.compile(aa1,re.S)
        #print '_+_+',b
        try:
            post_url=re.findall(post_url_pattern,b)[0]
        except:
            post_url=re.findall(post_url_pattern1,b)[0]
        
        ################################################
        try:
            media_area=re.findall(media_pattern,b)[0]
            
            pics=re.findall(pic_pattern,media_area)
            pics_name=','.join(pics)
            print pics_name
        except:
            pass
        print post_url
        #print '+_+++++++++++++++++++++'
        ##############################################
        id='sina'+str(post_id)
        site=18
        board='sina'
        floor=0
        register_date='2005-01-01'
        title='新浪'.decode('gbk').encode('utf-8')
        #print post.decode('utf-8','ignore').encode('gbk','ignore')
        
        #################################################
        if inner_flag==1:
            print '_+_+_+_+_+_+'
            f=open(r'C:\Users\MINUS\Desktop\work\weibo_pycurl\1231.txt','wb')
            f.write(b)
            f.close()
            inner_allcontent=re.findall(inner_allcontent_pa,b)[0]
            #print inner_content
            inner_content=inner_allcontent.replace('nt','')
            f=open(r'C:\Users\MINUS\Desktop\work\weibo_pycurl\123.txt','wb')
            f.write(inner_allcontent)
            f.close()
            
            ############################
            inner_user=re.findall(inner_username_pa,inner_content)[0]
            print inner_user
            ############################
            inner_post_id=re.findall(inner_post_id_pa,inner_content)[0]
            print inner_post_id
            ############################
            inner_posterid=re.findall(inner_posterid_pa,inner_content)[0]
            print inner_posterid
            ###########################
            inner_posttime=re.findall(inner_posttime_pa,inner_content)[0]
            inner_posttime = inner_posttime[:-3]
            inner_posttime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(inner_posttime)))
            print inner_posttime
            ###########################
            inner_content=re.findall(inner_content_pa,inner_content)
            inner_content=map(lambda x:parse_html_content(x),inner_content)[0]
            print inner_content
            #############################
            inner_message_content=re.findall(inner_message_content_pa,inner_allcontent)[0]
            inner_message=re.findall(inner_message_pa,inner_message_content)
            print inner_message
            # a=raw_input()
            inner_repost=inner_message[0]
            inner_comment=inner_message[1]
            print inner_comment,inner_repost
            ############################# 
            if 'class="WB_media_a' in inner_allcontent:
                inner_pics_content=re.findall(inner_pics_pa,inner_allcontent)[0]
                inner_pics=re.findall(pic_pattern,inner_pics_content)
                inner_pics=','.join(inner_pics)
                print inner_pics
        print '+++++++++++++++++++++++'
        
def getpage(path):
    f=file(path,'rb')
    con=f.read()
    f.close()
    return con
    
if __name__=='__main__':
    html = getpage('%s/res.txt' % setting.CURRENT_PATH)
    parse(html)