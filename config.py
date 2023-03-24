import random

######################[Configuracoes]######################


# qual =  "Audio aleatório sem imagens"
# qual =  "Audio aleatório sem imagens com duração"
# qual =  "Audio aleatório com imagens"
# qual =  "Audio aleatório com imagens com duração"
# qual =  "Vídeo aleatório para áudio"
# qual =  "Vídeo aleatório para áudio com duração"
# qual =  "Vídeo aleatório para áudio com prints"
# qual =  "Vídeo aleatório para áudio com duração e prints"
# qual =  "Vídeo aleatório para áudio com prints selecionados"
# qual =  "Vídeo aleatório para áudio com duração e prints selecionados"
# qual =  "Vídeo aleatório para vídeo"
qual =  "Vídeo aleatório para vídeo com duração"

aleatorio = "sim"

# completo_ou_duracao = "completo"
completo_ou_duracao = "duração"

# dividir_a_cada = 25
dividir_a_cada = "aleatorio"

intervalo_minimo_dividir = 10
intervalo_maximo_dividir = 60

duracao = 18000
intervalo_minimo = 30
intervalo_maximo = 50
# intervalo_maximo = 100
primeiro_intervalo_tempo = random.randint(30, 60)


# nome_do_arquivo = "the_caretaker2"
# sub_pagina_do_arquivo = "the_caretaker"

nome_do_arquivo = "Worlds End Valentine"
sub_pagina_do_arquivo = "omori"


pagina_do_arquivo = f"input_raw/{sub_pagina_do_arquivo}"
local_do_arquivo = f"input_raw/{sub_pagina_do_arquivo}/{nome_do_arquivo}"


salvar_em =f"output/{nome_do_arquivo}"

sample_rate = 44100


imagem_path = "imagens"
sub_pagina_das_imagens = "persona"
pagina_das_imagens = "imagens/persona"




