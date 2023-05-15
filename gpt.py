import requests
import json
import openai
# get topic
prompt = 'Please ignore all previous instructions. You are an expert copywriter who writes catchy titles for blog posts.   Write a catchy blog post title with a hook for a trendy topic. The titles should be written in the english language. The titles should be less than 60 characters. The titles should include the words from the trendy topic. Do not use single quotes, double quotes or any other enclosing characters. Do not self reference. Do not explain what you are doing.'
# get text data
openai.api_key = "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"
post_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

topic = post_response.choices[0].text
with open('file1.txt', 'w') as f:
    f.write(topic)
    f.close()

prompt = "write a blog post about " + post_response.choices[0].text + " in 3000 words"
try:
    with open('prompt.txt','w') as f:
        f.write(prompt)
        f.close()
    post_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )
except Exception as e:
    with open('error.txt','w') as f:
        f.write(e)
        f.close()
    print(e)
# Set up authentication for the Pexels API
pexels_api_key = 'NmCsE0tFXpS5CK6ybm123zmTx3qwljDetwpTvcEHXeNqu1YLtxWIOCz6'
pexels_base_url = 'https://api.pexels.com/v1'

# Search for photos related to a keyword using the Pexels API
keyword = topic
headers = {
    'Authorization': pexels_api_key
}
params = {
    'query': keyword,
    'per_page': 1
}
response = requests.get(
    f"{pexels_base_url}/search",
    headers=headers,
    params=params
)
if response.status_code == 200:
    image_url = response.json()['photos'][0]['src']['large']
else:
    print(f'Error searching for photos: {response.text}')

# Upload the image to the WordPress site
image_data = requests.get(image_url).content
with open('file2.txt','w') as f:
    f.write(post_response.choices[0].text)
    f.close()

headers = {
    'Content-Type': 'image/jpeg',
    'Content-Disposition': 'attachment; filename="image.jpg"'
}
# Set up the API endpoint URL
base_url = 'https://trends.21centuryvibe.com/wp-json/wp/v2'
url = 'https://trends.21centuryvibe.com/wp-json/wp/v2/posts'
# Set up the authentication credentials
username = 'user'
password = '1aEN ddTz q6OV xvKV grWb rtsG'

auth = (username, password)
response = requests.post(
    f"{base_url}/media",
    headers=headers,
    data=image_data,
    auth=auth
)
if response.status_code == 201:
    image_id = response.json()['id']
else:
    print(f'Error uploading image: {response.text}')

# Set up the post data as a dictionary
post_data = {
    'title': topic,
    'content': post_response.choices[0].text,
    'featured_media': image_id,
    'status': 'publish'
}
# Convert the post data dictionary to JSON
json_data = json.dumps(post_data)

# Set up the request headers
headers = {
    'Content-Type': 'application/json'
}

# Send the POST request to create the new post
response = requests.post(url, auth=(username, password), headers=headers, data=json_data)

# Check the response status code to ensure the request was successful
if response.status_code == 201:
    print('Post created successfully')
else:
    print('Error creating post:', response.text)