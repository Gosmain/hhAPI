from hh_api.hh_api import HeadHunterAPI
from hh_api.hh_params import HeadHunterParametersForRequest
from hh_api.hh_data_process import HeadHunterDataProcessing as hhdp
from configs import config
from hh_working_files.hh_scribe import HHScribe
from hh_working_files.hh_inspector import HHInspector
import os
import telebot

bot = telebot.TeleBot(os.environ['TOKEN'])


@bot.message_handler(content_types=['text'])
def get_text_messages(message, ):
  '''Метод для обработки сообщение в телеграм.
  
  :param message: сообщение от пользователя
  '''

  if message.text.lower() == "получить вакансии":

    with open('vacancies.txt', 'r') as f:

      for line in f.readlines():

        bot.send_message(message.from_user.id, line)

  elif message.text.lower() == "обновить вакансии":

    HHScribe.clear_file('vacancies.txt')
    HHScribe.clear_file('req.txt')

    hh = HeadHunterAPI()

    for key in config.KEY_WORDS:

      params = HeadHunterParametersForRequest.vacancies(key, '1')

      for element in hh.vacancies(params):

        string = f'{hhdp.get_name(element)} {hhdp.get_salary_value(element)} {hhdp.get_salary_currency(element)} {hhdp.get_link(element)}\n'

        if HHInspector.check_string('vacancies.txt', string):
          HHScribe.write_down('vacancies.txt', string)
          HHScribe.write_down('req.txt', f'{hhdp.get_requirement(element)}\n')

    bot.send_message(message.from_user.id, "вакансии обновлены")
