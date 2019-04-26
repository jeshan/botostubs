import keyword

import boto3

import pythonic


def get_method_signature(service_model, operation_name, shapes, class_name):
    pythonic_op_name = pythonic.xform_name(operation_name)
    operation_model = service_model.operation_model(operation_name)
    input_shape = operation_model.input_shape
    output_shape = operation_model.output_shape
    parameters = input_shape.members if input_shape else {}

    primitive_map = {
        'string': 'str',
        'integer': 'int'
    }

    if input_shape:
        append_to_shapes(input_shape, class_name, shapes)
    if output_shape:
        append_to_shapes(output_shape, class_name, shapes)

    param_list = get_param_list(input_shape, parameters, primitive_map, shapes, class_name)

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


def get_param_list(input_shape, parameters, primitive_map, shapes, class_name):
    param_list = ['self']
    for name, param in parameters.items():
        item = get_param_name(input_shape, name, param, primitive_map, shapes, class_name)
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


def get_param_name(shape, name, param, primitive_map, shapes, class_name):
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


def get_class_signature(name, documentation, methods, shapes_in_classes):
    method_str = '\n\n'.join(methods)
    shape_str = []

    for shape_class in shapes_in_classes:
        if shape_class[1] != name:
            continue
        params = ''
        shape_begin = 'pass'
        base_type = 'Mapping' if shape_class[0].type_name == 'structure' else 'object'
        shape_str.append(f"""    class {shape_class[0].name}({base_type}):
        {shape_begin}{params}
""")

    shape_str = '\n'.join(shape_str)
    doc_str = f'    """{documentation}"""'.replace('<p>', '').replace('</p>', '')

    return f"""class {name}(BaseClient):
{doc_str}

{shape_str}
{method_str}

"""


def get_class_output(client_name):
    method_signatures = []
    shapes_in_classes = []
    client = boto3.client(client_name)
    class_name = type(client).__name__
    service_model = client._service_model
    for name in service_model.operation_names:
        method_signatures.append(get_method_signature(service_model, name, shapes_in_classes, class_name))
    return get_class_signature(class_name, service_model.documentation, method_signatures, shapes_in_classes)


if __name__ == '__main__':

    print('from collections.abc import Mapping')
    print('from typing import List')
    print('from botocore.client import BaseClient\n\n')

    boto3.setup_default_session()
    for client_name in boto3.DEFAULT_SESSION.get_available_services():
        print(get_class_output(client_name))
