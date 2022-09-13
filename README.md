# <p align="center"><b>Ward - Sistema de automação de faturamento.</b></p>
  ![logo](/img/logo.png)
  
  
## Conteúdo
- [ Descrição ](#desc)
- [ Autores ](#autores)
- [ Histórias dos usuários ](#hist)
- [ Diagrama UML ](#uml)
- [ Formatos de Arquivo ](#excel)


<a name="desc"></a>
## Descrição

O projeto tem a ideia de construir uma API visando a automação no processo de criação e fechamento de faturas de microempresas ou profissionais autônomos, buscando a economia de tempo e eficiência, para assim gerar mais produtividade a essas entidades. Também garantindo que o cliente final receba sua cobrança de forma simples, rápida e em dia.


A automação consiste no consumo de um arquivo de excel base, onde o usuário irá definir quais os insumos, produtos ou qualquer outros materiais presentes em seu estoque, com seus devidos preços de custo. Em seguida, o usuário poderá subir outros arquivos com os itens que estão sendo consumidos, para cada um de seus clientes. Dessa forma, o sistema irá atualizar seu estoque e, ao final da data de fechamento de fatura (escolhida pelo usuário), irá enviar a fatura completa para cada um dos clientes propostos pelo usuário.

Todos os formatos de envio de arquivo excel estão disponíveis em seguida.


<a name="autores"></a>
## Autores

- [@Giovanni Montevechi](https://www.github.com/GiovanniMP)
- [@Rodrigo Camargo](https://github.com/RSiCamargo)


<a name="hist"></a>
## Histórias dos usuários

Como <b>administrador do processo</b>, eu quero que a API execute as requisições feitas pelos usuários de forma adequada, chamando os processos adequados para cada requisição, e retornando os valores de acordo, para que, no final dos períodos propostos, os faturamentos sejam gerados de forma consistente.

#### Critérios de aceitação:
- As requisições devem ser feitas de acordo com as solicitações.
- Apenas usuários qualificados podem realiza-las.
- Todos os dados de cada cliente devem ser guardados no banco corretamente.
- Os fechamentos devem ser realizados de acordo com as datas propostas pelos usuários, para cada cliente.
- - Devem ser gerados logs para controle das etapas.

#### Story Points: 13

</br>
</br>

Como <b>usuário do sistema</b>, eu gostaria que o sistema consumisse todos os dados enviados pelo excel, uma vez respeitando todos os critérios disponíveis e por fim, associando esses dados ao meu perfil para que eu seja capaz de manter em ordem todo o meu inventário.

#### Critérios de aceitação:
- O excel deve ser consumido armazenando todas as informações em seus devidos locais.
- As informações devem ser associadas ao perfil do usuário identificado.

#### Story Points: 3

</br>
</br>

Como <b>usuário do sistema</b>, gostaria que conforme forem enviados arquivos contendo o consumo do meu estoque (para cada cliente), o sistema trate de forma adequada o fluxo de insumos para o faturamento, e atualize meu estoque.

#### Critérios de aceitação:
- O excel deve ser consumido armazenando todas as informações em seus devidos locais.
- O estoque do usuário deverá ser atualizado de acordo com a utilização dos insumos declarados no excel.

#### Story Points: 2

</br>
</br>

Como <b>usuário do sistema</b>, eu gostaria que o sistema gerasse o faturamento com a possibilidade de pagamento via pix para meus clientes.

#### Critérios de aceitação:
- Deverá ser associado ao faturamento o redirecionamento para o pagamento pix (via url ou qr code) já com as informações do usuário e a quantia relativa à cobrança.

#### Story Points: 3

</br>
</br>

Como <b>usuário do sistema</b>, eu gostaria que assim que o faturamento dos clientes fechar (nas datas escolhidas por mim), ele seja enviado tanto para o email do cliente, como também uma cópia à mim.

#### Critérios de aceitação:
- O faturamento, de cada cliente, deve fechar na data escolhida pelo usuário.
- Ao fechar, deve ser enviado para o email do cliente (email passado pelo usuário).
- O usuário deve receber também uma cópia de todos os faturamentos.

#### Story Points: 3

</br>
</br>

Como <b>usuário do sistema</b>, assim que meu estoque estiver acabando (menos de 20% da quantidade inicial), gostaria de receber uma notificação via email. Também receber quando ele se esgotar por completo.

#### Critérios de aceitação:
- Notificação deve ser enviada para o email do usuário.

#### Story Points: 2

</br>
</br>

Como <b>cliente final do usuário</b>, gostaria de receber minha fatura completa por email, contendo todas as informações sobre os consumos, junto com o valor total a ser pago.

#### Critérios de aceitação:
- Fatura enviada deve conter detalhes dos consumos, junto à seus preços finais.

#### Story Points: 2

</br>
</br>

<a name="uml"></a>
## Diagrama UML

![Diagrama UML](/img/diagrama.png)


<a name="excel"></a>
## Planilhas a serem utilizadas

Exemplo de arquivo utilizado para o <b>controle de clientes e dados do usuário</b>. A chave PIX deve ser adicionada sem pontos, traços ou outros caracteres especiais, apenas números. A primeira linha de clientes deverá ser substituida por dados verdadeiros, assim como sua data de cobrança. 
Se a listagem de clientes ultrapassar o limite do template, dados adicionais poderão ser adicionados sequêncialmente nas mesmas colunas e 
respeitando suas formatações.

</br>
<img src="/img/datas.png">
</br>

[Download](/download/Exemplo-Dados.xlsx)

</br>

Exemplo de arquivo utilizado para o <b>controle diário de consumo dos insumos</b>. A data é relativa ao dia em que os insumos foram utilizados. A primeira linha de informações deverá ser substituída por valores verídicos, sendo eles o nome do cliente ligado ao produto, o nome do produto (mesmo nome utilizado em sua planilha de estoque, que será apresentada a seguir), quantidade utilizada/vendida e sua porcentagem de repasse (porcentagem em cima do seu custo de cada insumo).

</br>
<img src="/img/expense.png">
</br>

[Download](/download/Exemplo-Consumo.xlsx)

</br>

Exemplo de arquivo utilizado para o <b>controle de estoque do usuário</b>. A primeira linha de dados deverá ser substituída por valores verídicos. Essa tabela consiste no nome do insumo de seu estoque (mesmo nome utilizado na planilha de consumo já apresentada), quantidade que IRÁ ser adicionada em seu estoque do sistema (toda planilha de estoque que enviar será somada aos produtos já existentes em seu perfil) e seu valor de custo (quanto pagou pelo insumo).

</br>
<img src="/img/stock.png">
</br>

[Download](/download/Exemplo-Estoque.xlsx)
