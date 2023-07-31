import re

def replace_rp_string(input_string):
    # Remove 'Rp' and ',' characters using regular expressions
    cleaned_string = re.sub(r'Rp|,', '', input_string)

    # Convert to an integer and then format the number with thousand separators
    formatted_number = '{:,}'.format(int(cleaned_string))

    return formatted_number


input_string = 'Rp\xa01,500,000,00'
result = replace_rp_string(input_string)
print(result)  # Output: 1.500.000
