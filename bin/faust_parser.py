
def clean_faust_result(path='faust_results.csv', out='faust_results_dots.csv'):
    """
    Helper script to convert commas in strings
     to dots
    :return:
    """
    import csv
    fr = open(path, 'rb')
    csv_reader = csv.reader(fr)
    f_out = open(out, 'wb')
    csv_writer = csv.writer(f_out)
    for row in csv_reader:
        clean_row = [val.replace(',','.') for val in row]
        csv_writer.writerow(clean_row)
    f_out.close()
    fr.close()



