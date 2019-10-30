from math import *

def gen_combination_vector(dim):
	x = []
	for i in range(1,7):
		x.append([i])

	if dim != 1:
		y = []
		for i in gen_combination_vector(dim-1):
			for j in x:
				y.append(i+j)
	else:
		y = x
	return y

def remaining(atk, defe):
	atk.sort(reverse = True)
	defe.sort(reverse = True)
	remaining = len(atk)
	for i in range(min(len(atk), len(defe))):
		if atk[i] <= defe[i]:
			remaining-=1
	return remaining

def gen_base_values():
	final_dict = {}
	for atk in range(1,4):
		final_dict[atk] = {}
		for defe in range(1,4):
			final_dict[atk][defe] = {}
			result = {}
			total = 0
			state_space = gen_combination_vector(atk+defe)
			for i in state_space:
				r = remaining(i[:atk], i[atk:])
				try:
					result[r] += 1
				except KeyError:
					result[r] = 1
				total += 1

			for i in result:
				result[i] /= total
				final_dict[atk][defe][i] = result[i]

	return final_dict

def build_table():
	base_values = gen_base_values()
	final_dict = {}
	for i in range(0,51):
		for j in range(0,51):
			add_to_dict(i, j, final_dict, base_values)
	for i in final_dict:
		for j in final_dict[i]:
			add_stat(final_dict[i][j])
	return final_dict

def add_to_dict(atk, defe, d, b):
	if atk == 0:
		try:
			d[atk][defe] = {0:1}
		except KeyError:
			d[atk] = {}
			d[atk][defe] = {0:1}
		return
	if defe == 0:
		try:
			d[atk][defe] = {0:0, atk:1}
		except KeyError:
			d[atk] = {}
			d[atk][defe] = {0:0, atk:1}
		return

	t_atk = min(3, atk)
	t_defe = min(3, defe)

	min_throw = min(t_atk, t_defe)
	throw = b[t_atk][t_defe]
	min_remaining = min(throw)
	temp = {}

	for i in throw: #i is the number of remaining attackers
		y = d[atk-min_throw+i-min_remaining][defe-i+min_remaining]
		for j in y:
			try:
				temp[j] += y[j]*throw[i]
			except KeyError:
				temp[j] = y[j]*throw[i]

	try:
		d[atk][defe] = temp
	except KeyError:
		d[atk] = {}
		d[atk][defe] = temp

def get_mean(d):
	mean = 0
	for i in d:
		mean += i*d[i]
	return mean
	
def get_second_moment(d):
    moment = 0
    for i in d:
        moment += (i**2) * d[i]
    return moment

def add_stat(d):
	variance = 0
	mean = get_mean(d)
	moment = get_second_moment(d)
	d['mean'] = mean
	d['variance'] = moment - mean**2
	
x = build_table()
while True:
    atk = int(input('Inserisci le armate in attacco, -1 per finire: '))
    if atk == -1:
        break
    defe = int(input('Inserisci le armate in difesa, -1 per finire: '))
    if defe == -1:
        break
    this = x[atk][defe]
    for i in range(atk):
        if i< 10:
            print(' ', end='')
        print(i, end = ': ')
        for j in range(int(this[i]*100)):
            print('|', end = '')
        print('{:.2f}%'.format(this[i]*100))
    print('media: {:.2f}'.format(this['mean']))
    print('deviazione std: {:.3f}'.format(this['variance']**(1/2)))
    
    
'''
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, StringProperty

class Risiko(Widget):
	model = build_table()
	atk = ObjectProperty(None)
	defe = ObjectProperty(None)
	output = StringProperty('')

	def update(self, *kwargs):
		cell = self.model[self.atk.value][self.defe.value]
		win_chance = 1 - cell[0]
		self.output = 'Probabilità di vittoria: {wc:f}\nValore atteso: {mean:f}\nDeviazione standard: {variance:f}'.format\
					(wc=win_chance, mean=cell['mean'], variance = sqrt(cell['variance']))

class RisikoApp(App):
	def build(self):
		game = Risiko()
		Clock.schedule_interval(game.update, 1.0/60.0)
		return game


if __name__ == '__main__':
	RisikoApp().run()
'''