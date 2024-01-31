from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import requests
import datetime
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
import os
import json

# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

# Variables - GitHub
line_notify_id = os.environ['LINE_NOTIFY_ID']
sheet_key = os.environ['GOOGLE_SHEETS_KEY']
gs_credentials = os.environ['GS_CREDENTIALS']

# Variables - Google Colab
# line_notify_id = LINE_NOTIFY_ID
# sheet_key = GOOGLE_SHEETS_KEY
# gs_credentials = GS_CREDENTIALS

# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

# LINE Notify ID
LINE_Notify_IDs = list(line_notify_id.split())

# 定義查找nid代碼函數
def find_nid(title, text):
    title_line_numbers = []
    for i, line in enumerate(text.split('\n')):
        if title in line:
            title_line_numbers.append(i)

    if not title_line_numbers:
        print(f'Cannot find "{title}" in the text.')
        return None

    title_line_number = title_line_numbers[0]
    title_line = text.split('\n')[title_line_number]

    nid_start_index = title_line.index('nid="') + 5
    nid_end_index = title_line.index('"', nid_start_index)
    nid = title_line[nid_start_index:nid_end_index]

    return nid

# 取得網頁內容
def get_content(url):
  # 發送GET請求獲取網頁內容
  response = requests.get(url)

  # 解析HTML內容
  soup = BeautifulSoup(response.content, 'html.parser')

  # 找到所有的 <p> 標籤
  p_tags = soup.find_all('p')

  # 整理文字內容
  text_list = []
  for p in p_tags:
      text = p.text.strip()
      text_list.append(text)
  text = ' '.join(text_list)
  text = ' '.join(text.split())  # 利用 split() 和 join() 將多個空白轉成單一空白
  # text = text.replace(' ', '\n')  # 將空白轉換成換行符號
  text = text.replace(' ', '')  # 刪除空白
  return text

