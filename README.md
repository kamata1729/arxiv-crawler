# arxiv-crawler

Arxiv crawling slack bot runnnig on AWS Lambda

# What this slack bot does
1. Get new arxiv cs.CV papers ,publiched in the last 3 hours  
(If you want to change this category, please change `search_query` argument of `arxiv_crawl.get_new_arxiv_papers`)
2. Translate its abstract into Japanese
3. Post message to slack workspace like below: 
![](https://i.imgur.com/LhkcYRX.png)


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
after installing, do not forget to memo the **access tokens** in below image.  
![](https://i.imgur.com/xLtCz4A.png)

## 2. Setup Google Translation API
Go to https://cloud.google.com/ and enable `Google Translation API`  
After that, you have to get **API key**.  
This API costs some money, so I recommend you to register **free trial**  


## 3. Upload scripts to AWS Lambda

### 3.1 Make zip file
run below to create `arxiv_crawler.zip`

```
bash make_zip.sh
```

### 3.2 Upload zip file to AWS Lambda
Create your lambda function and upload `arxiv_crawler.zip`
The function handler should be specified as `arxiv_crawl.lambda_handler`

### 3.3 set enviroment params
Like bwlow image, set parameters.  
`CHANNEL_ID` is slack channel id which the bot will post messages
![](https://i.imgur.com/tXU3HjK.png)

### 3.4 Set CloudWatch Events trigger
Add `CloudWatch Events` trigger from the left-side list
![](https://i.imgur.com/nOLeJYz.png)

Define trigger role of the `CloudWatch Events` like below:  
![](https://i.imgur.com/p3mYVnw.png)
