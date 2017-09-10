import uestc
import argparse
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--accountData',
                      help='账户数据 例如{"2016060106007", "123456"}')
    args = parser.parse_args()
    print(args.accountData)

    print(type(json.loads(args.accountData)))
