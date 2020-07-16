#!/usr/bin/env python

__author__ = "Ruben Espino"

from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://indianapolis.craigslist.org/search/sof"
sof_jobs = {}  # Software Jobs
job_no = 0

while True:

    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    jobs = soup.find_all('p', {'class': 'result-info'})

    for job in jobs:
        title = job.find('a', {'class': 'result-title'}).text
        location_tag = job.find('span', {'class': 'result-hood'})
        location = location_tag.text[2:-1] if location_tag else 'N/A'
        date = job.find('time', {'class': 'result-date'}).text
        link = job.find('a', {'class': 'result-title'}).get('href')
        job_response = requests.get(link)
        job_data = job_response.text
        job_soup = BeautifulSoup(job_data, 'html.parser')
        job_description = job_soup.find('section', {'id': 'postingbody'}).text
        job_attribute_tag = job_soup.find('p', {'class': 'attrgroup'})
        job_attributes = job_attribute_tag.text if job_attribute_tag else 'N/A'

        job_no += 1
        sof_jobs[job_no] = [
            title, location, date, link, job_attributes, job_description
            ]
        # print(
        #     f'Job Title: {title}'
        #     f'\nLocation: {location}'
        #     f'\nDate: {date}'
        #     f'\nLink: {link}'
        #     f'\n{job_attributes}'
        #     f'\nJob Description {job_description}'
        #     f'\n---'
        #     )

    url_tag = soup.find('a', {'title': 'next page'})

    if url_tag.get('href'):
        url = 'https://indianapolis.craigslist.org' + url_tag.get('href')
        print(url)
    else:
        break
print('Total Jobs: ', job_no)

sof_jobs_df = pd.DataFrame.from_dict(
    sof_jobs,
    orient='index',
    columns=[
        'Job Title',
        'Location',
        'Date',
        'Link',
        'Job Attributes',
        'Job Description'
        ])
sof_jobs_df.head()
sof_jobs_df.to_csv('jobs.csv')
