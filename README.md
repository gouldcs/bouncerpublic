# Bouncer Bot v1.0
_Server security, guaranteed._
___
#### Purpose
The purpose of the Bouncer is to provide a 2FA email service to
   groups that desire a way to domain-lock their servers. This is a
   function that is available on other platforms like Slack,
   but doesn't yet exist on Discord.

   Many users who are asked to join a new server, whether it be for
   fun, for work, or school, likely will not create a new account for
   this purpose. The Bouncer's goal is to make it possible for
   users to continue to use their personal accounts to join servers
   like these, while also having a way to confirm their domain. This
   also serves as a security function for businesses and universities
   that wish to avoid raids, and maintain a professional workspace.
   
___
#### Quickstart

The quickstart for Bouncer is fairly straightforward. This guide assumes that you have
no virtual environment set up, no version of Python installed, and none of the necessary APIs
installed either. Running Bouncer locally is not suggested, and it is suggested that you
instead run this bot from a server to assure nearly 24/7 access to Bouncer.

   0. **Clone the repo**  
      Create a working directory and clone the repo inside this directory. If you need
      help in doing so, a tutorial can be found [here](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).
      
   1. **Set up a Virtual Environment (Suggested)**  
      In your working directory (not inside the repo), set up a virtual environment. This requires python.
      Bouncer was built and tested using Python 3.8.5 and cannot guarantee functionality
      on older versions of Python. You can install Python 3.8.5 [here](https://www.python.org/downloads/release/python-385/).
      You can set up a virtual environment by running the following
      command in cmd/terminal in your working directory:  
      ```
      python3 -m venv bouncer-env
      ```
      then activate the virtual environment by running:  
      ```
      bouncer-env/Scripts/activate.bat
      ```
      or on MacOS:
      ```
      source bouncer-env/bin/activate
      ```
   2. **Install required Libraries**  
      Change to your repo directory and run the following command
      to install all libraries used within this code from the requirements.txt document:
      ```
      pip install -r requirements.txt
      ```
   3. **Run Bouncer**  
      Bouncer is now ready to run. You can do so through the command line. In your
      working directory, run:
      ```
      python BouncerBot.py
      ```
      Bouncer will now be active on Discord.
      
      An example of a minimal bot is shown here: https://discordpy.readthedocs.io/en/latest/quickstart.html
   
___
   
#### Setup

   While there is a small set of requirements, they are rather easy
   steps to follow, and the process should take no longer than five
   minutes.

   1. **Invite the bot to the server.** 
   
      This link allows anyone to add this bot to their server:
   
      [Click here to invite Bouncer to your server](https://discord.com/api/oauth2/authorize?client_id=748287402572775505&permissions=268502018&scope=bot)
      
      The details of the link above are documented here:
      
      https://discordpy.readthedocs.io/en/latest/discord.html#inviting-your-bot

   2. **Set up your server.**  
      Your server needs to be protected, by default, from anyone who
      might randomly join who does not belong there. In order to
      enable such protections, you must go to your server settings,
      and disable all permissions for the @everyone role. Then,
      create a role with the default permissions you want your basic
      users to have. ***In this version, it is required that you name
      your role 'Student' with the exact same capitalization. Any
      modification to this name will cause the bot to not work.***

   3. **Add support for current users.**  
      Give all your current users the default role (in this version,
      the 'Student' role) so that they maintain their presence on the
      Discord server.

   4. **Congratulations.**  
      That is everything! The bot is now set up and ready to thwart
      unwanted users from joining the server.
      
___

#### Functionality
   Bouncer functions as expected from a 2FA email system. The flow has been designed
   to make it easy for users to verify their identity, and frustrating for intruders
   to deal with. Here is what to expect:
   
   1. Upon joining the server, you will receive a message from Bouncer:  
      ![](https://media.discordapp.net/attachments/656379081264332814/749000626914197604/intro_msg.PNG)
   2. If you enter a bad email, Bouncer will let you know:  
      ![](https://media.discordapp.net/attachments/656379081264332814/749000646803587133/invalid_email.PNG)
   3. Once you enter an email associated with the domain, it will notify you:  
      ![](https://media.discordapp.net/attachments/656379081264332814/749000659554009108/valid_email.PNG)
   4. You get 5 attempts to enter the correct code:  
      ![](https://media.discordapp.net/attachments/656379081264332814/749000688511746088/invalid_code.PNG)
   5. And if you exceed the 5 attempts, the process will restart:  
      ![](https://media.discordapp.net/attachments/656379081264332814/749000708002414602/invalid_restart.PNG)
   6. Providing a correct email will yield an email in this format:  
      ![](https://media.discordapp.net/attachments/656379081264332814/749000758971596810/verification_code.PNG)
   7. Once you enter the correct code, Bouncer will let you know:  
      ![](https://media.discordapp.net/attachments/656379081264332814/749000739485122630/success.PNG)
   8. And you will get your role within the server:  
      ![](https://media.discordapp.net/attachments/656379081264332814/749003193320734880/role_get.PNG)
   9. If you fail the process 3 times, you will be informed and kicked from the server:
      ![](https://media.discordapp.net/attachments/656379081264332814/749029129164292136/failed.PNG)

___
#### References

Bouncer is a bot created by Cameron Gould, with support
from *Masao Kitamura*, *Adian Dionisio*, and *Trey Moen* in the 
interest of creating a security feature for the Computer 
Science LMU server. Further development to modularize end 
generalize the code in order to support more services than 
just LMU is planned, as well as added functionality to improve
user experience.
