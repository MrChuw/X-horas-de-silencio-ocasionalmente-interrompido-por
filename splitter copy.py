from moviepy.editor import ImageClip, AudioFileClip, ColorClip, VideoFileClip, concatenate_videoclips
import random
import os
import numpy as np
from scipy.io.wavfile import write
import humanize
import datetime as dt
import timeit
import time
from config import qual, aleatorio, dividir_a_cada, duracao, intervalo_minimo, intervalo_maximo, primeiro_intervalo_tempo, nome_do_arquivo, pagina_do_arquivo, salvar_em, sample_rate, pagina_das_imagens
humanize.i18n.activate("pt_BR")

"""
Opções:
OPÇÕES ONDE O AUDIO É COLOCADO DE FORMA ALEATÓRIA:

Áudio aleatório sem imagens:
- Completo, cortado em intervalos definidos por "dividir_a_cada" e colocado aleatoriamente em "X horas de silêncio".
- O áudio só termina quando não houver mais clipes de áudio.

Áudio aleatório sem imagens com duração:
- Cortado em intervalos definidos por "dividir_a_cada" e colocado aleatoriamente em "X horas de silêncio".
- O áudio termina quando a duração máxima for atingida.
- Pode ser usado para criar o clássico "X horas de silêncio".

Áudio aleatório com imagens:
- Cortado em intervalos definidos por "dividir_a_cada" e colocado aleatoriamente em "X horas de silêncio".
- O áudio só termina quando não houver mais clipes de áudio.
- As imagens serão usadas em sequência se houver mais de uma.

Áudio aleatório com imagens com duração:
- Cortado em intervalos definidos por "dividir_a_cada" e colocado aleatoriamente em "X horas de silêncio".
- O áudio termina quando a duração máxima for atingida.
- Pode ser usado para criar o clássico "X horas de silêncio".
- As imagens serão usadas em sequência se houver mais de uma.

Vídeo aleatório para áudio:
- O vídeo é cortado em intervalos definidos por "dividir_a_cada" e colocado aleatoriamente em "X horas de silêncio" para se tornar um arquivo de áudio.
- O áudio só termina quando não houver mais clipes de áudio.

Vídeo aleatório para áudio com duração:
- O vídeo é cortado em intervalos definidos por "dividir_a_cada" e colocado aleatoriamente em "X horas de silêncio" para se tornar um arquivo de áudio.
- O áudio termina quando a duração máxima for atingida.
- Pode ser usado para criar o clássico "X horas de silêncio".

Vídeo aleatório para áudio com imagens:
- Semelhante ao "Áudio aleatório com imagens", mas começa com um vídeo em vez de um arquivo de áudio.

Vídeo aleatório para áudio com imagens e duração:
- Semelhante ao "Áudio aleatório com imagens com duração", mas começa com um vídeo em vez de um arquivo de áudio.

Vídeo aleatório para áudio com imagens e seleção:
- Semelhante ao "Áudio aleatório com imagens", mas permite a seleção de imagens específicas.

Vídeo aleatório para áudio com imagens, duração e seleção:
- Semelhante ao "Áudio aleatório com imagens com duração", mas permite a seleção de imagens específicas.

Vídeo aleatório para vídeo:
- Semelhante ao "Áudio aleatório com imagens", mas usa o clip do video passado.

Vídeo aleatório para vídeo com duração:
- Semelhante ao "Áudio aleatório com imagens com duração", mas usa o clip do video passado.


"""



# Áudio sem imagem pelo tempo do clip mais o silencio # Feito
# Áudio sem imagem por tempo predeterminado # Feito
# Áudio com imagem(s) pelo tempo do clip mais o silencio # Feito
# Áudio com imagem(s) por tempo predeterminado # Feito
# Vídeo sem imagem(s) pelo tempo do clip mais o silencio # Feito
# Vídeo sem imagem(s) por tempo predeterminado # Feito
# Vídeo com imagem(s) pelo tempo do clip mais o silencio # Feito
# Vídeo com imagem(s) por tempo predeterminado # Feito
# Vídeo para áudio com prints selecionados # Feito
# Vídeo para vídeo pelo tempo do clip mais o silencio  # Feito
# Vídeo para vídeo por tempo predeterminado  # Feito
# ------------------------------------------
# Vários arquivos de input
# Vários áudios para áudio # TODO:
# Etc # TODO:
# E só pelo rolê, pegar tudo e criar um Full length



arquivos = [
		os.path.join(pagina_do_arquivo, f)
		for f in os.listdir(pagina_do_arquivo)
		if f.split(".")[0] in nome_do_arquivo
	]


imagens = [
		os.path.join(pagina_das_imagens, f)
		for f in os.listdir(pagina_das_imagens)
	]

