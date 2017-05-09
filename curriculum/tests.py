# -*- coding: utf-8 -*-

import logging
import xml.dom.minidom

dom = xml.dom.minidom.parse('../chisch/curriculun_categorys/internet.xml')

root = dom.documentElement

first_level_type_nodes = dom.getElementsByTagName('first_level_type')

for first_level_type_node in first_level_type_nodes:
    node_id = first_level_type_node.getAttribute('id')
    node_value = first_level_type_node.getAttribute('value')

