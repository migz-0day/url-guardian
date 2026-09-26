import ipaddress
from urllib.parse import urlparse
import sqlite3
import whois
from datetime import datetime
import requests

def create_database():
 conn = sqlite3.connect("hist.db")

 cursor = conn.cursor()
 cursor.execute("""
   CREATE TABLE IF NOT EXISTS HISTORY(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         url TEXT,
         risk TEXT,
         score  INTEGER,
         confidence INTEGER,
         reason TEXT,
         scanned_at TEXT
         )
         """)
 conn.commit()
 conn.close()

from flask import Flask, render_template
app=Flask(__name__)
@app.route("/")

def home():
    return render_template("home.html")
from flask import request,jsonify
@app.route("/scan",methods=["post"])

def scan():
    data = request.get_json()
    url=data["url"]
    score= 0
    confidence=[]
    reasons = []   
    Warning = 0

    if url.startswith("https://"):
        reasons.append("secure protocol")         
    else:
        score += 30
        Warning+=1
        reasons.append("uses insecure protocol")

    if len(url) >50:
        score +=10
        Warning+=1
        reasons.append("URL suspeciously long")

    if len(url)>80:
       score +=20
       Warning+=1
       reasons.append("too long")    

    host=urlparse(url).hostname
    try:
      ipaddress.ip_address(host)
      score +=30
      Warning+=1
      reasons.append("uses an IP address and not a domain")
    except ValueError:
      pass

    port=urlparse(url).port
    if port is not None and port not in [80,443]:
     score+=10
     Warning+=1
     reasons.append("uses unrecognized port")

    try:
      w=whois.whois(host)
      creation=w.creation_date

      if isinstance(creation,list):
        creation=creation[0]

      if creation:
        age=datetime.now(creation.tzinfo)-creation
        age_days=age.days
        print("domain age:", age_days,"days")
      if age_days < 30:
          score+=15
          Warning+=1
          reasons.append("domain was registerd recently")
    except Exception as e:
      print("whois lookup failed",e)

    try:
      response=requests.get(
        url,
        allow_redirects=True,
        timeout=10
        )
      redirect_count=len(response.history)
      if redirect_count >0 :
        score+=min(redirect_count*5,20)
        Warning+=1
        reasons.append(f"URL redirects {redirect_count} time(s).")
      if redirect_count >3:
        reasons.append("URL has a long redirect chain.")
        print("redirects:",redirect_count)
        print("final URL :",response.url)
    except requests.RequestException as e:
      print("Redirect check failed: ",e)
    
    """"
    if not host:
     return jsonify({
      "error":"invalid url"
    })
    if host:
     parts=host.split(".")
    if len(parts)>4:
     score+=15
     Warning+=1
     reasons.append("many subdomains")
     """
    """
    if "://"not in url:
      url="http://"+url
      host=urlparse(url).hostname
      score +=5
      Warning+=1
      reasons.append("assummed protocal as http")
    """

    if not url.startswith (("http://","https://",)):
     url="http://"+url
     score+=5
     Warning+=1
     reasons.append("assummed to http protocal")

    path=urlparse(url).path
    if "//"in path:
     score+=10
     Warning+=1
     reasons.append("contains repeated slashes in path")

   
    if host is not None and "xn--" in host:
      score +=35
      Warning+=1
      reasons.append("uses nationalized(punycode)domain")
      print(host)

    if host is not None and host.count("-") >3:
       score +=10
       reasons.append("has to many hyphens")
    
       
    count=0
    for letter in url:
       if letter.isdigit():
        count+= 1
    if count>=6:
      score +=10
      Warning+=1
      reasons.append("many numbers")     
           
    keywords=[
            "login","claim","details",
            "verify","password",
            "bank","confirm",
            "secure","signin",
            "free","update",
            "gift","accept",
            "winner"
        ]
    for keyword in keywords:
            if keyword in url.lower():
             score+=25
             Warning+=1
             reasons.append(f"contains{keyword}") 
    
    similars={
        "0":"o",
        "1":"l",
        "1":"i",
        "$":"s",
        "4":"a",
        "@":"a",
        "7":"t",
        }   
    original_url=url.lower()
    normalized_url=original_url
    similar_found=False
    for old,new in similars.items():
     if old in normalized_url:   
      normalized_url=normalized_url.replace(old,new)
      similar_found=True
    if normalized_url!=original_url:
     score+=10
     Warning+=1
     reasons.append("might have an interchanged character")
    
    brands=[
       "meta","amazon","google","gmail","facebook","microsoft","netflix","spotify","amazon","apple",
       "samsung","disney","ebay","zoom",
       "instagram","discord","whatsapp","tiktok","reddit","telegram",
       "aws","azure","cloudflare",
       "openAI","anthropic","nvidia",
       "gmail","github","gitlab",
       "stripe","cisco","linkedIn","y-combinator",
       "linux","ubuntu","windows","oracle","ibm",
       "visa","paypal","mastercard","binance",
       "steam","xbox"
    ]                    
    for brand in brands:
     if brand in normalized_url and brand not in original_url:
       score +=20
       Warning+=1
       reasons.append(f"should be'{brand}'")   

    if score > 100:
       score=100
    
    if score>=120:
       risk="high risk"
    elif score>=90:
       risk="caution"           
    elif score >=60:
     risk="unsafe"
    elif score >=30:
     risk="suspecious"
    else:
     risk="safe"

    if Warning==0:
       confidence=99
    elif Warning==1:
       confidence=45
    elif Warning==2:
       confidence =65
    elif Warning ==3:
       confidence =80
    elif Warning==4:
       confidence=90
    else:
       confidence=98

    current_time=datetime.now().strftime("%Y-%m-%D %H:%M:%S")
    conn=sqlite3.connect("hist.db")
    cursor=conn.cursor()
    cursor.execute(
       "INSERT INTO history(url,risk,score,confidence,reason,scanned_at)VALUES(?,?,?,?,?,?)",
       (url,risk,score,confidence,",".join(reasons),current_time)
    )
    conn.commit()
    conn.close()

    print(reasons,score)
    print("scan() called")
    return jsonify({
        "url":url,
        "risk":risk,
        "score":score,
        "confidence":confidence,
        "reasons":reasons   
    })

@app.route("/history")
def history():
   conn=sqlite3.connect("hist.db")
   cursor=conn.cursor()

   cursor.execute("""
      SELECT url,risk,score,confidence,reason,scanned_at
      FROM history
      ORDER BY id DESC
      LIMIT 50      
     """)
   history=cursor.fetchall()
   conn.close()
   return jsonify(history)
"""
test=whois.whois("google.com")
creation= test.creation_date   
print("creation date:",creation)
if isinstance(creation,list):
  creation=creation[0]
  age= datetime.now(creation.tzinfo) - creation
print("domain age:", age.days,"days")
"""
if __name__=="__main__":
    create_database()
    app.run(debug=True)