fps = 30
black_clip = ColorClip((800, 600), color=(0, 0, 0))

def audio_splitter(aleatorio):
	# abre a música
	musica = AudioFileClip(arquivos[0])

	# calcula a duração da música
	duracao_total = musica.duration

	# divide a música em trechos de tempo pré-determinados
	clipes = []
	for i in range(0, int(duracao_total), dividir_a_cada):
		# define o intervalo de tempo do trecho
		inicio = i
		fim = i + dividir_a_cada
		fim = min(fim, duracao_total)
		# if fim > duracao_total:
		# 	fim = duracao_total
		# recorta o trecho da música
		clipes.append(musica.subclip(inicio, fim))

		# salva o trecho em um arquivo separado
		# nome_arquivo = f"trecho_{i}.mp3"
		# trecho.write_audiofile(f"{salvar_em}/{nome_arquivo}", fps=44100, nbytes=2, bitrate="192k")
	if aleatorio == "sim":
		random.shuffle(clipes)
	return clipes

def video_splitter(aleatorio):
	_inicio = time.time()
	# abre a música
	video = VideoFileClip(arquivos[0])

	# calcula a duração da música
	duracao_total = video.duration

	clipes = []

	# divide a música em trechos de tempo pré-determinados
	for i in range(0, int(duracao_total), dividir_a_cada):
		# define o intervalo de tempo do trecho
		inicio = i
		fim = i + dividir_a_cada
		fim = min(fim, duracao_total)
		# if fim > duracao_total:
		# 	fim = duracao_total
		# recorta o trecho da música
		clipes.append(video.subclip(inicio, fim))
	if aleatorio == "sim":
		random.shuffle(clipes)
	_final = time.time()
	print(humanize.precisedelta(dt.timedelta(seconds=int(_final - _inicio))))
	return clipes

def gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, start_time=0, ordenado_ou_duracao="ordenado"):
	intervals = [primeiro_intervalo_tempo]
	if ordenado_ou_duracao == "ordenado":
		for sound in clipes:
			sound_duration = sound.duration
			pause_duration = random.randint(intervalo_minimo, intervalo_maximo)
			intervals.append(pause_duration)
			start_time += sound_duration + pause_duration
	else:
		while start_time < duracao:
			for sound in clipes:
				sound_duration = sound.duration
				pause_duration = random.randint(intervalo_minimo, intervalo_maximo)
				intervals.append(pause_duration)
				start_time += sound_duration + pause_duration
				if start_time > duracao:
					break
	[intervals.append(random.randint(intervalo_minimo, intervalo_maximo)) for _ in range(10)]
	print(humanize.precisedelta(dt.timedelta(seconds=int(start_time))))
	return intervals, start_time

def gerar_silencio(start_time):
	total_samples = int(round(start_time) * sample_rate)
	audio_data = np.zeros((total_samples,), dtype=np.int16)
	write("silence.wav", sample_rate, audio_data)
	return AudioFileClip("silence.wav")

def gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada=None, ordenado_ou_duracao="ordenado"):
	video_clips = [(black_clip.set_duration(intervals[0])).set_audio(silence.set_duration(intervals[0]))]
	_duracao = 0
	if imagem_video_nada is None:
		for i, clip in enumerate(clipes):
			intervalo = intervals[i % len(intervals)]
			_duracao += clip.duration + intervalo
			video_clips.extend([
				(black_clip.set_audio(clip)).set_duration(clip.duration),
				(black_clip.set_duration(intervalo)).set_audio(silence.set_duration(intervalo))
			])
			if _duracao > duracao and ordenado_ou_duracao == "duracao":
				break
	elif imagem_video_nada == "imagem":
		if len(imagens) == 1:
			for i, clip in enumerate(clipes):
				intervalo = intervals[i % len(intervals)]
				_duracao += clip.duration + intervalo
				video_clips.extend([
					(ImageClip(imagens[0]).set_audio(clip)).set_duration(clip.duration),
					(black_clip.set_duration(intervalo)).set_audio(silence.set_duration(intervalo))
				])
				if _duracao > duracao and ordenado_ou_duracao == "duracao":
					break
		else:
			for i, clip in enumerate(clipes):
				imagem = imagens[i % len(imagens)]  # índice da imagem a ser usada
				intervalo = intervals[i % len(intervals)]
				_duracao += clip.duration + intervalo
				video_clips.extend([
					(ImageClip(imagem).set_audio(clip)).set_duration(clip.duration),
					(black_clip.set_duration(intervalo)).set_audio(silence.set_duration(intervalo))
				])
				if _duracao > duracao and ordenado_ou_duracao == "duracao":
					break
	elif imagem_video_nada == "imagem do video":
		for i, clip in enumerate(clipes):
			intervalo = intervals[i % len(intervals)]
			_duracao += clip.duration + intervalo
			video_clips.extend([
				clip.to_ImageClip(t=0).set_audio(clip.audio).set_duration(clip.duration), 
				(black_clip.set_duration(intervalo)).set_audio(silence.set_duration(intervalo))])
			if _duracao > duracao and ordenado_ou_duracao == "duracao":
				break
	elif imagem_video_nada == "video":
		for i, clip in enumerate(clipes):
			intervalo = intervals[i % len(intervals)]
			_duracao += clip.duration + intervalo
			video_clips.extend([
				clip.set_audio(clip.audio).set_duration(clip.duration), 
				(black_clip.set_duration(intervalo)).set_audio(silence.set_duration(intervalo))])
			if _duracao > duracao and ordenado_ou_duracao == "duracao":
				break

	return video_clips

