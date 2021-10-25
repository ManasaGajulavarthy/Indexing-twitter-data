'''
@author: Souvik Das
Institute: University at Buffalo
'''

import demoji, re, datetime
import preprocessor


# demoji.download_codes()


class TWPreprocessor:
    @classmethod
    def preprocess(cls, tweet, type, country=None):
        '''
        Do tweet pre-processing before indexing, make sure all the field data types are in the format as asked in the project doc.
        :param tweet:
        :return: dict
        '''
        tweet_dict = {}
        tweet_dict['id'] = tweet.id_str
            #tweet_dict['country'] = tweet.place['country']
        tweet_dict['country'] = country
        tweet_dict['tweet_lang'] = tweet.lang
        tweet_dict['tweet_text'] = tweet.full_text
        if tweet.lang == 'en':
            tweet_dict['text_en'] = _text_cleaner(tweet.full_text)[0]
        elif tweet.lang == 'hi':
            tweet_dict['text_hi'] = _text_cleaner(tweet.full_text)[0]
        elif tweet.lang == 'es':
            tweet_dict['text_es'] = _text_cleaner(tweet.full_text)[0]
        tweet_dict['tweet_date'] = str(_get_tweet_date(tweet.created_at))
        tweet_dict['verified'] = tweet.user.verified
        if type == "poi":
            tweet_dict['poi_id'] = tweet.user.id
            tweet_dict['poi_name'] = tweet.user.screen_name
        if type == "reply":
            tweet_dict['replied_to_tweet_id'] = tweet.in_reply_to_status_id
            tweet_dict['replied_to_user_id'] = tweet.in_reply_to_user_id
            tweet_dict['reply_text'] = _text_cleaner(tweet.full_text)[0]
        tweet_dict['hashtags'] = _get_entities(tweet,'hashtags')
        tweet_dict['mentions'] = _get_entities(tweet,'mentions')
        tweet_dict['tweet_urls'] = _get_entities(tweet,'urls')
        tweet_dict['tweet_emoticons'] = _text_cleaner(tweet.full_text)[1]
        if tweet.coordinates:
            tweet_dict['geolocation'] = tweet.coordinates['coordinates']
        return tweet_dict

def _get_entities(tweet, type=None):
    result = []
    if type == 'hashtags':
        hashtags = tweet.entities['hashtags']

        for hashtag in hashtags:
            result.append(hashtag['text'])
    elif type == 'mentions':
        mentions = tweet.entities['user_mentions']

        for mention in mentions:
            result.append(mention['screen_name'])
    elif type == 'urls':
        urls = tweet.entities['urls']

        for url in urls:
            result.append(url['url'])

    return result


def _text_cleaner(text):
    emoticons_happy = list([
        ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
        ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
        '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
        'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
        '<3'
    ])
    emoticons_sad = list([
        ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
        ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
        ':c', ':{', '>:\\', ';('
    ])
    all_emoticons = emoticons_happy + emoticons_sad

    emojis = list(demoji.findall(text).keys())
    clean_text = demoji.replace(text, '')

    for emo in all_emoticons:
        if (emo in clean_text):
            clean_text = clean_text.replace(emo, '')
            emojis.append(emo)

    clean_text = preprocessor.clean(text)
    # preprocessor.set_options(preprocessor.OPT.EMOJI, preprocessor.OPT.SMILEY)
    # emojis= preprocessor.parse(text)

    return clean_text, emojis


def _get_tweet_date(tweet_date):
     date_str = datetime.datetime.strftime(tweet_date, '%a %b %d %H:%M:%S +0000 %Y')
     return _hour_rounder(datetime.datetime.strptime(date_str,'%a %b %d %H:%M:%S +0000 %Y'))


def _hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + datetime.timedelta(hours=t.minute // 30))
