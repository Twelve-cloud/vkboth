#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py: This script likes avatars of each friend of yours.
"""


from os.path import exists
from vk_api import vk_api


def init_bot() -> None:
    """
    init_bot: Initializes bot via entering login and password, getting
    access token, saving it into file 'access_token.txt'.
    """
    while True:
        try:
            session = vk_api.VkApi(
                login=input('Login: '),
                password=input('Password: '),
                scope=73730  # 65536 for non-expiring token, 2 for friends, 8192 for wall
            )

            session.auth(token_only=True)

            with open('access_token.txt', 'w') as ftoken:
                ftoken.write(session.token.get('access_token'))

        except Exception:
            print('Wrong Login or Password.')

        else:
            break


if __name__ == '__main__':
    if not exists('access_token.txt'):
        init_bot()

    access_token = open('access_token.txt').readline()
    session = vk_api.VkApi(token=access_token)
    method = vk_api.VkApiMethod(session)

    try:
        friends = method.friends.get().get('items')
        print(friends)
        MAX_PHOTOS = 1000

        while len(friends):
            sfriends = ','.join(str(friend) for friend in friends[:MAX_PHOTOS])
            users = method.users.get(user_ids=sfriends, fields='photo_id')

            photos = {
                user['id']: (photo := user['photo_id'])[photo.find('_') + 1:]
                for user in users if 'photo_id' in user
            }

            for user in photos:
                while True:
                    print(user)
                    try:
                        if not method.likes.isLiked(type='photo', owner_id=user, item_id=photos[user])['liked']:
                            method.likes.add(type='photo', owner_id=user, item_id=photos[user])
                            print('done')
                        break
                    except Exception as error:
                        print(error)

            friends = friends[MAX_PHOTOS:]

    except Exception as error:
        print(error)
