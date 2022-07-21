import xlsxwriter


def create_excel(workbook_name: str, worksheet_name: str, headers_list: list, data: list, thresh=0.5):

    """Creates Excel file from scraped data. If savings are above threshold - row gets colored green"""

    workbook = xlsxwriter.Workbook(workbook_name + '.xlsx')
    worksheet = workbook.add_worksheet(worksheet_name)
    bold = workbook.add_format({'bold': True})
    green_bg = workbook.add_format({'bg_color': '#6AA121', 'border': 1})
    for i, h in enumerate(headers_list):
        worksheet.write(0, i, str(h).capitalize(), bold)

    for index1, e in enumerate(data):
        for index2, h in enumerate(headers_list):
            savings = e.get('oszczędność')
            reference = e.get('stara cena')
            if isinstance(reference, float) and not isinstance(savings, float):
                threshold = reference * thresh
            elif isinstance(savings, float) and isinstance(reference, float) and savings > threshold:
                worksheet.write(index1 + 1, index2, e[h], green_bg)
            else:
                worksheet.write(index1 + 1, index2, e[h])
            worksheet.autofilter('A1:P1')

    workbook.close()
