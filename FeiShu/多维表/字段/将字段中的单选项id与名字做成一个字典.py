from typing import *

try:
    from xbot.app.logging import trace as print
except:
    from xbot import print


def extract_option_mapping(fields_data, target_field_name):
    """
    title: 从字段数据中提取选项映射
    description: 从字段数据列表中提取指定字段的选项，并生成ID到名称的映射字典。
    inputs:
        - fields_data (list): 字段数据列表，eg: [{"field_name": "销售小组", "property": {"options": [...]}}]
        - target_field_name (str): 目标字段名称，eg: "销售小组"
    outputs:
        - id_name_map (dict): ID到名称的映射字典，eg: {"opt_123": "北京组"}
    """

    # 提取目标字段的 options 并生成映射字典
    target_field = next(
        (field for field in fields_data if field["field_name"] == target_field_name),
        None
    )

    if target_field and "options" in target_field["property"]:
        id_name_map = {opt["id"]: opt["name"] for opt in target_field["property"]["options"]}
        print(f"生成的映射字典: {id_name_map}")
        return id_name_map
    else:
        print(f"字段 '{target_field_name}' 未找到或没有 options 属性！")
        return {}
