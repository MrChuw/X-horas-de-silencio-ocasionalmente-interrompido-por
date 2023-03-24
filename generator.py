import os
import random
import numpy as np
from scipy.io.wavfile import write
from moviepy.editor import *

audio_folder = "input/rick_roll"
image_folder = "imagens/rick_roll"

nome_do_audio = "" or None

imagem_para_o_audio = "" or None

fps = 25  # frames por segundo
# duration = 18000
# # duration = 3600
# intervalo_minimo = 60
# intervalo_maximo = 600
sequencia = True

fps = 25
duration = 30000
intervalo_minimo = 60
intervalo_maximo = 100

sound_files = (
	f"{audio_folder}/{nome_do_audio}.mp3"
	if nome_do_audio is not None
	else [
		os.path.join(audio_folder, f)
		for f in os.listdir(audio_folder)
		if f.endswith('.wav') or f.endswith('.mp3')
	]
)

imagem_para_o_audio = (
	f"imagens/{nome_do_audio}.png" 
	if imagem_para_o_audio is not None 
	else [
		os.path.join(image_folder, f)
		for f in os.listdir(image_folder)
		if f.endswith('.png') or f.endswith('.jpg')
	]
)

def generate_audio():
	# criando uma lista de arquivos de som intercalados com intervalos de silêncio
	# adiciona o primeiro intervalo de silêncio aleatório para não começar ja no audio.
	primeiro_intervalo = random.randint(30, 60)
	intervals = [primeiro_intervalo]  # começa com um intervalo de silêncio
	sounds = []
	start_time = primeiro_intervalo
	del primeiro_intervalo
	i = 0
	while start_time < duration:
		if sequencia == True:
			# escolhe um som da lista na ordem
			sound_path = sound_files[i % len(sound_files)]
			sound = AudioFileClip(sound_path)
			sound_duration = sound.duration
			# adiciona o som e o tempo de duração na lista
			sounds.append(sound)
			# adiciona um intervalo de silêncio aleatório
			pause_duration = random.randint(intervalo_minimo, intervalo_maximo)
			intervals.append(pause_duration)
			# atualiza o tempo inicial
			start_time += sound_duration + pause_duration
			# incrementa o índice da lista de sons
			i += 1
			# se o índice atingir o final da lista, começa novamente do início
			if i == len(sound_files):
				break
		else:
			# escolhe um som aleatório
			sound_path = sound_files if nome_do_audio is not None else random.choice(sound_files)
			sound = AudioFileClip(sound_path)
			sound_duration = sound.duration
			# adiciona o som e o tempo de duração na lista
			sounds.append(sound)
			intervals.append(sound_duration)
			# adiciona um intervalo de silêncio aleatório
			pause_duration = random.randint(intervalo_minimo, intervalo_maximo)
			intervals.append(pause_duration)
			# atualiza o tempo inicial
			start_time += sound_duration + pause_duration

	# adiciona um último intervalo de silêncio para completar a duração total
	if sequencia != True:
		intervals.append(duration - start_time)
	else:
		intervals.append(round(start_time) - start_time)

	# cria um array de zeros com a duração necessária e salva como arquivo de áudio WAV
	sample_rate = 44100  # taxa de amostragem em Hz
	if sequencia != True:
		total_samples = int(duration * sample_rate)
	else:
		total_samples = int(round(start_time) * sample_rate)
	audio_data = np.zeros((total_samples,), dtype=np.int16)
	write("silence.wav", sample_rate, audio_data)

	# carrega o arquivo de áudio de silêncio e concatena com os clipes de som
	silence = AudioFileClip("silence.wav")
	audio_clips = [silence.set_duration(intervals[0])]
	for i, clip in enumerate(sounds):
		audio_clips.extend((clip, silence.set_duration(intervals[i+1])))
	# return concatenate_audioclips(audio_clips)
	return silence, sounds, intervals, concatenate_audioclips(audio_clips)

# função para gerar o vídeo com a tela preta
def generate_video(sounds, intervals, ):
	video_clips = [ColorClip((800, 600), color=(0, 0, 0)).set_duration(intervals[0])]
	for i, clip in enumerate(sounds):
		try:
			imagem = clip.filename.split("\\")[1].replace(".mp3", ".jpg").replace(".mp3", ".png")
			video_clips.extend((ImageClip(f'{image_folder}/{imagem}').set_duration(clip.duration), ColorClip((800, 600), color=(0, 0, 0)).set_duration(intervals[i+1])))
		except Exception:
			video_clips.extend((ColorClip((800, 600), color=(0, 0, 0)).set_duration(clip.duration), ColorClip((800, 600), color=(0, 0, 0)).set_duration(intervals[i+1])))
	return concatenate_videoclips(video_clips, method="compose")
	# return ColorClip((800, 600), color=(0, 0, 0)).set_duration(duration)

silence, sounds, intervals, audio_clip = generate_audio()
video_clip = generate_video(sounds, intervals, )
# combinação do vídeo com o áudio
video = video_clip.set_audio(audio_clip)

# salvando o vídeo
if nome_do_audio is None:
	video.write_videofile(
		"output/1_hora_de_silencio_ocasionalmente_interrompido_por_INSERIRNONEAQUI.mp4",
		fps=fps,
		threads=4,
		codec='libx264',
	)
else:
	video.write_videofile(
		f"output/1_hora_de_silencio_ocasionalmente_interrompido_por_{nome_do_audio}teste.mp4",
		fps=fps,
		threads=4,
		codec='libx264'
		)
# video.write_videofile(f"output/{nome_do_audio}.mp4", fps=fps, threads=4, codec='libx264')

