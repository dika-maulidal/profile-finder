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

    # Scraping the profile ID (using <link> tag or <meta> tag)
    profile_id = None
    canonical_link = soup.find('link', {'rel': 'canonical'})
    if canonical_link and 'href' in canonical_link.attrs:
        profile_id = canonical_link['href'].split('/')[-2]  # Extract ID from the URL

    if not profile_id:  # If not found, try to find using <meta> tag
        meta_tag = soup.find('meta', {'property': 'og:url'})
        if meta_tag and 'content' in meta_tag.attrs:
            profile_id = meta_tag['content'].split('/')[-1]  # Extract ID from the URL

    # Building the result dictionary, adding only if values are not None
    result = {}
    if name_text:
        result['name'] = name_text
    if profile_id:
        result['profile_id'] = profile_id
    if headline_text:
        result['headline'] = headline_text
    if join_date_text:
        result['join_date'] = join_date_text
    if city_text:
        result['city'] = city_text
    if about_text:
        result['about'] = about_text

    return result

# Fungsi untuk melakukan scraping dari Zepeto
def scrape_zepeto(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Scraping name
    name = soup.find('h2', class_='sc-fXazdy UjHkE')
    name_text = name.get_text(strip=True) if name else None

    # Scraping bio
    bio = soup.find('p', class_='sc-TtZnY gnBPmJ')
    bio_text = bio.get_text(strip=True) if bio else None

    # Scraping all list items (post, follower, and following)
    list_items = soup.find_all('li', class_='sc-oeezt OJJCp')

    # Scraping post count
    post_count = list_items[0].find('strong').get_text(strip=True) if len(list_items) > 0 and 'Post' in list_items[0].get_text() else '0'

    # Scraping follower count
    follower_count = list_items[1].find('strong').get_text(strip=True) if len(list_items) > 1 and 'Follower' in list_items[1].get_text() else '0'

    # Scraping following count
    following_count = list_items[2].find('strong').get_text(strip=True) if len(list_items) > 2 and 'Following' in list_items[2].get_text() else '0'

    # Scraping avatar URL and Profile ID
    avatar_img = soup.find('img', alt='avatar-image')
    avatar_url = avatar_img['src'] if avatar_img else None

    # Extracting Profile ID from avatar URL
    profile_id = None
    if avatar_url:
        profile_id = avatar_url.split('/users/')[1].split('/')[0]

    # Building the result dictionary
    result = {}
    if name_text:
        result['name'] = name_text
    if profile_id:
        result['profile_id'] = profile_id
    if bio_text:
        result['bio'] = bio_text
    result['posts'] = post_count
    result['followers'] = follower_count
    result['following'] = following_count
    if avatar_url:
        result['avatar_url'] = avatar_url

    return result

# Codewars scraper
def scrape_codewars(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize variables
    name_text, clan_text, join_date_text, last_seen_text, avatar_url = None, None, None, None, None
    social_media = []
    following_count, followers_count, allies_count = '0', '0', '0'

    # Find all div elements with class 'stat'
    stat_divs = soup.find_all('div', class_='stat')

    for stat_div in stat_divs:
        text = stat_div.get_text(strip=True)

        # Scraping the name
        if "Name:" in text:
            name_text = text.replace("Name:", "").strip()

        # Scraping the clan
        elif "Clan:" in text:
            clan_text = text.replace("Clan:", "").strip()

        # Scraping the join date
        elif "Member Since:" in text:
            join_date_text = text.replace("Member Since:", "").strip()

        # Scraping the last seen date
        elif "Last Seen:" in text:
            last_seen_text = text.replace("Last Seen:", "").strip()

        # Scraping social media profile links
        elif "Profiles:" in text:
            links = stat_div.find_all('a', href=True)
            for link in links:
                social_media.append(link['href'])

        # Scraping the following count
        elif "Following:" in text:
            following_count = text.replace("Following:", "").strip()

        # Scraping the followers count
        elif "Followers:" in text:
            followers_count = text.replace("Followers:", "").strip()

        # Scraping the allies count
        elif "Allies:" in text:
            allies_count = text.replace("Allies:", "").strip()

    # Scraping the avatar URL
    avatar_img = soup.find('img', alt=lambda value: value and "Avatar" in value)
    if avatar_img:
        avatar_url = avatar_img['src']

    # Building the result dictionary
    result = {}
    if name_text:
        result['name'] = name_text
    if clan_text:
        result['clan'] = clan_text
    if join_date_text:
        result['join_date'] = join_date_text
    if last_seen_text:
        result['last_seen'] = last_seen_text
    if social_media:
        result['social_media'] = social_media
    result['following'] = following_count
    result['followers'] = followers_count
    result['allies'] = allies_count
    if avatar_url:
        result['avatar_url'] = avatar_url

    return result

# XMind Scrapper
def scrape_xmind(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Scraping Name (mengabaikan tautan "Edit")
    name_div = soup.find('div', class_='share-profile__username')
    if name_div:
        # Ambil teks tanpa tautan "Edit"
        name_text = next(name_div.stripped_strings, None)

    # Scraping Location
    location_span = soup.find('span', class_='icon-location')
    location_tooltip = location_span.find_parent('span')['title'] if location_span else None

    # Scraping Website
    website_span = soup.find('span', class_='icon-website')
    website_tooltip = website_span.find_parent('span')['title'] if website_span else None

    # Scraping Company
    company_span = soup.find('span', class_='icon-company')
    company_tooltip = company_span.find_parent('span')['title'] if company_span else None

    # Scraping About
    about_span = soup.find('span', class_='icon-about')
    about_tooltip = about_span.find_parent('span')['title'] if about_span else None

    # Scraping Featured Count
    featured_div = soup.find('div', class_='share-profile__switcher', attrs={'data-tab': 'featured'})
    featured_count = featured_div.find('span', class_='share-profile__switcher-count').get_text(strip=True) if featured_div else '0'

    # Scraping Public Count
    public_div = soup.select_one('div.share-profile__switcher.active[data-tab="public"]')
    
    if public_div:
        public_count = public_div.find('span', class_='share-profile__switcher-count').get_text(strip=True)
    else:
        print("Error: Elemen 'public' tidak ditemukan.")
        public_count = '0'

    # Scraping Private Count
    private_div = soup.find('div', class_='share-profile__switcher', attrs={'data-tab': 'private'})
    private_count = private_div.find('span', class_='share-profile__switcher-count').get_text(strip=True) if private_div else '0'

    # Building the result dictionary
    result = {}
    if name_text:
        result['name'] = name_text
    if location_tooltip:
        result['location'] = location_tooltip
    if website_tooltip:
        result['website'] = website_tooltip
    if company_tooltip:
        result['company'] = company_tooltip
    if about_tooltip:
        result['about'] = about_tooltip
    result['featured_count'] = featured_count
    result['public_count'] = public_count
    result['private_count'] = private_count

    return result   