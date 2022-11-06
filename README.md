# <p align="center"><b>Ward - Sistema de automação de faturamento.</b></p>
  ![logo](/static/img/logo.png)
  
  
## Conteúdo
- [ Descrição ](#desc)
- [ Autores ](#autores)
- [ Histórias dos usuários ](#hist)
- [ Diagrama UML ](#uml)
- [ Formatos de Arquivo ](#excel)


<a name="desc"></a>
## Descrição

O projeto tem a ideia de construir um sistema visando a automação no processo de criação e fechamento de faturas de microempresas ou profissionais autônomos, buscando a economia de tempo e eficiência, para assim gerar mais produtividade a essas entidades. Também garantindo que o cliente final receba sua cobrança de forma simples, rápida e em dia.


A automação consiste no cadastro de informações de consumo pelo usuário do sistema, onde ele irá definir quais os insumos, produtos ou qualquer outro material presente em seu estoque, com seus devidos preços de custo. Ele poderá também realizar o cadastro de seus clientes e os produtos de seus estoques. Dessa forma, o sistema irá atualizar seu estoque e, ao final da data de fechamento de fatura (escolhida pelo usuário), irá enviar a fatura completa para cada um dos clientes propostos pelo usuário. O usuário terá a opção de editar o corpo do email a ser enviado para seus clientes.


<a name="autores"></a>
## Autores

- [@Giovanni Montevechi](https://www.github.com/GiovanniMP)
- [@Rodrigo Camargo](https://github.com/RSiCamargo)


<a name="hist"></a>
## Histórias dos usuários

Como <b>administrador do processo</b>, eu quero que o sistema execute as requisições feitas pelos usuários de forma adequada, chamando os processos adequados para cada requisição, e retornando os valores de acordo, para que, no final dos períodos propostos, os faturamentos sejam gerados de forma consistente.

#### Critérios de aceitação:
- As requisições devem ser feitas de acordo com as solicitações.
- Apenas usuários qualificados podem realiza-las.
- Todos os dados de cada cliente devem ser guardados no banco corretamente.
- Os fechamentos devem ser realizados de acordo com as datas propostas pelos usuários, para cada cliente.
- - Devem ser gerados logs para controle das etapas.

#### Story Points: 13

</br>
</br>

Como <b>usuário do sistema</b>, eu gostaria que o sistema lidasse com todos os dados enviados pelos inputs, uma vez respeitando todos os critérios disponíveis e por fim, associando esses dados ao meu perfil para que eu seja capaz de manter em ordem todo o meu inventário.

#### Critérios de aceitação:
- Os dados compostos nos inputs devem ser consumidos armazenando todas as informações em seus devidos locais.
- As informações devem ser associadas ao perfil do usuário identificado.

#### Story Points: 3

</br>
</br>

Como <b>usuário do sistema</b>, gostaria que conforme forem enviados dados contendo o consumo do meu estoque (para cada cliente), o sistema trate de forma adequada o fluxo de insumos para o faturamento, e atualize meu estoque.

#### Critérios de aceitação:
- Os dados devem ser consumidos armazenando todas as informações em seus devidos locais.
- O estoque do usuário deverá ser atualizado de acordo com a utilização dos insumos inseridos previamente pelo sistema.

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

![Diagrama UML](/static/img/diagrama.png)
