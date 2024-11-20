import pandas as pd
from datetime import datetime, timedelta
import random

num_linhas = 78654

data = {
    "ID": list(range(1, num_linhas + 1)),
    "Data_Verificação": [datetime.now() - timedelta(days=random.randint(0, 30)) for _ in range(num_linhas)],
    "Tipo_verificação": [random.choice(["Texto", "Imagem", "Vídeo", "Áudio"]) for _ in range(num_linhas)],
    "Categoria_Conteudo": [random.choice(["Política", "Saúde", "Economia", "Esportes", "Educação"]) for _ in range(num_linhas)],
    "Resultado_Verificação": [random.choice(["Verdadeiro", "Falso", "Indeterminado"]) for _ in range(num_linhas)],
    "Fonte_Informação": [random.choice(["WhatsApp", "Facebook", "Twitter", "Instagram", "Outros"]) for _ in range(num_linhas)]
}

df = pd.DataFrame(data)

file_path = 'seu_arquivo3.xlsx'
df.to_excel(file_path, index=False)

print(f"Arquivo '{file_path}' criado com sucesso!")
