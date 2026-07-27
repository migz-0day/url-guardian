# features
*HTTPS dtection
*URL length analysis
*
*suspecious keywords(login,varify,bank,free)
*IP-address URLs
*URL shortener detection
*Risk score(0-100)color coding red,orange,yellow,green
*time of scan
*search previous scans

#
*if its http it will give the orange signal,if its an extended(http://Rvibs-login-pay.mnbv) or suspecious URL it gives red.somethin like https://Rvibs.ac.ke it will show green
# how it works
*when scan is clicked js(fetch("/scan")) then flask receives the request(@app.route("/scan"))
*python checks URL[HTTPS?, length? ,keywords?,risk score]
*python sends json back{
                       "risk":"high", medium,low
                       "score":85
                       }
*js receives it,response.json().  display:> (color code)high Risk 
                                           score 
# history
we can scan Rvibs.ac.ke
python saves:> Rvibs.ac.ke
               safe       
               time
also it gives the resons for the results:
                Rvibs-login.mnb.ac.ke
                Risk Score:90
                reasons
                .HTTP
                .Login keyword
                .Long URL