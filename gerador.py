import os
import random
import numpy as np
from scipy.io.wavfile import write
from moviepy.editor import *

audio_folder = "audios/sons_de_felps"
image_folder = "imagens"

nome_do_audio = None

imagem_para_o_audio = "nada"

fps = 25  # frames por segundo
duration = 18000
# duration = 3600
intervalo_minimo = 60
intervalo_maximo = 600

# fps = 25
# duration = 300
# intervalo_minimo = 60
# intervalo_maximo = 100

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
		if f.endswith('.png')
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
	while start_time < duration:
		# escolhe um som aleatório
		sound_path = sound_files if nome_do_audio is not None else random.choice(sound_files)
		sound = AudioFileClip(sound_path)
		sound_duration = sound.duration
		# adiciona o som e o tempo de duração na lista
		sounds.append(sound)
		# adiciona um intervalo de silêncio aleatório
		pause_duration = random.randint(intervalo_minimo, intervalo_maximo)
		intervals.append(pause_duration)
		# atualiza o tempo inicial
		start_time += sound_duration + pause_duration

	# adiciona um último intervalo de silêncio para completar a duração total
	intervals.append(duration - start_time)

	# cria um array de zeros com a duração necessária e salva como arquivo de áudio WAV
	sample_rate = 44100  # taxa de amostragem em Hz
	total_samples = int(duration * sample_rate)
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
			video_clips.extend((ImageClip(imagem_para_o_audio).set_duration(clip.duration), ColorClip((800, 600), color=(0, 0, 0)).set_duration(intervals[i+1])))
		except Exception:
			video_clips.extend((ColorClip((800, 600), color=(0, 0, 0)).set_duration(clip.duration), ColorClip((800, 600), color=(0, 0, 0)).set_duration(intervals[i+1])))
	return concatenate_videoclips(video_clips)
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
		f"output/1_hora_de_silencio_ocasionalmente_interrompido_por_{nome_do_audio}.mp4",
		fps=fps,
		threads=4,
		codec='libx264'
		)
# video.write_videofile(f"output/{nome_do_audio}.mp4", fps=fps, threads=4, codec='libx264')

