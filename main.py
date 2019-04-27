import keyword

import boto3
import botocore
from botocore.waiter import WaiterModel
import inspect

import pythonic

primitive_map = {
    'string': 'str',
    'integer': 'int'
}  # TODO: add more


def get_method_signature(service_model, operation_name, shapes, class_name):
    pythonic_op_name = pythonic.xform_name(operation_name)
    operation_model = service_model.operation_model(operation_name)
    input_shape = operation_model.input_shape
    output_shape = operation_model.output_shape
    parameters = input_shape.members if input_shape else {}

    if input_shape:
        append_to_shapes(input_shape, class_name, shapes)
    if output_shape:
        append_to_shapes(output_shape, class_name, shapes)

    param_list = get_param_list(input_shape, parameters, shapes, class_name)

    param_str = ', '.join(param_list)

    operation_doc = operation_model.documentation.replace('<p>', '').replace('</p>', '')
    docstr = f'"""{operation_doc}\n'
    append_return_type = ' -> ' + output_shape.name if output_shape else ''
    rest_params = f":param {get_doc_str(input_shape)}"

    return f"""    def {pythonic_op_name}({param_str}){append_return_type}:
        {docstr}
        :param self:
        {rest_params}
        :return: {get_doc_str(output_shape)}        \"\"\"
        pass"""


def get_doc_str(shape, prefix='', level=1):
    docstr = ''
    if not shape or not hasattr(shape, 'members') or not shape.members.items():
        return docstr
    if level > 3:
        return
    indent = "&nbsp;&nbsp;&nbsp;&nbsp;" * level
    for param_key, param_value in shape.members.items():
        doc = param_value.documentation.replace('"""', 'triple-quotes').replace('<p>', '').replace('</p>', '')
        if hasattr(param_value, 'members'):
            if level == 1:
                doc += ':'
            if level > 1:
                doc += f"""{indent}<b>{param_key}</b>: {doc}"""

            sub_result = get_doc_str(param_value, indent, level + 1)
            if not sub_result:
                docstr += doc
                break
            docstr += sub_result
        if level == 1:
            docstr = f"""{param_key}: {prefix} {doc}<br/>{docstr}"""
        else:
            docstr = f"""{prefix} <i>{param_key}</i> {doc}<br/>{docstr}"""
    return docstr


def get_param_list(input_shape, parameters, shapes, class_name):
    param_list = ['self']
    for name, param in parameters.items():
        item = get_param_name(input_shape, name, param, shapes, class_name)
        if name in input_shape.required_members:
            param_list.insert(1, item)
        else:
            param_list.append(item)
    return param_list


def append_to_shapes(shape, class_name, shapes):
    for item in shapes:
        if str(item[0]) == str(shape) and item[1] == class_name:
            return
    shapes.append((shape, class_name))


def get_param_name(shape, name, param, shapes, class_name):
    item = name
    if keyword.iskeyword(name):
        item += '_'
    primitive_name = primitive_map.get(param.type_name)
    if primitive_name:
        item = item + ': ' + primitive_name
    elif param.type_name == 'list':
        item = item + ': List[' + param.member.name + ']'
        append_to_shapes(param.member, class_name, shapes)
    else:
        item = item + ': ' + param.name
        append_to_shapes(param, class_name, shapes)
    if name not in shape.required_members:
        item = item + '=None'  # what if required/optional ones are not in order?
    return item


def get_class_signature(client_name, name, documentation, methods, shapes_in_classes, waiter_model, paginator_model):
    method_str = '\n\n'.join(methods)
    shape_str = get_shape_str(name, shapes_in_classes)
    resource_str = print_resource(client_name)
    doc_str = f'    """{documentation}"""'.replace('<p>', '').replace('</p>', '')
    waiter_str = get_waiter_str(waiter_model)
    paginator_str = get_paginator_str(paginator_model)

    return f"""class {name}(BaseClient):
{doc_str}

{waiter_str}
{paginator_str}
{shape_str}
{method_str}

{resource_str}
"""


def get_shape_str(name, shapes_in_classes):
    shape_str = []

    for shape_class in shapes_in_classes:
        if shape_class[1] != name:
            continue
        base_type = 'Mapping' if shape_class[0].type_name == 'structure' else 'object'
        shape_str.append(f"""    class {shape_class[0].name}({base_type}):
        pass
    """)

    return '\n'.join(shape_str)


def get_waiter_str(waiter_model):
    value = ''
    if not waiter_model:
        return value
    for name in waiter_model.waiter_names:
        waiter = waiter_model.get_waiter(name)
        wait_docstr = f'"""see function `{pythonic.xform_name(waiter.operation)}` for valid parameters"""'
        value += f"""    class {name}Waiter(Waiter):
        def wait(self, **kwargs):
            {wait_docstr}
            pass
"""
    value += '\n'
    return value


