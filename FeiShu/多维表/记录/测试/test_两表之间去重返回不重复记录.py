from unittest import TestCase

from FeiShu.多维表.记录.两表之间去重返回不重复记录 import compare_and_filter_lists


class TestListComparison(TestCase):
    def setUp(self):
        # 公共测试数据
        self.base_item = {
            "fields": {
                "促销码信息": "TESTCODE",
                "店铺": "测试店铺",
                "亚马逊商城(站点)": "测试站点",
                "ASIN": "B0TEST001",
                "销售人员": {"users": [{"id": "user_test"}]},
                "销售小组名称": [{"text": "测试小组"}]
            }
        }

    def test_normal_case(self):
        """验证基础过滤功能"""
        # 准备数据
        list1 = [
            {**self.base_item},
            {
                "fields": {
         ** self.base_item["fields"],
        "ASIN": "B0UNIQUE001",
        "促销码信息": "UNIQUE_CODE"
        }
        },{
            "fields": {
                "店铺": "特殊店铺",
                "ASIN": "B0MISSING02",
                "销售人员": {"users": []}
            }
        }
        ]

        list2 = [{**self.base_item}]

        # 预期结果
        expected = [{
            'ASIN': 'B0UNIQUE001',
            '促销码信息': 'UNIQUE_CODE',
            '店铺': '测试店铺',
            '亚马逊商城(站点)': '测试站点',
            '销售人员': [{'id': 'user_test'}],
            '销售小组': '测试小组'
        }]

        # 执行测试
        result = compare_and_filter_lists(list1, list2)
        print(list1)
        print(list2)
        print(result)
        self.assertListEqual(result, expected)

    def test_edge_cases(self):
        """处理边界条件"""
        # 空列表测试
        self.assertEqual(compare_and_filter_lists([], []), [])

        # 部分字段缺失
        list1 = [{
            "fields": {
                "店铺": "特殊店铺",
                "ASIN": "B0MISSING01",
                "销售人员": {"users": []}
            }
        }]

        expected = [{
            'ASIN': 'B0MISSING01',
            '促销码信息': None,
            '店铺': '特殊店铺',
            '亚马逊商城(站点)': None,
            '销售人员': [],
            '销售小组': None
        }]

        self.assertListEqual(compare_and_filter_lists(list1, []), expected)

    def test_full_duplicates(self):
        """完全重复数据过滤"""
        duplicate_item = {**self.base_item}
        list1 = [duplicate_item, duplicate_item]
        list2 = [duplicate_item]

        result = compare_and_filter_lists(list1, list2)
        self.assertEqual(len(result), 1)  # 去重后应保留0条，但list2中已有则过滤
        self.assertEqual(result, [])

    def test_data_anomalies(self):
        """异常数据结构处理"""
        anomaly_data = [
            {
                "fields": {
                    "销售人员": "invalid_format",  # 错误类型
                    "销售小组名称": [{"no_text": "错误结构"}]
                }
            },
            {
                "fields": {
                    "销售小组名称": {"text": "非列表结构"}  # 错误结构
                }
            }
        ]

        expected = [
            {
                'ASIN': None,
                '促销码信息': None,
                '店铺': None,
                '亚马逊商城(站点)': None,
                '销售人员': [],
                '销售小组': None
            },
            {
                'ASIN': None,
                '促销码信息': None,
                '店铺': None,
                '亚马逊商城(站点)': None,
                '销售人员': [],
                '销售小组': None
            }
        ]

        result = compare_and_filter_lists(anomaly_data, [])
        self.assertListEqual(result, expected)

    def test_performance(self):
        """大数据量性能测试"""
        # 生成10万条测试数据
        bulk_data = [{**self.base_item, "fields": {**self.base_item["fields"], "ASIN": f"B0BULK{i}"}} for i in
                     range(100000)]

        # 确保在合理时间内完成（例如5秒内）
        import time
        start = time.time()
        result = compare_and_filter_lists(bulk_data, bulk_data[:50000])
        duration = time.time() - start

        self.assertEqual(len(result), 50000)
        self.assertLess(duration, 5, "性能未达预期")