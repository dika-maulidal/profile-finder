import requests
from bs4 import BeautifulSoup

# General function to fetch a URL and check if the account exists
def check_social_media(url, expected_code, not_found_string, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == expected_code and not_found_string not in response.text:
            return {'status': True, 'response': response}
        else:
            return {'status': False}
    except requests.exceptions.RequestException:
        return {'status': False}

# GitHub scraper
def scrape_github(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Scraping the name (not the nickname)
    name = soup.find('span', {'itemprop': 'name'})
    name_text = name.get_text(strip=True) if name else None

    # Scraping social media links (all links with class "Link--primary" and rel="nofollow me")
    social_media_links = []
    social_media_anchors = soup.find_all('a', {'class': 'Link--primary', 'rel': 'nofollow me'})
    for anchor in social_media_anchors:
        url = anchor.get('href')
        if url and url.startswith('https://'):
            social_media_links.append(url)

    # Scraping the bio
    bio = soup.find('div', class_='p-note user-profile-bio mb-3 js-user-profile-bio f4')
    bio_text = bio.find('div').get_text(strip=True) if bio and bio.find('div') else None

    # Scraping the location
    location = soup.find('li', {'itemprop': 'homeLocation'})
    location_text = location.find('span', class_='p-label').get_text(strip=True) if location else None

    # Scraping the profile ID
    profile_meta = soup.find('meta', {'name': 'twitter:image'})
    profile_id = profile_meta['content'].split('/u/')[-1].split('?')[0] if profile_meta else None

    # Scraping the organization
    organization = soup.find('li', {'itemprop': 'worksFor'})
    organization_name = organization.find('div').get_text(strip=True) if organization else None

    # Scraping avatar image URL
    avatar_anchor = soup.find('a', {'itemprop': 'image'})
    avatar_url = avatar_anchor.get('href') if avatar_anchor else None

    # Scraping followers and following
    followers = soup.find('a', href=lambda x: x and 'tab=followers' in x)
    followers_count = followers.find('span', class_='text-bold').get_text(strip=True) if followers else '0'

    following = soup.find('a', href=lambda x: x and 'tab=following' in x)
    following_count = following.find('span', class_='text-bold').get_text(strip=True) if following else '0'

    # Building the result dictionary, adding only if values are not None
    result = {}
    if name_text:
        result['name'] = name_text
    if social_media_links:
        result['social_media_links'] = social_media_links  # Adding social media links
    if bio_text:
        result['bio'] = bio_text
    if location_text:
        result['location'] = location_text
    if profile_id:
        result['profile_id'] = profile_id
    if organization_name:
        result['organization'] = organization_name
    if avatar_url:
        result['avatar_url'] = avatar_url  # Adding avatar URL
    result['followers'] = followers_count
    result['following'] = following_count

    return result
