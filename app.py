import sqlite3
from datetime import datetime
import sched
import win32api


scheduler = sched.scheduler()


def database():
    conn = sqlite3.connect('agendamento.db')
    c = conn.cursor()
    c.execute('''create table if not exists tbl_agendamento (id INTEGER PRIMARY KEY,
                                                            cliente TEXT,
                                                            data TEXT,
                                                            hora TEXT,
                                                            obs TEXT                                                                                                
    )''')


def agendamento():
    conn = sqlite3.connect('agendamento.db')
    c = conn.cursor()
    cliente = input('Informe o NOME do cliente: ')
    agenda_data = input("Qual a DATA do TREINAMENTO: ")
    agenda_hora = input("Qual a HORÁRIO do TREINAMENTO: ")
    obs = input('Observação: ')

    c.execute('''INSERT INTO tbl_agendamento (cliente, data, hora, obs)
                VALUES (?, ?, ?, ?)''', (cliente, agenda_data, agenda_hora, obs))
    conn.commit()
    print(
        'TREINAMENTO agendado com sucesso para o cliente {} na data {} às {}'.format(cliente, agenda_data, agenda_hora)
    )


def viwer():
    pass


def init():
    conn = sqlite3.connect('agendamento.db')
    c = conn.cursor()

    data = datetime.now()
    data_atual = data.strftime("%d/%m %H:%M")

    for cliente, data_agenda, hora_agenda, obs_agenda in c.execute('SELECT cliente, data, hora, obs '
                                                                   'FROM tbl_agendamento'):
        if data_agenda and hora_agenda in data_atual:
            msg = f'TREINAMENTO AGENDADO COM CLIENTE: {cliente} às {hora_agenda} Observação: {obs_agenda}'
            win32api.MessageBox(0, msg, f'TREINAMENTO COM: {cliente}', 0x00001000)

    scheduler.enter(delay=30, priority=0, action=init)


if __name__ == '__main__':
    init()
    scheduler.run(blocking=True)
