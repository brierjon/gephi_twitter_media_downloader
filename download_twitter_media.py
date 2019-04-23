import os
import tweepy
import credentials
import csv
from functions import get_entities, item_retrieve, if_no_dir_make
from settings import media_filter
import glob
import sys
import datetime as dt
import argparse

def main():
    parser = argparse.ArgumentParser(description='Twitter Media Downloader: A basic script for downloading embedded'
                                                 'media from Tweets. Takes a csv of tweet ids or an export of the data'
                                                 'table generated by the Gephi Twitter-Steamining-Importer Plugin.')

    parser.add_argument('-G', '--Gephi', action='store_true', default=False,
                        help='Use if your .csv was generated by Gephi', required=False)
    parser.add_argument('-c', '--column', default=None, help='Name of the column containing the tweet ids.', )
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Use to output a full report including tweets without associated media', required=False)
    parser.add_argument('-nV', '--NoVideo', action='store_false', default=True)
    parser.add_argument('-nP', '--NoPhoto', action='store_false', default=True)
    parser.add_argument('-nA', '--NoAnimatedGif', action='store_false', default=True)
    args = vars(parser.parse_args())

    media_filter['animated_gif'] = args['NoAnimatedGif']
    media_filter['photo'] = args['NoPhoto']
    media_filter['video'] = args['NoVideo']


    if not args['Gephi']:
        if args['column'] is None:
            sys.exit('Please provide a column name using the argument -c')

    print('**** Welcome to the Gephi/Twitter Media Downloader ****')

    if credentials.CONSUMER_KEY == '' or credentials.CONSUMER_SECRET == '':

        print('We will need your Twitter API Consumer Key and Consumer Secret to continue...')
        print('To avoid this prompt in the future please edit the "credentials.py" file.')
        CONSUMER_KEY = input('Please paste your Consumer Key here and press enter: ')
        CONSUMER_SECRET = input('Please paste your Consumer Secret here and press enter: ')
    else:
        CONSUMER_KEY = credentials.CONSUMER_KEY
        CONSUMER_SECRET = credentials.CONSUMER_SECRET

    print('Establishing folders...')
    if_no_dir_make(os.path.join('media', 'video'))
    if_no_dir_make(os.path.join('media', 'photo'))
    if_no_dir_make(os.path.join('media', 'animated_gif'))
    if_no_dir_make('reports')

    if args['Gephi']:

        print ('[*] Please ensure your Gephi export .csv file is in the same folder as this script')
        if input('[*] When ready enter "y"...').lower() == 'y':
            # Read in data from Gephi export and build list of tweet_ids with a parallel list of indexes.
            indexes = []
            tweet_ids = []

            print('[*] Loading your Gephi Export...')
            file_list = glob.glob('*.csv')

            if len(file_list) == 0:
                sys.exit('[!] No file found...Quitting')
        else:
            sys.exit('Quitting...')

    else:
        if args['column'] is not None:
            print(f"[*] Please ensure your .csv file is in the same folder as this script and that the column "
                  f"containing the tweet ids is named {args['column']}.")
            if input('[*] When ready enter "y"...').lower() == 'y':
                # Read in data from .csv and build list of tweet_ids with a parallel list of indexes.
                indexes = []
                tweet_ids = []

                print('[*] Loading your .CSV file...')
                file_list = glob.glob('*.csv')

                if len(file_list) == 0:
                    sys.exit('[!] No file found...Quitting')
            else:
                sys.exit('Quitting...')

    print('.csv file found')
    print(f'The script will now load {file_list[0]}')
    if input('Continue?...y/n').lower() != 'y':
        sys.exit('Quitting')

    with open(file_list[0], mode='r', encoding='utf-8-sig') as f:
        csv_reader = csv.DictReader(f)

        if args['Gephi']:
            for i, row in enumerate(csv_reader):
                if row['twitter_type'] == 'Tweet':
                    indexes.append(i)
                    tweet_ids.append(row['Id'])
        else:
            for i, row in enumerate(csv_reader):
                indexes.append(i)
                tweet_ids.append(row[args['column']])
    print(f'Located {len(indexes)} tweet ids in {file_list[0]}')

    # Establish Twitter API connection
    print('Establishing API Link...')
    try:
        auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except tweepy.TweepError:
        print('Error establishing API...')
        print(f'Is your CONSUMER_KEY correct?: {CONSUMER_KEY}')
        print(f'Is your CONSUMER_SECRET correct?: {CONSUMER_SECRET}')
        sys.exit('Quitting')

    # Iterate over the Ids check for the presence of media and generate a data dictionary of urls and meta_data
        # for reporting and media retrieval.

    print('Checking for media...')
    report_data = []
    for i, _id in enumerate(tweet_ids):
        if i % 10 == 0:
            print(f'Checked {i} of {len(tweet_ids)} tweets...')
        try:
            data = api.get_status(_id, include_entities=True)._json

            data_dict = get_entities(data, _id)
            data_dict['original_row'] = indexes[i] +2
            data_dict['tweet_url'] = f'https://twitter.com/statuses/{str(_id)}'
            data_dict['user'] = data['user']['screen_name']
            report_data.append(data_dict)

        except tweepy.TweepError as e:
            report_data.append({'message': e, 'original_row': indexes[i]+2, 'tweet_id': _id})
            continue

    num_media = len([x for x in report_data if 'medium' in x])
    print(f'Retrieved meta-data for {num_media} media items...')

    print('Retrieving Media items...')
    # Retrieve media items
    for row in report_data:
        if 'medium' in row:
            item_retrieve(row)
    now_str = dt.datetime.today().strftime('%Y-%m-%d')
    report_name = f'{file_list[0][:-4]}_{now_str}_report.csv'
    print(f'Writing Report: {report_name} to the "reports" folder')
    # Write report
    with open(os.path.join('reports',report_name), mode='w') as csv_file:
        fieldnames = ['original_row','tweet_id','tweet_url','bitrate','type',
                      'medium','media_url','media_file','user','message']
        writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writeheader()

        if not args['verbose']:
            report_data = [x for x in report_data if ('medium' in x) and (x['media_url'] != 'N/A')]
        for report in report_data:
            writer.writerow(report)
    print(f'Job Complete. Check the "media" folder for your files. Have a nice day!')


if __name__ == '__main__':
    main()
