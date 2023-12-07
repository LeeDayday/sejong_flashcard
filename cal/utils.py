from calendar import HTMLCalendar
from .models import Content, NewUserInfo
import os, requests
from bs4 import BeautifulSoup

import datetime

class Calendar2(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar2, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, contents):
        contents_per_day = contents.filter(start_time__day=day)
        d = ''
        for content in contents_per_day:
            d += f'<li> {content.get_html_url} </li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, contents):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, contents)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        owner = NewUserInfo.objects.latest("updated_at")
        contents = Content.objects.filter(start_time__year=self.year, start_time__month=self.month, owner=owner)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, contents)}\n'
        return cal


def contest_crawling():
    result = []
    for page in range(1, 3):
        url = f'https://www.wevity.com/?c=find&s=1&gp={page}'
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        view_list = soup.find('ul', 'list').find_all('li')
        print(view_list)
        for i in view_list:
            all_title = i.find_all(['div', 'tit'])
            if "공모전명" in all_title[0].get_text():
                continue
            title = all_title[0].get_text()
            title2 = title.replace('\n', '')

            contents = i.find_all(['div', 'organ'])
            contents3 = contents[2].get_text().replace('\n', '')

            ddate = i.find_all(['div', 'day'])
            ddate3 = ddate[3].get_text().replace('\n', '')
            ddate3 = ddate3.replace('\t', '')
            ddate3 = ddate3.replace('\r', '')

            ddate3 = "".join(filter(str.isdigit, str(ddate3)))
            ddate3 = int(ddate3)-1
            today = datetime.date.today()
            time_d = datetime.timedelta(ddate3)
            time_d += today

            link = i.find_all(['div','tit','a','href'])
            link = 'https://www.wevity.com/' + str(link)[28:78]
            link = link.replace('amp;', '')
            item_obj = {'title': contents3,
                        'content': title2,
                        'date': time_d,
                        'link':link}
            result.append(item_obj)
    result.sort(key = lambda x:x['date'])
    return result

def school_cal_crawling():
    result = []
    url = 'http://www.sejong.ac.kr/unilife/program_01.html?menu_id=1.1'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    view_list = soup.select('#content > div.calendar_wrap')

    for i in view_list:
        all_title = i.find_all(['h4'])

        ym = all_title[0].get_text()
        y, m = ym.index("년"), ym.index("월")
        year = int(ym[:y])
        month = int(ym[y+1:m])

        # 달력 일정 뽑기
        contents = i.find_all(['#div > calendar_list', 'ul', 'li'])
        contents3 = contents[0].get_text().split('\n')[1:-1]
        for j in contents3:
            date = str(year)+"/"+str(month)
            item_obj = {'date': date,
                        'content': j}
            result.append(item_obj)
    return result
def check(j, t):
    tmp = j[t:]
    if ')' in tmp:
        x = j[t:].index(')') + t+1
        z = 14 if t == 5 else 13
        if x > z:
            x = t
    else:
        x = t
    return t