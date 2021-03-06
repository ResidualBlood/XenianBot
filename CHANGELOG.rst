Changelog
=========

2.5.3 (unreleased)
------------------

- Nothing changed yet.


2.5.2 (2019-02-15)
------------------

- Send as group of 10 by default for anime dbs
- Send groups of 10 if max group size of 10 is exceeded by the user in anime db
- Fix default option not working in ``extract_option_from_string``
- Print bot info on start
- Remove obsolete prints
- Fix turning of download mode
- Fix crash when sending file to user when no url is defined
- Version bump


2.5.1 (2019-01-12)
------------------

- Fix animedatabase filetype detection was not working properly


2.5.0 (2019-01-12)
------------------

- Fix not being able to group send images when the the image was a link instead of a local path
- Replace Yandex- with Google-Translate
- Remove ``/danbooru_latest`` and replace ``/danbooru_search`` with ``/danbooru``
- Add more danbooru like services. Instead of just danbooru we get safebooru and konachan too
- Rename Danbooru class to AnimeDtabases because it fits better
- Send images from danbooru search async to getting the images to increase speed and with the users feedbackloop
- If possible send url of danbooru entry if the file could not be sent
- Add ``zip`` to any animedatabase search to get the flies in a zip file + all information about the files
- Install mr.developer
- Update dependency versions


2.4.0 (2019-01-05)
------------------

- Show progressbar of items being sent by danbooru search / latest
- Add @XenianBot to danbooru search / latest results
- Remember where danbooru files where downloaded too
- Be able to group the search result again with group=SIZE
- Add danbooru API limit warning
- Allow tag options and qualifiers like ``-some_tag``, ``*some`` & ``order:score``
- Handle different filtypes correctly


2.3.0 (2019-01-05)
------------------

- Define and use an api key for Danbooru with the ``DANBOORU_API_TOKEN`` variable
- Increase Danbooru image limit from 5 to 20
- Notify user about successful restart with ``/restart``
- Call not implemented when yandex translate is run without api key
- Fix corrupt danbooru post image url
- Send full file too together with the danbooru photos
- Send danbooru images faster by not trying to send them as a group
- Send danbooru images only available to premium members as long a premium account is given in the settings


2.2.0 (2018-12-26)
------------------

- Clear zip download queue with ``/zip_clear``
- Prevent too long message error on /commands rst


2.1.0 (2018-12-25)
------------------

- Added an alias command ``/help`` for ``/commands``
- Fixed usage alias commands overriding real commands
- Add ``/zip_mode`` command which lets the user download items into a zip file


2.0.5 (2018-11-26)
------------------

- Fix error when saving a ``CustomNamedTemporaryFile`` file.
- Fix not being able to save sticker as image in sticker search
- Tell user that RIS is not working if the file path is not an url instead of just telling nothing
- Fix not working alias function
- Bump ``gTTS-token`` version to fix TTS
- Fix file type when saving ``voices``


2.0.4 (2018-11-26)
------------------

- Fix file permissions for copied files under unix systems


2.0.3 (2018-11-26)
------------------

- Fix file copying on unix devices


2.0.2 (2018-11-26)
------------------

-  Fix ``/commands raw`` command not working


2.0.1 (2018-11-26)
------------------

-  Fix paths in settings template


2.0.0 (2018-11-26)
------------------

Added
~~~~~

-  Custom user specific databases, use commands ``/save`` and ``/save_mode`` more information in ``/commands``
-  Be able to show custom DB entries with ``/db_list``
-  Add functionality to add alias commands just like a normal command but a string as ``command`` value, which points to
   a ``command_name``. Additionally ``title``, ``description``, ``hidden`` and ``group`` can be set.
-  Autogenerate ResT for all commands with ``/commands rst``, but be aware that double whitespace are not printed. You
   get "\\ \\ " instead, which can be replaced.

Changes
~~~~~~~

-  Bot refactoring:
    -  package ``xenian.bot`` instead of ``xenian_bot``
    -  buildout instead of pipenv
    -  ``bin/bot`` instead of ``run_bot.py``
-  Split utils up and put them in an ``utils`` package
-  Moved the download functions from the reverse search image commands to the utils
-  Combined the reverse search MessageHandlers to one
-  Cleaned up reverse search image command
-  Autodownload ffmpeg if it cannot be found by imageio
-  Improve windows compatibility with file handling
-  Optimized GIF downloader for local file uploader
-  Run GIF downloader asynchronously so users won't get stuck
-  Reply to user message on GIF download, so that the user sees to which GIF the message belongs
-  Improve TTS error message
-  Rename ``tty`` command to ``tts`` (Text-To-Speech) but add an ``tty`` alias for the time being
-  Be able to set a CallbackQueryHandler for a CallbackQuery sender


