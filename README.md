# <p align="center"><b>Ward - Sistema de automação de faturamento.</b></p>
  ![alt text](/img/logo.png)
  
  
## Conteúdo
- [ Descrição ](#desc)
- [ Autores ](#autores)
- [ Histórias dos usuários ](#hist)
- [ Diagrama UML ](#uml)
- [ Fromatos de Arquivo ](#excel)


<a name="desc"></a>
## Descrição

O projeto tem a ideia de construir uma API visando a automação no processo de criação e fechamento de faturas de microempresas  
ou profissionais autônomos, buscando a economia de tempo e eficiência, para assim gerar mais produtividade a essas entidades.  
Também garantindo que o cliente final receba sua cobrança de forma simples, rápida e em dia.


A automação consiste no consumo de um arquivo de excel base, onde o usuário irá definir quais os insumos, produtos ou qualquer outros materiais presentes em seu estoque, com seus devidos preços de custo. Em seguida, o usuário poderá subir outros arquivos com os itens que estão sendo consumidos, para cada um de seus clientes. Dessa forma, o sistema irá atualizar seu estoque e, ao final da data de fechamento de fatura (escolhida pelo usuário), irá enviar a fatura completa para cada um dos clientes propostos pelo usuário.

Todos os formatos de envio de arquivo excel estão disponíveis em seguida.


<a name="autores"></a>
## Autores

- [@Giovanni Montevechi](https://www.github.com/GiovanniMP)
- [@Rodrigo Camargo](https://github.com/RSiCamargo)


<a name="hist"></a>
## Histórias dos usuários

Como <b>administrador do processo</b>, eu quero que a API execute as requisições feitas pelos usuários de forma adequada, chamando o os processos adequados para cada requisições, e retornando os valores de acordo, para que,
no final dos períodos propostos, os faturamentos sejam gerados de forma consistente.

#### Critérios de aceitação:
- As requisições devem ser feitas de acordo com as solicitações.
- Apenas usuários qualificados podem realiza-las.
- Todos os dados de cada cliente devem ser guardados no banco corretamente.
- Os fechamentos devem ser realizados de acordo com as datas propostas pelos usuários, para cada cliente.

#### Story Points: 13

</br>
</br>

Como <b>usuário do sistema</b>, eu gostaria que o sistema consumisse todos os dados enviados pelo excel, uma vez respeitando todos os critérios disponível, e por fim associando esses dados ao meu perfil, para que eu seja capaz
de manter em ordem todo o meu inventário.

#### Critérios de aceitação:
- O excel deve ser consumido armazenando todas as informações em seus devidos locais
- As informações devem ser associadas ao perfil do usuário identificado.

#### Story Points: 3

</br>
</br>

Como <b>usuário do sistema</b>, gostaria que conforme forem enviados arquivos contendo o consumo do meu estoque (para cada cliente), o sistema trate de forma adequada o fluxo de insumos para o faturamento, e atualize meu estoque.

#### Critérios de aceitação:
- O excel deve ser consumido armazenando todas as informações em seus devidos locais
- O estoque do usuário deverá ser atualizado de acordo com a utilização dos insumos declarados no excel

#### Story Points: 2

</br>
</br>

Como <b>usuário do sistema</b>, eu queria que o sistema gerasse o faturamento com a possibilidade de pagamento via pix para meus clientes.

#### Critérios de aceitação:
- Deverá ser associado ao faturamento o redirecionamento para o pagamento pix (via url ou qr code) já com as informações do usuário e a quantia relativa à cobrança.

#### Story Points: 3

</br>
</br>

Como <b>usuário do sistema</b>, 

#### Critérios de aceitação:


#### Story Points: 

</br>
</br>

Como <b>usuário do sistema</b>, 

#### Critérios de aceitação:


#### Story Points: 

</br>
</br>

Como <b>cliente final do usuário</b>, 

#### Critérios de aceitação:


#### Story Points: 




<a name="uml"></a>
## Diagrama UML

![Diagrama UML](link)


<a name="excel"></a>
## Formatos aceitos de Excel

Serão adicionados futuramente.
