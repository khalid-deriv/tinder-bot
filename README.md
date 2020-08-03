# tinder-bot
A deep learning-powered tinder bot to make your life easy

## How to use:

1. Clone the repository

2. Open the repository folder by running `cd <REPO_NAME>`

3. Install the Requests package by running `pip install requests`

4. Get your Authentication Token by one of two ways:
    - run `python phone_auth.py` and follow the screen prompt to enter your phone number and OTP code. Then copy the given token and paste it in your config file
    - go to [Tinder.com](https://tinder.com/) and login via phone number. Press `ctrl + Shift + I` and go to the `Application` tab. On the left menu, select `Local Storage` and then choose the Tinder domain. Copy the `TinderWeb/APIToken` value and paste it in your config file

5. Begin auto-swiping by running `python swipe.py`
