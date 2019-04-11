# arxiv-crawler

arxiv crawling slack bot runnnig on AWS Lambda

# Usage
## 1. Create slack bot
### 1.1 Create slack app & bot user  
Open https://api.slack.com/apps?new_app=1 to create slack app  
Then, go to `Bot users` tab and create bot user of the app

### 1.2 Add permission to your slack bot
Open `OAuth & Permissions` and select permission scope like below image.  
Your bot needs `chat:write:bot` permission.

![](https://i.imgur.com/52xx3PJ.png)

### 1.3 Install slack bot to your workspace
install bot to your workspace.  
after installing, do not forget to memo the access tokens in below image.  
![](https://i.imgur.com/xLtCz4A.png)

## 2. Setup Google Translation API
Go to https://cloud.google.com/ and enable `Google Translation API`  
Then, you can get API key 

## 3. Upload scripts to AWS Lambda

### 3.1 Make zip file
run below to create `arxiv_crawling.zip`

```
bash make_zip.sh
```

### 3.2 Upload zip file to AWS Lambda
Create your lambda function and upload `arxiv_crawling.zip`

### 3.3 set enviroment params
Like bwlow image, set parameters.  
`CHANNEL_ID` is slack channel id which the bot will post messages
![](https://i.imgur.com/tXU3HjK.png)
