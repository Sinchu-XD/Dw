from bs4 import BeautifulSoup

with open('diskwala_download_page.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Get file name
file_name = soup.find_all('p', class_='MuiTypography-body1')
file_name = file_name[0].text if file_name else 'Not found'

# Get file type
file_type = soup.find('span', class_='MuiTypography-caption')
file_type = file_type.text if file_type else 'Not found'

# Get uploader name
uploader = soup.find_all('h6', class_='MuiTypography-h6')
uploader = uploader[1].text.replace("File By: ", "") if len(uploader) > 1 else 'Not found'

print(f"File Name: {file_name}\nFile Type: {file_type}\nUploaded By: {uploader}")
