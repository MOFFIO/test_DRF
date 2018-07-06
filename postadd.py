# -*- coding: utf-8 -*-

import string
import requests
import ConfigParser
import random
import json


URL = 'http://127.0.0.1:9002'

mail_domain = ['ukr.net', 'gmail.com', 'mail.com', 'i.ua', 'mail.co.uk', 'mega.com', 'pron.ua']
letters = string.ascii_lowercase


def get_mail_domain(mail_domain):
    return random.choice(mail_domain)


def get_name(letters, length):
    return ''.join(random.choice(letters) for i in range(length))


def generate_email(length):
    return get_name(letters, length) + '@' + get_mail_domain(mail_domain)


def generate_content():
    return ' '.join([get_name(letters, 8) for i in range(50)])


def create_user(email, password):
    url = "{url}/user/signup/".format(url=URL)
    response = requests.post(url, data={'email': email, 'password': password})
    return response.status_code == 201


def get_token(email, password):
    url = "{url}/user/token/".format(url=URL)
    response = requests.post(url, data={'email': email, 'password': password})
    if response.status_code == 200:
        data = json.loads(response.text)
        return data['token']


def post_create(content, token):
    url = "{url}/post/".format(url=URL)
    response = requests.post(url, data={'content': content}, headers={'Authorization': 'Token {}'.format(token)})
    if response.status_code == 201:
        data = json.loads(response.text)
        return data['id']


def post_like(post_id, token):
    url = "{url}/post/{post}/like/".format(url=URL, post=post_id)
    response = requests.put(url, headers={'Authorization': 'Token {}'.format(token)})
    return response.status_code == 201


users_count = 0
user_post = 0
user_likes = 0
configfile = 'postadd.cfg'

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read(configfile)

    users_count = config.getint('CONFIG', 'users_count')
    user_post = config.getint('CONFIG', 'user_post')
    user_likes = config.getint('CONFIG', 'user_likes')

    password = 'qwerty123'

    emails = [generate_email(8) for i in range(users_count)]

    [create_user(email, password) for email in emails]
    tokens = [get_token(email, password) for email in emails]
    posts = []

    for token in tokens:
        if token:
            post_count = random.randint(0, user_post)
            user_posts = [post_create(generate_content(), token) for i in range(post_count)]
            posts.extend(user_posts)

    for token in tokens:
        likes_count = random.randint(0, user_likes)
        for i in range(likes_count):
            post_id = random.choice(posts)
            post_like(post_id, token)
