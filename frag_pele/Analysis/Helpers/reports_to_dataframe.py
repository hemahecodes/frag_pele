import re
import pandas as pd


def report_to_df(report_list):
    """
        This function merge the content of different report for PELE simulations in a single file pandas Data Frame.
    """
    data = []
    for report in report_list:
        tmp_data = pd.read_csv(report, sep='    ', engine='python')
        tmp_data = tmp_data.iloc[1:]  # We must discard the first row
        processor = re.findall('\d+$', report)
        tmp_data['Processor'] = processor[0]
        data.append(tmp_data)
    result = pd.concat(data)
    return result

