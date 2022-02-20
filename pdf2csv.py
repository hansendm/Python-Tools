import tabula
import camelot

# Method 1
filename = input("Enter File Path: ")
df = tabula.read_pdf(filename, encoding='utf-8', spreadsheet=True, pages='1')
df.to_csv('output.csv')

# Method 2
tables = camelot.read_pdf('file.pdf')
tables.export('file.csv', f='csv', compress=True)
