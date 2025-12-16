import requests
from bs4 import BeautifulSoup
import time

# 定义请求头，模拟浏览器访问
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_university_ranking(page_url):
    """
    爬取单页的大学排名信息
    :param page_url: 目标页面的URL
    :return: 该页的大学排名列表，每个元素为包含排名、名称、总分的字典
    """
    try:
        # 发送GET请求，设置超时和重试
        response = requests.get(page_url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # 抛出HTTP错误
        response.encoding = response.apparent_encoding  # 自动识别编码
        soup = BeautifulSoup(response.text, "html.parser")

        # 定位排名数据的表格行（需根据实际页面结构调整选择器）
        ranking_list = []
        # 示例选择器，需根据目标网站的HTML结构修改
        rows = soup.select("table tbody tr")
        for row in rows:
            # 提取排名、大学名称、总分（标签和类名需按实际页面调整）
            rank = row.select_one(".rank").text.strip() if row.select_one(".rank") else "未知"
            name = row.select_one(".univ-name").text.strip() if row.select_one(".univ-name") else "未知"
            score = row.select_one(".score").text.strip() if row.select_one(".score") else "未知"
            ranking_list.append({
                "排名": rank,
                "学校名称": name,
                "总分": score
            })
        return ranking_list
    except Exception as e:
        print(f"爬取页面{page_url}失败：{str(e)}")
        return []

def crawl_all_ranks(base_url, total_pages):
    """
    爬取所有页面的大学排名
    :param base_url: 基础URL（包含翻页参数占位符）
    :param total_pages: 总页数
    :return: 所有大学的排名数据
    """
    all_ranks = []
    for page in range(1, total_pages + 1):
        # 构造翻页URL（需根据目标网站的翻页规则修改，如page=1、p=1等）
        page_url = base_url.format(page)
        print(f"正在爬取第{page}页：{page_url}")
        page_ranks = get_university_ranking(page_url)
        if page_ranks:
            all_ranks.extend(page_ranks)
        time.sleep(1)  # 延迟1秒，避免请求过快被封IP
    return all_ranks

if __name__ == "__main__":
    # 注意：需替换为实际提供中国大学排名的网站URL，以及对应的翻页规则和选择器
    # 示例：假设目标网站的翻页URL为"https://example.com/ranking?page={}"，总页数为20
    BASE_URL = "https://example.com/university-ranking?page={}"
    TOTAL_PAGES = 20  # 根据实际总页数调整（近600所高校，若每页30条则为20页）

    # 开始爬取
    print("开始爬取中国大学排名信息...")
    university_ranks = crawl_all_ranks(BASE_URL, TOTAL_PAGES)

    # 输出结果
    if university_ranks:
        print(f"\n共爬取到{len(university_ranks)}所高校的排名信息：")
        for idx, univ in enumerate(university_ranks[:10], 1):  # 打印前10条示例
            print(f"{idx}. {univ['排名']} | {univ['学校名称']} | 总分：{univ['总分']}")
        # 可将数据保存为CSV/Excel文件
        # save_to_csv(university_ranks, "university_ranking.csv")
    else:
        print("未爬取到任何排名信息，请检查URL和页面选择器是否正确。")
