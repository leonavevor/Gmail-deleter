
from __future__ import print_function

import argparse
import sys
from typing import Literal

from gmail_handler import GmailBulkHandler
from oauth2client import tools 



INVALID_INPUT_TEXT = 'Invalid input! Try again'
MENU_TEXT = """
1. Delete all messages
2. Delete messages from category
3. Delete messages from specific user
4. Empty trash
5. Empty spam
7. Exit

WARNING: All messages will be deleted permanently (not moved to Trash).
"""

try:
    arguments = argparse.ArgumentParser(parents=[tools.argparser], description='Mass mail deleter for Gmail')
    arguments.add_argument('-s', '--secret', type=str, help='Path to the Google client secret json', required=False)
except ImportError:
    arguments = None

args = arguments.parse_args()
secret_file_path = args.secret

print("secret_file_path: ", secret_file_path)
print("args: ", args)
gmail = GmailBulkHandler(secret_file_path, args)


def main(delete_type: Literal['soft_delete', 'permanent_delete'] = 'soft_delete'):
    """Main function for the mail deleter.
       NOTE: soft_delete will move the messages to trash but permanent_delete will delete the messages permanently
    args:
        delete_type: Type of deletion. Can be 'soft_delete' or 'permanent_delete'
    """

    while True:
        print(MENU_TEXT)
        try:
            choice = int(input('Choose an option: '))
            if choice == 1:
                messages: list = list(gmail.list_messages_matching_query(user_id='me', query='is:unread category:promotions from:(-me) after:2023/3/16 before:2025/3/17'))

            elif choice == 2:
                labels = gmail.get_labels()
                for i, label in enumerate(labels):
                    print(str(i+1) + ': ' + label['name'])
                try:
                    label_choice = int(input('Choose label for deletion: '))
                    if label_choice <= 0 or label_choice >= len(labels) + 1:
                        print(INVALID_INPUT_TEXT)
                        continue
                except ValueError:
                    print(INVALID_INPUT_TEXT)
                else:
                    messages: list = list(gmail.list_messages_with_label(label_ids=labels[label_choice-1]['id']))

            elif choice == 3:
                user_choice = str(input('Choose user whose messages you want to delete: '))
                messages: list = list(gmail.list_messages_matching_query(user_id='me', query='from:' + user_choice))

            elif choice == 4:
                messages: list = list(gmail.list_messages_with_label(user_id='me', label_ids='TRASH'))

            elif choice == 5:
                messages: list = list(gmail.list_messages_with_label(user_id='me', label_ids='SPAM'))

            else:
                sys.exit(1)

            print("count of messages: ", sum(1 for _ in messages))
            print("START messages:===================================")
            for message in messages:
                print(message)
                print("messages: -----------------------------------")
            print("END messages: ===================================")

            proceed = input('Do you want to proceed with the deletion? (y/n): ')
            if proceed.lower() == 'y':
                print('Deleting messages...')
                delete_msgs(delete_type, messages)
            else:
                print('Delete operation cancelled')
                continue

        except ValueError:
            print(INVALID_INPUT_TEXT)


def delete_msgs(delete_type: str, messages: list):
    if delete_type == 'soft_delete':
        for message in messages:
           gmail.delete_message(msg_id=message['id'])
        print('Messages moved to Trash')
    else:
        # for message in messages[:10]:
        #    gmail.delete_message_perm(msg_id=message['id'])
        gmail.delete_messages_perm(msgs=messages)
        print('Messages deleted permanently')


if __name__ == '__main__':
    main('soft_delete')