def get_paginator_str(paginator_model):
    value = ''
    if not paginator_model:
        return value
    for name, paginator in paginator_model._paginator_config.items():
        wait_docstr = f'"""see function `{pythonic.xform_name(name)}` for valid parameters"""'
        value += f"""    class {name}Paginator(Paginator):
        def wait(self, **kwargs):
            {wait_docstr}
            pass
"""
    value += '\n'
    return value


def print_resource(resource_name):
    result = f'    class {resource_name.title()}Resource:\n'
    try:
        resource = boto3.resource(resource_name)
    except boto3.exceptions.ResourceNotExistsError:
        return ''
    for sub_resource in resource.meta.resource_model.subresources:
        result += print_sub_resource(resource_name, resource, sub_resource)
    result += print_actions(resource.meta.resource_model.actions)
    result += print_collections(resource)
    result += '\n\n'
    return result


def print_sub_waiters(resource):
    waiters = resource.resource.model.waiters
    result = ''
    for waiter in waiters:
        result += f"""            def {waiter.name}(self):
                pass

"""
    return result


def print_collections(resource):
    result = ''
    for collection in resource.meta.resource_model.collections:
        result += f"""        class {collection.resource.type}ResourceCollection(List[dict], ResourceCollection):
            pass

"""
        result += f"""        {collection.name}: {collection.resource.type}ResourceCollection = None
"""
    return result


def print_sub_resource(resource_name, resource, sub_resource):
    def get_shape_str(name, shapes_in_classes):
        shape_str = []

        for shape_class in shapes_in_classes:
            if shape_class[1] != name:
                continue
            base_type = 'Mapping' if shape_class[0].type_name == 'structure' else 'object'
            shape_str.append(f"""            class {shape_class[0].name}({base_type}):
                pass
""")

        return '\n'.join(set(shape_str))

    service_model = resource.meta.client.meta.service_model  # sub_resource.resource.meta.client.meta.service_model
    attr = getattr(resource, sub_resource.name)

    params = []
    shape_classes = []
    for identifier in sub_resource.resource.identifiers:
        params.append(pythonic.xform_name(identifier.target))

    model_shape = sub_resource.resource.model.shape
    attributes_doc = '\n            '
    if model_shape:
        shape = service_model.shape_for(model_shape)
        attributes = resource.meta.resource_model.get_attributes(shape)
        for key, value in attributes.items():
            type_shape = value[1]
            attributes_doc += get_param_name(type_shape, key, type_shape, shape_classes, resource_name) + f"""
            """
    resource_doc = f'"""{inspect.getdoc(attr)}"""'
    params_str = ''
    if len(params):
        params_str = ', ' + ', '.join(params)
    return f"""        
        class {sub_resource.name}:
            {resource_doc}

            def __init__(self{params_str}):
                pass
            
{get_shape_str(resource_name, shape_classes)}        {attributes_doc}
{print_sub_waiters(sub_resource)}{print_sub_actions(sub_resource.resource.model.actions)}
"""


def print_actions(actions):
    result = ''
    for action in actions:
        result += f"""        def {action.name}(self, **kwargs) -> dict:
            pass

"""
    result += f"""        def get_available_subresources(self) -> List[str]:
            pass

"""
    return result


def print_sub_actions(actions):
    result = ''
    for action in actions:
        result += f"""            def {action.name}(self, **kwargs) -> dict:
                return {action.resource.type + '()' if action.resource else '{}'}

"""
    return result


def get_class_output(client_name):
    method_signatures = []
    shapes_in_classes = []
    client = boto3.client(client_name)
    class_name = type(client).__name__
    service_model = client._service_model
    waiter_config = client._get_waiter_config()
    waiter_model = WaiterModel(waiter_config) if 'waiters' in waiter_config else None
    try:
        paginator_model = botocore.session.get_session().get_paginator_model(client_name)
    except botocore.exceptions.UnknownServiceError:
        paginator_model = None # meaning it probably doesn't have paginators
    for name in service_model.operation_names:
        method_signatures.append(get_method_signature(service_model, name, shapes_in_classes, class_name))
    return get_class_signature(client_name, class_name, service_model.documentation, method_signatures,
                               shapes_in_classes, waiter_model, paginator_model)


def print_header():
    print('from collections.abc import Mapping')
    print('from typing import List')
    print('from boto3.resources.collection import ResourceCollection')
    print('from botocore.waiter import Waiter')
    print('from botocore.paginate import Paginator')
    print('from botocore.client import BaseClient\n\n')


def print_clients():
    clients = boto3.DEFAULT_SESSION.get_available_services()
    for client_name in clients:
        print(get_class_output(client_name))


def go():
    print_header()
    boto3.setup_default_session()
    print_clients()


if __name__ == '__main__':
    go()
