from telegram import Audio, Bot, Chat, Document, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, PhotoSize, \
    Sticker, Update, Video
from telegram.ext import CallbackQueryHandler, Filters, MessageHandler

from xenian_bot import mongodb_database
from xenian_bot.commands import filters
from xenian_bot.utils import render_template, user_is_admin_of_group
from .base import BaseCommand

__all__ = ['image_db']


class CustomDB(BaseCommand):
    """Create Custom Databases by chat_id and tag
    """

    group = 'Custom'
    ram_db = {}

    def __init__(self):
        self.commands = [
            {
                'command': self.toggle_mode,
                'description': 'Create an custom database',
                'args': ['tag'],
                'command_name': 'save_mode',
                'options': {
                    'filters': ~ Filters.group,
                    'pass_args': True,
                },
            },
            {
                'title': 'Save object',
                'command': self.save_command,
                'command_name': 'save',
                'description': 'Reply to save an object to a custom db',
                'args': ['tag'],
                'options': {
                    'pass_args': True,
                },
            },
            {
                'title': 'Save object',
                'command': self.save_command,
                'handler': CallbackQueryHandler,
                'hidden': True,
                'options': {
                    'pattern': '^save\s\w+$',
                },
            },
            {
                'title': 'Available DBs',
                'command': self.available,
                'description': 'Show created databases',
            },
            {
                'title': 'Remove DB',
                'command': self.delete,
                'description': 'Delete selected database',
            },
            {
                'title': 'Remove DB',
                'command': self.real_delete,
                'handler': CallbackQueryHandler,
                'description': 'Delete the database for real',
                'options': {
                    'pattern': '^(delete\s\w+|sure\s\w+|cancel)$',
                }
            },
            {
                'title': 'Show available tags as keyboard buttons',
                'command': self.show_tag_chooser,
                'handler': CallbackQueryHandler,
                'hidden': True,
                'options': {
                    'pattern': '^show_tags',
                }
            },
            {
                'title': 'Save object',
                'description': 'Send objects while /save_mode is turned of to save them into your defined db',
                'handler': MessageHandler,
                'command': self.save,
                'options': {
                    'filters': (
                            (
                                    Filters.video
                                    | Filters.document
                                    | Filters.photo
                                    | Filters.sticker
                                    | Filters.audio
                                    | Filters.voice
                                    | Filters.text
                            )
                            & filters.custom_db_save_mode
                            & ~ Filters.group
                    ),
                },
            },
        ]
        self.telegram_object_collection = mongodb_database.telegram_object_collection
        self.custom_db_save_mode = mongodb_database.custom_db_save_mode

        super(CustomDB, self).__init__()

    def get_current_tag(self, update: Update, tags: list = None):
        """Get the current active tag

        Args:
            update (:obj:`telegram.update.Update`): Telegram Api Update Object
            tags (:obj:`list`, optional): List of tags sent by the user if it is is set the first one will be taken

        Returns:
            :obj:`str`: The currently active tag for this user
        """
        if tags:
            return tags[0].lower()

        chat = self.custom_db_save_mode.find_one({'chat_id': update.message.chat_id})
        if chat and chat.get('tag', ''):
            return chat['tag'].lower()
        return ''

    def toggle_mode(self, bot: Bot, update: Update, args: list = None):
        """Toggle save mode

        Args:
            bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
            update (:obj:`telegram.update.Update`): Telegram Api Update Object
            args (:obj:`list`, optional): List of sent arguments
        """
        tag = 'user'
        if args:
            tag = args[0].lower()

        chat_id = update.message.chat_id
        data = self.custom_db_save_mode.find_one({'chat_id': chat_id})
        new_mode = not data['mode'] if data else True
        self.custom_db_save_mode.update({'chat_id': chat_id},
                                        {'chat_id': chat_id, 'mode': new_mode, 'tag': tag},
                                        upsert=True)
        if new_mode:
            update.message.reply_text('Save mode turned of for `[%s]`. You can send me any type of Telegram object not '
                                      'to save it.' % tag, parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text('Save mode turned off')

    def show_tag_chooser(self, bot: Bot, update: Update, method: str = None, message: str = None):
        """Show available tags in inline-keyboard-buttons

        Args:
            bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
            update (:obj:`telegram.update.Update`): Telegram Api Update Object
            method (:obj:`str`, optional): Method to call when clicked (callback query method), is obligatory if you
                method is not called by the bot itself
            message (:obj:`str`, optional): Message to send to the user
        """
        callback_query = getattr(update, 'callback_query', None)
        if not callback_query and not method:
            return ValueError('Wither callback_query or method must be set')

        if callback_query:
            if (update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]
                    and not user_is_admin_of_group(update.effective_chat, update.effective_user)):
                return
            args = callback_query.data.split(' ')
            args = list(filter(lambda string: string.strip() if string.strip() else None, args))

            if args[1] == 'cancel':
                update.callback_query.message.delete()
                return

            if callback_query:
                method = args[1] if len(args) > 1 else ''
                if not method:
                    update.message.reply_text('Something went wrong, try again or contact an admin /error')

            if len(args) > 2:
                message = ' '.join(args[2:])
        message = message or 'Choose a tag:'

        db_items = self.telegram_object_collection.find({'chat_id': update.message.chat_id})
        tag_list = list(set([item['tag'] for item in db_items]))
        if tag_list:
            button_list = [tag_list[i:i + 3] for i in range(0, len(tag_list), 3)]
            button_list = [
                [InlineKeyboardButton(tag, callback_data='{} {}'.format(method, tag)) for tag in group]
                for group in button_list
            ]
        else:
            button_list = [[InlineKeyboardButton('user', callback_data='%s user' % method)]]

        button_list.append([InlineKeyboardButton('Cancel', callback_data='show_tags cancel')])

        buttons = InlineKeyboardMarkup(button_list)
        if callback_query:
            callback_query.message.edit(message, reply_markup=buttons)
        else:
            update.message.reply_text(message, reply_markup=buttons)

    def save_command(self, bot: Bot, update: Update, args: list = None):
        """Save image in reply

        Args:
            bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
            update (:obj:`telegram.update.Update`): Telegram Api Update Object
            args (:obj:`list`, optional): List of sent arguments
        """
        if (update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]
                and not user_is_admin_of_group(update.effective_chat, update.effective_user)):
            if update.message:
                update.message.reply_text('Only admins can use this command in groups')
            return

        self.ram_db.setdefault('save_reply', {})
        reply_to_message = getattr(update.message, 'reply_to_message', None)
        previous_message = self.ram_db['save_reply'].get(update.effective_user.id, None)
        if not reply_to_message and not previous_message:
            update.message.reply_text('You have to reply to some message.')
            return

        callback_query = getattr(update, 'callback_query', None)
        if callback_query:
            args = list(set(callback_query.data.split(' ')) - {'save'})
            callback_query.message.delete()
            update.message = previous_message
        elif not args:
            self.ram_db['save_reply'][update.effective_user.id] = update.message
            self.show_tag_chooser(bot, update, 'save')
            return

        tag = self.get_current_tag(update, args)
        self.save(bot, update, tag)
        self.ram_db['save_reply'][update.effective_user.id] = None

    def save(self, bot: Bot, update: Update, tag: str = None):
        """Save a gif

        Args:
            bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
            update (:obj:`telegram.update.Update`): Telegram Api Update Object
            tag (:obj:`tag`, optional): Tag for the image
        """

        reply_to = False
        telegram_object = (
                update.message.document
                or update.message.video
                or update.message.photo
                or update.message.sticker
                or update.message.audio
                or update.message.voice
        )
        if not telegram_object:
            if getattr(update.message, 'reply_to_message'):
                telegram_object = (
                        update.message.reply_to_message.document
                        or update.message.reply_to_message.video
                        or update.message.reply_to_message.photo
                        or update.message.reply_to_message.sticker
                        or update.message.reply_to_message.audio
                        or update.message.reply_to_message.voice
                        or update.message.reply_to_message.text
                )
            reply_to = bool(telegram_object)
            if not reply_to:
                telegram_object = update.message.text

        if not telegram_object:
            update.message.reply_text('You either have to send something or reply to something')
            return

        message = None
        if not tag:
            tag = self.get_current_tag(update)

        if isinstance(telegram_object, str):
            message = {
                'type': 'text',
                'text': telegram_object,
                'file_id': '',
            }
        else:
            message = {
                'type': 'document',
                'text': (getattr(update.message.reply_to_message, 'caption') if reply_to
                         else getattr(update.message, 'caption')),
                'file_id': telegram_object.file_id,
            }
            if isinstance(telegram_object, Document):
                message['type'] = 'document'
            elif isinstance(telegram_object, Video):
                message['type'] = 'video'
            elif isinstance(telegram_object, PhotoSize):
                message['type'] = 'photo'
            elif isinstance(telegram_object, Sticker):
                message['type'] = 'sticker'
            elif isinstance(telegram_object, Audio):
                message['type'] = 'audio'

        if not message:
            update.message.reply_text('There was an error please contact an admin via /error or retry your action.')
            return

        message['chat_id'] = update.message.chat_id
        message['tag'] = tag
        self.telegram_object_collection.update(message, message, upsert=True)

        update.message.reply_text('{} was saved to `{}`!'.format(message['type'].title(), tag),
                                  parse_mode=ParseMode.MARKDOWN)

    def available(self, bot: Bot, update: Update):
        """Show available databases

        Args:
            bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
            update (:obj:`telegram.update.Update`): Telegram Api Update Object
        """
        db_items = self.telegram_object_collection.find({'chat_id': update.message.chat_id})
        data = {}
        for item in db_items:
            tag = item['tag']
            title = tag.title()
            data_category = data.get(tag, {
                'title': title,
                'tag': tag,
                'video': 0,
                'document': 0,
                'photo': 0,
                'sticker': 0,
                'audio': 0,
                'voice': 0,
                'text': 0,
                'items': []
            })
            data_category[item['type']] += 1
            data_category['items'].append(item)

            data[tag] = data_category

        update.message.reply_text(render_template('available_dbs.html.mako', categories=data),
                                  parse_mode=ParseMode.HTML)

    def delete(self, bot: Bot, update: Update):
        """Show database delete list

        Args:
            bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
            update (:obj:`telegram.update.Update`): Telegram Api Update Object
        """
        db_items = self.telegram_object_collection.find({'chat_id': update.message.chat_id})
        tag_list = list(set([item['tag'] for item in db_items]))

        button_list = [tag_list[i:i + 3] for i in range(0, len(tag_list), 3)]
        button_list = [[InlineKeyboardButton(tag, callback_data='sure %s' % tag) for tag in group]
                       for group in button_list]
        button_list.append([InlineKeyboardButton('Cancel', callback_data='cancel')])

        update.message.reply_text(
            text='Select the database to delete:',
            reply_markup=InlineKeyboardMarkup(button_list)
        )

    def real_delete(self, bot: Bot, update: Update):
        """Actually delete a databases

        Args:
            bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
            update (:obj:`telegram.update.Update`): Telegram Api Update Object
        """
        data = update.callback_query.data
        if data.startswith('sure'):
            update.callback_query.message.edit_text(
                'Are you sure:',
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('Yes', callback_data='delete %s' % data.split(' ')[1]),
                    InlineKeyboardButton('Cancel', callback_data='cancel'),
                ]])
            )
        elif data == 'cancel':
            update.callback_query.message.delete()
        elif data.startswith('delete'):
            tag = data.split(' ')[1]
            self.telegram_object_collection.delete_many({'chat_id': update.callback_query.message.chat_id, 'tag': tag})
            update.callback_query.message.edit_text('%s deleted!' % tag.title())
        else:
            update.callback_query.message.edit_text('Something went wrong, try again or contact admin via /error.')


image_db = CustomDB()