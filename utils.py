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

# Kaskus scraper
def scrape_kaskus(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Scraping the name
    name = soup.find('span', {'class': 'C(c-black) Fz(18px) Fw(700)'})
    name_text = name.get_text(strip=True) if name else None

    # Scraping the join date
    join_date = soup.find('div', {'data-tippy-content': 'Join Date'})
    join_date_text = join_date.find('span').get_text(strip=True) if join_date else None

    # Scraping the user ID
    user_id = soup.find('div', {'data-tippy-content': 'User ID'})
    user_id_text = user_id.find('span', {'class': 'Fz(12px)'}).get_text(strip=True) if user_id else None

    # Scraping the bio
    bio = soup.find('div', {'class': 'Ta(c) Lh(18px)'})
    bio_text = bio.get_text(strip=True) if bio else None

    # Scraping the number of posts (Post)
    posts = soup.find('div', text='Post')
    posts_count = posts.find_previous_sibling('div').get_text(strip=True) if posts and posts.find_previous_sibling('div') else '0'

    # Scraping the number of followers (Pengikut)
    followers = soup.find('div', text='Pengikut')
    followers_count = followers.find_previous_sibling('div').get_text(strip=True) if followers and followers.find_previous_sibling('div') else '0'

    # Scraping the number of following (Mengikuti)
    following = soup.find('div', text='Mengikuti')
    following_count = following.find_previous_sibling('div').get_text(strip=True) if following and following.find_previous_sibling('div') else '0'

    # Scraping avatar image URL
    avatar_img = soup.find('img', {'id': 'jsImageAvatar'})
    avatar_url = avatar_img['src'] if avatar_img else None

    # Building the result dictionary, adding only if values are not None
    result = {}
    if name_text:
        result['name'] = name_text
    if join_date_text:
        result['join_date'] = join_date_text
    if user_id_text:
        result['user_id'] = user_id_text
    if bio_text:
        result['bio'] = bio_text
    if avatar_url:
        result['avatar_url'] = avatar_url
    result['followers'] = followers_count
    result['following'] = following_count
    result['posts'] = posts_count

    return result

# Dicoding scraper
def scrape_dicoding(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Scraping the name
    name = soup.find('h2', {'class': 'profile-headline-name text-white'})
    name_text = name.get_text(strip=True) if name else None

    # Scraping the headline
    headline = soup.find('p', {'class': 'profile-headline-text text-white'})
    headline_text = headline.get_text(strip=True) if headline else None

    # Scraping the join date
    join_date = soup.find('span', {'title': 'time'})
    join_date_text = join_date.get_text(strip=True) if join_date else None

    # Scraping the city
    city = soup.find('span', {'title': 'city'})
    city_text = city.get_text(strip=True) if city else None

    # Scraping the about section
    about = soup.find('div', {'class': 'profile-about-description fr-view'})
    about_text = about.get_text(strip=True) if about else None

    # Building the result dictionary, adding only if values are not None
    result = {}
    if name_text:
        result['name'] = name_text
    if headline_text:
        result['headline'] = headline_text
    if join_date_text:
        result['join_date'] = join_date_text
    if city_text:
        result['city'] = city_text
    if about_text:
        result['about'] = about_text

    return result
