from telegram import Update
from telegram.ext import ContextTypes

from config import settings
from database import (add_one_biker, get_all_bikers, get_all_travels,
                      in_group_check, insert_data)

bold_start = '\033[1m'
bold_end = '\033[0m'


  

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not in_group_check:
        return await context.bot.send_message(chat_id=update.message.from_user.id, text=('Permission denied'))
    user_info = await context.bot.get_chat_member(chat_id=update.message.chat_id, user_id=update.message.from_user.id)
    await context.bot.send_message(
        # message_thread_id=update._effective_message.message_thread_id,
        chat_id=update.message.from_user.id,
        text=(
            f'Cлава роботам, смерть всем человекам'
            f'\nIn dev...'
            f'\nДля начала работы с ботом введите команду /trip'
        )
    )
    if user_info.status == 'creator' or 'administartor':
        await context.bot.send_message(
            # message_thread_id=update._effective_message.message_thread_id,
            chat_id=message.from_user.id,
            text=f'Tututut'
        )


async def trip_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):   
    chat_id = update.message.from_user.id
    await context.bot.send_message(
        # message_thread_id=update._effective_message.message_thread_id,
        chat_id=chat_id,
        text=(
            f'Привет, *\\{update.message.from_user.first_name}*'
            f'\nФункционал, редактирования/удаления в процеесе разработки\.'
            f'\nПри возникновении проблем в работе с ботом' 
            f' или при наличии идей по доработке функционала просьба писать @cyllonn'
            f'\nДля просмота всех планируемых поездок введи команду *\/calendar*'
            f'\n*Для добавления информации о поездке отправь сообщение в следующем формате:*'
        ),
        parse_mode='MarkdownV2'

    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f'<b>set_trip</b>'
            f'\n<b>1. Название маршрута</b>: Монгольский трип 2025'
            f'\n<b>2. Дата</b>: 2025-06-21'
            f'\n<b>3. Маршрут</b>: Уренгой - Уланбатор'
            f'\n<b>4. Расстояние</b>: 12000км'
            f'\n<b>5. Максимальная длительность</b>: 17 дней'
            f'\n<b>6. Описание</b>: Немного отсебятины о маршруте и всем сопутствующем!'

        ),
        parse_mode='HTML'
    )
    # if user_info.status == 'creator' or 'administartor':
    #     await context.bot.send_message(
    #         message_thread_id=update._effective_message.message_thread_id,
    #         chat_id=update.effective_chat.id,
    #         text=f'Tututut'
    #     )


async def answer_trip_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_bikers = await get_all_bikers()
    cur_biker = None
    for biker in all_bikers:
        if biker.user_chat_id == update.message.from_user.id:
            cur_biker = biker
    if not cur_biker:
        cur_biker = await add_one_biker(
            {
                'first_name': update.message.from_user.first_name,
                'username': update.message.from_user.username,
                'user_chat_id': update.message.from_user.id
            }
        )
    if 'set_trip' in update.message.text:
        try:
            await insert_data(update, cur_biker)
            await context.bot.send_message(chat_id=update.message.chat_id, text='Travel\'s added succeful')
        except:
            await context.bot.send_message(chat_id=update.message.chat_id, text='Ошибка при добавлении данных')


async def calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    travels = await get_all_travels()
    for travel in travels:
        res = travel.to_dict()
        print(travel.biker.user_chat_id)
        await context.bot.send_message(chat_id=update.message.from_user.id,
                                       text=(
                                           f'\n<b>ID</b>: {res["id"]} '
                                           f'\n<b>1. Название маршрута</b>: {res["title"]} '
                                           f'\n<b>2. Дата</b>: {res["date"]}'
                                           f'\n<b>3. Маршрут</b>: {res["route"]}'
                                           f'\n<b>4. Расстояние</b>: {res["distance"]}'
                                           f'\n<b>5. Максимальная длительность</b>: {res["trip_time"]}'
                                           f'\n<b>6. Описание</b>: {res["description"]}'
                                           f'\n<b>7. Идейный вдохновитель мероприятия</b>: '
                                           f'<a href="tg://user?id={update.message.from_user.id}">'
                                           f'{update.message.from_user.first_name}</a>'
                                       ),
                                       parse_mode='HTML'
                                       )


async def welcome_new_member(update: Update, context):
    message = (
        f'\U0001F44B {update.message.new_chat_members[0].first_name}! Добро пожаловать в группу {update.message.chat.title}! \U0001F44B'
        f'\n\U0001f3cd\U0000FE0F\U0001f3cd\U0000FE0F\U0001f3cd\U0000FE0F\U0001f3cd\U0000FE0F'
    )

    await context.bot.send_message(chat_id=update.message.chat_id, text=message)
