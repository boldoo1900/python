from slacker import Slacker

slack = Slacker("HERE IS YOUR TOKEN")

slack.chat.post_message('#bottest_channel',  'test bot!', as_user=True)

# Get users list
# response = slack.users.list()
# users = response.body['members']