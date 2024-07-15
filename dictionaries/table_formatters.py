#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#------------------#
# Define functions #
#------------------#

def format_table(nested_dict, keys=None, display_index=True, index_header='Index'):
    """
    Format a nested dictionary into a table string with specific formatting rules.
    
    Note
    ----
    The keys in every subdictionary must represent a value in a generic scope.
    For example, use {'flora': 'grass', 'fruit': 'apple'} 
    instead of {'grass': 'green', 'apple': 'red'}
    to avoid long headers and ensure a clean table format.
    
    If the `keys` argument is None, the keys of the first subdictionary
    in the nested dictionary will be used as the column names. 
    This is to avoid long headers and maintain a consistent table structure.
    However, if the subdictionaries contain specific keys, this mechanism 
    will cause those specific keys to be lost in favour of the generic keys 
    from the first subdictionary.
    
    The key list corresponding to every subdictionary must be of the same length,
    otherwise a ValueError is raised.
    A tip to avoid this error would be to set the value to None for any of the keys, 
    if that key is not going to be used.

    Parameters
    ----------
    nested_dict : dict of dict
        A nested dictionary to format.
    keys : list of str, optional
        An optional list of keys to use as column names.
    display_index : bool, optional
        Whether to display the index column. Default is True.
    index_header : str, optional
        If display_index= True, use this name for the column that contains indices.
        Default name is 'Index'.
    
    Raises
    ------
    ValueError
        If subdictionaries have different lengths or if the keys list length does not match.
    
    Returns
    -------
    table : str
        The formatted table string.
    """
    if not nested_dict:
        raise ValueError("The nested dictionary is empty.")
    
    # Ensure all subdictionaries are of the same length
    first_len = len(next(iter(nested_dict.values())))
    if not all(len(subdict) == first_len for subdict in nested_dict.values()):
        raise ValueError("All subdictionaries in the nested dictionary must be of the same length.")
    
    # Use the keys from the first subdictionary if not provided
    if keys is None:
        keys = list(next(iter(nested_dict.values())).keys())
    else:
        # Ensure the provided keys list length matches the subdictionaries' keys length
        if len(keys) != first_len:
            raise ValueError("The length of the keys list must match the length of the subdictionaries' keys.")
    
    # Calculate max width for each column
    column_widths = {key: len(key) for key in keys}
    for subdict in nested_dict.values():
        for idx, key in enumerate(keys):
            original_key = list(subdict.keys())[idx]
            value = subdict.get(original_key, "")
            column_widths[key] = max(column_widths[key], len(str(value)))

    # Create the header row
    if display_index:
        max_index_width = max(len(str(idx)) for idx in nested_dict.keys())
        column_widths[index_header] = max(len(index_header), max_index_width)
        headers = [index_header] + keys
    else:
        headers = keys
    
    # Build the header string
    header_row = '|' + '|'.join(f"{header:^{column_widths[header]}}" for header in headers) + '|'
    
    # Build the header underline string
    underline_row = '|' + '|'.join('=' * column_widths[header] for header in headers) + '|'
    
    # Build the content rows
    content_rows = []
    for idx, subdict in nested_dict.items():
        if display_index:
            row = [f"{idx:^{column_widths[index_header]}}"]
        else:
            row = []
        for key in keys:
            original_key = list(subdict.keys())[keys.index(key)]
            value = subdict.get(original_key, "")
            row.append(f"{str(value):^{column_widths[key]}}")
        content_rows.append('|' + '|'.join(row) + '|')
    
    # Combine all parts
    table = '\n'.join([header_row, underline_row] + content_rows)
    return table

# # Example usage
# nested_dict = {
#     1: {'key1': 'val11', 'key2': 'val12'},
#     2: {'key1': 'val21', 'key2': 'val22'},
#     3: {'key1': 'val31', 'key2': 'val32'}
# }

# # Print the table with the index
# print(format_table(nested_dict, display_index=True))

# # Print the table without the index
# print(format_table(nested_dict, display_index=False))

# # Print the table with custom headers
# custom_keys = ['Column1', 'Column2']
# print(format_table(nested_dict, keys=custom_keys, display_index=True))


