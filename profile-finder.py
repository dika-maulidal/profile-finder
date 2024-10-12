"""
Made by Dika Maulidal
"""

import json
from concurrent.futures import ThreadPoolExecutor
from utils import check_social_media, scrape_github, scrape_kaskus, scrape_dicoding, scrape_zepeto
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

# ASCII Art
ascii_art = f"""{Fore.LIGHTBLUE_EX}
 ___            ___  _  _            ___  _         _           
| . \\ _ _  ___ | | '<_>| | ___  ___ | __><_>._ _  _| | ___  _ _ 
|  _/| '_>/ . \\| |- | || |/ ._>|___|| _> | || ' |/ . |/ ._>| '_>
|_|  |_|  \\___/|_|  |_||_|\\___.     |_|  |_||_|_|\\___|\\___.|_|  
{Style.RESET_ALL}
"""

# Load data from the JSON file
def load_json_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Function to check an account and scrape further details
def check_account(site, target_account, pbar, found_counter):
    site_name = site.get('name')
    uri_check = site.get('uri_check')
    e_code = site.get('e_code')
    m_string = site.get('m_string')
    category = site.get('cat')

    # Replace {account} with target_account
    url = uri_check.replace('{account}', target_account)

    # Check if the account exists
    result = check_social_media(url, e_code, m_string)

    if result['status']:
        # Increment the counter if an account is found
        found_counter[0] += 1

        output = f"\n{Style.BRIGHT}[{Fore.LIGHTBLUE_EX}+{Style.RESET_ALL}{Style.BRIGHT}] Found {Fore.LIGHTBLUE_EX}on{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{site_name}{Style.RESET_ALL}:\n" \
                 f"    {Style.BRIGHT}[{Fore.WHITE}{Fore.LIGHTBLUE_EX}URL{Fore.RESET}{Style.BRIGHT}{Fore.WHITE}] {url}\n" \
                 f"    {Style.BRIGHT}[{Fore.WHITE}{Fore.LIGHTBLUE_EX}Social Media{Fore.RESET}{Style.BRIGHT}{Fore.WHITE}] {site_name}\n" \
                 f"    {Style.BRIGHT}[{Fore.WHITE}{Fore.LIGHTBLUE_EX}Categories{Fore.RESET}{Style.BRIGHT}{Fore.WHITE}] {category}"

        # If the site is GitHub, scrape additional information
        if site_name == 'GitHub':
            scraped_data = scrape_github(result['response'].text)
            for key, value in scraped_data.items():
                output += f"\n    {Style.BRIGHT} - [{Fore.LIGHTCYAN_EX}{key.capitalize()}{Style.RESET_ALL}{Style.BRIGHT}] {value}"

        # If the site is Kaskus, scrape additional information
        elif site_name == 'Kaskus':
            scraped_data = scrape_kaskus(result['response'].text)
            for key, value in scraped_data.items():
                output += f"\n    {Style.BRIGHT} - [{Fore.LIGHTCYAN_EX}{key.capitalize()}{Style.RESET_ALL}{Style.BRIGHT}] {value}"

        # If the site is Dicoding, scrape additional information
        elif site_name == 'Dicoding':
            scraped_data = scrape_dicoding(result['response'].text)
            for key, value in scraped_data.items():
                output += f"\n    {Style.BRIGHT} - [{Fore.LIGHTCYAN_EX}{key.capitalize()}{Style.RESET_ALL}{Style.BRIGHT}] {value}"

        # If the site is Zepeto, scrape additional information
        elif site_name == 'Zepeto':
            scraped_data = scrape_zepeto(result['response'].text)
            for key, value in scraped_data.items():
                output += f"\n    {Style.BRIGHT} - [{Fore.LIGHTCYAN_EX}{key.capitalize()}{Style.RESET_ALL}{Style.BRIGHT}] {value}"

        tqdm.write(output)

    pbar.update(1)  # Update progress bar after each check

# Main function to run the OSINT tool with progress bar
def run_osint(target_accounts):
    # Load the JSON data
    data = load_json_data('data/data-profile.json')  # Load the provided JSON
    sites = data['sites']

    found_counter = [0]  # This will keep track of how many accounts were found

    # Print the ASCII art
    print(ascii_art)

    # Loop through each username
    for target_account in target_accounts:
        print(f"{Fore.LIGHTCYAN_EX}\nSearching for username: {target_account}{Style.RESET_ALL}")
        
        with tqdm(total=len(sites), desc=f"{Fore.LIGHTBLUE_EX}Scanning{Style.RESET_ALL}", unit="site", leave=True, bar_format="{l_bar}{bar}{r_bar}", colour="cyan") as pbar:
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(check_account, site, target_account, pbar, found_counter) for site in sites]
                for future in futures:
                    future.result() 
    
    print(f"{Fore.LIGHTCYAN_EX}\nScan Completed! Found {found_counter[0]} out of {len(sites)} sites.{Style.RESET_ALL}")

if __name__ == "__main__":
    target_input = input(f"{Fore.LIGHTCYAN_EX}\nEnter usernames to search : {Style.RESET_ALL}")
    target_accounts = target_input.split()  # Split the input string into multiple usernames
    run_osint(target_accounts)
