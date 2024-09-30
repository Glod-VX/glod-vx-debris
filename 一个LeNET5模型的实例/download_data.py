
import os
import requests
from bs4 import BeautifulSoup
import time

# 下载单个网页内容
def download_page(url, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text(separator='\n')  # 提取页面中的文本内容

        filename = url.split('/')[-1] or 'index.html'
        filepath = os.path.join(save_dir, filename + '.txt')

        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"下载完成: {filepath}")
        except Exception as e:
            print(f"写入文件失败: {filepath}, 错误: {e}")
    else:
        print(f"无法下载页面: {url}, 状态码: {response.status_code}")

# 批量下载网页内容
def download_all_pages(base_url, save_dir, pause_time=1):
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"无法访问基础URL: {base_url}, 状态码: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找页面中的所有链接
    links = soup.find_all('a', href=True)
    page_links = [base_url + link['href'] for link in links if link['href'].endswith('.htm') or link['href'].endswith('.html')]

    # 下载每个页面的内容
    for idx, page_link in enumerate(page_links):
        print(f"正在下载第 {idx + 1}/{len(page_links)} 个页面: {page_link}")
        download_page(page_link, save_dir)
        time.sleep(pause_time)  # 等待一段时间，避免过于频繁的请求

if __name__ == "__main__":
    base_url = "https://www.marxists.org/chinese/lenin/mia-chinese-lenin-18950907.htm"  # 基础URL
    save_directory = "./lenin_texts"  # 保存网页内容的文件夹

    download_all_pages(base_url, save_directory)
