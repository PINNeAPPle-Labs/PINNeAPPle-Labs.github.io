/**
 * Cria os dois formulários de pré-acesso do PINNeAPPle Studio (PT e EN).
 *
 * Como usar
 * ---------
 * 1. Abra https://script.google.com com a conta Google da empresa (não a pessoal:
 *    o formulário fica no Drive de quem roda o script).
 * 2. Novo projeto, apague o conteúdo e cole este arquivo inteiro.
 * 3. Rode a função `criarFormulariosDePreAcesso` (Run ▶), autorize, e abra o
 *    "Registro de execução" (Execution log): os dois links saem lá.
 *
 * O que ele faz, em ordem
 * -----------------------
 * * cria o formulário em português e o em inglês, com 3 perguntas obrigatórias e
 *   1 opcional (curto de propósito: cada campo a mais derruba a resposta);
 * * liga a coleta de e-mail, então não existe campo "e-mail" para preencher à mão;
 * * cria uma planilha de respostas para cada um e liga o formulário a ela;
 * * escreve a mensagem de confirmação em cada idioma;
 * * imprime os links curtos (forms.gle) e o link de edição de cada formulário.
 *
 * O que ele NÃO faz (o Google não expõe essas opções na API)
 * ----------------------------------------------------------
 * * notificar por e-mail a cada resposta: abra o formulário, aba Respostas, os
 *   três pontinhos, "Receber notificações de novas respostas";
 * * deixar o link público para qualquer pessoa: em Enviar > Link, escolha
 *   "Qualquer pessoa com o link" (se a conta for de organização, o padrão é
 *    restrito e ninguém de fora consegue responder).
 *
 * Rodar de novo cria formulários novos, não atualiza os antigos: rode uma vez e
 * guarde os links.
 */

var SITE = 'https://pinneapple-labs.github.io';

var FORMS = [
  {
    chave: 'pt',
    titulo: 'Pré-acesso ao PINNeAPPle Studio',
    descricao: 'O Studio abre em 2027, em prévia fechada. Quem entra na lista recebe o ' +
      'convite antes, na ordem de inscrição, e ajuda a decidir o que entra primeiro. ' +
      'São três perguntas, e o e-mail já vem da sua conta Google.\n' + SITE,
    nome: 'Nome',
    empresa: 'Empresa',
    area: 'Área de atuação',
    areas: ['CFD e fluidos', 'Estrutural', 'Térmico', 'Eletromagnetismo', 'Gêmeo digital', 'Outra'],
    problema: 'Qual problema você quer resolver primeiro?',
    problemaAjuda: 'Opcional. Uma frase basta: o caso que você gostaria de rodar no Studio.',
    confirmacao: 'Recebido. Você está na lista, em ordem de inscrição. O convite sai no e-mail ' +
      'cadastrado quando abrirmos a prévia, em 2027. Se quiser adiantar, responda contando o ' +
      'caso que você quer rodar primeiro.',
    planilha: 'Pré-acesso PT (respostas)'
  },
  {
    chave: 'en',
    titulo: 'Early access to PINNeAPPle Studio',
    descricao: 'The Studio opens in 2027, in a closed preview. Whoever joins the list gets the ' +
      'invite first, in sign-up order, and helps decide what ships first. ' +
      'Three questions, and the e-mail comes from your Google account.\n' + SITE,
    nome: 'Name',
    empresa: 'Company',
    area: 'Field',
    areas: ['CFD and fluids', 'Structural', 'Thermal', 'Electromagnetics', 'Digital twin', 'Other'],
    problema: 'What do you want to solve first?',
    problemaAjuda: 'Optional. One sentence is enough: the case you would like to run in the Studio.',
    confirmacao: 'Received. You are on the list, in sign-up order. The invite goes to the e-mail ' +
      'you signed in with when we open the preview, in 2027. If you want to get ahead, reply ' +
      'with the case you want to run first.',
    planilha: 'Early access EN (responses)'
  }
];


function criarFormulariosDePreAcesso() {
  var links = [];

  FORMS.forEach(function (spec) {
    var form = FormApp.create(spec.titulo);
    form.setDescription(spec.descricao);

    // O e-mail vem da conta Google: um campo a menos para preencher.
    form.setCollectEmail(true);
    form.setAllowResponseEdits(true);
    form.setProgressBar(true);
    form.setShuffleQuestions(false);
    form.setConfirmationMessage(spec.confirmacao);
    form.setAcceptingResponses(true);

    form.addTextItem()
      .setTitle(spec.nome)
      .setRequired(true);

    form.addTextItem()
      .setTitle(spec.empresa)
      .setRequired(true);

    form.addMultipleChoiceItem()
      .setTitle(spec.area)
      .setChoiceValues(spec.areas)
      .setRequired(true);

    form.addParagraphTextItem()
      .setTitle(spec.problema)
      .setHelpText(spec.problemaAjuda)
      .setRequired(false);

    // As respostas caem numa planilha própria, uma por formulário.
    var sheet = SpreadsheetApp.create(spec.planilha);
    form.setDestination(FormApp.DestinationType.SPREADSHEET, sheet.getId());

    var publicado = form.getPublishedUrl();
    var curto = form.shortenFormUrl(publicado);

    links.push({
      idioma: spec.chave,
      curto: curto,
      publicado: publicado,
      editar: form.getEditUrl(),
      planilha: sheet.getUrl()
    });
  });

  links.forEach(function (l) {
    Logger.log(
      '\n=== ' + l.idioma.toUpperCase() + ' ===\n' +
      'Link para o site : ' + l.curto + '\n' +
      'Link completo    : ' + l.publicado + '\n' +
      'Editar           : ' + l.editar + '\n' +
      'Respostas        : ' + l.planilha + '\n'
    );
  });

  Logger.log('Cole o link curto de cada idioma em PREACCESS_FORM no build.py do site.');
  return links;
}
