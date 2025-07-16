# 💼 Calculadora de Salário

Uma calculadora de salário completa e interativa, desenvolvida com Python e Tkinter. Suporta diferentes tipos de trabalhadores — **Mensalista**, **Horista** e **Diarista** — com cálculo automático de **INSS**, **IRRF**, **FGTS**, **salário líquido**, além de **horas e minutos extras**.

---

## ✨ Funcionalidades

- 📌 Suporte a 3 tipos de trabalhadores:
  - Mensalista
  - Horista
  - Diarista
- 📊 Cálculo de:
  - Salário Bruto
  - INSS (alíquotas progressivas – 2025)
  - IRRF
  - FGTS (8%)
  - Salário Líquido
  - Valor da Hora e do Minuto
- 🕐 Horas e minutos extras com cálculo proporcional
- ⚠️ Validação de entradas com mensagens de erro amigáveis
- 💻 Interface gráfica leve e intuitiva com Tkinter

---

## 🖼️ Captura de Tela

<img width="653" height="684" alt="image" src="https://github.com/user-attachments/assets/ceb2a364-d79a-4573-a642-fc1316cbdf0d" />

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (interface gráfica nativa do Python)

---

## 🚀 Como Executar

### ✅ Opção 1: Executar via Python (recomendado para desenvolvedores)

> Certifique-se de ter o Python 3.10 ou superior instalado.

```
git clone https://github.com/seu-usuario/calculadora-salario.git
cd calculadora-salario
python -m interface
```

### 🪄 Opção 2: Usar o Executável (Windows)
Baixe o executável diretamente no link abaixo (não precisa instalar Python):

📥 [Download do main.exe](https://github.com/LuisComS8592/Salary_Calculator/releases)

- Dê duplo clique no arquivo main.exe
- Compatível com Windows 10 ou superior (64 bits)
  
## 🧪 Testado com

✅ Python 3.12.0 (Windows)
✅ Tkinter padrão
✅ PyInstaller 6.5 (para gerar o .exe)

## 📂 Estrutura do Projeto

```
Salary_Calculator/
├── calculos.py           # Lógica de cálculo (INSS, IRRF, FGTS, salário bruto/liquido)
├── interface.py          # Interface gráfica com Tkinter
├── main.py               # Ponto de entrada da aplicação (executa a interface)
├── README.md             # Este arquivo
├── .gitignore
```

## 🧾 Licença
Este projeto está licenciado sob a MIT License – veja o arquivo LICENSE para detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Se encontrar algum bug ou tiver ideias de melhoria:

- Faça um fork
- Crie uma branch (git checkout -b feature/nova-funcionalidade)
- Commit suas mudanças (git commit -m 'feat: nova funcionalidade')
- Envie um Pull Request
