########### Python 2.7 #############
import httplib, urllib, base64, json

###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = '29120edd1c5e49afb6a5c7ee489e264a'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0'

headers = {
    # Request headers.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.urlencode({
    # Request parameters. All of them are optional.
    'visualFeatures': 'description',
    'language': 'en',
})

# The URL of a JPEG image to analyze.
body = "{'url':'https://scontent-iad3-1.xx.fbcdn.net/v/t35.0-12/24726147_1641730655848963_260168319_o.jpg?_nc_ad=z-m&_nc_cid=0&oh=c85115f4a6bf04b5010027c07c3900a3&oe=5A26ABD8'}"

try:
    # Execute the REST API call and get the response.
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=False, indent=2))
    conn.close()

except Exception as e:
    print('Error:')
    print(e)