[1.4.0] - 2018.05.18
--------------------


Added
~~~~~

-  Print raw commands list for the BotFather with ``/commands raw``
-  New filter ``bot_admin``, check if current user is a bot admin
-  ``/random`` - send a random anime gif
-  ``/save_gif`` - *hidden* - save the gif replied to as an anime gif
-  ``/toggle_gif_save`` - *hidden* - toggle auto save sent gifs as anime gif
-  New filter ``anime_save_mode`` to determine if gif save mode is turned on
-  New filters for group permissions: ``bot_group_admin``, ``user_group_admin``, ``reply_user_group_admin``,
   ``all_admin_group``


Changes
~~~~~~~

-  Move dabooru to the **Anime** group
-  Move Video Downloader to the Download group

Fixed
~~~~~

-  Use title for indirect commands instead of command name


[1.3.0] - 2018.05.18
--------------------


Added
~~~~~

-  Mako Template Engine integration


Changes
~~~~~~~

-  Reimplemented the ``/commands`` command with a mako template

Removed
~~~~~~~

-  Temporarily remove the Instagram functionality, better version will come back in the future


[1.2.1] - 2018.02.04
--------------------


Changes
~~~~~~~

-  Fix links to users
-  Fix image to text and translate command name in CHANGELOG and README


[1.2.0] - 2018.02.04
--------------------


Added
~~~~~

-  Group setting for commands
-  Use MongoDB as database, configuration must be set in settings.py
-  Create collection in database with all user, messages and chats
-  ``/itt [-l LANG]`` - Image to Text: Extract text from images
-  ``/itt_lang`` - Languages for ItT: Available languages for Image to Text
-  ``/itt_translate [TEXT] [-lf LANG] [-lt LANG]`` - Image to Text Translation: Extract text from images and translate
   it. ``-lf`` (default: detect, /itt_lang) language on image, to ``-lt`` (default: en, normal language codes) language.


Changes
~~~~~~~

-  Fix command default options
-  Use Filters.all as default for MessageHandler
-  Yandex translate got new function for itself, it is used by the ``/translate`` and ``/itt_translate`` command.


[1.1.2] - 2018-02-04
--------------------


Changes
~~~~~~~

-  Fixed non admin user could use ``/kick``, ``/ban``, ``/warn``
-  Fixed grammatical error in a group management text


[1.1.1] - 2018-02-01
--------------------


Changes
~~~~~~~

-  Add Yandex API Token to settings.example.py


[1.1.0] - 2018-02-01
--------------------


Added
~~~~~

-  ``/tty [TEXT] [-l LANG]`` - Text to speech: Convert text the given text or the message replied to, to text. Use
   ``-l`` to define a language, like de, en or ru
-  ``/translate [TEXT] [-lf LANG] [-lt LANG]`` Translate a reply or a given text from ``-lf`` (default: detect) language
   to ``-lt`` (default: en) language
-  Add utility function ``get_option_from_string`` to extract options from strings sent by a user


Changes
~~~~~~~

-  Update reverse image search wait message if possible
-  Danbooru search only sends finished messages in private chat


[1.0.0] - 2018-01-26
--------------------


Added
~~~~~

-  ``/delete`` has to be a reply to another message to delete this message and warn the user
-  ``/unwarn`` to remove all warnings from a user. Reply with it to a message
-  Add command ``/rules`` to show a groups rules
-  Add command ``/rules`` to show a groups rules
-  Add command ``/rules_define YOUR_RULES`` to define new rules in a group
-  Add command ``/rules_remvoe`` to remove the groups rules
-  Specify a time until user can return from kick with ``/kick [TIME]``
-  Add ``/calc EQUATION`` command to calculate equations inside groups
-  Added ``LOG_LEVEL`` to settings
-  Instagram credentials to the ``settings.py``, which are used for one central Instagram account, instead of
   ``/instali`` and ``/instalo``
-  ``/insta_follow PROFILE_LINK/S OR USERNAME/S`` Instagram Follow: Tell @XenianBot to follow a specific user on
   Instagram, this is used to access private accounts.
-  ``/contribute YOUR_REQUEST`` Send the supporters and admins a request of any kind
-  ``/error ERROR_DESCRIPTION`` If you have found an error please use this command.

Changed
~~~~~~~

-  Run math function asynchronous
-  Disable directly solving equations without command sent to groups
-  Fix not shortening solutions form the calculator
-  Fix message too long for Telegram, for too long solutions from the calculator
-  Remove all ``True`` and ``False`` before trying to calculate so a message with just “true” doesn’t get returned


Removed
~~~~~~~

-  ``/instali``, ``/instalo`` have both been removed in order to have one central defined account
