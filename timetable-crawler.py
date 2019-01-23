from requests_html import HTMLSession
import sys

def translate_station_name(chinese_name):
    code = {'左營站': 'ZUY', '台中站' : 'TAC', '台北站' : 'TPE', '南港站' : 'NAG'}
    return code[chinese_name]

session = HTMLSession()
r = session.get('https://www.thsrc.com.tw/tw/TimeTable/DailyTimeTable/' + sys.argv[1])

train_list = r.html.find('[bgcolor=\"#FFFFFF\"], [bgcolor=\"#EAEAEA\"]')

for train in train_list:
    train_no = train.find('.text_orange_link')[0].text
    # find origin and destination
    stations = list(filter(lambda t: t.text != '', train.find('.text_grey2')))
    origin_station = translate_station_name(stations[0].attrs['title'])
    dest_station = translate_station_name(stations[-1].attrs['title'])

    origin_time = stations[0].text
    dest_time = stations[-1].text

    print(train_no, origin_station, origin_time, dest_station, dest_time)
