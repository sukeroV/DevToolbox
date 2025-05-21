t = {('TESTCODE', '测试店铺', '测试站点', 'B0TEST001'),
('TESTCODE', '测试店铺', '测试站点', 'B0TEST001'),
('UNIQUE_CODE', '测试店铺', '测试站点', 'B0UNIQUE001'),
(None, '特殊店铺', None, 'B0MISSING02')}



for i in t:
    print(i)
    if i in t:
        print("yes")