# LINE Notify
def LINE_Notify(category, date, title, unit, link, content):
  for LINE_Notify_ID in LINE_Notify_IDs:
    headers = {
            'Authorization': 'Bearer ' + LINE_Notify_ID,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    if content == '':
        params = {'message': f'''【{category}】{title}
⦾公告日期：{date}
⦾發佈單位：{unit}
⦾更多資訊：{link}'''}
    else:
        params = {'message': f'''【{category}】{title}
⦾公告日期：{date}
⦾發佈單位：{unit}
⦾內容：{content}
⦾更多資訊：{link}'''}

    r = requests.post('https://notify-api.line.me/api/notify',
                            headers=headers, params=params)
    print(r.status_code)  #200

# Google Sheets 紀錄
scope = ['https://www.googleapis.com/auth/spreadsheets']
info = json.loads(gs_credentials)

creds = Credentials.from_service_account_info(info, scopes=scope)
gs = gspread.authorize(creds)

def google_sheets_refresh():

  global sheet, worksheet, rows_sheets, df

  # 使用表格的key打開表格
  sheet = gs.open_by_key(sheet_key)
  worksheet = sheet.get_worksheet(0)

  # 讀取所有行
  rows_sheets = worksheet.get_all_values()
  # 使用pandas創建數據框
  df = pd.DataFrame(rows_sheets)

# 開啟網頁
urls = {
    '最新消息':'https://www.kjsh.ntpc.edu.tw/ischool/widget/site_news/main2.php?uid=WID_0_2_0175a41dca498eab35e73c7c40fd1c141d1f3a58&maximize=1&allbtn=0' # 最新消息
    ,'榮譽榜':'https://www.kjsh.ntpc.edu.tw/ischool/widget/site_news/main2.php?uid=WID_0_2_0f31e8a5a7bc3c4ef6609345e33cd3ae6b3e97cc&maximize=1&allbtn=0' # 榮譽榜
    ,'校務通報':'https://www.kjsh.ntpc.edu.tw/ischool/widget/site_news/main2.php?uid=WID_0_2_b1568f22c498d41d46e53b69325a31e78d51c87c&maximize=1&allbtn=0' # 校務通報
    ,'研習':'https://www.kjsh.ntpc.edu.tw/ischool/widget/site_news/main2.php?uid=WID_0_2_e04b673ba655cf5fbdbab4e815d941418b3ec90c&maximize=1&allbtn=0'# 研習
    ,'師生活動與競賽':'https://www.kjsh.ntpc.edu.tw/ischool/widget/site_news/main2.php?uid=WID_0_2_548130b3d109474559de5f5f564d0a729c3c7b3d&maximize=1&allbtn=0' # 師生活動與競賽
    ,'防疫專區':'https://www.kjsh.ntpc.edu.tw/ischool/widget/site_news/main2.php?uid=WID_0_2_36ca124c0de704b62aead8039c9bbe125095f5aa&maximize=1&allbtn=0' # 防疫專區
    ,'招標公告':'https://www.kjsh.ntpc.edu.tw/ischool/widget/site_news/main2.php?uid=WID_0_2_27c842d8808109d6838dde8f0c1222d6177d71b8&maximize=1&allbtn=0' #招標公告
}

# 刷新Google Sheets表格
google_sheets_refresh()

# 取得Google Sheets nids列表
_nids = df[5].tolist()
nids = []
for n in _nids:
  try:
    nids.append(str(int(n)))
  except:
    continue

for category in urls:

    url = urls[category]

    # chromedriver 設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(binary_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # 等待網頁載入完成
    driver.implicitly_wait(10)

    # 找到表格元素
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    table_div = driver.find_element(By.ID, 'div_table_content')
    table = table_div.find_element(By.ID, 'ntb')
    html = table.get_attribute('outerHTML')

    # 解析HTML文件
    soup = BeautifulSoup(html, 'html.parser')

    # 格式化HTML文件
    formatted_html = soup.prettify()
    # print(formatted_html)

    # 找到表格中的所有資料列
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # 打印每一行的 HTML 內容
    # for row in rows:
    #     row_html = row.get_attribute('outerHTML')
    #     print(row_html)

    # 定義需要查找的最新幾筆資料（最多9筆）
    numbers_of_new_data = 9

    # 印出最新幾筆資料的標題、單位和連結
    for i in range(1, 1 + numbers_of_new_data):
        row = rows[i]
        # row_html = row.get_attribute('outerHTML')
        # print(row_html)
        cells = row.find_elements(By.TAG_NAME, 'td')
        date = cells[1].text
        title = cells[3].text
        unit = cells[2].text

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(row.get_attribute('outerHTML'), 'html.parser')

        # 找到 nid 的值
        nid = soup.find('tr')['nid']

        link = f'http://www.kjsh.ntpc.edu.tw/ischool/public/news_view/show.php?nid={nid}'
        content = get_content(link)
        print(f'date:{date}\tcategory:{category}\ttitle:{title}\tunit:{unit}\tnid:{nid}\tlink:{link}\tcontent:{content}')

        # 獲取當前日期
        today = datetime.date.today()

        # 將日期格式化為2023/02/11的形式
        formatted_date = today.strftime("%Y/%m/%d")

        # 檢查nid是否已經存在於表格中
        sent = not(str(int(nid)) in nids)

        if sent:

          # 檢查標題是否已經存在於表格中
          titles = df[3].tolist()
          if title in titles:
            continue

          # 獲取新行
          now = datetime.datetime.now() + datetime.timedelta(hours=8)
          new_row = [now.strftime("%Y-%m-%d %H:%M:%S"), category, date, title, unit, nid, link, content]

          # 將新行添加到工作表中
          worksheet.append_row(new_row)

          # 獲取新行的索引
          new_row_index = len(rows) + 1

          # 更新單元格
          cell_list = worksheet.range('A{}:H{}'.format(new_row_index, new_row_index))
          for cell, value in zip(cell_list, new_row):
              cell.value = value
          worksheet.update_cells(cell_list)

          # 更新nids列表
          nids.append(int(nid))

          # 傳送至LINE Notify
          print(f'Sent: {nid}', end=' ')
          LINE_Notify(category, date, title, unit, link, content)

        # 刪除nid
        del nid

    # 關閉網頁
    driver.quit()
