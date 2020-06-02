from random import random
import math
import matplotlib.pyplot as plt


def msg_counter(lst_count, start, finish, t_window):
    n_window = int(finish // t_window) #в каком окне заявка ушла из очереди
    if len(lst_count) < n_window: #
        for i in range(n_window - len(lst_count)): #
            lst_count.append(0)
    for w in range(int(start // t_window), finish): #
        lst_count[w] += 1


def sinc_count(m):
    q_sinc = []
    d = 0
    t = 0
    m_count = []  # счётчик сообщений
    for i in range(m):  #для каждого сообщения
        u = random()  # генерируем U от 0 до 1
        t += - (math.log(u) / l)  # момент времени прихода нового сообщения
        if len(q_sinc) == 0: #если в очереди ничего нет
            di = msg_proc - ((t+msg_proc) % msg_proc) + msg_proc  #
        else:
            while len(q_sinc) > 0 and t > q_sinc[0]['finish']: #
                q_sinc.pop(0)    #удаляем ненужные нам заявки
            if len(q_sinc) != 0:
                di = q_sinc[len(q_sinc) - 1]['finish'] + msg_proc * 2 - t  #
            else:
                di = msg_proc - ((t+msg_proc) % msg_proc) + msg_proc  #иначе считаем время задержки так, будто у нас заявка только что пришла
        q_sinc.append({'start': t, 'finish': int(t + di - msg_proc)})  # момент прихода заявки
        msg_counter(m_count, q_sinc[len(q_sinc) - 1]['start'], q_sinc[len(q_sinc) - 1]['finish'], msg_proc)
        d += di #увеличиваем суммарную задержку
    md = d / m #ср задержка
    return md, m_count


def asinc_count(m):
    q_asinc = []  # очередь (буффер)
    d = 0  # суммарная задержка
    t = 0  # время
    for i in range(m):  # для каждого сообщения
        u = random()  # генерируем U от 0 до 1
        t += - (math.log(u) / l)  # момент времени прихода нового сообщения
        if len(q_asinc) == 0: #если в очереди ничего нет
            di = msg_proc #то заявка мб сразу обработана
        else:
            while len(q_asinc) > 0 and t > q_asinc[0] + msg_proc:
                q_asinc.pop(0) # удаляет и возвращает последний эл-т из списка
            if len(q_asinc) != 0: #если очередь не пуста
                di = q_asinc[len(q_asinc) - 1] + msg_proc * 2 - t  #
            else: #если все удалили и очередь пуста
                di = msg_proc  #
        q_asinc.append(t + di - msg_proc)  # момент прихода заявки
        d += di  # увеличиваем суммарную задержку
    md = d / m #ср задержка
    return md


m = int(input('Укажите количество сообщений:'))
l = 0.01
msg_proc = 1  # время обработки одного сообщения
l_plot = []  # список для лямбд для построения графика
d_sinc_t = []  # список для M[d(lambda)] теоретическое (синхронная система) для построения графика
d_asinc_t = []  # список для M[d(lambda)] теоретическое (асинхронная система) для построения графика
d_sinc = []  # список для M[d(lambda)] (синхронная система) для построения графика
d_asinc = []  # список для M[d(lambda)] (асинхронная система) для построения графика
n_t = []  # список для M[N(lambda)] теоретическое для построения графика
n = []
while l < 1:
    mn_t = (l * (2 - l)) / (2 * (1 - l))  # M[n(lambda)] теоретическое
    l_plot.append(l)
    md_asinc = asinc_count(m)
    md_sinc, mn = sinc_count(m)
    d_sinc_t.append((mn_t / l) + 0.5)
    d_asinc_t.append(mn_t / l)
    d_sinc.append(md_sinc)
    d_asinc.append(md_asinc)
    n_t.append(mn_t)
    n.append(sum(mn) / len(mn))
    l += 0.01


#plt.plot(1, 2, 1)
plt.figure(1)
plt.plot(l_plot, d_sinc, label="M[D] синхронное практическое")
plt.plot(l_plot, d_sinc_t, label="M[D] синхронное теоретическое")
plt.plot(l_plot, d_asinc, label="M[D] асинхронное практическое")
plt.plot(l_plot, d_asinc_t, label="M[D] асинхронное теоретическое")
plt.title('M[D]', fontstyle="oblique")
plt.ylabel('M[D]', fontstyle="oblique")
plt.xlabel('lambda', fontstyle="oblique")
plt.legend()
plt.figure(2)
#plt.subplot(1, 2, 2)
plt.plot(l_plot, n, label="M[N] практическое")
plt.plot(l_plot, n_t, label="M[N] теоретическое")
plt.title('M[N]', fontstyle="oblique")
plt.ylabel('M[N]', fontstyle="oblique")
plt.xlabel('lambda', fontstyle="oblique")
plt.legend()
plt.show()