def audio_sem_imagem_audio_completo():
	start_time = primeiro_intervalo_tempo
	clipes = audio_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="ordenado")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, ordenado_ou_duracao="ordenado")
	return concatenate_videoclips(video_clips, method="compose")

def audio_sem_imagem_duracao():
	start_time = primeiro_intervalo_tempo
	clipes = audio_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="duracao")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, ordenado_ou_duracao="ordenado")
	return concatenate_videoclips(video_clips, method="compose")

def audio_com_imagem_audio_completo():
	start_time = primeiro_intervalo_tempo
	clipes = audio_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="ordenado")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada="imagem", ordenado_ou_duracao="ordenado")
	return concatenate_videoclips(video_clips, method="compose")

def audio_com_imagem_duracao():
	start_time = primeiro_intervalo_tempo
	clipes = audio_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="duracao")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada="imagem", ordenado_ou_duracao="duracao")
	return concatenate_videoclips(video_clips, method="compose")

def video_para_audio_completo():
	start_time = primeiro_intervalo_tempo
	clipes = video_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="ordenado")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada=None, ordenado_ou_duracao="ordenado")
	return concatenate_videoclips(video_clips, method="compose")

def video_para_audio_duracao():
	start_time = primeiro_intervalo_tempo
	clipes = video_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="duracao")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada=None, ordenado_ou_duracao="duracao")
	return concatenate_videoclips(video_clips, method="compose")

def video_para_audio_completo_com_prints():
	start_time = primeiro_intervalo_tempo
	clipes = video_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="ordenado")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada="imagem do video", ordenado_ou_duracao="ordenado")
	return concatenate_videoclips(video_clips, method="compose")

def video_para_audio_duracao_com_prints():
	start_time = primeiro_intervalo_tempo
	clipes = video_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="duracao")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada="imagem do video", ordenado_ou_duracao="duracao")
	return concatenate_videoclips(video_clips, method="compose")

def video_para_audio_completo_com_prints_selecionados():
	start_time = primeiro_intervalo_tempo
	clipes = video_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="ordenado")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada="imagem", ordenado_ou_duracao="ordenado")
	return concatenate_videoclips(video_clips, method="compose")

def video_para_audio_duracao_com_prints_selecionados():
	start_time = primeiro_intervalo_tempo
	clipes = video_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="ordenado")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada="imagem", ordenado_ou_duracao="ordenado")
	return concatenate_videoclips(video_clips, method="compose")

def video_em_ordem_completo():
	start_time = primeiro_intervalo_tempo
	clipes = video_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="ordenado")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada="video", ordenado_ou_duracao="ordenado")
	return concatenate_videoclips(video_clips, method="compose")

def video_em_ordem_duracao():
	start_time = primeiro_intervalo_tempo
	clipes = video_splitter(aleatorio)
	intervals, start_time = gerar_intervalo_time(clipes, duracao, intervalo_minimo, intervalo_maximo, ordenado_ou_duracao="duracao")
	silence = gerar_silencio(start_time)
	video_clips = gerar_video_clips(clipes, intervals, silence, black_clip, imagem_video_nada="video", ordenado_ou_duracao="duracao")
	return concatenate_videoclips(video_clips, method="compose")

