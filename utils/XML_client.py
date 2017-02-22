# !/usr/bin/python
# -*- coding=utf-8 -*-

import unittest
from xml.etree.ElementTree import ElementTree, Element
import xml.etree.ElementTree as ET


def read_xml(in_path):
    '''''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree


def write_xml(tree, out_path):
    '''''将xml文件写出
       tree: xml树
       out_path: 写出路径'''
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def if_match(node, kv_map):
    '''''判断某个节点是否包含所有传入参数属性
       node: 节点
       kv_map: 属性及属性值组成的map'''
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True


# ---------------search -----

def find_nodes(tree, path):
    '''''查找某个路径匹配的所有节点
       tree: xml树
       path: 节点路径'''
    return tree.findall(path)


def get_node_by_keyvalue(nodelist, kv_map):
    '''''根据属性及属性值定位符合的节点，返回节点
       nodelist: 节点列表
       kv_map: 匹配属性及属性值map'''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


# ---------------change -----

def change_node_properties(nodelist, kv_map, is_delete=False):
    '''''修改/增加 /删除 节点的属性及属性值
       nodelist: 节点列表
       kv_map:属性及属性值map'''
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))


def change_node_text(nodelist, text, is_add=False, is_delete=False):
    '''''改变/增加/删除一个节点的文本
       nodelist:节点列表
       text : 更新后的文本'''
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text


def create_node(tag, property_map, content):
    '''''新造一个节点
       tag:节点标签
       property_map:属性及属性值map
       content: 节点闭合标签里的文本内容
       return 新节点'''
    element = Element(tag, property_map)
    element.text = content
    return element


def add_child_node(nodelist, element):
    '''''给一个节点添加子节点
       nodelist: 节点列表
       element: 子节点'''
    for node in nodelist:
        node.append(element)


def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    '''''同过属性及属性值定位一个节点，并删除之
       nodelist: 父节点列表
       tag:子节点标签
       kv_map: 属性及属性值列表'''
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)


def del_xml_configuration(file_obj, change_dic, new_dic):
    """

    :param file_obj: file obj
    :param change: dic
    :param new: dic
    :return:
    """
    # tree = ElementTree()
    Tree = ET.ElementTree(file=file_obj)
    root = Tree.getroot()
    change_lis = []
    circle_change(change_dic, '', change_lis)
    for change in change_lis:
        # print change_dic,type(change_dic)
        for index, attrib_dic in change.items():
            a = find_nodes(root, index)
            change_node_properties(a, attrib_dic)
            # print a, attrib_dic
    circle_find_list(new_dic, root)

    return Tree


# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)

def circle_find_list(objs, root):
    if isinstance(objs, dict):
        for k, v in objs.items():
            new_tree = root.find(k)
            circle_find_list(v, new_tree)
    if isinstance(objs, list):
        print root.tag
        root.clear()
        for obj in objs:
            for k in obj:
                v = obj[k]
                new_e = create_node(k, v, "what")
                root.append(new_e)



def circle_change(obj, s, result_lis):
    if not isinstance(obj, dict):
        # print s,obj
        aa = s.split('/')[1:-1]
        b = s.split('/')[-1]
        # print aa
        m = ''
        for a in aa:
            m = m + '/' + a
        result_lis.append({m[1:]: {b: obj}})
    else:
        for k, v in obj.items():
            # print s
            m = s + '/' + k
            circle_change(v, m, result_lis)


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level + 1)
            if not e.tail or not e.tail.strip():
                e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem


if __name__ == '__main__':
    # unittest.main()
    # 1. 读取xml文件
    tree = read_xml("./test.xml")
    print type(tree)
    # 2. 属性修改
    # A. 找到父节点
    nodes = find_nodes(tree, "processers/processer")
    # print nodes
    # B. 通过属性准确定位子节点
    result_nodes = get_node_by_keyvalue(nodes, {"name": "BProcesser"})
    # C. 修改节点属性
    change_node_properties(result_nodes, {"age": "1"})
    # D. 删除节点属性
    change_node_properties(result_nodes, {"value": ""}, True)

    # 3. 节点修改
    # A.新建节点
    a = create_node("person", {"age": "15", "money": "200000"}, "this is the firest content")
    # B.插入到父节点之下
    add_child_node(result_nodes, a)

    # 4. 删除节点
    # 定位父节点
    del_parent_nodes = find_nodes(tree, "processers/services/service")
    # 准确定位子节点并删除之
    target_del_node = del_node_by_tagkeyvalue(del_parent_nodes, "chain", {"sequency": "chain1"})

    # 5. 修改节点文本
    # 定位节点
    text_nodes = get_node_by_keyvalue(find_nodes(tree, "processers/services/service/chain"), {"sequency": "chain3"})
    change_node_text(text_nodes, "new text")

    # 6. 输出到结果文件
    write_xml(tree, "./out.xml")
