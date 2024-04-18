# InoaChallenge

O objetivo do sistema é auxiliar um investidor nas suas decisões de comprar/vender ativos. Para tal, o sistema deve registrar periodicamente a cotação atual de ativos da B3 e também avisar, via e-mail, caso haja oportunidade de negociação.

Os seguintes requisitos funcionais são necessários:

Expor uma interface web para permitir que o usuário configure:

- os ativos da B3 a serem monitorados;
- os parâmetros de túnel de preço (www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/regras-e-parametros-de-negociacao/tuneis-de-negociacao) de cada ativo;
- a periodicidade da checagem (em minutos) de cada ativo.
- O sistema deve obter e armazenar as cotações dos ativos cadastrados de alguma fonte pública qualquer, respeitando a periodicidade configurada por ativo.
- A interface web deve permitir consultar os preços armazenados dos ativos cadastrados.
- Enviar e-mail para o investidor sugerindo a compra sempre que o preço de um ativo monitorado cruzar o seu limite inferior do túnel, e sugerindo a venda sempre que o preço de um ativo monitorado cruzar o seu limite superior do túnel

The system's goal is to assist an investor in making buy/sell decisions for assets. To achieve this, the system must periodically record the current price of assets from B3 and also notify, via email, if there is a trading opportunity.

/

The following functional requirements are necessary:

- The assets from B3 to be monitored.
- The price tunnel parameters (www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-participantes-e-traders/regras-e-parametros-de-negociacao/tuneis-de-negociacao) for each asset.
- The frequency of checking (in minutes) for each asset.
- The system must retrieve and store the prices of registered assets from any public source, respecting the configured frequency per asset.
- The web interface should allow querying the stored prices of registered assets.
- Send an email to the investor suggesting a purchase whenever the price of a monitored asset crosses its lower tunnel limit, and suggesting a sale whenever the price of a monitored asset crosses its upper tunnel limit.

## Sumário / Table of Contents

1. [Instalação / Installation](#instalação--installation)
2. [Uso / Usage](#uso--usage)
3. [Escolhas no desenvolvimento / Development Choices](#escolhas-no-desenvolvimento--development-choices)

## Instalação / Installation

Na pasta em que o arquivo manage.py está, digite o comando abaixo para instalar todas as dependências do projeto / In the folder that the file manage.py is, type the following command to install all the dependicies

```
python -m pip install -r requirements.txt
```

Para adicionar os serviços de crontab necessarios digite / To add all the crontab services needed type

```
python manage.py crontab add
```

Para remover basta digitar o comando / To remove just type the command

```
python manage.py crontab remove
```

Para conseguir enviar os emails é necessário configurar as seguintes variáveis dentro do arquivo inoaChallenge/settings.py / In order to be able to send email's it's necessary to configure the following variables inside the file inoaChallenge/settings.py

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '<HOST>'
EMAIL_PORT = '<PORT>'
EMAIL_HOST_USER = '<USER>'
EMAIL_HOST_PASSWORD = '<PASSWORD>'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
```

## Uso / Usage

Para iniciar o servidor do projeto basta digitar / To start the server of the project just type

```
python manage.py runserver
```

## Escolhas no desenvolvimento / Development Choices

Bibliotecas escolhidas durante o desenvolvimento / Libraries chosen during development

- yfinance - Usado para adquirir informações e valores dos ativos pedidos / Used to aquire information and values of the assets

- django-crontab - Usado para executar tarefas de verificar preços dos ativos para mandar email e também para atualizar os preços diários dos ativos / Used to execute tasks to verify the prices of the assets and then send email and to update the prices of the assets

- django-chartjs - Usado para mostrar os gráficos dos preços das ações / Used to show the prices of the assets in charts

Decisões tomadas / Decisions

- Para simular valores em tempo real, dado que o yfinance não fornece dados em tempo real, ajustamos as datas do dia anterior para refletir os valores como se fossem do dia atual. Isso nos permite uma simulação dos dados em tempo real / To simulate real-time values, since yfinance doesn't provide real-time data, we adjusted the dates from the previous day to reflect the values as if they were from today. This allows us to simulate real-time data reception
