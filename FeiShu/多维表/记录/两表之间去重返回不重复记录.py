from typing import List, Dict, Tuple

# from typing import *
#
# try:
#     from xbot.app.logging import trace as print
# except:
#     from xbot import print


def find_unique_records(new_list: List[Dict], old_list: List[Dict], config: Dict = None) -> Tuple[
    List[Dict], List[Dict]]:
    """
    title: 精准查找差异记录
    description: 比对两个列表，返回新增记录和重复记录。通过对比 `%new_list%` 和 `%old_list%` 中的关键字段，找出新增和重复的记录。
    inputs:
        - new_list (list): 需要检测的新记录列表, eg: [{"fields": {"ASIN": "B001", "店铺": "ABC"}}]
        - old_list (list): 作为基准的旧记录列表, eg: [{"fields": {"ASIN": "B002", "店铺": "XYZ"}}]
        - config (dict): 销售小组映射配置, eg: {"组A": "Group A"}
    outputs:
        - unique_records (list): 新增记录, eg: [{"ASIN": "B001", "店铺": "ABC"}]
        - duplicate_records (list): 重复记录, eg: [{"ASIN": "B002", "店铺": "XYZ"}]
    """
    config = config or {}

    def _normalize(record: Dict) -> Dict:
        """深度数据清洗和标准化"""
        fields = record.get('fields', {})

        standardized = {
            'ASIN': str(fields.get('ASIN', '')).strip().upper(),
            '优惠券名称': str(fields.get('优惠券名称', '')).strip(),
            '店铺': str(fields.get('店铺', '')).strip(),
            '站点': str(fields.get('站点', '')).strip()
        }

        sales_info = fields.get('销售人员', {})
        user_id = ''
        if isinstance(sales_info, dict):
            users = sales_info.get('users', [{}])
            user_id = users[0].get('id', '') if users else ''
        elif isinstance(sales_info, list) and len(sales_info) > 0:
            user_id = sales_info[0].get('id', '')

        sales_group = fields.get('销售小组', '')
        if isinstance(sales_group, list):
            sales_group = sales_group[0] if sales_group else ''
        sales_group = config.get(str(sales_group).strip(), str(sales_group).strip())

        return {
            **standardized,
            "_hash": hash((
                standardized['ASIN'],
                standardized['优惠券名称'],
                standardized['店铺'],
                standardized['站点']
            )),
            "salesman_id": user_id.strip(),
            "sales_group": sales_group
        }

    existing_hashes = set()
    for record in old_list:
        try:
            norm = _normalize(record)
            existing_hashes.add(norm["_hash"])
        except Exception as e:
            print(f"旧数据处理异常: {str(e)}")
            continue

    unique_records = []
    duplicate_records = []

    for record in new_list:
        try:
            norm = _normalize(record)
            output = {
                "ASIN": norm["ASIN"],
                "优惠券名称": norm["优惠券名称"],
                "店铺": norm["店铺"],
                "站点": norm["站点"],
                "销售人员": [{"id": norm["salesman_id"]}] if norm["salesman_id"] else [],
                "销售小组": norm["sales_group"]
            }

            if norm["_hash"] not in existing_hashes:
                unique_records.append(output)
            else:
                duplicate_records.append(output)

        except Exception as e:
            print(f"新数据处理异常: {str(e)}")
            continue

    return unique_records, duplicate_records


# from typing import *
#
# try:
#     from xbot.app.logging import trace as print
# except:
#     from xbot import print


def compare_and_filter_lists(list1: list, list2: list) -> list:
    """
    title: 列表比对过滤
    description: 根据指定字段比对两个列表，过滤出`%list1%`中独有的记录，并重新格式化输出
    inputs:
        - list1 (list): 主列表, eg: [{"fields":{"ASIN":"123"}}]
        - list2 (list): 对比列表, eg: [{"fields":{"ASIN":"456"}}]
    outputs:
        - result (list): 过滤结果, eg: [{"ASIN":"123"}]
    """

    def _extract_key_fields(item):
        fields = item.get('fields', {})
        return (
            fields.get('促销码信息'),
            fields.get('店铺'),
            fields.get('亚马逊商城(站点)'),
            fields.get('ASIN')
        )

    def _process_sales_info(fields):
        sales_users = fields.get('销售人员', {}).get('users', [])
        sales_people = [{'id': user.get('id')} for user in sales_users]

        sales_group = fields.get('销售小组名称', [])
        sales_group_value = sales_group[0]["text"] if isinstance(sales_group, list) and sales_group else None

        return sales_people, sales_group_value

    # 构建list2的键集合
    set2_keys = {_extract_key_fields(item) for item in list2}



    # 生成不重复的条目
    result = []
    for item in list1:
        fields = item.get('fields', {})
        key = _extract_key_fields(item)

        if key not in set2_keys:
            sales_people, sales_group_value = _process_sales_info(fields)

            new_entry = {
                'ASIN': key[3],
                '促销码信息': key[0],
                '店铺': key[1],
                '亚马逊商城(站点)': key[2],
                '销售人员': sales_people,
                '销售小组': sales_group_value
            }
            result.append(new_entry)

    return result
