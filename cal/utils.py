from calendar import HTMLCalendar
from .models import Content
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
        contents = Content.objects.filter(start_time__year=self.year, start_time__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, contents)}\n'
        return cal


def contest_crawling():
    result = []
    url = 'https://www.wevity.com/'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    view_list = soup.find('ul', 'list').find_all(['li'])
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

        item_obj = {'title': contents3,
                    'content': title2,
                    'date': time_d}
        result.append(item_obj)

    return result
