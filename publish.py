import instagrapi, dotenv, os, time, json, pytz
from datetime import datetime

# Credentials
print('🔑 Loading credentials...')
dotenv.load_dotenv()
username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')
totp_seed = os.getenv('INSTAGRAM_TOTP_SEED')

# Client
print('🔑 Creating client...')
client = instagrapi.Client()

print('🔑 Generating TOTP...')
totp = client.totp_generate_code(totp_seed)

print(f'🔑 Logging in as {username}...')
client.login(
  username=username,
  password=password,
  verification_code=totp
)


print(f'✅ Successfully logged in as {username}')

while True:
  try:
    # Load json file
    with open('stories.json') as f:
      stories_list = json.load(f)
    
    date = time.strftime("%d-%m")

    # Check if a story has already been uploaded for today
    stories = 0
    for story in stories_list:
      if story['day'] == date and story['type'] == 'midi':
        stories += 1
        break

    if stories != 0:
      print('❌ Story already uploaded for today...')
      time.sleep(3600)
      continue

    path_prefix = 'renders/final/'
    path_suffix = '.png'
    media_path = f'{path_prefix}m-{date}{path_suffix}'

    if not os.path.exists(media_path):
      print(f'❌ Media not found: {media_path}')
      pass

    # Upload to story
    print(f'📸 Uploading {media_path}...')

    response = (
      client.photo_upload_to_story(
        media_path,
        f'Menu du jour du {date}',
        extra_data={"audience": "besties"}
      )
    )

    print('✅ Successfully uploaded to story')

    sotry_id = response.id
    paris_tz = pytz.timezone('Europe/Paris')
    paris_time = datetime.now(paris_tz)
    story_date = paris_time.strftime("%Y-%m-%d %H:%M:%S")
    story_day = date

    print(f'📸 Story ID: {sotry_id}')
    print(f'📸 Story Date: {story_date}')
    print(f'📸 Story Day: {story_day}')

    json_file = 'stories.json'
    print(f'📝 Writing to {json_file}...')

    stories_list.append({
      'id': sotry_id,
      'date': story_date,
      'day': story_day,
      'type': 'midi'
    })

    with open(json_file, 'w') as f:
      json.dump(stories_list, f, indent=2)

    print(f'✅ Successfully saved to {json_file}')
  except KeyboardInterrupt:
    print('🛑 Exiting...')
    break
  except Exception as e:
    print(f'🚨 An error occurred: {e}')
    break
