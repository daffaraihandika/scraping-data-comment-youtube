from googleapiclient.discovery import build
import requests
import json
from datetime import datetime
import urllib.request

URL = "https://www.googleapis.com/youtube/v3/commentThreads"
API_KEY = "AIzaSyDS33GM81iifJIxSbvKNvkXWQkj7LpS6r4"
VIDEO_ID = "4bhFLX4DS04"

URL_CHANNEL= "https://www.googleapis.com/youtube/v3/channels"

# channel youtube
url_channel = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={VIDEO_ID}&key={API_KEY}"

json_url = urllib.request.urlopen(url_channel)
data = json.loads(json_url.read())

video_desc = []

desc_video = data["items"][0]["snippet"]["description"]
judul_video = data["items"][0]["snippet"]["title"]
video_published_at = data["items"][0]["snippet"]["publishedAt"]

video_desc.append(
    {
        "Judul_Video": judul_video,
        "Deskripsi": desc_video,
        "Published_at": video_published_at
    }
)

# comment youtube
response = requests.get(f"{URL}?key={API_KEY}&videoId={VIDEO_ID}&part=snippet")
response_json = response.json()


youtube = build('youtube', 'v3', developerKey = API_KEY)

comments = []
while True:
    for item in response_json["items"]:
        author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        content = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
        likes = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
        totalReply = item["snippet"]["totalReplyCount"]
        video_id = item["snippet"]["videoId"]
        
        comments.append({
            "author": author,
            "comment": content,
            "published_at": published_at,
            "likes": likes,
            "reply_comment": totalReply,
            "id_video": video_id
        })
            
        print(f"collecting from: {author}")
        
        if totalReply > 0 :
            parent = item["snippet"]["topLevelComment"]["id"]
            data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent, textFormat='plainText').execute()
            
            for i in data2["items"]:
                name = i["snippet"]["authorDisplayName"]
                comment = i["snippet"]["textDisplay"]
                published_at = i["snippet"]['publishedAt']
                likes = i["snippet"]['likeCount']
                
                comments.append(
                    {
                        "author": name,
                        "comment": comment,
                        "published_at": published_at,
                        "likes": likes,
                        "id_video": video_id
                    }
                )           
        
        
    
    if "nextPageToken" in response_json:
        page_token = response_json["nextPageToken"]
        response = requests.get(f"{URL}?key={API_KEY}&videoId={VIDEO_ID}&part=snippet&pageToken={page_token}")
        response_json = response.json()
    else:
        break
    
with open('hasilScraping.json', 'w') as f :
    json.dump(comments, f)
    
with open('InformasiVideo.json', 'w') as f :
    json.dump(video_desc, f)

print(f"\n\n\ncomments:\n{comments}")
print(f"count comment: {len(comments)}")

print("finished.")
