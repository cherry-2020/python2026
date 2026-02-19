#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的网页爬虫示例
此脚本演示如何使用Python的requests和BeautifulSoup库进行基本的网页抓取
注意：使用时请遵守网站的robots.txt规则和相关法律法规
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urljoin

class SimpleWebScraper:
    def __init__(self, user_agent=None):
        """初始化爬虫"""
        # 设置请求头，模拟浏览器访问
        self.headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 创建会话对象
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_page(self, url, max_retries=3):
        """获取网页内容，支持重试机制"""
        retries = 0
        while retries < max_retries:
            try:
                # 添加随机延迟，避免请求过快
                time.sleep(random.uniform(1, 3))
                response = self.session.get(url, timeout=10)
                response.raise_for_status()  # 检查请求是否成功
                return response.text
            except requests.RequestException as e:
                retries += 1
                print(f"请求失败，第{retries}次重试: {e}")
                if retries >= max_retries:
                    print(f"达到最大重试次数，放弃请求: {url}")
                    return None
        return None
    
    def parse_html(self, html_content, selector=None):
        """解析HTML内容"""
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 如果提供了选择器，则使用选择器提取内容
        if selector:
            return soup.select(selector)
        
        return soup
    
    def extract_links(self, html_content, base_url=None):
        """从HTML中提取链接"""
        soup = self.parse_html(html_content)
        if not soup:
            return []
        
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # 如果提供了基础URL，将相对链接转换为绝对链接
            if base_url:
                href = urljoin(base_url, href)
            links.append(href)
        
        return links
    
    def save_to_csv(self, data, filename, fieldnames):
        """将数据保存到CSV文件"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"数据已保存到: {filename}")
            return True
        except Exception as e:
            print(f"保存CSV失败: {e}")
            return False
    
    def crawl_example(self, url="https://quotes.toscrape.com/"):
        """示例：抓取名人名言网站的数据"""
        print(f"开始抓取: {url}")
        
        # 获取首页内容
        html = self.get_page(url)
        if not html:
            return []
        
        # 解析网页
        soup = self.parse_html(html)
        
        # 提取名言和作者信息
        quotes_data = []
        for quote in soup.select('.quote'):
            text = quote.select_one('.text').get_text(strip=True)
            author = quote.select_one('.author').get_text(strip=True)
            tags = [tag.get_text() for tag in quote.select('.tag')]
            
            quotes_data.append({
                'text': text,
                'author': author,
                'tags': ', '.join(tags)
            })
        
        print(f"共抓取到 {len(quotes_data)} 条名言")
        
        # 保存到CSV文件
        self.save_to_csv(quotes_data, 'quotes.csv', ['text', 'author', 'tags'])
        
        return quotes_data

def main():
    # 创建爬虫实例
    scraper = SimpleWebScraper()
    
    print("======= Python网页爬虫示例 =======")
    print("此脚本将抓取 quotes.toscrape.com 网站的名言数据")
    print("注意：本示例仅用于学习目的，请遵守网站的使用条款")
    print("====================================")
    
    # 运行示例爬取
    data = scraper.crawl_example()
    
    # 打印前3条结果作为预览
    print("\n预览前3条结果:")
    for i, item in enumerate(data[:3]):
        print(f"\n{i+1}. 名言: {item['text']}")
        print(f"   作者: {item['author']}")
        print(f"   标签: {item['tags']}")
    
    # 打印使用说明
    print("\n======= 使用说明 =======")
    print("1. 您可以修改crawl_example方法来抓取其他网站")
    print("2. 使用selector参数自定义CSS选择器提取内容")
    print("3. 爬虫包含基本的反爬措施：随机延迟和请求头设置")
    print("4. 重要：爬取网站时请遵守robots.txt规则和相关法律法规")

if __name__ == "__main__":
    main()