def format_table_from_list(dict_list,
                           keys=None,
                           display_index=True,
                           index_header='Index'):
    """
    Format a list of dictionaries into a table string with specific formatting rules.
    
    Note
    ----
    The keys in every dictionary must represent a value in a generic scope.
    For example, use {'flora': 'grass', 'fruit': 'apple'}
    instead of {'grass': 'green', 'apple': 'red'}
    to avoid long headers and ensure a clean table format.
    
    If the `keys` argument is None, the keys of the first dictionary in the list
    will be used as the column names.
    This is to avoid long headers and maintain a consistent table structure.
    However, if the dictionaries contain specific keys, this mechanism will cause
    those specific keys to be lost in favour of the generic keys from the
    first dictionary.
    
    The key list corresponding to every dictionary must be of the same length,
    otherwise a ValueError is raised.
    A tip to avoid this error would be to set the value to None for any of the keys, 
    if that key is not going to be used.

    Parameters
    ----------
    dict_list : list of dict
        A list of dictionaries to format.
    keys : list of str, optional
        An optional list of keys to use as column names.
    display_index : bool, optional
        Whether to display the index column. Default is True.
    index_header : str, optional
        If display_index= True, use this name for the column that contains indices.
        Default name is 'Index'.
        
    
    Raises
    ------
    ValueError
        If dictionaries have different lengths or if the keys list length does not match.
    
    Returns
    -------
    table : str
        The formatted table string.
    """
    if not dict_list:
        raise ValueError("The dictionary list is empty.")
    
    # Ensure all dictionaries are of the same length
    first_len = len(dict_list[0])
    if not all(len(d) == first_len for d in dict_list):
        raise ValueError("All dictionaries in the list must be of the same length.")
    
    # Use the keys from the first dictionary if not provided
    if keys is None:
        keys = list(dict_list[0].keys())
    else:
        # Ensure the provided keys list length matches the dictionaries' keys length
        if len(keys) != first_len:
            raise ValueError("The length of the keys list must match the length of the dictionaries' keys.")
    
    # Calculate max width for each column
    column_widths = {key: len(key) for key in keys}
    for subdict in dict_list:
        for idx, key in enumerate(keys):
            original_key = list(subdict.keys())[idx]
            value = subdict.get(original_key, "")
            column_widths[key] = max(column_widths[key], len(str(value)))

    # Create the header row
    if display_index:
        max_index_width = max(len(str(idx)) for idx in range(1, len(dict_list) + 1))
        column_widths[index_header] = max(len(index_header), max_index_width)
        headers = [index_header] + keys
    else:
        headers = keys
    
    # Build the header string
    header_row = '|' + '|'.join(f"{header:^{column_widths[header]}}" for header in headers) + '|'
    
    # Build the header underline string
    underline_row = '|' + '|'.join('=' * column_widths[header] for header in headers) + '|'
    
    # Build the content rows
    content_rows = []
    for idx, subdict in enumerate(dict_list, start=1):
        if display_index:
            row = [f"{idx:^{column_widths[index_header]}}"]
        else:
            row = []
        for key in keys:
            original_key = list(subdict.keys())[keys.index(key)]
            value = subdict.get(original_key, "")
            row.append(f"{str(value):^{column_widths[key]}}")
        content_rows.append('|' + '|'.join(row) + '|')
    
    # Combine all parts
    table = '\n'.join([header_row, underline_row] + content_rows)
    return table

# # Example usage
# dict_list = [
#     {'key1': 'val11', 'key2': 'val12'},
#     {'key1': 'val21', 'key2': 'val22'},
#     {'key1': 'val31', 'key2': 'val32'}
# ]

# # dict_list = [
# #     {'bayern': 'alemania', 'leipzig': 'alemania'},
# #     {'olaizola': 'aimar', 'irujo': 'juan'},
# #     {'ziskar II': 'karlos', 'lujan': 'vladimir'}
# # ]

# # Print the table with the index
# print(format_table_from_list(dict_list, display_index=True))
# print(2*"\n")

# # Print the table without the index
# print(format_table_from_list(dict_list, display_index=False))
# print(2*"\n")

# # Print the table with custom headers
# custom_keys = ['Futbola', 'Esku pilota edo pala']
# print(format_table_from_list(dict_list, keys=custom_keys, display_index=True))



def format_table_from_lists(keys, values, display_index=True, index_header='Index'):
    """
    Format two lists into a table string with specific formatting rules.
    
    Note
    ----
    If specific values are given in the `keys` list, the header may be long,
    and no key filtering is performed as in other methods.

    Parameters
    ----------
    keys : list of str
        A list of keys to use as column names.
    values : list
        A list of values corresponding to each key.
    display_index : bool, optional
        Whether to display the index column. Default is True.
    index_header : str, optional
        If display_index= True, use this name for the column that contains indices.
        Default name is 'Index'.
    
    Raises
    ------
    ValueError
        If the length of `keys` does not match the length of `values`.
    
    Returns
    -------
    table : str
        The formatted table string.
    """
    if len(keys) != len(values):
        raise ValueError("The length of keys and values lists must be the same.")
    
    # Calculate max width for each column
    column_widths = {key: len(key) for key in keys}
    for key, value in zip(keys, values):
        column_widths[key] = max(column_widths[key], len(str(value)))

    # Create the header row
    if display_index:
        max_index_width = len(str(len(values)))
        column_widths[index_header] = max(len(index_header), max_index_width)
        headers = [index_header] + keys
    else:
        headers = keys
    
    # Build the header string
    header_row = '|' + '|'.join(f"{header:^{column_widths[header]}}" for header in headers) + '|'
    
    # Build the header underline string
    underline_row = '|' + '|'.join('=' * column_widths[header] for header in headers) + '|'
    
    # Build the content rows
    content_rows = []
    for idx, value in enumerate(values, start=1):
        if display_index:
            row = [f"{idx:^{column_widths[index_header]}}"]
        else:
            row = []
        for key in keys:
            row.append(f"{str(value):^{column_widths[key]}}")
        content_rows.append('|' + '|'.join(row) + '|')
    
    # Combine all parts
    table = '\n'.join([header_row, underline_row] + content_rows)
    return table

# # Example usage
# keys = ['Key1', 'Key2', 'Key3']
# values = ['Value1', 'Value2', 'Value3']

# # Print the table with the index
# print(format_table_from_lists(keys, values, display_index=True))
# print(2*"\n")

# # Print the table without the index
# print(format_table_from_lists(keys, values, display_index=False))