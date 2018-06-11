from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
from telethon.errors import SessionPasswordNeededError


def get_pinned_message(username, api_id, api_hash, phone, name):
    # (2) Create the client and connect
    client = TelegramClient(
        username,
        api_id,
        api_hash,
        update_workers=1,
        spawn_read_thread=False
    )
    client.connect()

    # Ensure you're authorized
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))

    me = client.get_me()

    try:
        cid = client.get_entity(name).id  # Replace with Channel.username
    except:
        print('Problem with {}'.format(name))
        return
    
    # cid = '1297947823'
    channel_entity = client.get_entity(PeerChannel(cid))
    channel_info = client(GetFullChannelRequest(channel_entity))
    # print(channel_info)
    pinned_msg_id = channel_info.full_chat.pinned_msg_id

    pinned_msg = None
    if pinned_msg_id is not None:
        pinned_msg = client(
            GetHistoryRequest(
                channel_entity,
                limit=1,
                offset_date=None,
                offset_id=pinned_msg_id + 1,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            )
        )
    return pinned_msg

# pm = get_pinned_message(username, api_id, api_hash, 'nnamdii')
# print(len(pm.messages))
# print(pm.stringify())
# @client.on(events.NewMessage)
# def my_event_handler(event):
#     print('*'*45)
#     print(event.raw_text)
#     print('*'*45)
#     print(event)
#     # if 'hello' in event.raw_text:
#     #     event.reply('hi!')

# client.idle()