def criar_video():
	# define the functions for each value of qual
	FUNCTIONS = {
		"Audio aleatório sem imagens": audio_sem_imagem_audio_completo,
		"Audio aleatório sem imagens com duração": audio_sem_imagem_duracao,
		"Audio aleatório com imagens": audio_com_imagem_audio_completo,
		"Audio aleatório com imagens com duração": audio_com_imagem_duracao,
		"Vídeo aleatório para áudio": video_para_audio_completo,
		"Vídeo aleatório para áudio com duração": video_para_audio_duracao,
		"Vídeo aleatório para áudio com prints": video_para_audio_completo_com_prints,
		"Vídeo aleatório para áudio com duração e prints": video_para_audio_duracao_com_prints,
		"Vídeo aleatório para áudio com prints selecionados": video_para_audio_completo_com_prints_selecionados,
		"Vídeo aleatório para áudio com duração e prints selecionados": video_para_audio_duracao_com_prints_selecionados,
		"Vídeo aleatório para vídeo": video_em_ordem_completo,
		"Vídeo aleatório para vídeo com duração": video_em_ordem_duracao,
	}

	# define the output filenames for each value of qual
	OUTPUT_NAMES = {
		"Audio aleatório sem imagens": "todos_os_clips_sem_imagens",
		"Audio aleatório sem imagens com duração": "por_duracao_sem_imagens",
		"Audio aleatório com imagens": "todos_os_clips_com_imagens",
		"Audio aleatório com imagens com duração": "por_duracao_com_imagens",
		"Vídeo aleatório para áudio": "video_para_todos_os_clips_sem_imagens",
		"Vídeo aleatório para áudio com duração": "video_por_duracao_clips_sem_imagens",
		"Vídeo aleatório para áudio com prints": "video_para_todos_os_clips_com_imagens",
		"Vídeo aleatório para áudio com duração e prints": "video_por_duracao_clips_com_imagens",
		"Vídeo aleatório para áudio com prints selecionados": "video_para_todos_os_clips_com_imagens_selecionados",
		"Vídeo aleatório para áudio com duração e prints selecionados": "video_por_duracao_clips_com_imagens_selecionados",
		"Vídeo aleatório para vídeo": "video_para_todos_os_clips_para_video",
		"Vídeo aleatório para vídeo com duração": "video_por_duracao_para_video",
	}



	function = FUNCTIONS[qual]
	output_name = OUTPUT_NAMES[qual]

	if "completo" in qual:
		completo_ou_duracao = "completo"
	elif "duração" in qual:
		completo_ou_duracao = "completo"

	video = function(completo_ou_duracao)

	horas = humanize.precisedelta(dt.timedelta(seconds=int(video.duration)))
	# nome_horas = f"{horas} hora" if horas == 1 else f"{horas} horas"
	nome_horas = horas.replace(" ", "_").replace(",", "")

	# video.write_videofile(
	# 	f"{salvar_em}/{nome_horas}_de_silencio_ocasionalmente_interrompido_por_{nome_do_arquivo}_{output_name}.mp4",
	# 	fps=fps,
	# 	threads=4,
	# 	codec='libx264',
	# )

	# Cria a pasta se ela não existir
	if not os.path.exists(salvar_em):
		os.makedirs(salvar_em)

	# Cria uma pasta dentro da subpasta com o nome do arquivo se ela não existir
	if not os.path.exists(f"{salvar_em}/{nome_do_arquivo}"):
		os.makedirs(f"{salvar_em}/{nome_do_arquivo}")

	# Verifica se já existe um arquivo com o mesmo nome e adiciona um número ao final
	# se necessário para evitar arquivos repetidos
	num = 1
	while os.path.exists(f"{salvar_em}/{nome_horas}_de_silencio_ocasionalmente_interrompido_por_{nome_do_arquivo}_{output_name}_{num}.mp4"):
		num += 1
	nome_final = f"{salvar_em}/{nome_do_arquivo}/{nome_horas}_de_silencio_ocasionalmente_interrompido_por_{nome_do_arquivo}_{output_name}_{num}.mp4"

	video.write_videofile(
		f"{nome_final}",
		fps=fps,
		threads=4,
		codec='libx264',
	)
	return True

tempo = timeit.timeit(criar_video, number=1)
print(tempo)
print(humanize.precisedelta(dt.timedelta(seconds=int(tempo))))

print(tempo)


# _inicio = time.time()
# # abre a música
# video = VideoFileClip(arquivos[0])

# # calcula a duração da música
# duracao_total = video.duration

# metade = duracao_total / 2

# clipes = []

# # divide a música em trechos de tempo pré-determinados
# for i in range(0, int(duracao_total), round(metade)):
# 	# define o intervalo de tempo do trecho
# 	inicio = i
# 	fim = i + metade
# 	fim = min(fim, duracao_total)
# 	# if fim > duracao_total:
# 	# 	fim = duracao_total
# 	# recorta o trecho da música
# 	clipes.append(video.subclip(inicio, fim))
# _final = time.time()
# print(humanize.precisedelta(dt.timedelta(seconds=int(_final - _inicio))))


# clipes[0].write_videofile("input_raw/the_caretaker/the_caretaker1.mp4", fps=fps, threads=4, codec='libx264')
# clipes[1].write_videofile("input_raw/the_caretaker/the_caretaker2.mp4", fps=fps, threads=4, codec='libx264')
