# Copied from botocore, licensed under the Apache licence 2.0.
# Copyright 2012-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

import re

_xform_cache = {
    ('CreateCachediSCSIVolume', '_'): 'create_cached_iscsi_volume',
    ('CreateCachediSCSIVolume', '-'): 'create-cached-iscsi-volume',
    ('DescribeCachediSCSIVolumes', '_'): 'describe_cached_iscsi_volumes',
    ('DescribeCachediSCSIVolumes', '-'): 'describe-cached-iscsi-volumes',
    ('DescribeStorediSCSIVolumes', '_'): 'describe_stored_iscsi_volumes',
    ('DescribeStorediSCSIVolumes', '-'): 'describe-stored-iscsi-volumes',
    ('CreateStorediSCSIVolume', '_'): 'create_stored_iscsi_volume',
    ('CreateStorediSCSIVolume', '-'): 'create-stored-iscsi-volume',
    ('ListHITsForQualificationType', '_'): 'list_hits_for_qualification_type',
    ('ListHITsForQualificationType', '-'): 'list-hits-for-qualification-type',
}

_partial_renames = {'ipv-6': 'ipv6', 'ipv_6': 'ipv6', 's_3_resources': 's3_resources', 's-3-resources': 's3-resources'}

_special_case_transform = re.compile('[A-Z]{3,}s$')
_first_cap_regex = re.compile('(.)([A-Z][a-z]+)')
_number_cap_regex = re.compile('([a-z])([0-9]+)')
_end_cap_regex = re.compile('([a-z0-9])([A-Z])')


def xform_name(name, sep='_', _xform_cache=_xform_cache, partial_renames=_partial_renames):
    """Convert camel case to a "pythonic" name.

    If the name contains the ``sep`` character, then it is
    returned unchanged.

    """
    if sep in name:
        # If the sep is in the name, assume that it's already
        # transformed and return the string unchanged.
        return name
    key = (name, sep)
    if key not in _xform_cache:
        if _special_case_transform.search(name) is not None:
            is_special = _special_case_transform.search(name)
            matched = is_special.group()
            # Replace something like ARNs, ACLs with _arns, _acls.
            name = name[: -len(matched)] + sep + matched.lower()
        s1 = _first_cap_regex.sub(r'\1' + sep + r'\2', name)
        s2 = _number_cap_regex.sub(r'\1' + sep + r'\2', s1)
        transformed = _end_cap_regex.sub(r'\1' + sep + r'\2', s2).lower()

        # Do partial renames
        for old, new in partial_renames.items():
            if old in transformed:
                transformed = transformed.replace(old, new)
        _xform_cache[key] = transformed
    return _xform_cache[key]
