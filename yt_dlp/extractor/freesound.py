import re

from .common import InfoExtractor
from ..utils import (
    float_or_none,
    get_element_by_class,
    get_element_by_id,
    unified_strdate,
)


class FreesoundIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?freesound\.org/people/[^/]+/sounds/(?P<id>[^/]+)'
    _TESTS = [
        {
        'url': 'https://www.freesound.org/people/Sami_Hiltunen/sounds/703362/',
        'md5': '8641662d9a184318e5ffa7460f324e52',
        'info_dict': {
            'id': '703362',
            'ext': 'mp3',
            'title': 'Experimental Noise 09 (Remember_Nothing)',
            'description': 'Part of the experimental noise collection, "Buried In The Noise".',
            'duration': 127.383,
            'uploader': 'Sami_Hiltunen',
            'upload_date': '20230923',
            'tags': ['soundscape', 'noise', 'wind', 'experimental'],
        }
    },
        {

        'url': 'http://www.freesound.org/people/miklovan/sounds/194503/',
        'md5': '57bce48a67d93610165d5c323da3f10b',
        'info_dict': {
            'id': '194503',
            'ext': 'mp3',
            'title': 'gulls in the city.wav',
            'description': 'the sounds of seagulls in the city',
            'duration': 130.233,
            'uploader': 'miklovan',
            'upload_date': '20130715',
            'tags': list,
        }
    }]

    def _real_extract(self, url):
        audio_id = self._match_id(url)

        webpage = self._download_webpage(url, audio_id)

        title = self._html_search_regex(
            r'<h1><a class="bw-link--black" href="/people/[^/]+/sounds/\d+/">([^<]+)</a></h1>',
            webpage, 'title')

        description = self._html_search_regex(
            r'<div id="soundDescriptionSection">\s*(<p>.+?</p>\s*)+',
            webpage, 'description', fatal=False)
        description = re.sub('<[^>]+>', '', description).strip()

        duration = float_or_none(
            self._html_search_regex(
                r'data-duration="([^"]+)"', webpage, 'duration'), default=None)

        upload_date = unified_strdate(self._html_search_regex(
            r'<p class="text-grey">([^<]+)</p>', webpage, 'upload date', fatal=False))

        uploader = self._html_search_regex(
            r'<a href="/people/([^/]+)/">', webpage, 'uploader', fatal=False)

        raw_tags = re.findall(
            r'<a href="/browse/tags/[^/]+/"  class="no-hover btn-inverse text-black[^>]*>([^<]+)</a>',
            webpage)
        tags = [tag.strip() for tag in raw_tags]

        audio_url = self._html_search_regex(
            r'data-mp3="([^"]+)"', webpage, 'audio URL')

        audio_urls = [audio_url]
        LQ_FORMAT = '-lq.mp3'
        if LQ_FORMAT in audio_url:
            audio_urls.append(audio_url.replace(LQ_FORMAT, '-hq.mp3'))

        formats = [{
            'url': format_url,
            'format_note': 'Stereo',
            'quality': quality,
        } for quality, format_url in enumerate(audio_urls)]

        return {
            'id': audio_id,
            'title': title,
            'description': description,
            'duration': duration,
            'uploader': uploader,
            'upload_date': upload_date,
            'tags': tags,
            'formats': formats,
        }


