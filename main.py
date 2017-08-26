import geoip2.database
import sys
from flask import Flask, request
import telepot
import socket
from telepot.loop import OrderedWebhook

reader = geoip2.database.Reader('c:/Users/creator/Desktop/telebot/GeoLite2-City.mmdb')
sadsmile = u'\U0001f605'
cool = u'\U0001f60e'
laught = u'\U0001f602'
TOKEN = sys.argv[1]
PORT = int(sys.argv[2])
URL = sys.argv[3]

class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        self._count += 1
        self.sender.sendMessage(self._count)


def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False


def printIp(tgt):
    response = reader.city(tgt)
    city = response.city.name
    region = response.subdivisions.most_specific.name
    country = response.country.name
    long = response.location.longitude
    lat = response.location.latitude
    output = [str(tgt), str(city), str(region), str(country), str(long), str(lat)]
    return output

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id, msg['text'])

    if content_type == 'text':
        if msg['text'] == '/start':
            bot.sendMessage(chat_id, text="Hi there, I'm a @Skunk_Hunter_bot and I can help you with getting an address of your Internet offenders. Just give me White IP-address and in few seconds I will return their geolocation.")
        else:
            try:
                tgt = msg['text']
                if valid_ip(tgt) == True:
                    tgt = printIp(tgt)
                    bot.sendMessage(chat_id, text="Target: %s Geo-located. \nCity: %s \nRegion: %s \nCountry: %s \nLongitude: %s \nLatitude: %s" % (tgt[0], tgt[1], tgt[2], tgt[3], tgt[4], tgt[5]))
                    bot.sendLocation(chat_id, tgt[5], tgt[4])
                else:
                    bot.sendMessage(chat_id, text="That shit you have typed is not an IP address. Try once more, homie. " + laught)
            except:
                bot.sendMessage(chat_id, text="Sorry, I don't know that IP " + sadsmile)
    else:
        bot.sendMessage(chat_id, msg['Sorry bruh, I understand only IP-addresses.' + cool])

app = Flask(__name__)
bot = telepot.Bot(TOKEN)
webhook = OrderedWebhook(bot, handle)


@app.route('/webhook', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'


if __name__ == '__main__':
    try:
        bot.setWebhook(URL)
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
    app.run(port=PORT, debug=True)



