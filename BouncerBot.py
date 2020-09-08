from __future__ import print_function

import discord

"""More Email packages"""
import base64
from email.mime.text import MIMEText

"""Imports Discord packages"""
from discord.ext.commands import Bot
from discord.utils import get

"""Imports packages used by the Google Gmail API"""
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


"""Imports random and string packages to perform necessary casting 
   for print statements, and random alphanumeric generation for 
   verification keys
"""
import random
import string


"""The prefix used for bot commands"""
BOT_PREFIX = "$"


"""The bot token.

    WARNING: Do not share this token with anyone. Do not display this
             token publicly as it can result in someone hijacking the
             bot and modifying the internal state.
"""
TOKEN = 'ENTER YOUR BOT TOKEN HERE'


"""Defines the gmail scope as an email client that is only authorized to
   send mail.
"""
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


"""client initialization; defines the bot as an object"""
client = Bot(command_prefix="BOT_PREFIX")


"""Authenticates tha Google API usage for BouncerBot.

    Returns:
    The service connection
    
    Citations:
    Code pulled from quickstart.py via
    https://developers.google.com/gmail/api/quickstart/python
"""
def email_setup():
    creds = None
    # The file token.pickle stores the user's access and refresh
    # tokens, and is created automatically when the authorization
    # flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log
    # in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

"""The authorized email client"""
SERVICE = email_setup()


"""Starts the process of 2FA once a new member joins the discord server
    
    Parameters:
    member: the member that joins the server
    
"""
@client.event
async def on_member_join(member):
    from_guild = member.guild
    await two_factor_process(member, from_guild)


"""Handles the flow of operations for 2FA via Discord.
    
    Parameters:
    member: the member that is being communicated with
    
"""
async def two_factor_process(member, from_guild):
    email_inputs = 0
    failed_attempts = 0
    complete = False
    SENDER = 'noreply.bouncebot@gmail.com'
    SUBJECT = 'Discord Verification Code'
    MESSAGE_TEXT = 'Your verification code: '
    PRIMARY_DOMAIN = '@domain1.co'
    SECONDARY_DOMAIN = '@domain2.co'
    await member.send('Welcome to the Server! In order to verify your '
                      'identity, please send a message containing '
                      '**ONLY** your full <Workplace Name> email'
                      '**(ex: aturing12@domain.co)**. ')

    def check(the_message):
        return the_message.author == member and the_message.channel \
               == member.dm_channel

    while not complete:

        email = await client.wait_for('message', check=check)

        if email_inputs == 10:
            await member.send('You have reached the maximum amount of '
                              'email submissions.')
            complete = True
        elif failed_attempts == 3:
            await member.send('**You have exceeded the maximum amount '
                              'of attempts. Bouncer has automatically '
                              'detected this as spam. You have been '
                              'removed from the server.**')
            await kick_user(member)
            complete = True
        else:
            if not (PRIMARY_DOMAIN in email.content
                    or SECONDARY_DOMAIN in email.content):
                email_inputs += 1
                await member.send('This is not a valid <Workplace Name> email. Please'
                                  ' use your <Workplace Name> email '
                                  '**(ex: aturing12'+ PRIMARY_DOMAIN +
                                  ' or aturing12' + SECONDARY_DOMAIN +
                                  ')**.')
            else:
                key = random_key()
                try:
                    created_message =\
                        create_message(sender=SENDER,
                                        to=email.content,
                                        subject=SUBJECT,
                                        message_text=MESSAGE_TEXT + key)
                    sent_message = send_message(service=SERVICE,
                                                user_id='me',
                                                message=created_message)
                    email_inputs = 0
                    complete = True
                    await member.send('Check your email for an 8-digit '
                                      'alphanumeric code. **Send the '
                                      'code back to me to gain access '
                                      'to '
                                      'the server.**')
                except:
                    print ('WARNING: There was an issue with sending an'
                           ' email.')

                code_success = await code_attempt(key, member)

                if (code_success == True):
                    await member.send('Thank you for verifying your '
                                      'student status! You now have '
                                      'access to the server.')
                    await grant_access(member, from_guild)
                else:
                    complete = False
                    await member.send('You have failed to send the '
                                      'correct verification code 5 '
                                      'times. You must restart the '
                                      'verification process by '
                                      'entering your <Workplace Name> email. '
                                      '**' +
                                       str(2 - failed_attempts) + ' '
                                       'attempts remaining.**')
                    failed_attempts += 1


"""Method used to verify that a code sent via email is sent back to 
   the Bot correctly. Will stop after 5 consecutive unsuccessful 
   attempts.
    
    Parameters:
    key: the verification code to check
    member: the member that the bot is verifying
    
    Returns:
    boolean: True if successfully verified, False after 5 failed 
    attempts
    
"""
async def code_attempt(key, member):

    attempts = 0
    complete = False
    authorized = False

    def check(the_message):
        return the_message.author == member and the_message.channel \
               == member.dm_channel

    while not complete:

        code = await client.wait_for('message', check=check)

        if (attempts == 4):
            await member.send('**Invalid key. You have reached the '
                              'maximum attempts for this code.**')
            complete = True
        else:
            if (code.content != key):
                attempts += 1
                await member.send('Invalid Key. Try again. **You have '
                                  + str(5 - attempts)
                                  + ' attempts left.**')
            else:
                authorized = True
                complete = True

    return authorized


"""Create a message for an email.

    Parameters:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
   
    Returns:
    An object containing a base64url encoded email object.
    
    Citations:
    Google API: https://developers.google.com/gmail/api/guides/sending
    Trey Moen: https://treymoen.com/
    
"""
def create_message(sender, to, subject, message_text):

  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


"""Sends a created message via gmail
    
    Parameters:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    message: the created message object
    
    Returns:
    Message to be sent.
    Citations:
    Google API: https://developers.google.com/gmail/api/guides/sending
    Trey Moen: https://treymoen.com/
    
"""
def send_message(service, user_id, message):

  try:
    message = (service.users().messages().send(userId=user_id,
                                               body=message).execute())
    return message
  except:
    print ('An error occurred.')


"""Creates a random alphanumeric key to send to the end user

    Returns:
    A random alphanumeric key
    
"""
def random_key():
    KEY_LENGTH = 8
    key_values = string.ascii_letters + string.digits
    key = ''.join(random.choice(key_values) for i in range(KEY_LENGTH))
    return key.upper()


"""A function that gives a user access to a server's basic role
    
    Parameters:
    member: the server member
    from_guild: the guild from which the member derived
    
"""
@client.event
async def grant_access(member, from_guild):
    role = get(from_guild.roles, name="ROLE_NAME")
    try:
        await member.add_roles(role, reason=None, atomic=True)
    except discord.errors.NotFound:
        await member.send('**Uh oh! It seems like you left the server '
                          'before I could assign you the proper role. '
                          'so sad to see you go!**')


"""Used to kick a member from the server.

   Parameters:
   member: the member the bot is communicating with

"""
async def kick_user(member):
    try:
        await member.kick(reason='Failed auth')
    except discord.errors.NotFound:
        await member.send('**Sorry for raining on your parade.**')


"""Runs the Discord Bot"""
client.run(TOKEN)