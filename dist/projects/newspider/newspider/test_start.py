import os


if __name__ == "__main__":
    os.chdir('rules')
    rules = os.listdir()
    print('模板文件：', rules)
    rule = input()

    for i in rules:
        if rule in i:
            os.system(f'scrapy test {i}')
            break