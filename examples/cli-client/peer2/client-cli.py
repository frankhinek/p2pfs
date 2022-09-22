from p2pfs.application import Application
from aioconsole import ainput
import asyncio
import json
import logging
import os
from pathlib import Path

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(handler)
log.setLevel(logging.INFO)

# Load config file.
with open('config.json') as f:
    config = json.loads(f.read())

app = Application(config)

async def cli():
    main_menu = """
    Choose which service you wish to use :

            1 : Share a file
            2 : Search for a file
            3 : Quit
    """

    share_menu = """
    Choose which file you wish to share :
    """

    search_field_menu = """
    Choose which field you wish to search by :

            1 : File Name
            2 : Artist
            3 : Song Title
            4 : Album
    """

    search_term_menu = """
    Enter your search term :
    """

    search_result_menu = """
    Do you want to download this file? (y/n)

    File Name : {}
       Artist : {}
   Song Title : {}
        Album : {}
    """
    
    clear()
    while True:
        print(main_menu)
        choice = await ainput('>> ')

        # Share a file
        if choice and int(choice) == 1:
            files = [file.name for file in Path('content').glob('*')]
            if files:
                share_menu_files = share_menu
                for i, file in enumerate(files, 1):
                    share_menu_files += f'\n{i: >13} : {file}'
                print(share_menu_files + '\n')
                choice = await ainput('>> ')
                if choice:
                    await app.publish(files[int(choice)-1])
            else:
                clear()
                print('\n    No files available to share in content directory.')

        # Search for a file
        elif choice and int(choice) == 2:
            clear()
            print(search_field_menu)
            field_name = await ainput('>> ')
            search_fields = {
                '1': 'filename',
                '2': 'artist',
                '3': 'title',
                '4': 'album'
            }
            clear()
            print(search_term_menu)
            search_term = await ainput('>> ')
            search_result = await app.search(search_fields[field_name], search_term)
            if search_result:
                print(search_result_menu.format(
                    search_result['metadata']['filename'],
                    search_result['metadata']['artist'],
                    search_result['metadata']['title'],
                    search_result['metadata']['album'],
                ))
                choice = await ainput('>> ')
                if choice.lower() == 'y' or choice.lower() == 'yes':
                    await app.download(search_result['url-list'], search_result['files'])
                
            else:
                clear()
                print('\nSearch returned no results')

        # Quit the application
        elif choice and int(choice) == 3:
            clear()
            await app.stop()
            break

def clear():
    _ = os.system('clear' if os.name == 'posix' else 'cls')

async def run_app():
    await app.start() 

async def main():
    tasks = []
    tasks.append(asyncio.create_task(cli()))
    tasks.append(asyncio.create_task(run_app()))

    await asyncio.gather(*tasks)

asyncio.run(main())